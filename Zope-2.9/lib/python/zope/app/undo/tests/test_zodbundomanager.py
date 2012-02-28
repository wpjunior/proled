##############################################################################
#
# Copyright (c) 2001, 2002 Zope Corporation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""ZODB Undo-manager tests

$Id: test_zodbundomanager.py 68944 2006-07-02 12:08:01Z philikon $
"""
from time import time
from unittest import TestCase, main, makeSuite
import transaction

from zope.testing.cleanup import CleanUp 
from zope.app.testing import ztapi
from zope.app.testing.placelesssetup import PlacelessSetup
from zope.app.security.interfaces import IAuthentication

from zope.app.undo import ZODBUndoManager
from zope.app.undo.interfaces import UndoError

testdata = [
    dict(id='1', user_name='/ jim', time=time(), description='des 1',
         location=u'/spam\N{CYRILLIC CAPITAL LETTER A}/1'),
    dict(id='2', user_name='/ jim', time=time(), description='des 2',
         location=u'/parrot/2'),
    dict(id='3', user_name='/ anthony', time=time(), description='des 3',
         location=u'/spam\N{CYRILLIC CAPITAL LETTER A}/spam/3'),
    dict(id='4', user_name='/ jim', time=time(), description='des 4',
         location=u'/spam\N{CYRILLIC CAPITAL LETTER A}/parrot/4'),
    dict(id='5', user_name='/ anthony', time=time(), description='des 5'),
    dict(id='6', user_name='/ anthony', time=time(), description='des 6'),
    dict(id='7', user_name='/ jim', time=time(), description='des 7',
         location=u'/spam\N{CYRILLIC CAPITAL LETTER A}/7'),
    dict(id='8', user_name='/ anthony', time=time(), description='des 8'),
    dict(id='9', user_name='/ jim', time=time(), description='des 9'),
    dict(id='10', user_name='/ jim', time=time(), description='des 10'),
    ]
testdata.reverse()

class StubDB(object):

    def __init__(self):
        self.data = list(testdata)

    def undoInfo(self, first=0, last=-20, specification=None):
        if last < 0:
            last = first - last + 1
        # This code ripped off from zodb.storage.base.BaseStorage.undoInfo
        if specification:
            def filter(desc, spec=specification.items()):
                for k, v in spec:
                    if desc.get(k) != v:
                        return False
                return True
        else:
            filter = None
        if not filter:
            # handle easy case first
            data = self.data[first:last]
        else:
            data = []
            for x in self.data[first:]:
                if filter(x): 
                    data.append(x)
                if len(data) >= last:
                    break
        return data

    def undo(self, id):
        self.data = [d for d in self.data if d['id'] != id]

class Test(PlacelessSetup, TestCase):

    def setUp(self):
        super(Test, self).setUp()

        # provide location adapter
        from zope.app.location.traversing import LocationPhysicallyLocatable
        from zope.app.location.interfaces import ILocation
        from zope.app.traversing.interfaces import IPhysicallyLocatable
        ztapi.provideAdapter(ILocation, IPhysicallyLocatable,
                             LocationPhysicallyLocatable)

        # define principals
        from zope.app.security.principalregistry import principalRegistry
        principalRegistry.definePrincipal('jim', 'Jim Fulton', login='jim')
        principalRegistry.definePrincipal('anthony', 'Anthony Baxter',
                                          login='anthony')
        ztapi.provideUtility(IAuthentication, principalRegistry)
        self.undo = ZODBUndoManager(StubDB())
        self.data = list(testdata)

    def testGetTransactions(self):
        self.assertEqual(list(self.undo.getTransactions()), self.data)

    def testGetPrincipalTransactions(self):
        self.assertRaises(TypeError, self.undo.getPrincipalTransactions, None)

        from zope.app.security.principalregistry import principalRegistry
        jim = principalRegistry.getPrincipal('jim')
        expected = [dict for dict in self.data if dict['user_name'] == '/ jim']
        self.assertEqual(list(self.undo.getPrincipalTransactions(jim)),
                         expected)

    def testGetTransactionsInLocation(self):
        from zope.interface import directlyProvides
        from zope.app.location import Location
        from zope.app.traversing.interfaces import IContainmentRoot

        root = Location()
        spam = Location()
        spam.__name__ = u'spam\N{CYRILLIC CAPITAL LETTER A}'
        spam.__parent__ = root
        directlyProvides(root, IContainmentRoot)

        expected = [dict for dict in self.data if 'location' in dict
                    and dict['location'].startswith(
                        u'/spam\N{CYRILLIC CAPITAL LETTER A}')]
        self.assertEqual(list(self.undo.getTransactions(spam)), expected)

        # now test this with getPrincipalTransactions()
        from zope.app.security.principalregistry import principalRegistry
        jim = principalRegistry.getPrincipal('jim')
        expected = [dict for dict in expected if dict['user_name'] == '/ jim']
        self.assertEqual(list(self.undo.getPrincipalTransactions(jim, spam)),
                         expected)

    def testUndoTransactions(self):
        ids = ('3','4','5')
        self.undo.undoTransactions(ids)
        expected = [d for d in testdata if (d['id'] not in ids)]
        self.assertEqual(list(self.undo.getTransactions()), expected)

        # assert that the transaction has been annotated
        txn = transaction.get()
        self.assert_(txn._extension.has_key('undo'))
        self.assert_(txn._extension['undo'] is True)

    def testUndoPrincipalTransactions(self):
        self.assertRaises(TypeError, self.undo.undoPrincipalTransactions,
                          None, [])
        
        from zope.app.security.principalregistry import principalRegistry
        jim = principalRegistry.getPrincipal('jim')
        self.assertRaises(UndoError, self.undo.undoPrincipalTransactions,
                          jim, ('1','2','3'))

        ids = ('1', '2', '4')
        self.undo.undoPrincipalTransactions(jim, ids)
        expected = [d for d in testdata if (d['id'] not in ids)]
        self.assertEqual(list(self.undo.getTransactions()), expected)

def test_suite():
    return makeSuite(Test)

if __name__=='__main__':
    main(defaultTest='test_suite')

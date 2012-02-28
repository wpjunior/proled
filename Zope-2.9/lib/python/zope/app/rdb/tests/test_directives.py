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
"""Test 'rdb' ZCML Namespace Directives

$Id: test_directives.py 29143 2005-02-14 22:43:16Z srichter $
"""
import unittest
from zope.app import zapi
from zope.app.testing.placelesssetup import PlacelessSetup
from zope.component import getUtilitiesFor, queryUtility
from zope.configuration import xmlconfig
from zope.app.rdb.interfaces import IZopeDatabaseAdapter
from zope.app.rdb.tests.test_zopedatabaseadapter import DAStub
from zope.app.rdb import ZopeConnection
import zope.app.rdb.tests

class DirectivesTest(PlacelessSetup, unittest.TestCase):

    def test_provideConnection(self):

        conns = list(zapi.getUtilitiesFor(IZopeDatabaseAdapter))
        self.assertEqual(conns, [])
        connectionstub = queryUtility(IZopeDatabaseAdapter, 'stub')
        self.assertEqual(connectionstub, None)

        self.context = xmlconfig.file("rdb.zcml", zope.app.rdb.tests)
        connectionstub = queryUtility(IZopeDatabaseAdapter, 'stub')
        connection = connectionstub()
        self.assertEqual(connectionstub.__class__, DAStub)
        conns = zapi.getUtilitiesFor(IZopeDatabaseAdapter)
           
        self.assertEqual([c[0] for c in conns], ["stub"])
        self.assertEqual(connection.__class__, ZopeConnection)


def test_suite():
    return unittest.TestSuite((
        unittest.makeSuite(DirectivesTest),
        ))

if __name__ == '__main__':
    unittest.main()

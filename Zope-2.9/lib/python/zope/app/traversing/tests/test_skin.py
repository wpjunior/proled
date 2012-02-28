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
# FOR A PARTICULAR PURPOSE
#
##############################################################################
"""Test skin traversal.

$Id: test_skin.py 29143 2005-02-14 22:43:16Z srichter $
"""
from unittest import TestCase, main, makeSuite
from zope.interface import Interface, directlyProvides

from zope.publisher.interfaces.browser import ISkin
from zope.app.testing import ztapi
from zope.app.testing.placelesssetup import PlacelessSetup


class FauxRequest(object):
    def shiftNameToApplication(self):
        self.shifted = 1

class IFoo(Interface):
    pass
directlyProvides(IFoo, ISkin)


class Test(PlacelessSetup, TestCase):

    def setUp(self):
        super(Test, self).setUp()
        ztapi.provideUtility(ISkin, IFoo, 'foo')

    def test(self):
        from zope.app.traversing.namespace import skin


        request = FauxRequest()
        ob = object()
        ob2 = skin(ob, request).traverse('foo', ())
        self.assertEqual(ob, ob2)
        self.assert_(IFoo.providedBy(request))
        self.assertEqual(request.shifted, 1)

def test_suite():
    return makeSuite(Test)

if __name__=='__main__':
    main(defaultTest='test_suite')

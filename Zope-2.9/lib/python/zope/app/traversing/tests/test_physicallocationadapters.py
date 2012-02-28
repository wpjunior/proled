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
"""Physical Location Adapter Tests

$Id: test_physicallocationadapters.py 29143 2005-02-14 22:43:16Z srichter $
"""
from unittest import TestCase, main, makeSuite
from zope.app.testing.placelesssetup import PlacelessSetup
from zope.app.testing import ztapi, setup
from zope.interface import implements

from zope.app.traversing.interfaces import IContainmentRoot
from zope.app.traversing.interfaces import IPhysicallyLocatable
from zope.app.container.contained import contained
from zope.app.component.site import SiteManagerContainer


class Root(object):
    implements(IContainmentRoot)

    __parent__ = None


class C(object):
    pass


class Test(PlacelessSetup, TestCase):

    def test(self):
        setup.setUpTraversal()

        root = Root()
        f1 = contained(C(), root, name='f1')
        f2 = contained(SiteManagerContainer(), f1, name='f2')
        f3 = contained(C(), f2, name='f3')
        
        adapter = IPhysicallyLocatable(f3)

        self.assertEqual(adapter.getPath(), '/f1/f2/f3')
        self.assertEqual(adapter.getName(), 'f3')
        self.assertEqual(adapter.getRoot(), root)
        self.assertEqual(adapter.getNearestSite(), root)

        setup.createSiteManager(f2)
        self.assertEqual(adapter.getNearestSite(), f2)

        
def test_suite():
    return makeSuite(Test)

if __name__=='__main__':
    main(defaultTest='test_suite')

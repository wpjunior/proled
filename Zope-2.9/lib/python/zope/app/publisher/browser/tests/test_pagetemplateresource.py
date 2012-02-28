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
"""Page Template based Resources Test

$Id: test_pagetemplateresource.py 29143 2005-02-14 22:43:16Z srichter $
"""
import os
from unittest import TestCase, main, makeSuite

from zope.publisher.interfaces import NotFound
from zope.app.testing import ztapi
from zope.security.checker import NamesChecker
from zope.publisher.browser import TestRequest

from zope.app.testing.placelesssetup import PlacelessSetup
from zope.app.publisher.browser.pagetemplateresource import \
     PageTemplateResourceFactory
from zope.app.traversing.interfaces import ITraversable
from zope.app.traversing.adapters import DefaultTraversable
import zope.app.publisher.browser.tests as p

test_directory = os.path.dirname(p.__file__)

checker = NamesChecker(
    ('__call__', 'request', 'publishTraverse')
    )

class Test(PlacelessSetup, TestCase):

    def setUp(self):
        super(Test, self).setUp()
        ztapi.provideAdapter(None, ITraversable, DefaultTraversable)

    def testNoTraversal(self):
        path = os.path.join(test_directory, 'testfiles', 'test.pt')
        request = TestRequest()
        factory = PageTemplateResourceFactory(path, checker, 'test.pt')
        resource = factory(request)
        self.assertRaises(NotFound, resource.publishTraverse,
                          resource.request, ())

    def testCall(self):
        path = os.path.join(test_directory, 'testfiles', 'testresource.pt')
        test_data = "Foobar"
        request = TestRequest(test_data=test_data)
        factory = PageTemplateResourceFactory(path, checker, 'testresource.pt')
        resource = factory(request)
        self.assert_(resource(), test_data)        

def test_suite():
    return makeSuite(Test)

if __name__=='__main__':
    main(defaultTest='test_suite')

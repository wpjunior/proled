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
"""Presentation Traverser Tests

$Id: test_presentation.py 29143 2005-02-14 22:43:16Z srichter $
"""
from unittest import TestCase, main, makeSuite
from zope.app.testing import ztapi
from zope.app.testing.placelesssetup import PlacelessSetup
from zope.app.traversing.namespace import view, resource
from zope.interface import Interface, implements
from zope.publisher.browser import TestRequest

class IContent(Interface):
    pass

class Content(object):
    implements(IContent)

class Resource(object):

    def __init__(self, request):
        pass

class View(object):

    def __init__(self, content, request):
        self.content = content


class Test(PlacelessSetup, TestCase):

    def testView(self):
        ztapi.browserView(IContent, 'foo', View)

        ob = Content()
        v = view(ob, TestRequest()).traverse('foo', ())
        self.assertEqual(v.__class__, View)

    def testResource(self):
        ztapi.browserResource('foo', Resource)

        ob = Content()
        r = resource(ob, TestRequest()).traverse('foo', ())
        self.assertEqual(r.__class__, Resource)


def test_suite():
    return makeSuite(Test)

if __name__=='__main__':
    main(defaultTest='test_suite')

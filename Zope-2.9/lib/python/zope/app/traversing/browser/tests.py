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
"""Test the AbsoluteURL view

$Id: tests.py 30886 2005-06-22 13:48:35Z hdima $
"""
from unittest import TestCase, main, makeSuite

from zope.app import zapi
from zope.app.container.contained import contained
from zope.app.testing import ztapi
from zope.app.testing.placelesssetup import PlacelessSetup
from zope.app.traversing.browser.absoluteurl import absoluteURL
from zope.app.traversing.browser.interfaces import IAbsoluteURL
from zope.i18n.interfaces import IUserPreferredCharsets
from zope.interface import Interface, implements
from zope.interface.verify import verifyObject
from zope.publisher.browser import TestRequest
from zope.publisher.http import IHTTPRequest, HTTPCharsets

class IRoot(Interface):
    pass

class Root(object):
    implements(IRoot)

class TrivialContent(object):
    """Trivial content object, used because instances of object are rocks."""

class TestAbsoluteURL(PlacelessSetup, TestCase):

    def setUp(self):
        super(TestAbsoluteURL, self).setUp()
        from zope.app.traversing.browser import AbsoluteURL, SiteAbsoluteURL
        ztapi.browserView(None, 'absolute_url', AbsoluteURL)
        ztapi.browserView(IRoot, 'absolute_url', SiteAbsoluteURL)
        ztapi.browserView(None, '', AbsoluteURL, providing=IAbsoluteURL)
        ztapi.browserView(IRoot, '', SiteAbsoluteURL, providing=IAbsoluteURL)
        ztapi.provideAdapter(IHTTPRequest, IUserPreferredCharsets,
                             HTTPCharsets)

    def test_interface(self):
        request = TestRequest()
        content = contained(TrivialContent(), Root(), name='a')
        view = zapi.getMultiAdapter((content, request), name='absolute_url')

        verifyObject(IAbsoluteURL, view)

    def testBadObject(self):
        request = TestRequest()
        view = zapi.getMultiAdapter((42, request), name='absolute_url')
        self.assertRaises(TypeError, view.__str__)
        self.assertRaises(TypeError, absoluteURL, 42, request)

    def testNoContext(self):
        request = TestRequest()
        view = zapi.getMultiAdapter((Root(), request), name='absolute_url')
        self.assertEqual(str(view), 'http://127.0.0.1')
        self.assertEqual(absoluteURL(Root(), request), 'http://127.0.0.1')

    def testBasicContext(self):
        request = TestRequest()

        content = contained(TrivialContent(), Root(), name='a')
        content = contained(TrivialContent(), content, name='b')
        content = contained(TrivialContent(), content, name='c')
        view = zapi.getMultiAdapter((content, request), name='absolute_url')
        self.assertEqual(str(view), 'http://127.0.0.1/a/b/c')
        self.assertEqual(absoluteURL(content, request),
                         'http://127.0.0.1/a/b/c')

        breadcrumbs = view.breadcrumbs()
        self.assertEqual(breadcrumbs,
                         ({'name':  '', 'url': 'http://127.0.0.1'},
                          {'name': 'a', 'url': 'http://127.0.0.1/a'},
                          {'name': 'b', 'url': 'http://127.0.0.1/a/b'},
                          {'name': 'c', 'url': 'http://127.0.0.1/a/b/c'},
                          ))

    def testBasicContext_unicode(self):
        #Tests so that AbsoluteURL handle unicode names as well
        request = TestRequest()
        root = Root()
        root.__name__ = u'\u0439'

        content = contained(TrivialContent(), root, name=u'\u0442')
        content = contained(TrivialContent(), content, name=u'\u0435')
        content = contained(TrivialContent(), content, name=u'\u0441')
        view = zapi.getMultiAdapter((content, request), name='absolute_url')
        self.assertEqual(str(view),
                         'http://127.0.0.1/%D0%B9/%D1%82/%D0%B5/%D1%81')
        self.assertEqual(view(),
                         'http://127.0.0.1/%D0%B9/%D1%82/%D0%B5/%D1%81')
        self.assertEqual(unicode(view),
                         u'http://127.0.0.1/\u0439/\u0442/\u0435/\u0441')
        self.assertEqual(absoluteURL(content, request),
                         'http://127.0.0.1/%D0%B9/%D1%82/%D0%B5/%D1%81')

        breadcrumbs = view.breadcrumbs()
        self.assertEqual(breadcrumbs,
                         ({'name':  '', 'url': 'http://127.0.0.1'},
                          {'name': u'\u0439', 'url': 'http://127.0.0.1/%D0%B9'},
                          {'name': u'\u0442',
                           'url': 'http://127.0.0.1/%D0%B9/%D1%82'},
                          {'name': u'\u0435',
                           'url': 'http://127.0.0.1/%D0%B9/%D1%82/%D0%B5'},
                          {'name': u'\u0441',
                           'url':
                           'http://127.0.0.1/%D0%B9/%D1%82/%D0%B5/%D1%81'},
                          ))

    def testRetainSkin(self):
        request = TestRequest()
        request._traversed_names = ('a', 'b')
        request._app_names = ('++skin++test', )

        content = contained(TrivialContent(), Root(), name='a')
        content = contained(TrivialContent(), content, name='b')
        content = contained(TrivialContent(), content, name='c')
        view = zapi.getMultiAdapter((content, request), name='absolute_url')
        base = 'http://127.0.0.1/++skin++test'
        self.assertEqual(str(view), base + '/a/b/c')

        breadcrumbs = view.breadcrumbs()
        self.assertEqual(breadcrumbs,
                         ({'name':  '', 'url': base + ''},
                          {'name': 'a', 'url': base + '/a'},
                          {'name': 'b', 'url': base + '/a/b'},
                          {'name': 'c', 'url': base + '/a/b/c'},
                          ))

    def testVirtualHosting(self):
        request = TestRequest()

        vh_root = TrivialContent()
        content = contained(vh_root, Root(), name='a')
        request._vh_root = content
        content = contained(TrivialContent(), content, name='b')
        content = contained(TrivialContent(), content, name='c')
        view = zapi.getMultiAdapter((content, request), name='absolute_url')
        self.assertEqual(str(view), 'http://127.0.0.1/b/c')

        breadcrumbs = view.breadcrumbs()
        self.assertEqual(breadcrumbs,
         ({'name':  '', 'url': 'http://127.0.0.1'},
          {'name': 'b', 'url': 'http://127.0.0.1/b'},
          {'name': 'c', 'url': 'http://127.0.0.1/b/c'},
          ))

    def testVirtualHostingWithVHElements(self):
        request = TestRequest()

        vh_root = TrivialContent()
        content = contained(vh_root, Root(), name='a')
        request._vh_root = content
        content = contained(TrivialContent(), content, name='b')
        content = contained(TrivialContent(), content, name='c')
        view = zapi.getMultiAdapter((content, request), name='absolute_url')
        self.assertEqual(str(view), 'http://127.0.0.1/b/c')

        breadcrumbs = view.breadcrumbs()
        self.assertEqual(breadcrumbs,
         ({'name':  '', 'url': 'http://127.0.0.1'},
          {'name': 'b', 'url': 'http://127.0.0.1/b'},
          {'name': 'c', 'url': 'http://127.0.0.1/b/c'},
          ))

    def testVirtualHostingInFront(self):
        request = TestRequest()

        root = Root()
        request._vh_root = contained(root, root, name='')
        content = contained(root, None)
        content = contained(TrivialContent(), content, name='a')
        content = contained(TrivialContent(), content, name='b')
        content = contained(TrivialContent(), content, name='c')
        view = zapi.getMultiAdapter((content, request), name='absolute_url')
        self.assertEqual(str(view), 'http://127.0.0.1/a/b/c')

        breadcrumbs = view.breadcrumbs()
        self.assertEqual(breadcrumbs,
         ({'name':  '', 'url': 'http://127.0.0.1'},
          {'name': 'a', 'url': 'http://127.0.0.1/a'},
          {'name': 'b', 'url': 'http://127.0.0.1/a/b'},
          {'name': 'c', 'url': 'http://127.0.0.1/a/b/c'},
          ))

    def testNoContextInformation(self):
        request = TestRequest()
        view = zapi.getMultiAdapter((None, request), name='absolute_url')
        self.assertEqual(str(view), 'http://127.0.0.1')
        self.assertEqual(absoluteURL(None, request), 'http://127.0.0.1')

    def testVirtualHostingWithoutContextInformation(self):
        request = TestRequest()
        request._vh_root = contained(TrivialContent(), Root(), name='a')
        view = zapi.getMultiAdapter((None, request), name='absolute_url')
        self.assertEqual(str(view), 'http://127.0.0.1')
        self.assertEqual(absoluteURL(None, request), 'http://127.0.0.1')


def test_suite():
    return makeSuite(TestAbsoluteURL)

if __name__=='__main__':
    main(defaultTest='test_suite')

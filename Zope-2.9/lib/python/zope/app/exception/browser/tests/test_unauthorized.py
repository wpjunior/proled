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
"""Test Unauthorized Exception Views

$Id: test_unauthorized.py 71681 2007-01-02 13:52:00Z adamg $
"""
from unittest import TestCase, main, makeSuite
from zope.interface import implements
from zope.publisher.browser import TestRequest
from zope.app.testing import ztapi
from zope.app.security.interfaces import IAuthentication, IPrincipal
from zope.app.exception.browser.unauthorized import Unauthorized
from zope.app.testing.placelesssetup import PlacelessSetup

class Unauthorized(Unauthorized):
    """Unusually done by ZCML."""

    def __init__(self, context, request):
        self.context = context
        self.request = request


class DummyPrincipal(object):
    implements(IPrincipal)  # this is a lie

    def __init__(self, id):
        self.id = id

    def getId(self):
        return self.id

class DummyAuthUtility(object):
    implements(IAuthentication)  # this is a lie

    def unauthorized(self, principal_id, request):
        self.principal_id = principal_id
        self.request = request


class DummyPrincipalSource(object):
    pass

class Test(PlacelessSetup, TestCase):

    def setUp(self):
        super(Test, self).setUp()
        self.auth = DummyAuthUtility()
        ztapi.provideUtility(IAuthentication, self.auth)

    def tearDown(self):
        super(Test, self).tearDown()

    def testUnauthorized(self):
        exception = Exception()
        try:
            raise exception
        except:
            pass
        request = TestRequest()
        request.setPrincipal(DummyPrincipal(23))
        u = Unauthorized(exception, request)
        u.issueChallenge()

        # Make sure the response status was set
        self.assertEqual(request.response.getStatus(), 403)

        # check headers that work around squid "negative_ttl"
        self.assertEqual(request.response.getHeader('Expires'),
                         'Mon, 26 Jul 1997 05:00:00 GMT')
        self.assertEqual(request.response.getHeader('Pragma'),
                         'no-cache')
        self.assertEqual(request.response.getHeader('Cache-Control'),
                         'no-store, no-cache, must-revalidate')
        
        # Make sure the auth utility was called
        self.failUnless(self.auth.request is request)
        self.assertEqual(self.auth.principal_id, 23)

    def testPluggableAuthUtility(self):
        exception = Exception()
        try:
            raise exception
        except:
            pass
        request = TestRequest()
        psrc = DummyPrincipalSource()
        request.setPrincipal(DummyPrincipal(23))
        u = Unauthorized(exception, request)
        u.issueChallenge()

        # Make sure the response status was set
        self.assertEqual(request.response.getStatus(), 403)

        # Make sure the auth utility was called
        self.failUnless(self.auth.request is request)
        self.assertEqual(self.auth.principal_id, 23)

def test_suite():
    return makeSuite(Test)

if __name__=='__main__':
    main(defaultTest='test_suite')

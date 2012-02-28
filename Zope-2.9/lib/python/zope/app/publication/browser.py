##############################################################################
#
# Copyright (c) 2002 Zope Corporation and Contributors.
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
"""Browser Publication Code

This module implements browser-specific publication and traversal components
for the publisher.

$Id: browser.py 38357 2005-09-07 20:14:34Z srichter $
"""
__docformat__ = 'restructuredtext'

from zope.interface import providedBy
from zope.interface import directlyProvides

from zope.publisher.interfaces.browser import IBrowserPublisher
from zope.publisher.interfaces.browser import IDefaultSkin
from zope.publisher.interfaces.browser import IDefaultBrowserLayer

from zope.app import zapi
from zope.app.publication.publicationtraverse \
     import PublicationTraverser as PublicationTraverser_
from zope.app.publication.http import BaseHTTPPublication
from zope.security.checker import ProxyFactory

class PublicationTraverser(PublicationTraverser_):

    def traverseRelativeURL(self, request, ob, path):
        ob = self.traversePath(request, ob, path)

        while True:
            adapter = IBrowserPublisher(ob, None)
            if adapter is None:
                return ob
            ob, path = adapter.browserDefault(request)
            ob = ProxyFactory(ob)
            if not path:
                return ob

            ob = self.traversePath(request, ob, path)

class BrowserPublication(BaseHTTPPublication):
    """Web browser publication handling."""

    def getDefaultTraversal(self, request, ob):
        if IBrowserPublisher.providedBy(ob):
            # ob is already proxied, so the result of calling a method will be
            return ob.browserDefault(request)
        else:
            adapter = zapi.queryMultiAdapter((ob, request), IBrowserPublisher)
            if adapter is not None:
                ob, path = adapter.browserDefault(request)
                ob = ProxyFactory(ob)
                return ob, path
            else:
                # ob is already proxied
                return ob, None

    def afterCall(self, request, ob):
        super(BrowserPublication, self).afterCall(request, ob)
        if request.method == 'HEAD':
            request.response.setResult('')

# For now, have a factory that returns a singleton
class PublicationFactory(object):

    def __init__(self, db):
        self.__pub = BrowserPublication(db)

    def __call__(self):
        return self.__pub

def setDefaultSkin(request):
    """Sets the default skin for the request.

    The default skin is a marker interface that can be registered as an
    adapter that provides IDefaultSkin for the request type.

    If a default skin is not available, the default layer
    (IDefaultBrowserLayer) is used.

    To illustrate, we'll first use setDefaultSkin without a registered
    IDefaultSkin adapter:

      >>> from zope.publisher.interfaces.browser import IBrowserRequest
      >>> from zope.interface import implements
      >>> class Request(object):
      ...     implements(IBrowserRequest)

      >>> request = Request()
      >>> IDefaultBrowserLayer.providedBy(request)
      False

      >>> setDefaultSkin(request)
      >>> IDefaultBrowserLayer.providedBy(request)
      True

    When we register a default layer, however:

      >>> from zope.interface import Interface
      >>> class IMySkin(Interface):
      ...     pass
      >>> from zope.app.testing import ztapi
      >>> ztapi.provideAdapter(IBrowserRequest, IDefaultSkin, IMySkin)

    setDefaultSkin uses the layer instead of IDefaultBrowserLayer.providedBy:

      >>> request = Request()
      >>> IMySkin.providedBy(request)
      False
      >>> IDefaultSkin.providedBy(request)
      False

      >>> setDefaultSkin(request)

      >>> IMySkin.providedBy(request)
      True
      >>> IDefaultBrowserLayer.providedBy(request)
      False

    Any interfaces that are directly provided by the request coming into this
    method are replaced by the applied layer/skin interface:

      >>> request = Request()
      >>> class IFoo(Interface):
      ...     pass
      >>> directlyProvides(request, IFoo)
      >>> IFoo.providedBy(request)
      True
      >>> setDefaultSkin(request)
      >>> IFoo.providedBy(request)
      False

    """
    adapters = zapi.getSiteManager().adapters
    skin = adapters.lookup((providedBy(request),), IDefaultSkin, '')
    if skin is not None:
        directlyProvides(request, skin)
    else:
        directlyProvides(request, IDefaultBrowserLayer)

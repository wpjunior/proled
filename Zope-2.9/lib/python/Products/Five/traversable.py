##############################################################################
#
# Copyright (c) 2004, 2005 Zope Corporation and Contributors.
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
"""Machinery for making things traversable through adaptation

$Id: traversable.py 69329 2006-08-01 18:05:22Z alecm $
"""
from zope.component import getMultiAdapter, ComponentLookupError
from zope.interface import implements, Interface
from zope.publisher.interfaces import ILayer
from zope.publisher.interfaces.browser import IBrowserRequest

from zope.app.traversing.interfaces import ITraverser, ITraversable
from zope.app.traversing.adapters import DefaultTraversable
from zope.app.traversing.adapters import traversePathElement
from zope.app.publication.browser import setDefaultSkin
from zope.app.interface import queryType

from Acquisition import aq_base
from webdav.NullResource import NullResource
import Products.Five.security
from zExceptions import NotFound
from ZPublisher import xmlrpc

_marker = object()

class FakeRequest(dict):
    implements(IBrowserRequest)

    def has_key(self, key):
        return False

    def getURL(self):
        return "http://codespeak.net/z3/five"

class Traversable:
    """A mixin to make an object traversable using an ITraverser adapter.
    """
    __five_traversable__ = True

    def __bobo_traverse__(self, REQUEST, name):
        """Hook for Zope 2 traversal

        This method is called by Zope 2's ZPublisher upon traversal.
        It allows us to trick it into faking the Zope 3 traversal system
        by using an ITraverser adapter.
        """
        # We are trying to be compatible with Zope 2 and 3 traversal
        # behaviour as much as possible.  Therefore the first part of
        # this method is based on BaseRequest.traverse's behaviour:
        # 1. If an object has __bobo_traverse__, use it.
        # 2. Otherwise do attribute look-up or, if that doesn't work,
        #    key item lookup.
        result = _marker
        if hasattr(self, '__fallback_traverse__'):
            try:
                return self.__fallback_traverse__(REQUEST, name)
            except (AttributeError, KeyError):
                pass
            except NotFound:
                # OFS.Application.__bobo_traverse__ calls
                # REQUEST.RESPONSE.notFoundError which sets the HTTP
                # status code to 404
                try:
                    REQUEST.RESPONSE.setStatus(200)
                except AttributeError:
                    pass
        else:
            # See if the object itself has the attribute, try acquisition
            # later
            if getattr(aq_base(self), name, _marker) is not _marker:
                return getattr(self, name)
            try:
                # item access should never acquire
                result = self[name]
                # WebDAV requests will always return something,
                # sometimes it's a NullResource, which we will ignore
                # and return later if necessary
                if not isinstance(result, NullResource):
                    return result
            except (KeyError, IndexError, TypeError, AttributeError):
                pass

        # This is the part Five adds:
        # 3. If neither __bobo_traverse__ nor attribute/key look-up
        # work, we try to find a Zope 3-style view.

        # For that we need to make sure we have a good request
        # (sometimes __bobo_traverse__ gets a stub request)
        if not IBrowserRequest.providedBy(REQUEST):
            # Try to get the REQUEST by acquisition
            REQUEST = getattr(self, 'REQUEST', None)
            if not IBrowserRequest.providedBy(REQUEST):
                REQUEST = FakeRequest()
                setDefaultSkin(REQUEST)

        # Con Zope 3 into using Zope 2's checkPermission
        Products.Five.security.newInteraction()

        # Use the ITraverser adapter (which in turn uses ITraversable
        # adapters) to traverse to a view.  Note that we're mixing
        # object-graph and object-publishing traversal here, but Zope
        # 2 has no way to tell us when to use which...
        # TODO Perhaps we can decide on object-graph vs.
        # object-publishing traversal depending on whether REQUEST is
        # a stub or not?
        try:
            return ITraverser(self).traverse(
                path=[name], request=REQUEST).__of__(self)
        except (ComponentLookupError, LookupError,
                AttributeError, KeyError, NotFound):
            pass

        # Fallback on acquisition, let it raise an AttributeError if it must
        try:
            return getattr(self, name)
        except AttributeError:
            if result is not _marker:
                return result
            raise

    __bobo_traverse__.__five_method__ = True


class FiveTraversable(DefaultTraversable):

    def traverse(self, name, furtherPath):
        context = self._subject
        __traceback_info__ = (context, name, furtherPath)
        # Find the REQUEST
        REQUEST = getattr(context, 'REQUEST', None)
        if not IBrowserRequest.providedBy(REQUEST):
            REQUEST = FakeRequest()
            setDefaultSkin(REQUEST)
        # Try to lookup a view
        try:
            return getMultiAdapter((context, REQUEST), Interface, name)
        except ComponentLookupError:
            pass

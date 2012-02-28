##############################################################################
# Copyright (c) 2003 Zope Corporation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
##############################################################################
"""Specific HTTP Traverser

$Id: traversal.py 38178 2005-08-30 21:50:19Z mj $
"""
from zope.interface import implements
from zope.publisher.interfaces.browser import IBrowserPublisher
from zope.publisher.interfaces import NotFound

from zope.app import zapi
from zope.app.location.interfaces import ILocation
from zope.app.schema.interfaces import IMutableSchema
from zope.app.traversing.interfaces import TraversalError, ITraversable
from zope.app.traversing.namespace import UnexpectedParameters

_marker = object()

class SchemaFieldTraverser(object):
    implements(IBrowserPublisher)
    __used_for__ = IMutableSchema

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def publishTraverse(self, request, name):
        subob = self.context.get(name, None)

        if subob is None:

            view = zapi.queryMultiAdapter((self.context, request), name=name)
            if view is not None:
                if ILocation.providedBy(view):
                    view.__parent__ = self.context
                    view.__name__ = name

                return view

            raise NotFound(self.context, name, request)

        return subob

    def browserDefault(self, request):
        c = self.context
        view_name = zapi.getDefaultViewName(c, request)
        view_uri = "@@%s" % view_name
        return c, (view_uri,)

class SchemaFieldTraversable(object):
    """Traverses Schema Fields.
    """

    implements(ITraversable)
    __used_for__ = IMutableSchema

    def __init__(self, context):
        self._context = context

    def traverse(self, name, furtherPath):
        subobj = self._context.get(name, _marker)
        if subobj is _marker:
            raise TraversalError(name)

        return subobj

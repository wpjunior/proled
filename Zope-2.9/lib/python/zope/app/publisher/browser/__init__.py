##############################################################################
#
# Copyright (c) 2003 Zope Corporation and Contributors.
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
"""Provide zope app-server customizatioin of publisher browser facilities

$Id: __init__.py 39906 2005-11-05 12:16:38Z hdima $
"""
from zope.component.interfaces import ComponentLookupError, IDefaultViewName
from zope.component import getSiteManager

import zope.interface
from zope.interface import implements, directlyProvidedBy, directlyProvides
from zope.publisher.browser import BrowserLanguages
from zope.i18n.interfaces import IUserPreferredLanguages
from zope.i18n.interfaces import IModifiableUserPreferredLanguages

from zope.app.location import Location
from zope.app.publisher.interfaces.browser import IBrowserView
from zope.publisher.interfaces.browser import ISkin


key = "zope.app.publisher.browser.IUserPreferredLanguages"

class BrowserView(Location):
    """Browser View.

    >>> view = BrowserView("context", "request")
    >>> view.context
    'context'
    >>> view.request
    'request'

    >>> view.__parent__
    'context'
    >>> view.__parent__ = "parent"
    >>> view.__parent__
    'parent'
    """

    implements(IBrowserView)

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __getParent(self):
        return getattr(self, '_parent', self.context)

    def __setParent(self, parent):
        self._parent = parent

    __parent__ = property(__getParent, __setParent)


class IDefaultViewNameAPI(zope.interface.Interface):

    def getDefaultViewName(object, request, context=None):
        """Get the name of the default view for the object and request.

        The request must implement IPresentationRequest, and provides the
        desired view type.  The nearest one to the object is found.
        If a matching default view name cannot be found, raises
        ComponentLookupError.

        If context is not specified, attempts to use
        object to specify a context.
        """

    def queryDefaultViewName(object, request, default=None, context=None):
        """Look for the name of the default view for the object and request.

        The request must implement IPresentationRequest, and provides
        the desired view type.  The nearest one to the object is
        found.  If a matching default view name cannot be found,
        returns the default.

        If context is not specified, attempts to use object to specify
        a context.
        """

# TODO: needs tests
def getDefaultViewName(object, request, context=None):
    name = queryDefaultViewName(object, request, context=context)
    if name is not None:
        return name
    raise ComponentLookupError("Couldn't find default view name",
                               context, request)

def queryDefaultViewName(object, request, default=None, context=None):
    name = getSiteManager(context).adapters.lookup(
        map(zope.interface.providedBy, (object, request)), IDefaultViewName)
    return name or default

def applySkin(request, skin):
    """Change the presentation skin for this request.

    >>> import pprint
    >>> from zope.interface import Interface, providedBy
    >>> class SkinA(Interface): pass
    >>> directlyProvides(SkinA, ISkin)
    >>> class SkinB(Interface): pass
    >>> directlyProvides(SkinB, ISkin)
    >>> class IRequest(Interface): pass

    >>> class Request(object):
    ...     implements(IRequest)

    >>> req = Request()

    >>> applySkin(req, SkinA)
    >>> pprint.pprint(list(providedBy(req).interfaces()))
    [<InterfaceClass zope.app.publisher.browser.SkinA>,
     <InterfaceClass zope.app.publisher.browser.IRequest>]

    >>> applySkin(req, SkinB)
    >>> pprint.pprint(list(providedBy(req).interfaces()))
    [<InterfaceClass zope.app.publisher.browser.SkinB>,
     <InterfaceClass zope.app.publisher.browser.IRequest>]
    """
    # Remove all existing skin declarations (commonly the default skin).
    ifaces = [iface
              for iface in directlyProvidedBy(request)
              if not ISkin.providedBy(iface)]
    # Add the new skin.
    ifaces.append(skin)
    directlyProvides(request, *ifaces)

class NotCompatibleAdapterError(Exception):
    """Adapter not compatible with
       zope.i18n.interfaces.IModifiableBrowserLanguages has been used.
    """

class CacheableBrowserLanguages(BrowserLanguages):

    implements(IUserPreferredLanguages)

    def getPreferredLanguages(self):
        languages_data = self._getLanguagesData()
        if "overridden" in languages_data:
            return languages_data["overridden"]
        elif "cached" not in languages_data:
            languages_data["cached"] = super(
                CacheableBrowserLanguages, self).getPreferredLanguages()
        return languages_data["cached"]

    def _getLanguagesData(self):
        annotations = self.request.annotations
        languages_data = annotations.get(key)
        if languages_data is None:
            annotations[key] = languages_data = {}
        return languages_data

class ModifiableBrowserLanguages(CacheableBrowserLanguages):

    implements(IModifiableUserPreferredLanguages)

    def setPreferredLanguages(self, languages):
        languages_data = self.request.annotations.get(key)
        if languages_data is None:
            # Better way to create a compatible with
            # IModifiableUserPreferredLanguages adapter is to use
            # CacheableBrowserLanguages as base class or as example.
            raise NotCompatibleAdapterError("Adapter not compatible with "
                "zope.i18n.interfaces.IModifiableBrowserLanguages "
                "has been used.")
        languages_data["overridden"] = languages
        self.request.setupLocale()

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
"""Site and Local Site Manager implementation

A local site manager has a number of roles:

  - A local site manager, that provides a local adapter and utility registry.

  - A place to do TTW development and/or to manage database-based code.

  - A registry for persistent modules.  The Zope 3 import hook uses the
    SiteManager to search for modules.

$Id: site.py 39075 2005-10-11 20:54:48Z srichter $
"""

import zope.event
import zope.interface
import zope.component
from zope.component.exceptions import ComponentLookupError
from zope.security.proxy import removeSecurityProxy

from zope.app import zapi
from zope.app.component import adapter
from zope.app.component import interfaces
from zope.app.component import registration
from zope.app.component.hooks import setSite
from zope.app.container.btree import BTreeContainer
from zope.app.container.contained import Contained
from zope.app.event import objectevent
from zope.app.filerepresentation.interfaces import IDirectoryFactory
from zope.app.traversing.interfaces import IContainmentRoot

##############################################################################
# from zope.app.module import resolve

# Break the dependency on zope.app.module.  In the long run,
# we need to handle this better.  Perhaps througha utility.

## def findModule(name, context=None):
##     """Find the module matching the provided name."""
##     module = ZopeModuleRegistry.findModule(name)
##     return module or sys.modules.get(name)

import sys

def resolve(name, context=None):
    """Resolve a dotted name to a Python object."""
    pos = name.rfind('.')
    mod = sys.modules.get(name[:pos])
##    mod = findModule(name[:pos], context)
    return getattr(mod, name[pos+1:], None)

# from zope.app.module import resolve
##############################################################################

# Goes away in 3.3.
import bbb.site

class SiteManagementFolder(registration.RegisterableContainer,
                           BTreeContainer):
    zope.interface.implements(interfaces.ISiteManagementFolder)


class SMFolderFactory(object):
    zope.interface.implements(IDirectoryFactory)

    def __init__(self, context):
        self.context = context

    def __call__(self, name):
        return SiteManagementFolder()


class SiteManagerContainer(bbb.site.BBBSiteManagerContainer, Contained):
    """Implement access to the site manager (++etc++site).

    This is a mix-in that implements the IPossibleSite
    interface; for example, it is used by the Folder implementation.
    """
    zope.interface.implements(interfaces.IPossibleSite)

    # BBB: Deactive in 3.3 again. Now provided by BBBSiteManagerContainer
    #_sm = None

    def getSiteManager(self):
        if self._sm is not None:
            return self._sm
        else:
            raise ComponentLookupError('no site manager defined')

    def setSiteManager(self, sm):
        if interfaces.ISite.providedBy(self):
            raise TypeError("Already a site")

        if zope.component.interfaces.ISiteManager.providedBy(sm):
            self._sm = sm
            sm.__name__ = '++etc++site'
            sm.__parent__ = self
        else:
            raise ValueError('setSiteManager requires an ISiteManager')

        zope.interface.directlyProvides(
            self, interfaces.ISite,
            zope.interface.directlyProvidedBy(self))

        zope.event.notify(interfaces.NewLocalSite(sm))

def _findNextSiteManager(site):
    while True:
        if IContainmentRoot.providedBy(site):
            # we're the root site, return None
            return None

        try:
            site = zapi.getParent(site)
        except TypeError:
            # there was not enough context; probably run from a test
            return None

        if interfaces.ISite.providedBy(site):
            return site.getSiteManager()


class LocalUtilityRegistry(adapter.LocalAdapterRegistry):
    """Custom local adapter registry for utilities, since utilities do not
    just register themselves as null adapters, but also as subscribers."""

    def _updateAdaptersFromRegistration(self, radapters, registration):
        # Register as null adapter
        key = (False, registration.with, registration.name,
               registration.provided)
        radapters[key] = removeSecurityProxy(registration.component)
        # Register as subscriber
        key = (True, registration.with, '', registration.provided)
        radapters[key] = radapters.get(key, ()) + (
            removeSecurityProxy(registration.component), )


class LocalSiteManager(BTreeContainer,
                       bbb.site.BBBSiteManager,
                       zope.component.site.SiteManager):
    """Local Site Manager implementation"""
    zope.interface.implements(
        interfaces.ILocalSiteManager,
        interfaces.registration.IRegisterableContainerContaining)

    # See interfaces.registration.ILocatedRegistry
    next = None
    subs = ()
    base = None

    def __init__(self, site):
        # Locate the site manager
        self.__parent__ = site
        self.__name__ = '++etc++site'

        # Make sure everything is setup correctly
        BTreeContainer.__init__(self)

        # Set up adapter registries
        gsm = zapi.getGlobalSiteManager()
        self.adapters = adapter.LocalAdapterRegistry(gsm.adapters)
        self.utilities = LocalUtilityRegistry(gsm.utilities)

        # Setup located registry attributes
        next = _findNextSiteManager(site)
        self.setNext(next)

        # Setup default site management folder
        folder = SiteManagementFolder()
        zope.event.notify(objectevent.ObjectCreatedEvent(folder))
        self['default'] = folder


    def addSub(self, sub):
        """See interfaces.registration.ILocatedRegistry"""
        self.subs += (sub, )

    def removeSub(self, sub):
        """See interfaces.registration.ILocatedRegistry"""
        self.subs = tuple(
            [s for s in self.subs if s is not sub] )

    def setNext(self, next, base=None):
        """See interfaces.registration.ILocatedRegistry"""
        if self.next is not None:
            self.next.removeSub(self)
        if next is not None:
            next.addSub(self)
        self.next = next
        if next is not None:
            self.adapters.setNext(next.adapters)
            self.utilities.setNext(next.utilities)
        else:
            self.adapters.setNext(None)
            self.utilities.setNext(None)

    def __getRegistry(self, registration):
        """Determine the correct registry for the registration."""
        if interfaces.IUtilityRegistration.providedBy(registration):
            return self.utilities
        elif interfaces.IAdapterRegistration.providedBy(registration):
            return self.adapters
        raise ValueError("Unable to detect registration type or registration "
                         "type is not supported. The registration object must "
                         "provide `IAdapterRegistration` or "
                         "`IUtilityRegistration`.")

    def register(self, registration):
        """See zope.app.component.interfaces.registration.IRegistry"""
        registry = self.__getRegistry(registration)
        registry.register(registration)

    def unregister(self, registration):
        """See zope.app.component.interfaces.registration.IRegistry"""
        registry = self.__getRegistry(registration)
        registry.unregister(registration)

    def registered(self, registration):
        """See zope.app.component.interfaces.registration.IRegistry"""
        return self.adapters.registered(registration) or \
               self.utilities.registered(registration)

    def registrations(self):
        """See zope.component.interfaces.IRegistry"""
        for reg in self.adapters.registrations():
            yield reg
        for reg in self.utilities.registrations():
            yield reg


class AdapterRegistration(registration.ComponentRegistration):
    """Adapter component registration for persistent components

    This registration configures persistent components in packages to
    be adapters.
    """
    zope.interface.implements(interfaces.IAdapterRegistration)

    def __init__(self, required, provided, factoryName,
                 name='', permission=None):
        if not isinstance(required, (tuple, list)):
            self.required = required
            self.with = ()
        else:
            self.required = required[0]
            self.with = tuple(required[1:])
        self.provided = provided
        self.name = name
        self.factoryName = factoryName
        self.permission = permission

    def component(self):
# Didn't work ... tests failed
##         # Import here, so that we only have a soft dependence on
##         # zope.app.module
##         from zope.app.module import resolve
        factory = resolve(self.factoryName, self)
        return factory
    component = property(component)

    def getRegistry(self):
        return zapi.getSiteManager(self)


class UtilityRegistration(bbb.site.BBBUtilityRegistration,
                          registration.ComponentRegistration):
    """Utility component registration for persistent components

    This registration configures persistent components in packages to
    be utilities.
    """
    zope.interface.implements(interfaces.IUtilityRegistration)

    ############################################################
    # Make the adapter code happy.
    required = zope.interface.adapter.Null
    with = ()
    ############################################################

    def __init__(self, name, provided, component, permission=None):
        super(UtilityRegistration, self).__init__(component, permission)
        self.name = name
        self.provided = provided

    def getRegistry(self):
        return zapi.getSiteManager(self)


def threadSiteSubscriber(ob, event):
    """A subscriber to BeforeTraverseEvent

    Sets the 'site' thread global if the object traversed is a site.
    """
    setSite(ob)


def clearThreadSiteSubscriber(event):
    """A subscriber to EndRequestEvent

    Cleans up the site thread global after the request is processed.
    """
    clearSite()

# Clear the site thread global
clearSite = setSite
from zope.testing.cleanup import addCleanUp
addCleanUp(clearSite)


def SiteManagerAdapter(ob):
    """An adapter from ILocation to ISiteManager.

    The ILocation is interpreted flexibly, we just check for
    ``__parent__``.
    """
    current = ob
    while True:
        if interfaces.ISite.providedBy(current):
            return current.getSiteManager()
        current = getattr(current, '__parent__', None)
        if current is None:
            # It is not a location or has no parent, so we return the global
            # site manager
            return zapi.getGlobalSiteManager()

def changeSiteConfigurationAfterMove(site, event):
    """After a site is moved, its site manager links have to be updated."""
    next = None
    if event.newParent is not None:
        next = _findNextSiteManager(site)
    site.getSiteManager().setNext(next)

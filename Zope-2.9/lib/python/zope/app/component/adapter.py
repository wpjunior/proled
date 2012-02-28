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
"""Local/Persistent Adapter Registry

$Id: adapter.py 29143 2005-02-14 22:43:16Z srichter $
"""
__docformat__ = 'restructuredtext' 
import persistent

import zope.interface
from zope.security.proxy import removeSecurityProxy

from zope.app.component import registration
from zope.app.component import interfaces


class LocalSurrogate(zope.interface.adapter.Surrogate):
    """Local Surrogate

    Local surrogates are transient, rather than persistent. Their adapter
    data are stored in their registry objects.
    """
    def __init__(self, spec, registry):
        super(LocalSurrogate, self).__init__(spec, registry)
        self.registry = registry
        registry.baseFor(spec).subscribe(self)

    def clean(self):
        spec = self.spec()
        base = self.registry.baseFor(spec)
        ladapters = self.registry.adapters.get(spec)
        if ladapters:
            adapters = base.adapters.copy()
            adapters.update(ladapters)
        else:
            adapters = base.adapters
        self.adapters = adapters
        super(LocalSurrogate, self).clean()


class LocalAdapterRegistry(zope.interface.adapter.AdapterRegistry,
                           persistent.Persistent):
    """Local/persistent surrogate registry"""
    zope.interface.implements(interfaces.ILocalAdapterRegistry)
    
    _surrogateClass = LocalSurrogate

    # See interfaces.registration.ILocatedRegistry
    next = None
    subs = ()

    def __init__(self, base, next=None):
        # Base registry. This is always a global registry
        self.base = base
        # `adapters` is simple dict, since it is populated during every load
        self.adapters = {}
        self._registrations = ()
        super(LocalAdapterRegistry, self).__init__()
        self.setNext(next)

    def addSub(self, sub):
        """See interfaces.registration.ILocatedRegistry"""
        self.subs += (sub, )

    def removeSub(self, sub):
        """See interfaces.registration.ILocatedRegistry"""
        self.subs = tuple(
            [s for s in self.subs if s is not sub] )

    def setNext(self, next, base=None):
        """See interfaces.registration.ILocatedRegistry"""
        if base is not None:
            self.base = base
        if self.next is not None:
            self.next.removeSub(self)
        if next is not None:
            next.addSub(self)
        self.next = next
        self.adaptersChanged()

    def register(self, registration):
        """See zope.app.component.interfaces.registration.IRegistry"""
        self._registrations += (registration,)
        self.adaptersChanged()

    def unregister(self, registration):
        """See zope.app.component.interfaces.registration.IRegistry"""
        self._registrations = tuple([reg for reg in self._registrations
                                     if reg is not registration])
        self.adaptersChanged()

    def registered(self, registration):
        """See zope.app.component.interfaces.registration.IRegistry"""
        return registration in self._registrations

    def registrations(self):
        """See zope.app.component.interfaces.registration.IRegistry"""
        return self._registrations

    def __getstate__(self):
        state = persistent.Persistent.__getstate__(self).copy()
        
        for name in ('_default', '_null', 'adapter_hook',
                     'lookup', 'lookup1', 'queryAdapter', 'get',
                     'subscriptions', 'queryMultiAdapter', 'subscribers'
                     ):
            del state[name]
        return state

    def __setstate__(self, state):
        persistent.Persistent.__setstate__(self, state)
        zope.interface.adapter.AdapterRegistry.__init__(self)
    
    def baseFor(self, spec):
        """Used by LocalSurrogate"""
        return self.base.get(spec)

    def _updateAdaptersFromRegistration(self, radapters, registration):
        """Only to be used by _updateAdaptersFromLocalData, but can be
        overridden to implement custom behavior."""
        key = (False, registration.with, registration.name,
               registration.provided)
        radapters[key] = removeSecurityProxy(registration.component)

    def _updateAdaptersFromLocalData(self, adapters):
        """Update all adapter surrogates locally."""
        for registration in self._registrations:
            required = registration.required
            if required is None:
                required = zope.interface.adapter.Default
            radapters = adapters.get(required)
            if not radapters:
                radapters = {}
                adapters[required] = radapters

            # Needs more thought:
            # We have to remove the proxy because we're
            # storing the value amd we can't store proxies.
            # (Why can't we?)  we need to think more about
            # why/if this is truly safe
            self._updateAdaptersFromRegistration(radapters, registration)


    def adaptersChanged(self):
        """See interfaces.registration.ILocalAdapterRegistry"""
        adapters = {}
        if self.next is not None:
            for required, radapters in self.next.adapters.iteritems():
                adapters[required] = radapters.copy()
        
        self._updateAdaptersFromLocalData(adapters)

        if adapters != self.adapters:
            self.adapters = adapters

            # Throw away all of our surrogates, rather than dirtrying
            # them individually
            super(LocalAdapterRegistry, self).__init__()
            
            for sub in self.subs:
                sub.adaptersChanged()

    def baseChanged(self):
        """See interfaces.registration.ILocalAdapterRegistry"""
        super(LocalAdapterRegistry, self).__init__()
        for sub in self.subs:
            sub.baseChanged()


class AdapterRegistration(registration.ComponentRegistration):
    """A simple implementation of the adapter registration interface."""
    zope.interface.implements(interfaces.IAdapterRegistration)

    def __init__(self, required, provided, factory,
                 name='', permission=None, registry=None):
        if not isinstance(required, (tuple, list)):
            self.required = required
            self.with = ()
        else:
            self.required = required[0]
            self.with = tuple(required[1:])
        self.provided = provided
        self.name = name
        self.component = factory
        self.permission = permission
        self.registry = registry

    def getRegistry(self):
        return self.registry

    def __repr__(self):
        return ('<%s: ' %self.__class__.__name__ +
                'required=%r, ' %self.required +
                'with=' + `self.with` + ', ' +
                'provided=%r, ' %self.provided +
                'name=%r, ' %self.name +
                'component=%r, ' %self.component +
                'permission=%r' %self.permission +
                '>')

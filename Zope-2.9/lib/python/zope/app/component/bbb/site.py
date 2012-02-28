##############################################################################
#
# Copyright (c) 2005 Zope Corporation and Contributors.
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
"""Site-related BBB components

$Id$
"""
__docformat__ = "reStructuredText"
import zope.deprecation
from zope.component.bbb.service import IService
from zope.cachedescriptors import property

from zope.app import zapi
import registration


class BBBSiteManagerContainer(object):

    def _sm(self):
        if '_ServiceManagerContainer__sm' in self.__dict__:
            return self._ServiceManagerContainer__sm
        elif '_SiteManagerContainer__sm' in self.__dict__:
            return self._SiteManagerContainer__sm
        else:
            return None
    _sm = property.Lazy(_sm)
    

class BBBSiteManager(object):

    def utilities(self):
        gsm = zapi.getGlobalSiteManager()
        from zope.app.component.site import LocalUtilityRegistry
        return LocalUtilityRegistry(gsm.utilities)
    utilities = property.Lazy(utilities)

    def adapters(self):
        gsm = zapi.getGlobalSiteManager()
        from zope.app.component import adapter
        return adapter.LocalAdapterRegistry(gsm.adapters)        
    adapters = property.Lazy(adapters)

    def queryRegistrationsFor(self, cfg, default=None):
        return self.queryRegistrations(cfg.name, default)
    queryRegistrationsFor = zope.deprecation.deprecated(
        queryRegistrationsFor,
        'The site manager does not handle registrations directly anymore. '
        'The utility and adapter registry are available via the `utilities` '
        'and `adapters` attributes, respectively. '
        'The method will be gone in Zope 3.3.')

    def queryRegistrations(self, name, default=None):
        """See INameRegistry"""
        return registration.RegistrationStack(self, name)
    queryRegistrations = zope.deprecation.deprecated(
        queryRegistrations,
        'The site manager does not handle registrations directly anymore. '
        'The utility and adapter registry are available via the `utilities` '
        'and `adapters` attributes, respectively. '
        'The method will be gone in Zope 3.3.')

    def addSubsite(self, sub):
        return self.addSub(sub)
    addSubsite = zope.deprecation.deprecated(
        addSubsite,
        'Use `addSub()` instead. '
        'The reference will be gone in Zope 3.3.')

    def createRegistrationsFor(self, cfg):
        # Ignore
        pass
    createRegistrationsFor = zope.deprecation.deprecated(
        createRegistrationsFor,
        'The site manager does not handle registrations directly anymore. '
        'The utility and adapter registry are available via the `utilities` '
        'and `adapters` attributes, respectively. '
        'The reference will be gone in Zope 3.3.')

    def createRegistrations(self, name):
        # Ignore
        pass
    createRegistrations = zope.deprecation.deprecated(
        createRegistrations,
        'The site manager does not handle registrations directly anymore. '
        'The utility and adapter registry are available via the `utilities` '
        'and `adapters` attributes, respectively. '
        'The reference will be gone in Zope 3.3.')

    def listRegistrationNames(self):
        # Only used for services
        services = ['Utilities', 'Adapters']
        return [reg.name
                for reg in self.utilities.registrations()
                if reg.provided is IService] + services
    listRegistrationNames = zope.deprecation.deprecated(
        listRegistrationNames,
        'The site manager does not handle registrations directly anymore. '
        'The utility and adapter registry are available via the `utilities` '
        'and `adapters` attributes, respectively. '
        'The method will be gone in Zope 3.3.')
        
    def queryActiveComponent(self, name, default=None):
        return self.queryLocalService(name, default)
    queryActiveComponent = zope.deprecation.deprecated(
        queryActiveComponent,
        'The site manager does not handle registrations directly anymore. '
        'The utility and adapter registry are available via the `utilities` '
        'and `adapters` attributes, respectively. '
        'The method will be gone in Zope 3.3.')

    def getServiceDefinitions(self):
        gsm = zapi.getGlobalSiteManager()
        return gsm.getServiceDefinitions()
    getServiceDefinitions = zope.deprecation.deprecated(
        getServiceDefinitions,
        'The concept of services has been removed. Use utilities instead. '
        'The method will be gone in Zope 3.3.')

    def getService(self, name):
        return zapi.getUtility(IService, name, self)
    getService = zope.deprecation.deprecated(
        getService,
        'The concept of services has been removed. Use utilities instead. '
        'The method will be gone in Zope 3.3.')

    def queryLocalService(self, name, default=None):
        if name in _builtinServices:
            return self
        service = zapi.queryUtility(IService, name, self)
        if service is None:
            return default
        if zapi.getSiteManager(service) is not self:
            return default
        return service
    queryLocalService = zope.deprecation.deprecated(
        queryLocalService,
        'The concept of services has been removed. Use utilities instead. '
        'The method will be gone in Zope 3.3.')

    def getInterfaceFor(self, service_type):
        iface = [iface
                for name, iface in self.getServiceDefinitions()
                if name == service_type]
        return iface[0]
    getInterfaceFor = zope.deprecation.deprecated(
        getInterfaceFor,
        'The concept of services has been removed. Use utilities instead. '
        'The method will be gone in Zope 3.3.')

    def queryComponent(self, type=None, filter=None, all=0):
        # Ignore, hoping that noone uses this horrible method
        return []
    getInterfaceFor = zope.deprecation.deprecated(
        getInterfaceFor,
        'This method was pretty useless even before services were gone! '
        'The method will be gone in Zope 3.3.')

_builtinServices = ('Utilities', 'Adapters')


class BBBUtilityRegistration(object):

    def provided(self):
        if 'interface' in self.__dict__:
            return self.interface
    provided = property.Lazy(provided)

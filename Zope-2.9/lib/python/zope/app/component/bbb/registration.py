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
"""Registration BBB components

$Id$
"""
__docformat__ = "reStructuredText"
from persistent import Persistent
import zope.deprecation
from zope.cachedescriptors.property import Lazy
from zope.interface import implements
from zope.proxy import removeAllProxies
from zope.security.checker import InterfaceChecker, CheckerPublic
from zope.security.proxy import Proxy, removeSecurityProxy

from zope.app import zapi
from zope.app.container.contained import Contained

import interfaces


class RegistrationStack(Contained, Persistent):
    """Registration registry implemention

       A registration stack provides support for a collection of
       registrations such that, at any time, at most one is active.  The
       "stack" aspect of the api is designed to support "uninstallation",
       as will be described below.
       """
    implements(interfaces.IRegistrationStack)

    def __init__(self, container):
        self.__parent__ = container
        self.sitemanager = zapi.getSiteManager(container)

    def register(self, registration):
        self.sitemanager.register(registration)
        self._activate(registration)

    def unregister(self, registration):
        self.sitemanager.register(registration)
        self._deactivate(registration)

    def registered(self, registration):
        self.sitemanager.registered(registration)

    def _activate(self, registration):
        zope.event.notify(RegistrationActivatedEvent(registration))
        registration.activated()

    def _deactivate(self, registration):
        zope.event.notify(RegistrationDeactivatedEvent(registration))
        registration.deactivated()

    def activate(self, registration):
        self.sitemanager.register(registration)
        self._activate(registration)


    def deactivate(self, registration):
        self.sitemanager.register(registration)
        self._deactivate(registration)

    def active(self):
        return True

    def __nonzero__(self):
        return True

    def info(self):
        # This registration stack stub does not really know about the
        # registration it manages. Thus the registration component is None
        # here. It might be that someone has a problem with this code, but I
        # am sceptical that someone used this method manually.
        return [{'active': True,
                 'registration': None}]


NULL_COMPONENT = object()

class BBBComponentRegistration(object):

    _BBB_componentPath = None

    def __init__(self, component, permission=None):
        # BBB: 12/05/2004
        if isinstance(component, (str, unicode)):
            self.componentPath = component
        else:
            # We always want to set the plain component. Untrusted code will
            # get back a proxied component anyways.
            self.component = removeSecurityProxy(component)
        if permission == 'zope.Public':
            permission = CheckerPublic
        self.permission = permission

    def getComponent(self):
        return self.__BBB_getComponent()
    getComponent = zope.deprecation.deprecated(getComponent,
                              'Use component directly. '
                              'The reference will be gone in Zope 3.3.')

    def __BBB_getComponent(self):
        if self._component is NULL_COMPONENT:
            return self.__BBB_old_getComponent(self._BBB_componentPath)

        # This condition should somehow make it in the final code, since it
        # honors the permission.
        if self.permission:
            checker = InterfaceChecker(self.getInterface(), self.permission)
            return Proxy(self._component, checker)

        return self._component

    def __BBB_old_getComponent(self, path):
        service_manager = zapi.getSiteManager(self)

        # Get the root and unproxy it
        if path.startswith("/"):
            # Absolute path
            root = removeAllProxies(zapi.getRoot(service_manager))
            component = zapi.traverse(root, path)
        else:
            # Relative path.
            ancestor = self.__parent__.__parent__
            component = zapi.traverse(ancestor, path)

        if self.permission:
            if type(component) is Proxy:
                # There should be at most one security Proxy around an object.
                # So, if we're going to add a new security proxy, we need to
                # remove any existing one.
                component = removeSecurityProxy(component)

            interface = self.getInterface()

            checker = InterfaceChecker(interface, self.permission)

            component = Proxy(component, checker)

        return component

    def __BBB_setComponent(self, component):
        self._BBB_componentPath = None
        self._component = component

    component = property(__BBB_getComponent, __BBB_setComponent)

    def __BBB_getComponentPath(self):
        if self._BBB_componentPath is not None:
            return self._BBB_componentPath
        return '/' + '/'.join(zapi.getPath(self.component))

    def __BBB_setComponentPath(self, path):
        self._component = NULL_COMPONENT
        self._BBB_componentPath = path

    componentPath = property(__BBB_getComponentPath, __BBB_setComponentPath)
    componentPath = zope.deprecation.deprecated(
        componentPath,
        'Use component directly. '
        'The reference will be gone in Zope 3.3.')

    def __setstate__(self, dict):
        super(BBBComponentRegistration, self).__setstate__(dict)
        # For some reason the component path is not set correctly by the
        # default __setstate__ mechanism.
        if 'componentPath' in dict:
            self._component = NULL_COMPONENT
            self._BBB_componentPath = dict['componentPath']

        if isinstance(self._BBB_componentPath, (str, unicode)):
            self._component = NULL_COMPONENT


class BBBRegistry(object):

    def queryRegistrationsFor(self, cfg, default=None):
        return RegistrationStack(self, cfg.name)
    queryRegistrationsFor = zope.deprecation.deprecated(
        queryRegistrationsFor,
        'This method is not needed anymore, since registration stacks are '
        'gone. There is now always only one registration per configuration '
        'in the registry. '
        'The reference will be gone in Zope 3.3.')

    def createRegistrationsFor(self, cfg):
        # Ignore
        pass
    createRegistrationsFor = zope.deprecation.deprecated(
        createRegistrationsFor,
        'This method used to create a registration stack. These stacks are '
        'gone, so that this method is not required anymore. You can now '
        'directly activate and deactivate registrations with a registry. '
        'The reference will be gone in Zope 3.3.')
    

class BBBRegistrationManager(object):

    def _SampleContainer__data(self):
        from BTrees.OOBTree import OOBTree
        if '_data' in self.__dict__:
            return OOBTree(self._data)
    _SampleContainer__data = Lazy(_SampleContainer__data)


class BBBRegisterableContainer(object):

    def registrationManager(self):
        from zope.app.component.registration import RegistrationManager
        for obj in self.values():
            if isinstance(obj, RegistrationManager):
                return obj
    registrationManager = Lazy(registrationManager)

    def getRegistrationManager(self):
        return self.registrationManager
    getRegistrationManager = zope.deprecation.deprecated(
        getRegistrationManager,
        'This method has been deprecated in favor of the '
        '`registrationManager` attribute. '
        'The reference will be gone in Zope 3.3.')

    def findModule(self, name):
        from zope.app.module import findModule
        return findModule(name)
    findModule = zope.deprecation.deprecated(
        findModule,
        'This method has been deprecated and its functionality is now '
        'available via the `zope.app.module.findModule` function. '
        'The reference will be gone in Zope 3.3.')

    def resolve(self, name):
        from zope.app.module import resolve
        return resolve(name)
    findModule = zope.deprecation.deprecated(
        findModule,
        'This method has been deprecated and its functionality is now '
        'available via the `zope.app.module.resolve` function. '
        'The reference will be gone in Zope 3.3.')
        

class BBBRegistered(object):

    def addUsage(self, location):
        # Ignore in the hope that noone uses this
        pass
    addUsage = zope.deprecation.deprecated(
        addUsage,
        'The concept of usages has been deprecated. `Registered` is now a '
        'read-only adapter. '
        'The reference will be gone in Zope 3.3.')

    def removeUsage(self, location):
        # Ignore in the hope that noone uses this
        pass
    removeUsage = zope.deprecation.deprecated(
        removeUsage,
        'The concept of usages has been deprecated. `Registered` is now a '
        'read-only adapter. '
        'The reference will be gone in Zope 3.3.')

    def usages(self):
        return [zapi.getPath(reg.component)
                for reg in self.registrations]
    usages = zope.deprecation.deprecated(
        usages,
        'The concept of usages has been deprecated. You can get the '
        'registrations for a component now via the `registrations` attribute. '
        'The reference will be gone in Zope 3.3.')

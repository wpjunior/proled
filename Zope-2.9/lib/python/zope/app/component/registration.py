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
"""Component registration support

$Id: registration.py 40422 2005-11-30 05:00:44Z fdrake $
"""
from persistent import Persistent

import zope.event
from zope.component import subscribers
from zope.interface import implements
from zope.security.checker import InterfaceChecker, CheckerPublic
from zope.security.proxy import Proxy, removeSecurityProxy

from zope.app import zapi
from zope.app.component.interfaces import registration as interfaces
from zope.app.container.btree import BTreeContainer
from zope.app.container.contained import Contained
from zope.app.dependable.interfaces import IDependable, DependencyError
from zope.app.event import objectevent
from zope.app.location import inside
from zope.app.traversing.interfaces import TraversalError
from zope.app.i18n import ZopeMessageFactory as _

# BBB: First introduced in 3.1; should go away in 3.3 
import bbb


class RegistrationEvent(objectevent.ObjectEvent):
    """An event that is created when a registration-related activity occurred.
    """
    implements(interfaces.IRegistrationEvent)

class RegistrationActivatedEvent(RegistrationEvent):
    """An event that is created when a registration is activated."""
    implements(interfaces.IRegistrationActivatedEvent)

class RegistrationDeactivatedEvent(RegistrationEvent):
    """An event that is created when a registration is deactivated."""
    implements(interfaces.IRegistrationDeactivatedEvent)


class RegistrationStatusProperty(object):
    """A descriptor used to implement `IRegistration`'s `status` property."""
    def __get__(self, inst, klass):
        registration = inst
        if registration is None:
            return self

        registry = registration.getRegistry()
        if registry and registry.registered(registration):
            return interfaces.ActiveStatus

        return interfaces.InactiveStatus

    def __set__(self, inst, value):
        registration = inst
        registry = registration.getRegistry()
        if registry is None:
            raise ValueError('No registry found.')

        if value == interfaces.ActiveStatus:
            if not registry.registered(registration):
                registry.register(registration)
                zope.event.notify(RegistrationActivatedEvent(registration))

        elif value == interfaces.InactiveStatus:
            if registry.registered(registration):
                registry.unregister(registration)
                zope.event.notify(RegistrationDeactivatedEvent(registration))
        else:
            raise ValueError(value)


class SimpleRegistration(Persistent, Contained):
    """Registration objects that just contain registration data"""
    implements(interfaces.IRegistration,
               interfaces.IRegistrationManagerContained)

    # See interfaces.IRegistration
    status = RegistrationStatusProperty()

    def getRegistry(self):
        """See interfaces.IRegistration"""
        raise NotImplementedError(
              'This method must be implemented by each specific regstration.')


class ComponentRegistration(bbb.registration.BBBComponentRegistration,
                            SimpleRegistration):
    """Component registration.

    Subclasses should define a getInterface() method returning the interface
    of the component.
    """
    implements(interfaces.IComponentRegistration)

    def __init__(self, component, permission=None):
        # BBB: Will go away in 3.3.
        super(ComponentRegistration, self).__init__(component, permission)
        # self.component = component
        if permission == 'zope.Public':
            permission = CheckerPublic
        self.permission = permission

    def _getComponent(self):
        if self.permission and self.interface:
            checker = InterfaceChecker(self.interface, self.permission)
            return Proxy(self._component, checker)
        return self._component

    def _setComponent(self, component):
        # We always want to set the plain component. Untrusted code will
        # get back a proxied component anyways.
        self._component = removeSecurityProxy(component)

    # See zope.app.component.interfaces.registration.IComponentRegistration
    component = property(_getComponent, _setComponent)

    # See zope.app.component.interfaces.registration.IComponentRegistration
    interface = None


def SimpleRegistrationRemoveSubscriber(registration, event):
    """Receive notification of remove event."""
    sm = zapi.getSiteManager(registration)
    removed = event.object
    if (sm == removed) or inside(sm, removed):
        # we don't really care if the registration is active, since the site
        # is going away.
        return

    objectstatus = registration.status

    if objectstatus == interfaces.ActiveStatus:
        try:
            objectpath = zapi.getPath(registration)
        except: # TODO decide if this is really the best fall-back plan
            objectpath = str(registration)
        msg = _("Can't delete active registration (${path})",
                mapping={u'path': objectpath})
        raise DependencyError(msg)


def ComponentRegistrationRemoveSubscriber(componentRegistration, event):
    """Receive notification of remove event."""
    component = componentRegistration.component
    try:
        dependents = IDependable(component)
    except TypeError:
        return
    objectpath = zapi.getPath(componentRegistration)
    dependents.removeDependent(objectpath)


def ComponentRegistrationAddSubscriber(componentRegistration, event):
    """Receive notification of add event."""
    component = componentRegistration.component
    try:
        dependents = IDependable(component)
    except TypeError:
        return
    objectpath = zapi.getPath(componentRegistration)
    dependents.addDependent(objectpath)


def componentRegistrationEventNotify(componentReg, event):
    """Subscriber to dispatch registration events for components."""
    adapters = subscribers((componentReg.component, event), None)
    for adapter in adapters:
        pass # getting them does the work


def RegisterableMoveSubscriber(registerable, event):
    """A registerable cannot be moved as long as it has registrations in the
    registration manager."""
    if event.oldParent is not None and event.newParent is not None:
        if event.oldParent is not event.newParent:
            raise DependencyError(
                _("Can't move a registered component from its container."))


class Registered(bbb.registration.BBBRegistered, object):
    """An adapter from IRegisterable to IRegistered.

    This class is the only place that knows how 'Registered'
    data is represented.
    """
    implements(interfaces.IRegistered)
    __used_for__ = interfaces.IRegisterable

    def __init__(self, registerable):
        self.registerable = registerable

    def registrations(self):
        rm = zapi.getParent(self.registerable).registrationManager
        return [reg for reg in rm.values()
                if (interfaces.IComponentRegistration.providedBy(reg) and
                    reg.component is self.registerable)]


class RegistrationManager(bbb.registration.BBBRegistrationManager,
                          BTreeContainer):
    """Registration manager

    Manages registrations within a package.
    """
    implements(interfaces.IRegistrationManager)

    def addRegistration(self, reg):
        "See IWriteContainer"
        key = self._chooseName('', reg)
        self[key] = reg
        return key

    def _chooseName(self, name, reg):
        """Choose a name for the registration."""
        if not name:
            name = reg.__class__.__name__

        i = 1
        chosenName = name
        while chosenName in self:
            i += 1
            chosenName = name + str(i)

        return chosenName


class RegisterableContainer(bbb.registration.BBBRegisterableContainer):
    """Mix-in to implement `IRegisterableContainer`"""
    implements(interfaces.IRegisterableContainer,
               interfaces.IRegisterableContainerContaining)

    def __init__(self):
        super(RegisterableContainer, self).__init__()
        self.__createRegistrationManager()

    def __createRegistrationManager(self):
        "Create a registration manager and store it as `registrationManager`"
        # See interfaces.IRegisterableContainer
        self.registrationManager = RegistrationManager()
        self.registrationManager.__parent__ = self
        self.registrationManager.__name__ = '++registrations++'
        zope.event.notify(
            objectevent.ObjectCreatedEvent(self.registrationManager))


class RegistrationManagerNamespace(object):
    """Used to traverse to a Registration Manager from a
       Registerable Container."""
    __used_for__ = interfaces.IRegisterableContainer

    def __init__(self, ob, request=None):
        self.context = ob.registrationManager

    def traverse(self, name, ignore):
        if name == '':
            return self.context
        raise TraversalError(self.context, name)

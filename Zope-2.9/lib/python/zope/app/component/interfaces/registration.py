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
"""Interfaces for objects supporting registration

$Id: registration.py 39064 2005-10-11 18:40:10Z philikon $
"""
import zope.component.interfaces
from zope.interface import Interface, Attribute, implements
from zope.schema import Field, Choice, vocabulary
from zope.schema.interfaces import IField

from zope.app.annotation.interfaces import IAttributeAnnotatable
from zope.app.container.interfaces import IContainerNamesContainer
from zope.app.container.interfaces import IContained, IContainer
from zope.app.container.constraints import contains, containers
from zope.app.event.interfaces import IObjectEvent
from zope.app.i18n import ZopeMessageFactory as _

from zope.app.component import bbb

InactiveStatus = _('Inactive')
ActiveStatus = _('Active')


class IRegistrationEvent(IObjectEvent):
    """An event that involves a registration"""

class IRegistrationActivatedEvent(IRegistrationEvent):
    """This event is fired, when a component's registration is activated."""

class IRegistrationDeactivatedEvent(IRegistrationEvent):
    """This event is fired, when a component's registration is deactivated."""


class IRegistration(Interface):
    """Registration object

    A registration object represents a specific registration
    decision, such as registering an adapter or defining a permission.

    In addition to the attributes or methods defined here,
    registration objects will include additional attributes
    identifying how they should be used. For example, a service
    registration will provide a service type. An adapter
    registration will specify a used-for interface and a provided
    interface.
    """

    status = Choice(
        title=_("Registration status"),
        vocabulary=vocabulary.SimpleVocabulary(
            (vocabulary.SimpleTerm(InactiveStatus, title=InactiveStatus),
             vocabulary.SimpleTerm(ActiveStatus, title=ActiveStatus))),
        default=ActiveStatus
        )

class IComponent(IField):
    """A component path

    This is just the interface for the ComponentPath field below.  We'll use
    this as the basis for looking up an appropriate widget.
    """

class Component(Field):
    """A component path

    Values of the field are absolute unicode path strings that can be
    traversed to get an object.
    """
    implements(IComponent)


class IComponentRegistration(IRegistration):
    """Registration object that uses a component.

    An interface can optionally be specified that describes the interface the
    component provides for the registry.
    
    The interface will be used to produce a proxy for the component, if
    the permission is also specified.
    """
    component = Component(
        title=_("Registration Component"),
        description=_("The component the registration is for."),
        required=True)

    interface = Field(
        title=_("Component Interface"),
        description=_("The interface the component provides through this "
                      "registration."),
        required=False,
        default=None)

    permission = Choice(
        title=_("The permission needed to use the component"),
        vocabulary="Permissions",
        required=False
        )


class IRegistry(zope.component.interfaces.IRegistry):
    """A component that can be configured using a registration manager."""

    def register(registration):
        """Register a component with the registry using a registration.

        Once the registration is added to the registry, it will be active. If
        the registration is already registered with the registry, this method
        will quietly return.
        """

    def unregister(registration):
        """Unregister a component from the registry.

        Unregistering a registration automatically makes the component
        inactive. If the registration is not registered, this method will
        quietly return.
        """

    def registered(registration):
        """Determine whether a registration is registered with the registry.

        The method will return a Boolean value.
        """


class ILocatedRegistry(zope.component.interfaces.IRegistry):
    """A registry that is located in a tree of registries.

    
    """
    next = Attribute("Set the next local registry in the tree. This attribute "
                     "represents the parent of this registry node. If the "
                     "value is `None`, then this registry represents the "
                     "root of the tree")

    subs = Attribute("A collection of registries that describe the next level "
                     "of the registry tree. They are the children of this "
                     "registry node. This attribute should never be "
                     "manipulated manually. Use `addSub()` and `removeSub()` "
                     "instead.")

    base = Attribute("Outside of the local registry tree lies the global "
                     "registry, which is known as the base to every local "
                     "registry in the tree.")

    def addSub(sub):
        """Add a new sub-registry to the node.

        Important: This method should *not* be used manually. It is
        automatically called by `setNext()`. To add a new registry to the
        tree, use `sub.setNext(self, self.base)` instead!
        """

    def removeSub(sub):
        """Remove a sub-registry to the node.

        Important: This method should *not* be used manually. It is
        automatically called by `setNext()`. To remove a registry from the
        tree, use `sub.setNext(None)` instead!
        """

    def setNext(next, base=None):
        """Set the next/parent registry in the tree.

        This method should ensure that all relevant registies are updated
        correctly as well.
        """


class IRegistrationManager(IContainerNamesContainer):
    """Manage Registrations"""
    contains(IRegistration)

    def addRegistration(registration):
        """Add a registration to the manager.

        The function will automatically choose a name as which the
        registration will be known. The name of the registration inside this
        manager is returned.
        """


class IRegistrationManagerContained(IContained):
    """Objects that can be contained by the registration manager should
    implement this interface."""
    containers(IRegistrationManager)


class IRegisterableContainer(IContainer):
    """Containers with registration managers

    These are site-management folders of one sort or another.

    The container allows clients to access the registration manager
    without knowing it's name.

    The registration manager container *also* supports local-module
    lookup.
    """

    registrationManager = Field(
        title=_("Registration Manager"),
        description=_("The registration manager keeps track of all component "
                    "registrations."))


class IRegisterable(IContained):
    """Mark a component as registerable.

    All registerable components need to implement this interface. 
    """
    containers(IRegisterableContainer)


class IRegisterableContainerContaining(IContainer):
    """A container that can only contain `IRegisterable`s and
    `IRegisterableContainer`s.

    This interface was designed to be always used together with the
    `IRegisterableContainer`.
    """
    contains(IRegisterable, IRegisterableContainer)
    

class IRegistered(Interface, bbb.interfaces.IBBBRegistered):
    """An object that can track down its registrations.

    The object need not implement this functionality itself, but must at
    least support doing so via an adapter.
    """

    def registrations():
        """Return a sequence of registration objects for this object."""

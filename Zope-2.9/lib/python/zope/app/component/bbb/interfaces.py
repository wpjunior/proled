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
"""Various BBB interfaces

$Id$
"""
__docformat__ = "reStructuredText"
from zope.interface import Interface

class IRegistrationStack(Interface):
    """A stack of registrations for a set of parameters

    A service will have a registry containing registry stacks
    for specific parameters.  For example, an adapter service will
    have a registry stack for each given used-for and provided
    interface.

    The registry stack works like a stack: the first element is
    active; when it is removed, the element after it is automatically
    activated.  An explicit None may be present (at most once) to
    signal that nothing is active.  To deactivate an element, it is
    moved to the end.
    """

    def register(registration):
        """Register the given registration without activating it.

        Do nothing if the registration is already registered.
        """

    def unregister(registration):
        """Unregister the given registration.

        Do nothing if the registration is not registered.

        Implies deactivate() if the registration is active.
        """

    def registered(registration):
        """Is the registration registered?

        Return a boolean indicating whether the registration has been
        registered.
        """

    def activate(registration):
        """Make the registration active.

        The activated() method is called on the registration.  If
        another registration was previously active, its deactivated()
        method is called first.

        If the argument is None, the currently active registration if
        any is disabled and no new registration is activated.

        Raises a ValueError if the given registration is not registered.
        """

    def deactivate(registration):
        """Make the registration inactive.

        If the registration is active, the deactivated() method is
        called on the registration.  If this reveals a registration
        that was previously active, that registration's activated()
        method is called.

        Raises a ValueError if the given registration is not registered.

        The call has no effect if the registration is registered but
        not active.
        """

    def active():
        """Return the active registration, if any.

        Otherwise, returns None.
        """

    def info():
        """Return a sequence of registration information.

        The sequence items are mapping objects with keys:

        active -- A boolean indicating whether the registration is
                  active.

        registration -- The registration object.
        """

    def __nonzero__(self):
        """The registry is true iff it has no registrations."""


class IBBBRegistry(Interface):

    def queryRegistrationsFor(registration, default=None):
        """Return an IRegistrationStack for the registration.

        Data on the registration is used to decide which registry to
        return. For example, a service manager will use the
        registration name attribute to decide which registry
        to return.

        Typically, an object that implements this method will also
        implement a method named queryRegistrations, which takes
        arguments for each of the parameters needed to specify a set
        of registrations.

        The registry must be in the context of the registry.

        """

    def createRegistrationsFor(registration):
        """Create and return an IRegistrationStack for the registration.

        Data on the registration is used to decide which regsitry to
        create. For example, a service manager will use the
        registration name attribute to decide which regsitry
        to create.

        Typically, an object that implements this method will also
        implement a method named createRegistrations, which takes
        arguments for each of the parameters needed to specify a set
        of registrations.

        Calling createRegistrationsFor twice for the same registration
        returns the same registry.

        The registry must be in the context of the registry.

        """


class IBBBRegisterableContainer(Interface):

    def getRegistrationManager():
        """Get a registration manager.

        Find a registration manager.  Clients can get the
        registration manager without knowing its name. Normally,
        folders have one registration manager. If there is more than
        one, this method will return one; which one is undefined.

        An error is raised if no registration manager can be found.
        """

    def findModule(name):
        """Find the module of the given name.

        If the module can be find in the folder or a parent folder
        (within the site manager), then return it, otherwise, delegate
        to the module service.

        This must return None when the module is not found.
        """

    def resolve(name):
        """Resolve a dotted object name.

        A dotted object name is a dotted module name and an object
        name within the module.

        TODO: We really should switch to using some other character than
        a dot for the delimiter between the module and the object
        name.
        """    


class IBBBRegistered(Interface):
    """An object that can keep track of its configured uses.

    The object need not implement this functionality itself, but must at
    least support doing so via an adapter.
    """

    def addUsage(location):
        """Add a usage by location.

        The location is the physical path to the registration object that
        configures the usage.
        """
    def removeUsage(location):
        """Remove a usage by location.

        The location is the physical path to the registration object that
        configures the usage.
        """
    def usages():
        """Return a sequence of locations.

        A location is a physical path to a registration object that
        configures a usage.
        """


class IBBBSiteManager(Interface):
    """Service Managers act as containers for Services.

    If a Service Manager is asked for a service, it checks for those it
    contains before using a context-based lookup to find another service
    manager to delegate to.  If no other service manager is found they defer
    to the ComponentArchitecture ServiceManager which contains file based
    services.
    """

    def queryRegistrations(name, default=None):
        """Return an IRegistrationStack for the registration name.

        queryRegistrationsFor(cfg, default) is equivalent to
        queryRegistrations(cfg.name, default)
        """

    def createRegistrationsFor(registration):
        """Create and return an IRegistrationRegistry for the registration
        name.

        createRegistrationsFor(cfg, default) is equivalent to
        createRegistrations(cfg.name, default)
        """

    def listRegistrationNames():
        """Return a list of all registered registration names.
        """

    def queryActiveComponent(name, default=None):
        """Finds the registration registry for a given name, checks if it has
        an active registration, and if so, returns its component.  Otherwise
        returns default.
        """

    def queryLocalService(service_type, default=None):
        """Return a local service, if there is one

        A local service is one configured in the local service manager.
        """

    def addSubsite(subsite):
        """Add a subsite of the site

        Local sites are connected in a tree. Each site knows about
        its containing sites and its subsites.

        BBB: Replaced by addSub in ILocatedRegistry
        """
    

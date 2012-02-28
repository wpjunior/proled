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
"""Interfaces for folders.

$Id: interfaces.py 27514 2004-09-13 15:54:05Z fdrake $
"""
import zope.schema
from zope.deprecation import deprecated
from zope.interface import Interface

from zope.app.component.interfaces import registration
from zope.app.container.interfaces import IContainer
from zope.app.component.interfaces import IPossibleSite, ISite
from zope.app.component.interfaces import ILocalSiteManager
from zope.app.component.interfaces import ISiteManagementFolder

deprecated(('IPossibleSite', 'ISite'),
           'This interface has been moved to zope.app.component.interfaces. '
           'The reference will be gone in Zope 3.3.')

ISiteManager = ILocalSiteManager

deprecated('ISiteManager',
           'This interface has been moved to zope.app.component.interfaces '
           'and been renamed ISiteManager. '
           'The reference will be gone in Zope 3.3.')

class ILocalService(registration.IRegisterable):
    """A local service isn't a local service if it doesn't implement this.

    The contract of a local service includes collaboration with
    services above it.  A local service should also implement
    IRegisterable (which implies that it is adaptable to
    IRegistered).  Implementing ILocalService implies this.
    """

class ISimpleService(ILocalService):
    """Most local services should implement this instead of ILocalService.

    It implies a specific way of implementing IRegisterable,
    by subclassing IAttributeRegisterable.
    """

deprecated(('ILocalService', 'ISimpleService'),
           'The concept of services has been removed. Use utilities instead. '
           'The reference will be gone in Zope 3.3.')

class IComponentManager(Interface):

    def queryComponent(type=None, filter=None, all=0):
        """Return all components that match the given type and filter

        The objects are returned a sequence of mapping objects with keys:

        path -- The component path

        component -- The component

        all -- A flag indicating whether all component managers in
               this place should be queried, or just the local one.

        """

deprecated('IComponentManager',
           'This interface has been removed. It was horrible anyways. '
           'The reference will be gone in Zope 3.3.')

class IBindingAware(Interface):

    def bound(name):
        """Inform a service component that it is providing a service

        Called when an immediately-containing service manager binds
        this object to perform the named service.
        """

    def unbound(name):
        """Inform a service component that it is no longer providing a service

        Called when an immediately-containing service manager unbinds
        this object from performing the named service.
        """

deprecated('IBindingAware',
           'Now that services are gone, we do not need the binding support. '
           'The reference will be gone in Zope 3.3.')

class IServiceRegistration(registration.IComponentRegistration):
    """Service Registration

    Service registrations are dependent on the components that they
    configure. They register themselves as component dependents.

    The name of a service registration is used to determine the service
    type.
    """

    name = zope.schema.TextLine(
        title=u"Name",
        description=u"The name that is registered",
        readonly=True,
        # Don't allow empty or missing name:
        required=True,
        min_length=1,
        )

deprecated('IServiceRegistration',
           'The concept of services has been removed. Use utilities instead. '
           'The reference will be gone in Zope 3.3.')

class ISiteManagementFolders(IContainer, IComponentManager):
    """A collection of ISiteManagementFolder objects.

    An ISiteManagementFolders object supports simple containment as
    well as package query and lookup.
    
    """

deprecated('ISiteManagementFolders',
           'This interface has been removed. It was unused. '
           'The reference will be gone in Zope 3.3.')

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
"""Interfaces for the Local Component Architecture

$Id: __init__.py 39064 2005-10-11 18:40:10Z philikon $
"""
import zope.interface
import zope.schema
import zope.component
from zope.app.container.interfaces import IContainer
from zope.app.container.constraints import ContainerTypesConstraint
from zope.app.container.constraints import ItemTypePrecondition
from zope.app.i18n import ZopeMessageFactory as _
import registration

class ILocalAdapterRegistry(registration.IRegistry,
                            registration.ILocatedRegistry):

    def adaptersChanged():
        """Update the adapter surrogates, since the registrations changed."""

    def baseChanged():
        """Someone changed the base registry

        This should only happen during testing
        """

class IPossibleSite(zope.interface.Interface):
    """An object that could be a site
    """

    def setSiteManager(sitemanager):
        """Sets the site manager for this object.
        """

    def getSiteManager():
        """Returns the site manager contained in this object.

        If there isn't a site manager, raise a component lookup.
        """

class ISite(IPossibleSite):
    """Marker interface to indicate that we have a site"""

class ILocalSiteManager(zope.component.interfaces.ISiteManager,
                        registration.ILocatedRegistry,
                        registration.IRegistry):
    """Site Managers act as containers for registerable components.

    If a Site Manager is asked for an adapter or utility, it checks for those
    it contains before using a context-based lookup to find another site
    manager to delegate to.  If no other site manager is found they defer to
    the global site manager which contains file based utilities and adapters.
    """

class INewLocalSite(zope.interface.Interface):

    manager = zope.interface.Attribute("The new site manager")

class NewLocalSite:
    zope.interface.implements(INewLocalSite)
    
    def __init__(self, manager):
        self.manager = manager


class ISiteManagementFolder(registration.IRegisterableContainer,
                            IContainer):
    """Component and component registration containers."""

    __parent__ = zope.schema.Field(
        constraint = ContainerTypesConstraint(
            ILocalSiteManager,
            registration.IRegisterableContainer,
            ),
        )

class ILocalUtility(registration.IRegisterable):
    """Local utility marker.

    A marker interface that indicates that a component can be used as
    a local utility.

    Utilities should usually also declare they implement
    IAttributeAnnotatable, so that the standard adapter to
    IRegistered can be used; otherwise, they must provide
    another way to be adaptable to IRegistered.
    """


class IAdapterRegistration(registration.IComponentRegistration):
    """Local Adapter Registration for Local Adapter Registry

    The adapter registration is used to provide local adapters via the
    adapter registry. It is an extended component registration, whereby the
    component is the adapter factory in this case.
    """
    required = zope.schema.Choice(
        title = _("For interface"),
        description = _("The interface of the objects being adapted"),
        vocabulary="Interfaces",
        readonly = True,
        required=False,
        default=None)

    with = zope.schema.Tuple(
        title = _("With interfaces"),
        description = _("Additionally required interfaces"),
        readonly=True,
        value_type = zope.schema.Choice(vocabulary='Interfaces'),
        required=False,
        default=())

    provided = zope.schema.Choice(
        title = _("Provided interface"),
        description = _("The interface provided"),
        vocabulary="Interfaces",
        readonly = True,
        required = True)

    name = zope.schema.TextLine(
        title=_(u"Name"),
        readonly=False,
        required=True,
        default=u''
        )

    permission = zope.schema.Choice(
        title=_("The permission required for use"),
        vocabulary="Permission Ids",
        readonly=False,
        required=False,
        )

    # TODO: for now until we figure out a way to specify the factory directly
    factoryName = zope.schema.TextLine(
        title=_(u"Factory Name"),
        readonly=False,
        required=False,
        )


class IUtilityRegistration(IAdapterRegistration):
    """Utility registration object.

    Adapter registries are also used to to manage utilities, since utilities
    are adapters that are instantiated and have no required interfaces. Thus,
    utility registrations must fulfill all requirements of an adapter
    registration as well.
    """

    name = zope.schema.TextLine(
        title=_("Register As"),
        description=_("The name under which the utility will be known."),
        readonly=False,
        required=True,
        default=u''
        )

    provided = zope.schema.Choice(
        title=_("Provided interface"),
        description=_("The interface provided by the utility"),
        vocabulary="Utility Component Interfaces",
        readonly=True,
        required=True,
        )

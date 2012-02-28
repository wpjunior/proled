##############################################################################
#
# Copyright (c) 2002-2005 Zope Corporation and Contributors.
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

$Id: interfaces.py 28654 2004-12-20 21:13:50Z gintautasm $
"""
from zope.deprecation import deprecated
from zope.interface import Interface, implements
from zope.schema import TextLine
from zope.schema.interfaces import ITextLine
from zope.app.component.interfaces import registration

UnregisteredStatus = registration.InactiveStatus
RegisteredStatus = registration.InactiveStatus
ActiveStatus = registration.ActiveStatus

deprecated(('UnregisteredStatus', 'RegisteredStatus'),
           'Registered and unregistered status has have been collapsed into '
           'zope.app.component.interfaces.registration.InactiveStatus. '
           'Will be gone in Zope 3.3.')
deprecated('ActiveStatus',
           'ActiveStatus is now available in '
           'zope.app.component.interfaces.registration. '
           'Will be gone in Zope 3.3.')

IRegistrationEvent = registration.IRegistrationEvent
IRegistrationActivatedEvent = registration.IRegistrationActivatedEvent
IRegistrationDeactivatedEvent = registration.IRegistrationDeactivatedEvent

deprecated(('IRegistrationEvent',
            'IRegistrationActivatedEvent', 'IRegistrationDeactivatedEvent'),
           'The registration events have moved to '
           'zope.app.component.interfaces.registration. '
           'Will be gone in Zope 3.3.')


class INoLocalServiceError(Interface):
    """No local service to register with."""

class NoLocalServiceError(Exception):
    """No local service to configure

    An attempt was made to register a registration for which there is
    no local service.
    """
    implements(INoLocalServiceError)

deprecated(('INoLocalServiceError', 'NoLocalServiceError'),
           'The concept of services has been removed. This event will '
           'be gone in Zope 3.3.')

IRegistration = registration.IRegistration

deprecated(('IRegistrationEvent',
            'IRegistrationActivatedEvent', 'IRegistrationDeactivatedEvent'),
           'The registration events have moved to '
           'zope.app.component.interfaces.registration. '
           'Will be gone in Zope 3.3.')

class IComponentPath(ITextLine):
    """A component path

    This is just the interface for the ComponentPath field below.  We'll use
    this as the basis for looking up an appropriate widget.
    """

class ComponentPath(TextLine):
    """A component path

    Values of the field are absolute unicode path strings that can be
    traversed to get an object.
    """
    implements(IComponentPath)

deprecated(('IComponentPath', 'ComponentPath'),
           'Registrations now use component references instead of component '
           'paths. Use zope.app.component.interfaces.registration.Component '
           'instead. This field will be gone in Zope 3.3.')

IComponentRegistration = registration.IComponentRegistration

deprecated('IComponentRegistration',
           'The IComponentRegistration interface has moved to '
           'zope.app.component.interfaces.registration. '
           'This reference will be gone in Zope 3.3.')

from zope.app.component.bbb.interfaces import IRegistrationStack

deprecated('IRegistrationStack',
           'The registration stack concept has been removed. '
           'This interface will be gone in Zope 3.3.')

IRegistry = registration.IRegistry

deprecated('IRegistry',
           'The IRegistry interface has moved to '
           'zope.app.component.interfaces.registration. '
           'This reference will be gone in Zope 3.3.')

class IOrderedContainer(Interface):
    """Containers whose items can be reorderd."""

    def moveTop(names):
        """Move the objects corresponding to the given names to the top.
        """

    def moveUp(names):
        """Move the objects corresponding to the given names up.
        """

    def moveBottom(names):
        """Move the objects corresponding to the given names to the bottom.
        """

    def moveDown(names):
        """Move the objects corresponding to the given names down.
        """

deprecated('IOrderedContainer',
           'The ordered container should have not been declared here. The '
           'registerable container does not support this interface anymore, '
           'since it was useless anyways. '
           'This interface will be gone in Zope 3.3.')

IRegistrationManager = registration.IRegistrationManager
IRegisterableContainer = registration.IRegisterableContainer
IRegisterable = registration.IRegisterable
IRegistered = registration.IRegistered

deprecated(('IRegistrationManager', 'IRegisterableContainer',
            'IRegisterable', 'IRegistered'), 
           'This interface has moved to '
           'zope.app.component.interfaces.registration. '
           'This reference will be gone in Zope 3.3.')

IAttributeRegisterable = IRegisterable

deprecated('IAttributeRegisterable', 
           'Registrations are not stored on the component anymore and thus '
           'the attribute registerable is now simply a registerable. '
           'This reference will be gone in Zope 3.3.')

class INoRegistrationManagerError(Interface):
    """No registration manager error
    """

class NoRegistrationManagerError(Exception):
    """No registration manager

    There is no registration manager in a site-management folder, or
    an operation would result in no registration manager in a
    site-management folder.

    """
    implements(INoRegistrationManagerError)

deprecated(('INoRegistrationManagerError', 'NoRegistrationManagerError'),
           'It is now guaranteed that a registerable container has a '
           'registration manager; thus this error is never raised. '
           'This event will be gone in Zope 3.3.')

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
"""Component registration support for services

$Id: registration.py 29078 2005-02-07 22:50:03Z garrett $
"""
from zope.deprecation import deprecated

from zope.app.component import registration
from zope.component import subscribers
from zope.component import subscribers
from zope.component import subscribers

RegistrationEvent = registration.RegistrationEvent
RegistrationActivatedEvent = registration.RegistrationActivatedEvent
RegistrationDeactivatedEvent = registration.RegistrationDeactivatedEvent

deprecated(('RegistrationEvent',
            'RegistrationActivatedEvent', 'RegistrationDeactivatedEvent'),
           'The registration events have moved to '
           'zope.app.component.registration. '
           'Will be gone in Zope 3.3.')

RegistrationStatusPropery = registration.RegistrationStatusProperty

deprecated('RegistrationStatusProperty',
           'The status property has moved to zope.app.component.registration. '
           'Will be gone in Zope 3.3.')

from zope.app.component.bbb.registration import RegistrationStack
NotifyingRegistrationStack = RegistrationStack

deprecated(('RegistrationStack', 'NotifyingRegistrationStack'),
           'The registration stack concept has been removed. '
           'This class will be gone in Zope 3.3.')

SimpleRegistrationRemoveSubscriber = \
    registration.SimpleRegistrationRemoveSubscriber
SimpleRegistration = registration.SimpleRegistration

ComponentRegistration = registration.ComponentRegistration
ComponentRegistrationAddSubscriber = \
    registration.ComponentRegistrationAddSubscriber
ComponentRegistrationRemoveSubscriber = \
    registration.ComponentRegistrationRemoveSubscriber
RegisterableMoveSubscriber = registration.RegisterableMoveSubscriber

Registered = registration.Registered

RegistrationManager = registration.RegistrationManager

RegisterableContainer = registration.RegisterableContainer

deprecated(('ComponentRegistration', 'ComponentRegistrationAddSubscriber',
            'ComponentRegistrationRemoveSubscriber',
            'RegisterableMoveSubscriber', 'Registered',
            'RegistrationManager', 'RegisterableContainer'),
           'This class has moved to zope.app.component.registration. '
           'The reference will be gone in Zope 3.3.')

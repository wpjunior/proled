##############################################################################
#
# Copyright (c) 2003 Zope Corporation and Contributors.
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
"""Interfaces pertaining to local utilities.

$Id: interfaces.py 28582 2004-12-08 00:46:02Z srichter $
"""
import zope.component.interfaces
from zope.deprecation import deprecated

from zope.app.component.interfaces import IUtilityRegistration, ILocalUtility
from zope.app.component.interfaces.registration import IRegistry

deprecated(('IUtilityRegistration', 'ILocalUtility'),
           'This interface has been moved to zope.app.component.interfaces. '
           'The reference will be gone in Zope 3.3.')

class ILocalUtilityService(
        zope.component.interfaces.IUtilityService,
        IRegistry,
        ):
    """Local Utility Service."""

deprecated('ILocalUtilityService',
           'The concept of services has been removed. Use site manager API. '
           'The reference will be gone in Zope 3.3.')

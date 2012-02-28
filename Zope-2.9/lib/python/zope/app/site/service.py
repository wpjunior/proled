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
"""Service Manager code

$Id: service.py 29078 2005-02-07 22:50:03Z garrett $
"""
__docformat__ = "reStructuredText"
import zope.interface
import zope.deprecation

from zope.app.component.site import LocalSiteManager, UtilityRegistration
from zope.app.component.interfaces.registration import \
     IRegisterableContainerContaining as IRegisterableContainerContainer

zope.deprecation.__show__.off()
from zope.component.bbb.service import IService
from interfaces import IServiceRegistration
zope.deprecation.__show__.on()

zope.deprecation.deprecated(
    ('SiteManager', 'UtilityRegistration'),
    'This class has been moved to zope.app.component.site. '
    'The reference will be gone in Zope 3.3.')

zope.deprecation.deprecated(
    'IRegisterableContainerContainer',
    'This interface has been moved to zope.app.component.interfaces '
    'and been renamed to IRegisterableContainerContaining. '
    'The reference will be gone in Zope 3.3.')

ServiceManager = LocalSiteManager
SiteManager = LocalSiteManager

class ServiceRegistration(UtilityRegistration):
    zope.interface.implements(IServiceRegistration)

    def __init__(self, name, path, context=None):
        super(ServiceRegistration, self).__init__(name, IService, path)

zope.deprecation.deprecated(
    ('ServiceManager', 'ServiceRegistration'),
    'The concept of services has been removed. Use utilities instead. '
    'The reference will be gone in Zope 3.3.')

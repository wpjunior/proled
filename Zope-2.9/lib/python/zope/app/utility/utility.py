##############################################################################
# Copyright (c) 2003 Zope Corporation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
##############################################################################
"""Local utility service implementation.

Besides being functional, this module also serves as an example of
creating a local service; see README.txt.

$Id: utility.py 28662 2004-12-21 03:29:21Z srichter $
"""
from persistent import Persistent
from zope.deprecation import deprecated

from zope.app.component import getNextUtility, queryNextUtility
from zope.app.component.testing import testingNextUtility
from zope.app.component.site import UtilityRegistration
from zope.app.container.contained import Contained

deprecated(('getNextUtility', 'queryNextUtility'),
           'This function has been moved to zope.app.component. '
           'The reference will be gone in Zope 3.3.')

deprecated('testingNextUtility',
           'This function has been moved to zope.app.component.testing. '
           'The reference will be gone in Zope 3.3.')

deprecated('UtilityRegistration',
           'This class has been moved to zope.app.component.site. '
           'The reference will be gone in Zope 3.3.')


class LocalUtilityService(Persistent, Contained):
    # I really hope noone noone is using this class manually! 
    # ...6 months later: Yes, my book does. :(

    def getUtilitiesFor(self, interface):
        sm = self.__parent__.__parent__
        return sm.getUtilitiesFor(interface)
    
    def getUtility(self, interface, name=''):
        sm = self.__parent__.__parent__
        return sm.queryUtility(interface, name)

    def queryUtility(self, interface, name='', default=None):
        sm = self.__parent__.__parent__
        return sm.queryUtility(interface, name, default)


deprecated('LocalUtilityService',
           'Services have been removed. Use site manager API. '
           'The reference will be gone in Zope 3.3.')

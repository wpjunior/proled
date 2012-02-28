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
"""Service Manager Container

$Id: servicecontainer.py 25177 2004-06-02 13:17:31Z jim $
"""
__docformat__ = "reStructuredText"
from zope.deprecation import deprecated

from zope.app.component.site import SiteManagerContainer

ServiceManagerContainer = SiteManagerContainer

deprecated('ServiceManagerContainer',
           'This class has been moved to zope.app.component.site '
           'and been renamed to SiteManagerContainer. '
           'The reference will be gone in Zope 3.3.')

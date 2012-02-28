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
"""Collection of many common api functions

Makes imports easier

$Id: __init__.py 39058 2005-10-11 18:31:25Z philikon $
"""
from interfaces import IZAPI
from zope.interface import moduleProvides

from zope.security.proxy import isinstance

from zope.app.interface import queryType

moduleProvides(IZAPI)
__all__ = tuple(IZAPI)

from zope.component import *

from zope.app.publisher.browser import getDefaultViewName
from zope.app.publisher.browser import queryDefaultViewName
from zope.app.traversing.api import *
from zope.app.traversing.browser.absoluteurl import absoluteURL
from zope.app.exception.interfaces import UserError

name = getName

def principals():
    from zope.app.security.interfaces import IAuthentication
    return getUtility(IAuthentication)

# BBB: Gone in 3.3.
from zope.deprecation import deprecated
from zope.app import servicenames

deprecated('servicenames',
           'The concept of services has been removed. Please use utilities '
           'instead. This reference will be removed in Zope 3.3.')

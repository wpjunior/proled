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
"""Content Type convenience lookup functions 

$Id: __init__.py 26721 2004-07-23 20:46:49Z pruggera $
"""
__docformat__ = 'restructuredtext'
from zope.app.interface import queryType
from zope.app.content.interfaces import IContentType

def queryContentType(object):
    """Returns the interface implemented by object which implements
    `IContentType`."""
    return queryType(object, IContentType)



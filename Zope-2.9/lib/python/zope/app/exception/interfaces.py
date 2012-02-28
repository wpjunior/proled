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
"""General exceptions

$Id: interfaces.py 28280 2004-10-28 22:56:34Z jim $
"""
__docformat__ = 'restructuredtext'

from zope.interface import Interface, implements

class IUserError(Interface):
    """User error exceptions
    """

class UserError(Exception):
    """User errors

    These exceptions should generally be displayed to users unless
    they are handled.
    """
    implements(IUserError)

class ISystemErrorView(Interface):
    """Error views that can classify their contexts as system errors
    """

    def isSystemError():
        """Return a boolean indicating whether the error is a system errror
        """
    

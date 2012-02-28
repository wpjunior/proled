##############################################################################
#
# Copyright (c) 2004 Zope Corporation and Contributors.
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
"""Security Tests

$Id: __init__.py 29143 2005-02-14 22:43:16Z srichter $
"""
from zope.app import zapi
from zope.app.security.permission import Permission
from zope.app.security.interfaces import IPermission

def addCheckerPublic():
    """Add the CheckerPublic permission as 'zope.Public'"""

    perm = Permission('zope.Public', 'Public',
            """Special permission used for resources that are always public

            The public permission is effectively an optimization, sine
            it allows security computation to be bypassed.
            """
            )
    gsm = zapi.getGlobalSiteManager()
    gsm.provideUtility(IPermission, perm, perm.id)

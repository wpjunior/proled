##############################################################################
#
# Copyright (c) 2004 Zope Corporation and Contributors. All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
""" CMFSetup product initialization.

$Id: __init__.py 38660 2005-09-28 10:33:45Z yuppie $
"""

from AccessControl import ModuleSecurityInfo

from Products.GenericSetup import BASE, EXTENSION
from Products.GenericSetup import ManagePortal
from Products.GenericSetup import profile_registry


security = ModuleSecurityInfo( 'Products.CMFSetup' )
security.declareProtected( ManagePortal, 'profile_registry' )

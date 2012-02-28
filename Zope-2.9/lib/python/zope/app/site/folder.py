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
"""A site management folder contains components and component registrations.

$Id: folder.py 25177 2004-06-02 13:17:31Z jim $
"""
from zope.deprecation import deprecated
from zope.app.container.btree import BTreeContainer

from zope.app.component.site import SiteManagementFolder
from zope.app.component.site import SMFolderFactory

deprecated(('SiteManagementFolder', 'SMFolderFactory'),
           'This class has moved to zope.app.component.site. '
           'The reference will be gone in Zope 3.3.')

# I really hope that noone is using this.
class SiteManagementFolders(BTreeContainer):
    pass

deprecated('SiteManagementFolders',
           'This class has been deprecated. It was not used anyways. '
           'The reference will be gone in Zope 3.3.')

##############################################################################
#
# Copyright (c) 2001 Zope Corporation and Contributors. All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
""" Backward-compatibility module for CMFTopic product permissions.

$Id: TopicPermissions.py 36457 2004-08-12 15:07:44Z jens $
"""

from permissions import *

from warnings import warn

warn( "The module, 'Products.CMFTopic.TopicPermissions' is a deprecated "
      "compatiblity alias for 'Products.CMFTopic.permissions';  please use "
      "the new module instead.", DeprecationWarning)

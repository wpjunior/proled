##############################################################################
#
# Copyright (c) 2003 Zope Corporation and Contributors. All Rights Reserved.
# 
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
# 
##############################################################################
""" Product: CMFActionIcons

Define tool for mapping CMF actions onto icons.

$Id: __init__.py 40391 2005-11-28 16:21:21Z yuppie $
"""
from Products.CMFCore.DirectoryView import registerDirectory
from Products.CMFCore.utils import ToolInit
try:
    from Products.CMFSetup import EXTENSION
    from Products.CMFSetup import profile_registry
    from Products.CMFCore.interfaces import ISiteRoot
    has_profile_registry = True
except ImportError:
    has_profile_registry = False

import ActionIconsTool

actionicons_globals = globals()

registerDirectory( 'skins', actionicons_globals )

def initialize( context ):

    ToolInit( meta_type='CMF Action Icons Tool'
            , tools=( ActionIconsTool.ActionIconsTool, )
            , icon="tool.gif"
            ).initialize( context )

    if has_profile_registry:
        profile_registry.registerProfile('actionicons',
                                         'CMFActionIcons',
                                         'Adds action icon tool / settings.',
                                         'profiles/actionicons',
                                         'CMFActionIcons',
                                         EXTENSION,
                                         for_=ISiteRoot,
                                        )

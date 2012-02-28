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
"""Unique id generation and handling.

$Id: __init__.py 69357 2006-08-05 16:43:48Z shh $
"""

from sys import modules

from Products.CMFCore import utils
from Products.CMFCore.interfaces import ISiteRoot
from Products.GenericSetup import EXTENSION
from Products.GenericSetup import profile_registry

import UniqueIdAnnotationTool
import UniqueIdGeneratorTool
import UniqueIdHandlerTool

tools = (
    UniqueIdAnnotationTool.UniqueIdAnnotationTool,
    UniqueIdGeneratorTool.UniqueIdGeneratorTool,
    UniqueIdHandlerTool.UniqueIdHandlerTool,
)

this_module = modules[ __name__ ]

z_tool_bases = utils.initializeBasesPhase1(tools, this_module)

my_globals=globals()

def initialize(context):

    utils.initializeBasesPhase2(z_tool_bases, context)

    utils.ToolInit( 'CMF Unique Id Tool'
                  , tools=tools
                  , icon='tool.gif'
                  ).initialize(context)

    profile_registry.registerProfile('default',
                                     'CMFUid',
                                     'Adds UID support.',
                                     'profiles/default',
                                     'CMFUid',
                                     EXTENSION,
                                     for_=ISiteRoot)

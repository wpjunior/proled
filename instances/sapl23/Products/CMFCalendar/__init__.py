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
""" CMF Calendar product.

$Id: __init__.py 40635 2005-12-07 21:12:32Z tseaver $
"""

import sys

from Products.CMFCore import utils
from Products.CMFCore.interfaces import ISiteRoot
from Products.CMFCore.DirectoryView import registerDirectory
from Products.GenericSetup import EXTENSION
from Products.GenericSetup import profile_registry

import Event
import CalendarTool
from permissions import AddPortalContent


this_module = sys.modules[ __name__ ]

contentConstructors = (Event.addEvent,)
contentClasses = (Event.Event,)

tools = ( CalendarTool.CalendarTool, )

z_bases = utils.initializeBasesPhase1( contentClasses, this_module )

# This is used by a script (external method) that can be run
# to set up Events in an existing CMF Site instance.
event_globals=globals()

# Make the skins available as DirectoryViews
registerDirectory('skins', globals())

def initialize( context ):
    utils.ToolInit('CMF Calendar Tool', tools=tools, icon='tool.gif',
                   ).initialize( context )

    utils.initializeBasesPhase2( z_bases, context )
    utils.ContentInit( 'CMF Event'
                     , content_types = contentClasses
                     , permission = AddPortalContent
                     , extra_constructors = contentConstructors
                     , fti = Event.factory_type_information
                     ).initialize( context )

    profile_registry.registerProfile('default',
                                     'CMFCalendar',
                                     'Adds calendar support.',
                                     'profiles/default',
                                     'CMFCalendar',
                                     EXTENSION,
                                     for_=ISiteRoot,
                                    )

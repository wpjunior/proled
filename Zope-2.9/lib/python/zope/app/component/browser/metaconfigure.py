##############################################################################
#
# Copyright (c) 2001, 2002 Zope Corporation and Contributors.
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
"""Configuration handlers for 'tool' directive.

$Id: metaconfigure.py 28807 2005-01-12 16:19:27Z srichter $
"""
from zope.app.component.metaconfigure import utility
from zope.app.component.metaconfigure import interface as ifaceDirective
from tools import IToolType, IToolConfiguration, ToolConfiguration


def tool(_context, interface, title, description=None,
         folder="tools", unique=False):
    name = interface.getName()
    permission = 'zope.ManageContent'
    tool = ToolConfiguration(interface, title, description, unique)

    ifaceDirective(_context, interface, IToolType)
    utility(_context, IToolConfiguration, tool,
            permission=permission, name=name)

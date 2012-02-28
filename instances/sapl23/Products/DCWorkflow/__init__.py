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
""" Web-configurable workflow.

$Id: __init__.py 40346 2005-11-23 17:15:03Z yuppie $
"""

from Products.CMFCore.interfaces import ISiteRoot
from Products.CMFCore.utils import registerIcon
from Products.GenericSetup import EXTENSION
from Products.GenericSetup import profile_registry

import DCWorkflow, States, Transitions, Variables, Worklists, Scripts
import Default


def initialize(context):
    
    context.registerHelp(directory='help')
    context.registerHelpTitle('DCWorkflow')
    
    registerIcon(DCWorkflow.DCWorkflowDefinition,
                 'images/workflow.gif', globals())
    registerIcon(States.States,
                 'images/state.gif', globals())
    States.StateDefinition.icon = States.States.icon
    registerIcon(Transitions.Transitions,
                 'images/transition.gif', globals())
    Transitions.TransitionDefinition.icon = Transitions.Transitions.icon
    registerIcon(Variables.Variables,
                 'images/variable.gif', globals())
    Variables.VariableDefinition.icon = Variables.Variables.icon
    registerIcon(Worklists.Worklists,
                 'images/worklist.gif', globals())
    Worklists.WorklistDefinition.icon = Worklists.Worklists.icon
    registerIcon(Scripts.Scripts,
                 'images/script.gif', globals())

    profile_registry.registerProfile('revision2',
                                     'CMF Default Workflow [Revision 2]',
                                     'Adds revision 2 of default workflow.',
                                     'profiles/revision2',
                                     'DCWorkflow',
                                     EXTENSION,
                                     for_=ISiteRoot)

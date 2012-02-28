##############################################################################
#
# Copyright (c) 2002 Zope Corporation and Contributors. All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
""" Unit tests for DefaultWorkflow module.

$Id: test_DefaultWorkflow.py 38418 2005-09-09 08:40:13Z yuppie $
"""

from unittest import TestCase, TestSuite, makeSuite, main
import Testing
try:
    import Zope2
except ImportError: # BBB: for Zope 2.7
    import Zope as Zope2
Zope2.startup()

from Products.CMFCore.tests.base.dummy import DummyContent
from Products.CMFCore.tests.base.dummy import DummySite
from Products.CMFCore.tests.base.dummy import DummyTool
from Products.CMFCore.tests.base.dummy import DummyUserFolder

from Products.CMFCore.WorkflowTool import addWorkflowFactory
from Products.CMFCore.WorkflowTool import WorkflowTool

from Products.CMFDefault.MembershipTool import MembershipTool
from Products.CMFDefault.DefaultWorkflow import DefaultWorkflowDefinition

class DefaultWorkflowDefinitionTests(TestCase):

    def setUp(self):

        self.site = DummySite('site')
        self.site._setObject('portal_types', DummyTool())
        self.site._setObject('portal_workflow', WorkflowTool())
        self.site._setObject('portal_membership', MembershipTool())
        self.site._setObject('acl_users', DummyUserFolder())

        addWorkflowFactory(DefaultWorkflowDefinition,
                           id='default_workflow', title='default_workflow')

        self._constructDummyWorkflow()

    def test_z2interfaces(self):
        from Interface.Verify import verifyClass
        from Products.CMFCore.interfaces.portal_workflow \
                import WorkflowDefinition as IWorkflowDefinition
        from Products.CMFDefault.DefaultWorkflow \
                import DefaultWorkflowDefinition

        verifyClass(IWorkflowDefinition, DefaultWorkflowDefinition)

    def test_z3interfaces(self):
        try:
            from zope.interface.verify import verifyClass
            from Products.CMFCore.interfaces import IWorkflowDefinition
        except ImportError:
            # BBB: for Zope 2.7
            return
        from Products.CMFDefault.DefaultWorkflow \
                import DefaultWorkflowDefinition

        verifyClass(IWorkflowDefinition, DefaultWorkflowDefinition)

    def _constructDummyWorkflow(self):

        wftool = self.site.portal_workflow
        wftool.manage_addWorkflow('default_workflow (default_workflow)', 'wf')
        wftool.setDefaultChain('wf')

    def _getDummyWorkflow(self):
        wftool = self.site.portal_workflow
        return wftool.wf

    def test_isActionSupported(self):

        wf = self._getDummyWorkflow()
        dummy = self.site._setObject('dummy', DummyContent())

        for action in ('submit', 'retract', 'publish', 'reject',):
            self.assert_(wf.isActionSupported(dummy, action))

    def test_isActionSupported_with_keywargs(self):

        wf = self._getDummyWorkflow()
        dummy = self.site._setObject('dummy', DummyContent())

        for action in ('submit', 'retract', 'publish', 'reject',):
            self.assert_(wf.isActionSupported(dummy, action,
                                              arg1=1, arg2=2))

    # XXX more tests...

def test_suite():
    return TestSuite((
        makeSuite( DefaultWorkflowDefinitionTests ),
        ))

if __name__ == '__main__':
    main(defaultTest='test_suite')

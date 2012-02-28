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
""" Unit tests for DiscussionTool module.

$Id: test_DiscussionTool.py 38418 2005-09-09 08:40:13Z yuppie $
"""

from unittest import TestCase, TestSuite, makeSuite, main
import Testing
try:
    import Zope2
except ImportError: # BBB: for Zope 2.7
    import Zope as Zope2
Zope2.startup()


class DiscussionToolTests(TestCase):

    def test_z2interfaces(self):
        from Interface.Verify import verifyClass
        from Products.CMFCore.DiscussionTool import DiscussionTool
        from Products.CMFCore.interfaces.portal_actions \
                import ActionProvider as IActionProvider
        from Products.CMFCore.interfaces.portal_discussion \
                import oldstyle_portal_discussion as IOldstyleDiscussionTool

        verifyClass(IActionProvider, DiscussionTool)
        verifyClass(IOldstyleDiscussionTool, DiscussionTool)

    def test_z3interfaces(self):
        try:
            from zope.interface.verify import verifyClass
            from Products.CMFCore.interfaces import IActionProvider
            from Products.CMFCore.interfaces import IOldstyleDiscussionTool
        except ImportError:
            # BBB: for Zope 2.7
            return
        from Products.CMFCore.DiscussionTool import DiscussionTool

        verifyClass(IActionProvider, DiscussionTool)
        verifyClass(IOldstyleDiscussionTool, DiscussionTool)


class OldDiscussableTests(TestCase):

    def test_z2interfaces(self):
        from Interface.Verify import verifyClass
        from Products.CMFCore.DiscussionTool import OldDiscussable
        from Products.CMFCore.interfaces.Discussions \
                import OldDiscussable as IOldDiscussable

        verifyClass(IOldDiscussable, OldDiscussable)

    def test_z3interfaces(self):
        try:
            from zope.interface.verify import verifyClass
            from Products.CMFCore.interfaces import IOldstyleDiscussable
        except ImportError:
            # BBB: for Zope 2.7
            return
        from Products.CMFCore.DiscussionTool import OldDiscussable

        verifyClass(IOldstyleDiscussable, OldDiscussable)


def test_suite():
    return TestSuite((
        makeSuite( DiscussionToolTests ),
        makeSuite( OldDiscussableTests ),
        ))

if __name__ == '__main__':
    main(defaultTest='test_suite')

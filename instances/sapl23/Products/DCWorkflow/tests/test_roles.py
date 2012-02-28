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
""" Unit tests of role-mapping machinery.

$Id: test_roles.py 37135 2005-07-08 13:24:33Z tseaver $
"""

import unittest
import Testing
try:
    import Zope2
except ImportError: # BBB: for Zope 2.7
    import Zope as Zope2
Zope2.startup()

from OFS.Folder import Folder
from OFS.Application import Application
from Products.DCWorkflow.utils \
     import modifyRolesForPermission, modifyRolesForGroup


class RoleMapTests(unittest.TestCase):

    def setUp(self):
        self.app = Application()
        self.app.ob = Folder()
        self.ob = self.app.ob
        self.ob.__ac_local_roles__ = {
            '(Group) Administrators': ['Manager', 'Member'],
            '(Group) Users': ['Member'],
            }
        self.ob._View_Permission = ('Member', 'Manager')
        self.ob._View_management_screens_Permission = ('Manager',)

    def testModifyRolesForGroup(self):
        modifyRolesForGroup(
            self.ob, '(Group) Administrators', ['Owner'], ['Member', 'Owner'])
        modifyRolesForGroup(
            self.ob, '(Group) Users', [], ['Member'])
        self.assertEqual(self.ob.__ac_local_roles__, {
            '(Group) Administrators': ['Manager', 'Owner'],
            })
        modifyRolesForGroup(
            self.ob, '(Group) Administrators', ['Member'], ['Member', 'Owner'])
        modifyRolesForGroup(
            self.ob, '(Group) Users', ['Member'], ['Member'])
        self.assertEqual(self.ob.__ac_local_roles__, {
            '(Group) Administrators': ['Manager', 'Member'],
            '(Group) Users': ['Member'],
            })

    def testModifyRolesForPermission(self):
        modifyRolesForPermission(self.ob, 'View', ['Manager'])
        modifyRolesForPermission(
            self.ob, 'View management screens', ['Member'])
        self.assertEqual(self.ob._View_Permission, ['Manager'])
        self.assertEqual(
            self.ob._View_management_screens_Permission, ['Member'])


def test_suite():
    return unittest.makeSuite(RoleMapTests)

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')

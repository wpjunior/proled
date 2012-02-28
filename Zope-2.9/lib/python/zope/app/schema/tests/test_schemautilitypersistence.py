##############################################################################
#
# Copyright (c) 2003 Zope Corporation and Contributors.
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
"""Tests for Schema Utility Persistence

$Id: test_schemautilitypersistence.py 29143 2005-02-14 22:43:16Z srichter $
"""
import unittest

from persistent.tests.persistenttestbase import PersistentTest, DM
from zope.app.schema.wrapper import Struct
from zope.app.schema.schema import SchemaUtility
from zope.schema import Text, getFieldsInOrder
from zope.app.testing import setup

class PSchema(SchemaUtility):

    def __init__(self):
        super(PSchema, self).__init__()
        self.x = 0
        self.setName('PSchema')

    def inc(self):
        self.x += 1

class PersistentSchemaUtilityTest(PersistentTest):

    klass = PSchema

    def setUp(self):
        PersistentTest.setUp(self)
        setup.placefulSetUp(self)

    def testState(self):
        pass

#     def testChangeField(self):
#         f = Text(title=u'alpha')
#         p = self.klass()
#         p._p_oid = '\0\0\0\0\0\0hi'
#         dm = DM()
#         p._p_jar = dm
#         self.assertEqual(p._p_changed, 0)
#         self.assertEqual(dm.called, 0)
#         p.addField('alpha', f)
#         self.assertEqual(p._p_changed, 1)
#         self.assertEqual(dm.called, 1)
#         p._p_changed = 0
#         self.assertEqual(p._p_changed, 0)
#         self.assertEqual(dm.called, 1)
#         field = p['alpha']
#         field.title = u'Beta'
#         self.assertEqual(f._p_changed, 1)
#         self.assertEqual(p._p_changed, 1)
#         self.assertEqual(dm.called, 2)

#     def testAddField(self):
#         f = Text(title=u'alpha')
#         p = self.klass()
#         p._p_oid = '\0\0\0\0\0\0hi'
#         dm = DM()
#         p._p_jar = dm
#         self.assertEqual(p._p_changed, 0)
#         self.assertEqual(dm.called, 0)
#         p.addField('alpha', f)
#         self.assertEqual(p._p_changed, 1)
#         self.assertEqual(dm.called, 1)

#     def testRemoveField(self):
#         f = Text(title=u'alpha')
#         p = self.klass()
#         p._p_oid = '\0\0\0\0\0\0hi'
#         dm = DM()
#         p._p_jar = dm
#         self.assertEqual(p._p_changed, 0)
#         self.assertEqual(dm.called, 0)
#         p.addField('alpha', f)
#         self.assertEqual(p._p_changed, 1)
#         self.assertEqual(dm.called, 1)
#         p._p_changed = 0
#         self.assertEqual(p._p_changed, 0)
#         self.assertEqual(dm.called, 1)
#         p.removeField('alpha')
#         self.assertEqual(p._p_changed, 1)
#         self.assertEqual(dm.called, 2)

    def tearDown(self):
        PersistentTest.tearDown(self)
        setup.placefulTearDown()

def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(PersistentSchemaUtilityTest))
    return suite

if __name__ == '__main__':
    unittest.main()

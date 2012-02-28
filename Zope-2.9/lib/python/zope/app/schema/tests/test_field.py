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
"""Field Tests

$Id: test_field.py 29143 2005-02-14 22:43:16Z srichter $
"""
import unittest

from persistent.tests.persistenttestbase import DM

from zope.configuration import xmlconfig
from zope.schema import Text, getFieldsInOrder
from zope.security.checker import ProxyFactory
from zope.security.management import system_user, newInteraction
from zope.app.testing import setup
from zope.app.schema.wrapper import Struct
from zope.security.checker import getChecker, _defaultChecker
import zope.app.schema.tests


class ParticipationStub(object):

    def __init__(self, principal):
        self.principal = principal
        self.interaction = None


class FieldPersistence(unittest.TestCase):

    def test_field_change(self):
        f = Text(title=u'alpha')
        f = Struct(f)
        f._p_oid = '\0\0\0\0\0\0hi'
        dm = DM()
        f._p_jar = dm
        self.assertEqual(f._p_changed, 0)
        f.title = u'bar'
        self.assertEqual(f._p_changed, 1)
        self.assertEqual(dm.called, 1)

class FieldPermissions(unittest.TestCase):

    def setUp(self):
        setup.placefulSetUp()
        self.context = xmlconfig.file("fields.zcml", zope.app.schema.tests)

    def test_wrapped_field_checker(self):
        f1 = Text(title=u'alpha')
        f1 = ProxyFactory(f1)
        f2 = Text(title=u'alpha')
        f2 = Struct(f2)
        f2 = ProxyFactory(f2)
        self.assertEquals(getChecker(f1), getChecker(f2))
        self.failIf(getChecker(f1) is _defaultChecker)
        self.failIf(getChecker(f2) is _defaultChecker)

    def tearDown(self):
        setup.placefulTearDown()

def test_suite():
    return unittest.TestSuite((
        unittest.makeSuite(FieldPersistence),
        unittest.makeSuite(FieldPermissions),
        ))

if __name__ == '__main__':
    unittest.main()

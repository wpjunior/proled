##############################################################################
#
# Copyright (c) 2002 Zope Corporation and Contributors.
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
"""Test Persistent Schemas

$Id: test_schemautility.py 29143 2005-02-14 22:43:16Z srichter $
"""
from unittest import TestCase, makeSuite, TestSuite

from zope.configuration import xmlconfig
from zope.schema import Text, getFieldNamesInOrder, getFieldsInOrder
from zope.security.checker import getChecker, _defaultChecker, ProxyFactory
from zope.app.schema.schema import SchemaUtility
from zope.app.testing import setup
from zope.app import zapi
import zope.app.schema.tests

class ParticipationStub(object):

    def __init__(self, principal):
        self.principal = principal
        self.interaction = None


class SchemaUtilityTests(TestCase):

    def _createSchemaUtility(self):
        return SchemaUtility()

    def _additionalSetup(self):
        self.s = self._createSchemaUtility()
        self.s.setName('IFoo')
        self.alpha = Text(title=u"alpha")

    def setUp(self):
        setup.placefulSetUp()
        self._additionalSetup()

    def test_addField(self):
        s = self.s
        s.addField(u'alpha', self.alpha)
        self.assertEquals(
            [u'alpha',],
            getFieldNamesInOrder(s))

    def test_addFieldInsertsAtEnd(self):
        s = self.s
        s.addField(u'alpha', self.alpha)
        beta = Text(title=u"Beta")
        s.addField(u'beta', beta)
        self.assertEquals(
            [u'alpha', u'beta'],
            getFieldNamesInOrder(s))

    def test_removeField(self):
        s = self.s
        s.addField(u'alpha', self.alpha)
        s.removeField(u'alpha')
        self.assertEquals(
            [],
            getFieldNamesInOrder(s))

    def test_addFieldCollision(self):
        s = self.s
        s.addField(u'alpha', self.alpha)
        self.assertRaises(KeyError, s.addField, 'alpha', self.alpha)

    def test_removeFieldNotPresent(self):
        self.assertRaises(KeyError, self.s.removeField, 'alpha')

    def test_renameField(self):
        s = self.s
        s.addField(u'alpha', self.alpha)
        s.renameField(u'alpha', 'beta')
        self.assertEquals(
            [u'beta'],
            getFieldNamesInOrder(s))

    def test_renameFieldCollision(self):
        s = self.s
        s.addField(u'alpha', self.alpha)
        s.addField(u'beta', Text(title=u"Beta"))
        self.assertRaises(KeyError, s.renameField, 'alpha', 'beta')

    def test_renameFieldNotPresent(self):
        self.assertRaises(KeyError, self.s.renameField, 'alpha', 'beta')

    def test_insertField(self):
        s = self.s
        s.addField(u'alpha', self.alpha)
        beta = Text(title=u"Beta")
        s.insertField(u'beta', beta, 0)
        self.assertEquals(
            [u'beta', u'alpha'],
            getFieldNamesInOrder(s))

    def test_insertFieldCollision(self):
        s = self.s
        s.addField(u'alpha', self.alpha)
        beta = Text(title=u"Beta")
        self.assertRaises(KeyError, s.insertField, 'alpha', beta, 0)

    def test_insertFieldCornerCases(self):
        s = self.s
        gamma = Text(title=u"Gamma")
        # it's still possible to insert at beginning
        s.insertField(u'gamma', gamma, 0)
        self.assertEquals(
            [u'gamma'],
            getFieldNamesInOrder(s))
        # should be allowed to insert field at the end
        s.insertField(u'alpha', self.alpha, 1)
        self.assertEquals(
            [u'gamma', u'alpha'],
            getFieldNamesInOrder(s))
        # should be allowed to insert field at the beginning still
        delta = Text(title=u"Delta")
        s.insertField(u'delta', delta, 0)
        self.assertEquals(
            [u'delta', u'gamma', u'alpha'],
            getFieldNamesInOrder(s))

    def test_insertFieldBeyondEnd(self):
        s = self.s
        s.addField(u'alpha', self.alpha)
        beta = Text(title=u"Beta")
        self.assertRaises(IndexError, s.insertField,
                          'beta', beta, 100)

    def test_insertFieldBeforeBeginning(self):
        s = self.s
        s.addField(u'alpha', self.alpha)
        beta = Text(title=u"Beta")
        self.assertRaises(IndexError, s.insertField,
                          'beta', beta, -1)

    def test_moveField(self):
        s = self.s
        s.addField(u'alpha', self.alpha)
        beta = Text(title=u'Beta')
        s.addField(u'beta', beta)
        gamma = Text(title=u'Gamma')
        s.addField(u'gamma', gamma)
        s.moveField(u'beta', 3)
        self.assertEquals(
            [u'alpha', u'gamma', u'beta'],
            getFieldNamesInOrder(s))
        s.moveField(u'beta', 2)
        self.assertEquals(
            [u'alpha', u'gamma', u'beta'],
            getFieldNamesInOrder(s))
        s.moveField(u'beta', 1)
        self.assertEquals(
            [u'alpha', u'beta', u'gamma'],
            getFieldNamesInOrder(s))
        s.moveField(u'beta', 0)
        self.assertEquals(
            [u'beta', u'alpha', u'gamma'],
            getFieldNamesInOrder(s))

    def test_moveFieldBeyondEnd(self):
        s = self.s
        s.addField(u'alpha', self.alpha)
        beta = Text(title=u"Beta")
        s.addField(u'beta', beta)
        self.assertRaises(IndexError, s.moveField,
                          'beta', 100)

    def test_moveFieldBeforeBeginning(self):
        s = self.s
        s.addField(u'alpha', self.alpha)
        beta = Text(title=u"Beta")
        s.addField(u'beta', beta)
        self.assertRaises(IndexError, s.moveField,
                          'beta', -1)

    def test_traverseToField(self):
        context = xmlconfig.file("fields.zcml", zope.app.schema.tests)
        s = self.s
        s.addField(u'alpha', self.alpha)
        s = ProxyFactory(s)
        f1 = ProxyFactory(s[u'alpha'])
        order = f1.order
        f1 = zapi.traverse(s, 'alpha')
        self.assertEquals(f1.order, self.alpha.order)
        title = zapi.traverse(f1, 'title')
        self.assertEquals(title, self.alpha.title)
        fields = getFieldsInOrder(s)
        for k, v in fields:
            self.failUnless(v.title is not None)

    def tearDown(self):
        setup.placefulTearDown()


def test_suite():
    return TestSuite((
        makeSuite(SchemaUtilityTests),
         ))

#############################################################################
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
"""Form Directives Tests

$Id: test_directives.py 29405 2005-03-07 18:22:16Z poster $
"""
import os
import unittest
from cStringIO import StringIO

from zope.component.exceptions import ComponentLookupError
from zope.configuration.xmlconfig import xmlconfig, XMLConfig
from zope.app.traversing.interfaces import TraversalError
from zope.interface import Interface, implements
from zope.publisher.browser import TestRequest
from zope.schema import TextLine, Int
from zope.security.proxy import ProxyFactory

from zope.app import zapi
import zope.app.component
import zope.app.form.browser
import zope.app.publisher.browser
from zope.app.form.browser import TextWidget
from zope.app.testing.placelesssetup import PlacelessSetup
from zope.app.form.tests import utils

tests_path = os.path.join(
    os.path.dirname(zope.app.publisher.browser.__file__),
    'tests')

template = """<configure
   xmlns='http://namespaces.zope.org/zope'
   xmlns:browser='http://namespaces.zope.org/browser'
   i18n_domain='zope'>
   %s
   </configure>"""


request = TestRequest()

class Schema(Interface):

    text = TextLine(
        title=u'Text',
        description=u'Nice text',
        required=False)

class IC(Schema): pass

class Ob(object):
    implements(IC)

unwrapped_ob = Ob()
ob = utils.securityWrap(unwrapped_ob, IC)

class ISomeWidget(Interface):
    displayWidth = Int(
        title=u"Display Width",
        default=20,
        required=True)

class SomeWidget(TextWidget):
    implements(ISomeWidget)


class Test(PlacelessSetup, unittest.TestCase):

    def setUp(self):
        super(Test, self).setUp()
        XMLConfig('meta.zcml', zope.app.component)()
        XMLConfig('meta.zcml', zope.app.form.browser)()
        XMLConfig('meta.zcml', zope.app.publisher.browser)()

        from zope.app.testing import ztapi
        from zope.app.traversing.adapters import DefaultTraversable
        from zope.app.traversing.interfaces import ITraversable

        ztapi.provideAdapter(None, ITraversable, DefaultTraversable)

        
    def testAddForm(self):
        self.assertEqual(
            zapi.queryMultiAdapter((ob, request), name='add.html'),
            None)
        xmlconfig(StringIO(template % ("""
          <view
              type="zope.publisher.interfaces.browser.IBrowserRequest"
              for="zope.schema.interfaces.ITextLine"
              provides="zope.app.form.interfaces.IInputWidget"
              factory="zope.app.form.browser.TextWidget"
              permission="zope.Public"
              />

          <browser:addform
              for="zope.app.form.browser.tests.test_directives.IC"
              schema="zope.app.form.browser.tests.test_directives.Schema"
              name="add.html"
              label="Add a ZPT page"
              fields="text"
              permission="zope.Public" />
            """)))

        v = zapi.getMultiAdapter((ob, request), name='add.html')
        # expect to fail as standard macros are not configured
        self.assertRaises(TraversalError, v)

    def testEditForm(self):
        self.assertEqual(
            zapi.queryMultiAdapter((ob, request), name='edit.html'),
            None)
        xmlconfig(StringIO(template % ("""
          <view
              type="zope.publisher.interfaces.browser.IBrowserRequest"
              for="zope.schema.interfaces.ITextLine"
              provides="zope.app.form.interfaces.IInputWidget"
              factory="zope.app.form.browser.TextWidget"
              permission="zope.Public"
              />

          <browser:editform
              for="zope.app.form.browser.tests.test_directives.IC"
              schema="zope.app.form.browser.tests.test_directives.Schema"
              name="edit.html"
              label="Edit a ZPT page"
              fields="text"
              permission="zope.Public" />
            """)))

        v = zapi.getMultiAdapter((ob, request), name='edit.html')
        # expect to fail as standard macros are not configured
        self.assertRaises(TraversalError, v)

    def testEditFormWithMenu(self):
        self.assertEqual(
            zapi.queryMultiAdapter((ob, request), name='edit.html'),
            None)
        xmlconfig(StringIO(template % ('''
          <browser:menu id="test_menu" title="Test menu"/>
          <view
              type="zope.publisher.interfaces.browser.IBrowserRequest"
              for="zope.schema.interfaces.ITextLine"
              provides="zope.app.form.interfaces.IInputWidget"
              factory="zope.app.form.browser.TextWidget"
              permission="zope.Public"
              />
          <browser:editform
              for="zope.app.form.browser.tests.test_directives.IC"
              schema="zope.app.form.browser.tests.test_directives.Schema"
              name="edit.html"
              label="Edit a ZPT page"
              fields="text"
              permission="zope.Public"
              menu="test_menu"
              title="Test View"
              />
            ''')))

        v = zapi.queryMultiAdapter((ob, request), name='edit.html')
        # expect to fail as standard macros are not configured
        self.assertRaises(TraversalError, v)

    def testSchemaDisplay(self):
        self.assertEqual(
            zapi.queryMultiAdapter((ob, request), name='view.html'),
            None)
        xmlconfig(StringIO(template % ('''
          <view
              type="zope.publisher.interfaces.browser.IBrowserRequest"
              for="zope.schema.interfaces.IField"
              provides="zope.app.form.interfaces.IDisplayWidget"
              factory="zope.app.form.browser.DisplayWidget"
              permission="zope.Public"
              />

          <browser:schemadisplay
              for="zope.app.form.browser.tests.test_directives.IC"
              schema="zope.app.form.browser.tests.test_directives.Schema"
              name="view.html"
              label="View a ZPT page"
              fields="text"
              permission="zope.Public" />
            ''')))

        v = zapi.queryMultiAdapter((ob, request), name='view.html')
        # expect to fail as standard macros are not configured
        self.assertRaises(TraversalError, v)

    def testAddFormWithWidget(self):
        self.assertEqual(
            zapi.queryMultiAdapter((ob, request), name='add.html'),
            None)
        xmlconfig(StringIO(template % ('''
          <view
              type="zope.publisher.interfaces.browser.IBrowserRequest"
              for="zope.schema.interfaces.ITextLine"
              provides="zope.app.form.interfaces.IInputWidget"
              factory="zope.app.form.browser.TextWidget"
              permission="zope.Public"
              />

          <browser:addform
              for="zope.app.form.browser.tests.test_directives.IC"
              schema="zope.app.form.browser.tests.test_directives.Schema"
              name="add.html"
              label="Add a ZPT page"
              fields="text"
              permission="zope.Public">

            <widget
                field="text"
                class="zope.app.form.browser.tests.test_directives.SomeWidget"
                displayWidth="30"
                extra="foo"
                />

          </browser:addform>
            ''')), )

        view = zapi.queryMultiAdapter((ob, request), name='add.html')
        self.assert_(hasattr(view, 'text_widget'))
        self.assert_(isinstance(view.text_widget, SomeWidget))
        self.assertEqual(view.text_widget.extra, u'foo')
        self.assertEqual(view.text_widget.displayWidth, 30)


    def testEditFormWithWidget(self):
        self.assertEqual(
            zapi.queryMultiAdapter((ob, request), name='edit.html'),
            None)
        xmlconfig(StringIO(template % ('''
          <view
              type="zope.publisher.interfaces.browser.IBrowserRequest"
              for="zope.schema.interfaces.ITextLine"
              provides="zope.app.form.interfaces.IInputWidget"
              factory="zope.app.form.browser.TextWidget"
              permission="zope.Public"
              />

          <browser:editform
              for="zope.app.form.browser.tests.test_directives.IC"
              schema="zope.app.form.browser.tests.test_directives.Schema"
              name="edit.html"
              label="Edit a ZPT page"
              fields="text"
              permission="zope.Public">

            <widget
                field="text"
                class="zope.app.form.browser.tests.test_directives.SomeWidget"
                displayWidth="30"
                extra="foo"
                />

          </browser:editform>
            ''')), )

        view = zapi.queryMultiAdapter((ob, request), name='edit.html')
        self.assert_(hasattr(view, 'text_widget'))
        self.assert_(isinstance(view.text_widget, SomeWidget))
        self.assertEqual(view.text_widget.extra, u'foo')
        self.assertEqual(view.text_widget.displayWidth, 30)

    def testSchemaDisplayWithWidget(self):
        self.assertEqual(
            zapi.queryMultiAdapter((ob, request), name='view.html'),
            None)
        xmlconfig(StringIO(template % ('''
          <view
              type="zope.publisher.interfaces.browser.IBrowserRequest"
              for="zope.schema.interfaces.IField"
              provides="zope.app.form.interfaces.IDisplayWidget"
              factory="zope.app.form.browser.DisplayWidget"
              permission="zope.Public"
              />

          <browser:schemadisplay
              for="zope.app.form.browser.tests.test_directives.IC"
              schema="zope.app.form.browser.tests.test_directives.Schema"
              name="view.html"
              label="View a ZPT page"
              fields="text"
              permission="zope.Public">

            <browser:widget
                field="text"
                class="zope.app.form.browser.tests.test_directives.SomeWidget"
                displayWidth="30"
                extra="foo"
                />
          </browser:schemadisplay>
            ''')))

        view = zapi.queryMultiAdapter((ob, request), name='view.html')
        self.assert_(hasattr(view, 'text_widget'))
        self.assert_(isinstance(view.text_widget, SomeWidget))
        self.assertEqual(view.text_widget.extra, u'foo')
        self.assertEqual(view.text_widget.displayWidth, 30)


def test_suite():
    loader=unittest.TestLoader()
    return loader.loadTestsFromTestCase(Test)

if __name__=='__main__':
    unittest.TextTestRunner().run(test_suite())

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
"""Date Widget tests

$Id: test_datewidget.py 26567 2004-07-16 06:58:27Z srichter $
"""
import unittest, doctest
from zope.app.datetimeutils import parseDatetimetz
from zope.app.form.browser.tests.test_browserwidget import SimpleInputWidgetTest
from zope.app.form.interfaces import IInputWidget
from zope.app.form.browser import DateWidget
from zope.app.form.interfaces import ConversionError, WidgetInputError
from zope.schema import Date
from zope.interface.verify import verifyClass

class DateWidgetTest(SimpleInputWidgetTest):
    """Documents and tests the date widget.

        >>> verifyClass(IInputWidget, DateWidget)
        True
    """

    _FieldFactory = Date
    _WidgetFactory = DateWidget

    def test_hasInput(self):
        del self._widget.request.form['field.foo']
        self.failIf(self._widget.hasInput())
        self._widget.request.form['field.foo'] = u''
        self.failUnless(self._widget.hasInput())
        self._widget.request.form['field.foo'] = u'2003/03/26'
        self.failUnless(self._widget.hasInput())

    def test_getInputValue(self):
        TEST_DATE= u'2003/03/26'
        self._widget.request.form['field.foo'] = u''
        self.assertRaises(WidgetInputError, self._widget.getInputValue)
        self._widget.request.form['field.foo'] = TEST_DATE
        self.assertEquals(
            self._widget.getInputValue(), 
            parseDatetimetz(TEST_DATE).date())
        self._widget.request.form['field.foo'] = u'abc'
        self.assertRaises(ConversionError, self._widget.getInputValue)


def test_suite():
    return unittest.TestSuite((
        unittest.makeSuite(DateWidgetTest),
        doctest.DocTestSuite(),
        ))

if __name__=='__main__':
    unittest.main(defaultTest='test_suite')


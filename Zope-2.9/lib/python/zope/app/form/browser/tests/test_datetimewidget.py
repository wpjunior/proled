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
"""Datetime Widget Tests

$Id: test_datetimewidget.py 26567 2004-07-16 06:58:27Z srichter $
"""
import unittest, doctest
from zope.app.datetimeutils import parseDatetimetz
from zope.app.form.browser.tests.test_browserwidget import SimpleInputWidgetTest
from zope.app.form.interfaces import IInputWidget
from zope.app.form.browser import DatetimeWidget
from zope.app.form.interfaces import ConversionError, WidgetInputError
from zope.interface.verify import verifyClass

from zope.schema import Datetime


class DatetimeWidgetTest(SimpleInputWidgetTest):
    """Documents and tests the datetime widget.
        
        >>> verifyClass(IInputWidget, DatetimeWidget)
        True
    """

    _FieldFactory = Datetime
    _WidgetFactory = DatetimeWidget

    def test_hasInput(self):
        del self._widget.request.form['field.foo']
        self.failIf(self._widget.hasInput())
        # widget has input, even if input is an empty string
        self._widget.request.form['field.foo'] = u''
        self.failUnless(self._widget.hasInput())
        self._widget.request.form['field.foo'] = u'2003/03/26 12:00:00'
        self.failUnless(self._widget.hasInput())

    def test_getInputValue(self):
        TEST_DATE= u'2003/03/26 12:00:00'
        self._widget.request.form['field.foo'] = u''
        self.assertRaises(WidgetInputError, self._widget.getInputValue)
        self._widget.request.form['field.foo'] = TEST_DATE
        self.assertEquals(self._widget.getInputValue(), parseDatetimetz(TEST_DATE))
        self._widget.request.form['field.foo'] = u'abc'
        self.assertRaises(ConversionError, self._widget.getInputValue)


def test_suite():
    return unittest.TestSuite((
        unittest.makeSuite(DatetimeWidgetTest),
        doctest.DocTestSuite(),
        ))

if __name__=='__main__':
    unittest.main(defaultTest='test_suite')


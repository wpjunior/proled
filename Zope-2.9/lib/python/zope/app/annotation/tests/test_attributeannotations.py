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
"""Tests the 'AttributeAnnotations' adapter.

$Id: test_attributeannotations.py 26559 2004-07-15 21:22:32Z srichter $
"""
from unittest import main, makeSuite
from zope.testing.cleanup import CleanUp # Base class w registry cleanup
from zope.app.annotation.tests.annotations import IAnnotationsTest
from zope.app.annotation.attribute import AttributeAnnotations
from zope.app.annotation.interfaces import IAttributeAnnotatable
from zope.interface import implements

class Dummy(object):
    implements(IAttributeAnnotatable)

class AttributeAnnotationsTest(IAnnotationsTest, CleanUp):

    def setUp(self):
        self.annotations = AttributeAnnotations(Dummy())
        super(AttributeAnnotationsTest, self).setUp()


def test_suite():
    return makeSuite(AttributeAnnotationsTest)

if __name__=='__main__':
    main(defaultTest='test_suite')

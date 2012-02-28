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
"""Test the gts ZCML namespace directives.

$Id: testi18ndirectives.py 39985 2005-11-08 20:00:30Z jim $
"""
import os
import unittest

from zope.component.tests.placelesssetup import PlacelessSetup
from zope.configuration import xmlconfig

from zope.app import zapi
from zope.i18n.interfaces import ITranslationDomain
import zope.app.i18n
import zope.i18n.tests

template = """<configure
   xmlns='http://namespaces.zope.org/zope'
   xmlns:i18n='http://namespaces.zope.org/i18n'>
   %s
   </configure>"""


class DirectivesTest(PlacelessSetup, unittest.TestCase):

    def setUp(self):
        super(DirectivesTest, self).setUp()
        self.context = xmlconfig.file('meta.zcml', zope.app.i18n)

    def testRegisterTranslations(self):
        eq = self.assertEqual
        eq(zapi.queryUtility(ITranslationDomain), None)
        xmlconfig.string(
            template % '''
            <configure package="zope.i18n.tests">
            <i18n:registerTranslations directory="./locale" />
            </configure>
            ''', self.context)
        path = os.path.join(os.path.dirname(zope.i18n.tests.__file__),
                            'locale', 'en',
                            'LC_MESSAGES', 'zope-i18n.mo')
        util = zapi.getUtility(ITranslationDomain, 'zope-i18n')
        eq(util._catalogs, {'test': ['test'], 'en': [unicode(path)]})


def test_suite():
    return unittest.makeSuite(DirectivesTest)

if __name__ == '__main__':
    unittest.TextTestRunner().run(test_suite())

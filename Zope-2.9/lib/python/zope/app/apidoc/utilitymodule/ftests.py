##############################################################################
#
# Copyright (c) 2003, 2004 Zope Corporation and Contributors.
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
"""Functional Tests for Utility Documentation Module.

$Id: ftests.py 29269 2005-02-23 22:22:48Z srichter $
"""
import unittest
from zope.app.testing.functional import BrowserTestCase

class UtilityModuleTests(BrowserTestCase):
    """Just a couple of tests ensuring that the templates render."""

    def testMenu(self):
        response = self.publish(
            '/++apidoc++/Utility/menu.html', 
            basic='mgr:mgrpw')
        self.assertEqual(response.getStatus(), 200)
        body = response.getBody()
        self.assert_(body.find('IDocumentationModule') > 0)
        self.checkForBrokenLinks(body, '/++apidoc++/Utility/menu.html',
                                 basic='mgr:mgrpw')

    def testUtilityDetailsView(self):
        response = self.publish(
            '/++apidoc++/Utility/'
            'zope.app.apidoc.interfaces.IDocumentationModule/'
            'Utility/index.html',
            basic='mgr:mgrpw')
        self.assertEqual(response.getStatus(), 200)
        body = response.getBody()
        self.assert_(
            body.find(
               'zope.app.apidoc.utilitymodule.utilitymodule.UtilityModule') > 0)
        self.checkForBrokenLinks(
            body,
            '/++apidoc++/Utility/'
            'zope.app.apidoc.interfaces.IDocumentationModule/'
            'Utility/index.html',
            basic='mgr:mgrpw')


def test_suite():
    return unittest.TestSuite((
        unittest.makeSuite(UtilityModuleTests),
        ))

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')

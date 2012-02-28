##############################################################################
#
# Copyright (c) 2001 Zope Corporation and Contributors. All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE
#
##############################################################################
"""
$Id: tests.py 37557 2005-07-29 18:19:31Z benji_york $
"""

import sys
import os
import unittest
import StringIO

from zope.structuredtext import stng
from zope.structuredtext.document import Document
from zope.structuredtext.html import HTML

package_dir = os.path.dirname(stng.__file__)
regressions = os.path.join(package_dir, 'regressions')

files = ['index.stx','Acquisition.stx','ExtensionClass.stx',
        'MultiMapping.stx','examples.stx','Links.stx','examples1.stx',
        'table.stx','InnerLinks.stx']

def readFile(dirname,fname):
    myfile = open(os.path.join(dirname, fname), "r")
    lines = myfile.readlines()
    myfile.close()
    return ''.join(lines)

class StngTests(unittest.TestCase):

    def testDocumentClass(self):
        # testing Document
        # *cough* *cough* this can't be enough...
        for f in files:
            doc = Document()
            raw_text = readFile(regressions, f)
            text = stng.structurize(raw_text)
            self.assert_(doc(text))

    def testRegressionsTests(self):
        # HTML regression test
        for f in files:
            raw_text = readFile(regressions, f)
            doc = stng.structurize(raw_text)
            doc = Document()(doc)
            html = HTML()(doc)

            reg_fname = f.replace('.stx','.ref')
            reg_html  = readFile(regressions , reg_fname)

            self.assertEqual(reg_html.strip(), html.strip())

class BasicTests(unittest.TestCase):

    def _test(self, stxtxt, expected):
        doc = stng.structurize(stxtxt)
        doc = Document()(doc)
        output = HTML()(doc, level=1)
        self.failIf(output.find(expected) == -1)

    def testUnderline(self):
        self._test("xx _this is html_ xx",
                   "xx <u>this is html</u> xx")

    def testUnderline1(self):
        self._test("xx _this is html_",
                   "<u>this is html</u>")

    def testEmphasis(self):
        self._test("xx *this is html* xx",
                   "xx <em>this is html</em> xx")

    def testStrong(self):
        self._test("xx **this is html** xx",
                   "xx <strong>this is html</strong> xx")

    def testUnderlineThroughoutTags(self):
        self._test('<a href="index_html">index_html</a>',
                   '<a href="index_html">index_html</a>')

    def testUnderscoresInLiteral1(self):
        self._test("def __init__(self)",
                   "def __init__(self)")

    def testUnderscoresInLiteral2(self):
        self._test("this is '__a_literal__' eh",
                   "<code>__a_literal__</code>")

    def testUnderlinesWithoutWithspaces(self):
        self._test("Zopes structured_text is sometimes a night_mare",
                   "Zopes structured_text is sometimes a night_mare")

    def testAsterisksInLiteral(self):
        self._test("this is a '*literal*' eh",
        "<code>*literal*</code>")

    def testDoubleAsterisksInLiteral(self):
        self._test("this is a '**literal**' eh",
        "<code>**literal**</code>")

    def testLinkInLiteral(self):
        self._test("this is a '\"literal\":http://www.zope.org/.' eh",
        '<code>"literal":http://www.zope.org/.</code>')

    # TODO need unicode tests


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(StngTests))
    suite.addTest(unittest.makeSuite(BasicTests))
    return suite

def main():
    unittest.TextTestRunner().run(test_suite())

if __name__ == '__main__':
    main()

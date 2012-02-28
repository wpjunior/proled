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
"""Testing vocabulary directive.

$Id: test_directives.py 29143 2005-02-14 22:43:16Z srichter $
"""
import unittest

from zope.app.testing.placelesssetup import PlacelessSetup
from zope.configuration import xmlconfig
from zope.app.schema.vocabulary import ZopeVocabularyRegistry

import zope.app.schema


class MyFactory(object):
    def __init__(self, context, **kw):
        self.ob = context
        self.kw = kw


class DirectivesTest(PlacelessSetup, unittest.TestCase):

    extra_keywords = {"filter": "my-filter",
                      "another": "keyword"}

    def check_vocabulary_get(self, kw={}):
        context = object()
        registry = ZopeVocabularyRegistry()
        vocab = registry.get(context, "my-vocab")
        self.assert_(vocab.ob is context)
        self.assertEqual(vocab.kw, kw)

    def test_simple_zcml(self):
        self.context = xmlconfig.file("tests/simple_vocab.zcml",
                                      zope.app.schema)
        self.check_vocabulary_get()

    def test_passing_keywords_from_zcml(self):
        self.context = xmlconfig.file("tests/keywords_vocab.zcml",
                                      zope.app.schema)
        self.check_vocabulary_get(self.extra_keywords)


def test_suite():
    return unittest.TestSuite((
        unittest.makeSuite(DirectivesTest),
        ))

if __name__ == '__main__':
    unittest.main()

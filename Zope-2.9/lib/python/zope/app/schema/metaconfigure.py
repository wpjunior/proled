##############################################################################
#
# Copyright (c) 2003 Zope Corporation and Contributors.
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
"""ZCML special vocabulary directive handlers

$Id: metaconfigure.py 25177 2004-06-02 13:17:31Z jim $
"""
from zope.interface import directlyProvides
from vocabulary import IVocabularyFactory
from zope.app.component.metaconfigure import utility

class FactoryKeywordPasser(object):
    """Helper that passes additional keywords to the actual factory."""

    def __init__(self, factory, kwargs):
        self.factory = factory
        self.kwargs = kwargs

    def __call__(self, object):
        return self.factory(object, **self.kwargs)


def vocabulary(_context, name, factory, **kw):
    if kw:
        factory = FactoryKeywordPasser(factory, kw)
    directlyProvides(factory, IVocabularyFactory)
    utility(_context, IVocabularyFactory, factory, name=name)


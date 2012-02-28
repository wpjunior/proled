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
"""Vocabulary for the Source Type Registry

$Id: vocabulary.py 25177 2004-06-02 13:17:31Z jim $
"""
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

from zope.app import zapi
from zope.app.renderer.interfaces import ISource

def SourceTypeVocabulary(context):
    return SimpleVocabulary(
        [SimpleTerm(name, title=factory.title) for name, factory in 
         zapi.getFactoriesFor(ISource)])

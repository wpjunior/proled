##############################################################################
#
# Copyright (c) 2004 Zope Corporation and Contributors.
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
"""Utility Vocabulary.

This vocabulary provides terms for all utilities providing a given interface.

$Id: vocabulary.py 28582 2004-12-08 00:46:02Z srichter $
"""
from zope.deprecation import deprecated

from zope.app.component.vocabulary import *

deprecated(('UtilityTerm', 'UtilityVocabulary', 'UtilityNameTerm', 
            'UtilityComponentInterfacesVocabulary', 'UtilityNames'),
           'This class has been moved to zope.app.component.vocabulary. '
           'The reference will be gone in X3.3.')
           

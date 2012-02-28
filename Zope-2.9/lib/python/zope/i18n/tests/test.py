##############################################################################
#
# Copyright (c) 2004 Zope Corporation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.0 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""Misc tests

$Id: test.py 40011 2005-11-09 21:30:39Z jim $
"""
import unittest

from zope import component, interface
from zope.component.testing import setUp, tearDown
import zope.i18n.interfaces
from zope.i18n import _translate

class TestDomain:
    interface.implements(zope.i18n.interfaces.ITranslationDomain)

    def __init__(self, **catalog):
        self.catalog = catalog

    def translate(self, text, *_, **__):
        return self.catalog[text]
        

def test_fallback_domain():
    """\
Normally, the translation system will use a domain utility:

    >>> component.provideUtility(TestDomain(eek=u'ook'), name='my.domain')
    >>> _translate(u'eek', 'my.domain')
    u'ook'

Normally, if no domain is given, or if there is no domain utility
for the given domain, then the text isn't translated:

    >>> _translate(u'eek')
    u'eek'

    >>> _translate(u'eek', 'your.domain')
    u'eek'

A fallback domain factory can be provided. This is normally used for testing:

    >>> def fallback(domain=u''):
    ...     return TestDomain(eek=u'test-from-' + domain)
    >>> interface.directlyProvides(
    ...     fallback,
    ...     zope.i18n.interfaces.IFallbackTranslationDomainFactory,
    ...     )

    >>> component.provideUtility(fallback)

    >>> _translate(u'eek')
    u'test-from-'

    >>> _translate(u'eek', 'your.domain')
    u'test-from-your.domain'
    
    """

def test_suite():
    from zope.testing import doctest
    return unittest.TestSuite((
        doctest.DocTestSuite(setUp=setUp, tearDown=tearDown),
        ))

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')


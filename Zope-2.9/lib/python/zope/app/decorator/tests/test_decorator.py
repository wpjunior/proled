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
"""Context Tests

$Id: test_decorator.py 68827 2006-06-24 20:21:49Z tseaver $
"""

import pickle
import unittest
from zope.app.decorator import Decorator
from zope.interface import Interface, implements, directlyProvides, providedBy
from zope.interface import directlyProvidedBy, implementedBy
from zope.testing.doctestunit import DocTestSuite
from zope.security.interfaces import ForbiddenAttribute

class I1(Interface):
    pass
class I2(Interface):
    pass
class I3(Interface):
    pass
class I4(Interface):
    pass

class D1(Decorator):
  implements(I1)

class D2(Decorator):
  implements(I2)


def check_forbidden_call(callable, *args):
    try:
        return callable(*args)
    except ForbiddenAttribute, e:
        return 'ForbiddenAttribute: %s' % e[0]


def test_providedBy_iter_w_new_style_class():
    """
    >>> class X(object):
    ...   implements(I3)

    >>> x = X()
    >>> directlyProvides(x, I4)

    >>> [interface.getName() for interface in list(providedBy(x))]
    ['I4', 'I3']

    >>> [interface.getName() for interface in list(providedBy(D1(x)))]
    ['I4', 'I3', 'I1']

    >>> [interface.getName() for interface in list(providedBy(D2(D1(x))))]
    ['I4', 'I3', 'I1', 'I2']
    """

def test_providedBy_iter_w_classic_class():
    """
    >>> class X(object):
    ...   implements(I3)

    >>> x = X()
    >>> directlyProvides(x, I4)

    >>> [interface.getName() for interface in list(providedBy(x))]
    ['I4', 'I3']

    >>> [interface.getName() for interface in list(providedBy(D1(x)))]
    ['I4', 'I3', 'I1']

    >>> [interface.getName() for interface in list(providedBy(D2(D1(x))))]
    ['I4', 'I3', 'I1', 'I2']
    """

def test_suite():
    suite = DocTestSuite()
    suite.addTest(DocTestSuite('zope.app.decorator'))
    return suite


if __name__ == '__main__':
    unittest.main()

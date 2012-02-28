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
"""Location support tests

$Id: tests.py 25177 2004-06-02 13:17:31Z jim $
"""
import unittest
from zope.testing.doctestunit import DocTestSuite
from zope.app.location.location import Location
import zope.interface
from zope.app.traversing.interfaces import ITraverser

class TLocation(Location):
    """Simple traversable location used in examples."""

    zope.interface.implements(ITraverser)

    def traverse(self, path, default=None, request=None):
        o = self
        for name in path.split(u'/'):
           o = getattr(o, name)
        return o

def test_suite():
    return unittest.TestSuite((
        DocTestSuite('zope.app.location.location'),
        DocTestSuite('zope.app.location.traversing'),
        DocTestSuite('zope.app.location.pickling'),
        ))

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')





##############################################################################
#
# Copyright (c) 2002, 2003 Zope Corporation and Contributors.
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
"""Test OnlineHelp

$Id: test_onlinehelp.py 29143 2005-02-14 22:43:16Z srichter $
"""
import os
import unittest

from zope.interface import Interface, implements
from zope.testing.doctestunit import DocTestSuite
from zope.app.testing import ztapi, placelesssetup
from zope.app.traversing.interfaces import ITraversable, IPhysicallyLocatable,\
     ITraverser
from zope.app.traversing.adapters import Traverser, DefaultTraversable
from zope.app.location.traversing import LocationPhysicallyLocatable

class I1(Interface):
    pass

class Dummy1(object):
    implements(I1)

class Dummy2(object):
    pass

def testdir():
    import zope.app.onlinehelp.tests
    return os.path.dirname(zope.app.onlinehelp.tests.__file__)

def setUp(tests):
    placelesssetup.setUp()
    ztapi.provideAdapter(None, ITraverser, Traverser)
    ztapi.provideAdapter(None, ITraversable, DefaultTraversable)
    ztapi.provideAdapter(None, IPhysicallyLocatable,
                         LocationPhysicallyLocatable)

def test_suite():
      return unittest.TestSuite((
          DocTestSuite('zope.app.onlinehelp',
                       setUp=setUp, tearDown=placelesssetup.tearDown),
          DocTestSuite('zope.app.onlinehelp.onlinehelptopic',
                       setUp=setUp, tearDown=placelesssetup.tearDown),
          DocTestSuite('zope.app.onlinehelp.onlinehelp',
                       setUp=setUp, tearDown=placelesssetup.tearDown),
          ))

if __name__ == '__main__':
      unittest.main(defaultTest='test_suite')

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
"""Doc tests for the pagentemplate's 'engine' module

$Id: test_engine.py 26640 2004-07-20 20:01:05Z fdrake $
"""
import unittest
from zope.testing.doctestunit import DocTestSuite

def test_suite():
    return DocTestSuite('zope.app.pagetemplate.engine')

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')


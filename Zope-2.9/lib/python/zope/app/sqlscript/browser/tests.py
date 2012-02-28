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
# FOR A PARTICULAR PURPOSE
#
##############################################################################
"""DTML Page Evaluation Tests

$Id: tests.py 25177 2004-06-02 13:17:31Z jim $
"""
import unittest, doctest

def test_suite():
    return unittest.TestSuite((
        doctest.DocTestSuite('zope.app.sqlscript.browser.sqlscript'),
        ))
    
if __name__ == '__main__': unittest.main()

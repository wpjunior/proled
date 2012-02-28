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
"""Test 'etc' namespace

$Id: test_etc.py 29143 2005-02-14 22:43:16Z srichter $
"""
from unittest import TestCase, main, makeSuite
from zope.testing.cleanup import CleanUp # Base class w registry cleanup

class Test(CleanUp, TestCase):

    def testApplicationControl(self):
        from zope.app.traversing.namespace import etc
        from zope.app.applicationcontrol.applicationcontrol \
             import applicationController, applicationControllerRoot

        self.assertEqual(
            etc(applicationControllerRoot).traverse('process', ()),
            applicationController)

    def testSiteManager(self):
        from zope.app.traversing.namespace import etc
        class C(object):
            def getSiteManager(self): return 42

        self.assertEqual(etc(C()).traverse('site', ()), 42)



def test_suite():
    return makeSuite(Test)

if __name__=='__main__':
    main(defaultTest='test_suite')

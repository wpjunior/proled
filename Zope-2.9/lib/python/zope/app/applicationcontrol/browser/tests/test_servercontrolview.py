##############################################################################
#
# Copyright (c) 2001, 2002, 2003 Zope Corporation and Contributors.
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
"""Server Control View Tests

$Id: test_servercontrolview.py 40500 2005-12-02 18:58:00Z ctheune $
"""
import unittest

from zope.interface import implements
from zope.app import zapi
from zope.app.applicationcontrol.applicationcontrol import applicationController
from zope.app.applicationcontrol.browser.servercontrol import ServerControlView
from zope.app.applicationcontrol.interfaces import IServerControl
from zope.app.component.testing import PlacefulSetup

class ServerControlStub(object):
    implements(IServerControl)
    
    did_restart = None
    did_shutdown = None

    def restart(self, time):
        self.did_restart = time

    def shutdown(self, time):
        self.did_shutdown = time

class Test(PlacefulSetup, unittest.TestCase):

    def _TestView__newView(self, container, request):
        view = ServerControlView()
        view.context = container
        view.request = request
        return view

    def test_ServerControlView(self):
        control = ServerControlStub()
        zapi.getGlobalSiteManager().provideUtility(IServerControl, control)

        test_serverctrl = self._TestView__newView(
            applicationController,
            {'shutdown': 1,
             'time': 100},
            )
        test_serverctrl.action()
        self.assertEqual(control.did_shutdown, 100)

        test_serverctrl = self._TestView__newView(
            applicationController,
            {'restart': 1,
             'time': 100},
            )
        test_serverctrl.action()
        self.assertEqual(control.did_restart, 100)


def test_suite():
    return unittest.TestSuite((
        unittest.makeSuite(Test),
        ))

if __name__ == '__main__':
    unittest.main()

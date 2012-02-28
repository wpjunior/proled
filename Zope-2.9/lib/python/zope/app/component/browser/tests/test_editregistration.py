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
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""Registration Editing Tests

$Id: test_editregistration.py 40187 2005-11-16 23:37:25Z srichter $
"""
from zope.app.testing import ztapi
from unittest import TestCase, TestSuite, main, makeSuite
from zope.app.component.browser.registration import EditRegistration
from zope.app.container.interfaces import IContainer
from zope.app.container.interfaces import IObjectRemovedEvent
from zope.app.component.interfaces.registration import ActiveStatus
from zope.app.traversing.interfaces import IContainmentRoot
from zope.app.site.tests.placefulsetup import PlacefulSetup
from zope.interface import Interface, implements
from zope.app.publisher.browser import BrowserView
from zope.publisher.browser import TestRequest
from zope.app.container.contained import Contained

class Container(dict):
    implements(IContainer, IContainmentRoot)

class I(Interface):
    pass

class C(Contained):
    implements(I)
    status = ActiveStatus


class Test(PlacefulSetup, TestCase):

    def test_remove_objects(self):
        c1 = C()
        c2 = C()
        c7 = C()
        d = Container({'1': c1, '2': c2, '7': c7})
        view = EditRegistration(d, TestRequest())
        view.remove_objects(['2', '7'])
        self.assertEqual(d, {'1': c1})

    def test_registrationInfo(self):

        class V(BrowserView):
            def setPrefix(self, p):
                self._prefix = p

        ztapi.browserView(I, 'ItemEdit', V)

        c1 = C()
        c2 = C()
        c7 = C()
        d = Container({'1': c1, '2': c2, '7': c7})
        c1.__parent__ = d; c1.__name__ = '1'
        c2.__parent__ = d; c2.__name__ = '2'
        c7.__parent__ = d; c7.__name__ = '7'

        view = EditRegistration(d, TestRequest())

        info = view.registrationInfo()
        self.assertEqual(len(info), 3)
        self.assertEqual(info[0]['name'], '1')
        self.assertEqual(info[1]['name'], '2')
        self.assertEqual(info[2]['name'], '7')

def test_suite():
    return TestSuite((
        makeSuite(Test),
        ))

if __name__=='__main__':
    main(defaultTest='test_suite')

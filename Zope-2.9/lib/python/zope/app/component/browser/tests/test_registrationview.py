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
"""Tests for the RegistrationView view class.

$Id: test_registrationview.py 40187 2005-11-16 23:37:25Z srichter $
"""
import unittest
import zope.component
from zope.interface import implements
from zope.publisher.browser import TestRequest
from zope.testing import doctest, doctestunit
from zope.app.testing import setup
from zope.app.traversing.interfaces import IContainmentRoot

from zope.app.component.interfaces.registration import IRegistered
from zope.app.component.interfaces.registration import InactiveStatus
from zope.app.component.interfaces.registration import ActiveStatus
from zope.app.component.browser.registration import RegistrationView

pprint = doctestunit.pprint


def test():
    """
    >>> request = TestRequest()

    Check results when using an unregisted object:

    >>> view = RegistrationView(FakeRegisterable([]), request)
    >>> view.registered()
    False

    Returns for the active() and registration() methods are undefined
    for unregistred objects.

    The update() method shouldn't do anything with an action specified
    in the form:

    >>> request.response.setStatus(200)
    >>> view.update()
    >>> view.registered()
    False
    >>> request.response.getStatus()
    200

    This simulates submitting the form using the 'Activate' button:

    >>> request.form['activate'] = 'Activate'
    >>> view.update()
    >>> request.response.getStatus()
    302
    >>> request.response.getHeader('location')
    'addRegistration.html'

    Let's look at the case when the object has a single registration
    to begin with:

    >>> request = TestRequest()
    >>> reg = FakeRegistration(InactiveStatus)
    >>> reg.name = 'my fake'
    >>> view = RegistrationView(FakeRegisterable([reg]), request)
    >>> view.active()
    False
    >>> view.registered()
    True
    >>> pprint(view.registration())
    {'details': 'my fake',
     'url': 'http://127.0.0.1'}

    Make sure calling `update()` without an action doesn't change the
    registration:

    >>> request.response.setStatus(200)
    >>> view.update()
    >>> request.response.getStatus()
    200
    >>> view.active()
    False
    >>> view.registered()
    True
    >>> pprint(view.registration())
    {'details': 'my fake',
     'url': 'http://127.0.0.1'}

    Now test activating the object:

    >>> request.form['activate'] = 'Activate'
    >>> request.response.setStatus(200)
    >>> view.update()
    >>> request.response.getStatus()
    200
    >>> view.active()
    True
    >>> view.registered()
    True
    >>> pprint(view.registration())
    {'details': 'my fake',
     'url': 'http://127.0.0.1'}
    >>> reg.status == ActiveStatus
    True

    Now test deactivating an active object:

    >>> request.form = {'deactivate': 'Deactivate'}
    >>> request.response.setStatus(200)
    >>> view.update()
    >>> request.response.getStatus()
    200
    >>> view.active()
    False
    >>> view.registered()
    True
    >>> pprint(view.registration())
    {'details': 'my fake',
     'url': 'http://127.0.0.1'}
    >>> reg.status == InactiveStatus
    True
    """

def test_multiple_registrations():
    """
    >>> request = TestRequest()
    >>> reg1 = FakeRegistration(InactiveStatus)
    >>> reg1.name = 'reg1'
    >>> reg2 = FakeRegistration(ActiveStatus)
    >>> reg2.name = 'reg2'
    >>> view = RegistrationView(FakeRegisterable([reg1, reg2]), request)
    >>> view.active()
    False
    >>> view.registered()
    True
    >>> pprint(view.registration())
    {'details': 'reg1',
     'url': 'http://127.0.0.1'}

    Now make sure this view redirects us to the advanced registrations
    form since we have more than one registraion:

    >>> request.response.setStatus(200)
    >>> view.update()
    >>> request.response.getStatus()
    302
    """


class FakeRegisterable(object):
    implements(IRegistered)

    def __init__(self, usages):
        self._usages = usages

    def registrations(self):
        return self._usages


class FakeRegistration(object):
    implements(IContainmentRoot)

    def __init__(self, status):
        self.status = status


def setUp(test):
    zope.component.testing.setUp(test)
    setup.setUpTraversal()
    zope.component.provideAdapter(
        lambda x, y: x.name,
        (FakeRegistration, TestRequest), zope.interface.Interface,
        name='details')

def test_suite():
    return unittest.TestSuite((
        doctest.DocTestSuite(
        setUp=setUp, tearDown=zope.component.testing.tearDown,
        optionflags=doctest.NORMALIZE_WHITESPACE),
        ))

if __name__ == '__main__':
    unittest.main(default='test_suite')

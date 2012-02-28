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
"""Test HTTP DELETE verb

$Id: test_delete.py 40824 2005-12-16 18:58:49Z mgedmin $
"""
from unittest import TestCase, TestSuite, makeSuite
import zope.app.http.delete
from zope.publisher.browser import TestRequest
from zope.app.filerepresentation.interfaces import IWriteDirectory, IFileFactory
from zope.app.testing.placelesssetup import PlacelessSetup
from zope.interface import implements
from zope.app.container.contained import contained
from zope.app.publication.http import MethodNotAllowed


class UnwritableContainer(object):
    pass


class Container(object):

    implements(IWriteDirectory, IFileFactory)

    def __delitem__(self, name):
        delattr(self, name)


class TestDelete(PlacelessSetup, TestCase):

    def test(self):
        container = Container()
        container.a = 'spam'
        item = contained(Container(), container, name='a')

        request = TestRequest()
        delete = zope.app.http.delete.DELETE(item, request)
        self.assert_(hasattr(container, 'a'))
        self.assertEqual(delete.DELETE(), '')
        self.assert_(not hasattr(container, 'a'))

    def test_not_deletable(self):
        container = UnwritableContainer()
        container.a = 'spam'
        item = contained(UnwritableContainer(), container, name='a')
        request = TestRequest()
        delete = zope.app.http.delete.DELETE(item, request)
        self.assertRaises(MethodNotAllowed, delete.DELETE)


def test_suite():
    return TestSuite((
        makeSuite(TestDelete),
        ))

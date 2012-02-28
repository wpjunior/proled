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
"""Test HTTP PUT verb

$Id: test_put.py 70416 2006-09-28 08:54:26Z wosc $
"""
from unittest import TestCase, TestSuite, makeSuite
from StringIO import StringIO
import zope.app.http.put
from zope.publisher.browser import TestRequest
from zope.app.filerepresentation.interfaces import IWriteFile
from zope.app.filerepresentation.interfaces import IWriteDirectory, IReadDirectory, IFileFactory
from zope.app.testing.placelesssetup import PlacelessSetup
from zope.app.component.testing import PlacefulSetup, Place
from zope.app.location.interfaces import ILocation
from zope.interface import implements

class File(object):

    implements(IWriteFile)

    def __init__(self, name, content_type, data):
        self.name = name
        self.content_type = content_type
        self.data = data

    def write(self, data):
        self.data = data

class Container(Place):

    implements(IWriteDirectory, IReadDirectory, IFileFactory, ILocation)

    __name__ = None
    __parent__ = None

    def __setitem__(self, name, object):
        object.__name__ = name
        object.__parent__ = self
        setattr(self, name, object)

    def __getitem__(self, name):
        return getattr(self, name)

    def __call__(self, name, content_type, data):
        return File(name, content_type, data)


class TestNullPUT(PlacefulSetup, TestCase):

    def test(self):
        container = Container("put")
        self.rootFolder["put"] = container
        content = "some content\n for testing"
        request = TestRequest(StringIO(content),
                              {'CONTENT_TYPE': 'test/foo',
                               'CONTENT_LENGTH': str(len(content)),
                               })
        null = zope.app.http.put.NullResource(container, 'spam')
        put = zope.app.http.put.NullPUT(null, request)
        self.assertEqual(getattr(container, 'spam', None), None)
        self.assertEqual(put.PUT(), '')
        request.response.setResult('')
        file = container.spam
        self.assertEqual(file.__class__, File)
        self.assertEqual(file.name, 'spam')
        self.assertEqual(file.content_type, 'test/foo')
        self.assertEqual(file.data, content)

        # Check HTTP Response
        self.assertEqual(request.response.getStatus(), 201)
        self.assertEqual(request.response.getHeader("Location"),
                         "http://127.0.0.1/put/spam")

    def test_bad_content_header(self):
        ## The previous behavour of the PUT method was to fail if the request
        ## object had a key beginning with 'HTTP_CONTENT_' with a status of 501.
        ## This was breaking the new Twisted server, so I am now allowing this
        ## this type of request to be valid.
        container = Container("/put")
        self.rootFolder["put"] = container
        content = "some content\n for testing"
        request = TestRequest(StringIO(content),
                              {'CONTENT_TYPE': 'test/foo',
                               'CONTENT_LENGTH': str(len(content)),
                               'HTTP_CONTENT_FOO': 'Bar',
                               })
        null = zope.app.http.put.NullResource(container, 'spam')
        put = zope.app.http.put.NullPUT(null, request)
        self.assertEqual(getattr(container, 'spam', None), None)
        self.assertEqual(put.PUT(), '')
        request.response.setResult('')

        # Check HTTP Response
        self.assertEqual(request.response.getStatus(), 201)

class TestFilePUT(PlacelessSetup, TestCase):

    def test(self):
        file = File("thefile", "text/x", "initial content")
        content = "some content\n for testing"
        request = TestRequest(StringIO(content),
                              {'CONTENT_TYPE': 'test/foo',
                               'CONTENT_LENGTH': str(len(content)),
                               })
        put = zope.app.http.put.FilePUT(file, request)
        self.assertEqual(put.PUT(), '')
        request.response.setResult('')
        self.assertEqual(file.data, content)

    def test_bad_content_header(self):
        ## The previous behavour of the PUT method was to fail if the request
        ## object had a key beginning with 'HTTP_CONTENT_' with a status of 501.
        ## This was breaking the new Twisted server, so I am now allowing this
        ## this type of request to be valid.
        file = File("thefile", "text/x", "initial content")
        content = "some content\n for testing"
        request = TestRequest(StringIO(content),
                              {'CONTENT_TYPE': 'test/foo',
                               'CONTENT_LENGTH': str(len(content)),
                               'HTTP_CONTENT_FOO': 'Bar',
                               })
        put = zope.app.http.put.FilePUT(file, request)
        self.assertEqual(put.PUT(), '')
        request.response.setResult('')
        self.assertEqual(file.data, content)

        # Check HTTP Response
        self.assertEqual(request.response.getStatus(), 200)

def test_suite():
    return TestSuite((
        makeSuite(TestFilePUT),
        makeSuite(TestNullPUT),
        ))

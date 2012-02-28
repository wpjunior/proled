##############################################################################
# Copyright (c) 2004 Zope Corporation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
##############################################################################
"""External Editor Tests

$Id: test_external_edit.py 29143 2005-02-14 22:43:16Z srichter $
"""
import unittest
from base64 import encodestring

from zope.interface import implements, Interface, directlyProvides
from zope.publisher.browser import TestRequest

from zope.app import zapi
from zope.app.component.testing import PlacefulSetup
from zope.app.testing import ztapi
from zope.app.container.contained import contained
from zope.app.content.interfaces import IContentType
from zope.app.filerepresentation.interfaces import IReadFile
from zope.app.file.file import File, FileReadFile

from zope.app.externaleditor.interfaces import IExternallyEditable
from zope.app.externaleditor.browser import ExternalEditor

class IEditableFile(Interface): pass

class ReadFileAdapter(FileReadFile):

    def getContentType(self):
        return self.context.contentType

    def setContentType(self, ct):
        self.context.contentType = ct

    contentType = property(getContentType, setContentType)

class EditableFile(File):
    """An editable file"""
    implements(IExternallyEditable, IEditableFile)

class Test(PlacefulSetup, unittest.TestCase):

    def setUp(self):
        PlacefulSetup.setUp(self)
        PlacefulSetup.buildFolders(self)
        ztapi.browserView(IExternallyEditable, 'external_edit', ExternalEditor)
        ztapi.provideAdapter(IExternallyEditable, IReadFile, ReadFileAdapter)
        directlyProvides(IEditableFile, IContentType)

    def test_external_edit(self):
        basic = 'Basic %s' % encodestring('%s:%s' % ('testuser', 'testpass'))
        env = {'HTTP_AUTHORIZATION':
               basic}
        request = TestRequest(environ=env)
        container = zapi.traverse(self.rootFolder, 'folder1')
        file = EditableFile('Foobar', 'text/plain')
        self.assertEqual(file.contentType, 'text/plain')
        self.assertEqual(file.data, 'Foobar')
        file = contained(file, container, 'file')
        view = zapi.queryMultiAdapter((file, request), name='external_edit')
        self.failIf(view is None)
        expected = """\
url:http://127.0.0.1/folder1/file
content_type:text/plain
meta_type:IEditableFile
auth:%s
cookie:

Foobar""" % basic[:-1]
        self.assertEqual(view(), expected)

def test_suite():
    return unittest.TestSuite((
        unittest.makeSuite(Test),
        ))

if __name__ == '__main__':
    unittest.main()

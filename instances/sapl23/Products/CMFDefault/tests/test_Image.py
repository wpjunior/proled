##############################################################################
#
# Copyright (c) 2001 Zope Corporation and Contributors. All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
""" Unit tests for Image module.

$Id: test_Image.py 40346 2005-11-23 17:15:03Z yuppie $
"""

from unittest import TestCase, TestSuite, makeSuite, main
import Testing
try:
    import Zope2
except ImportError:
    # BBB: for Zope 2.7
    import Zope as Zope2
Zope2.startup()

from os.path import join as path_join
from cStringIO import StringIO

from AccessControl.SecurityManagement import newSecurityManager
from AccessControl.SecurityManagement import noSecurityManager
from AccessControl.User import UnrestrictedUser
from Products.Five import zcml
import Products
try:
    import transaction
except ImportError:
    # BBB: for Zope 2.7
    from Products.CMFCore.utils import transaction

from Products.CMFCore.tests.base.dummy import DummySite
from Products.CMFCore.tests.base.dummy import DummyTool
from Products.CMFCore.tests.base.testcase import PlacelessSetup
from Products.CMFCore.tests.base.testcase import RequestTest
from Products.CMFDefault import tests
from Products.CMFDefault.File import File
from Products.CMFDefault.Image import Image

TESTS_HOME = tests.__path__[0]
TEST_JPG = path_join(TESTS_HOME, 'TestImage.jpg')


class TestImageElement(TestCase):

    def setUp(self):
        self.site = DummySite('site')
        self.site._setObject( 'portal_membership', DummyTool() )

    def test_getId_on_old_Image_instance(self):
        image = self.site._setObject( 'testimage', Image('testimage') )
        self.assertEqual(image.getId(), 'testimage')
        self.assertEqual(image.id, 'testimage')
        # Mimick old instance when base classes had OFS.Image.Image first
        image.__name__ = 'testimage'
        delattr(image, 'id')
        self.assertEqual(image.getId(), 'testimage')
        self.assertEqual(image.id(), 'testimage')

    def test_getId_on_old_File_instance(self):
        file = self.site._setObject( 'testfile', File('testfile') )
        self.assertEqual(file.getId(), 'testfile')
        self.assertEqual(file.id, 'testfile')
        # Mimick old instance when base classes had OFS.Image.File first
        file.__name__ = 'testfile'
        delattr(file, 'id')
        self.assertEqual(file.getId(), 'testfile')
        self.assertEqual(file.id(), 'testfile')

    def test_EditWithEmptyFile(self):
        # Test handling of empty file uploads
        image = self.site._setObject( 'testimage', Image('testimage') )

        testfile = open(TEST_JPG, 'rb')
        image.edit(file=testfile)
        testfile.seek(0,2)
        testfilesize = testfile.tell()
        testfile.close()

        assert image.get_size() == testfilesize

        emptyfile = StringIO()
        image.edit(file=emptyfile)

        assert image.get_size() > 0
        assert image.get_size() == testfilesize

    def test_File_setFormat(self):
        # Setting the DC.format must also set the content_type property
        file = File('testfile', format='image/jpeg')
        self.assertEqual(file.Format(), 'image/jpeg')
        self.assertEqual(file.content_type, 'image/jpeg')
        file.setFormat('image/gif')
        self.assertEqual(file.Format(), 'image/gif')
        self.assertEqual(file.content_type, 'image/gif')
 
    def test_Image_setFormat(self):
        # Setting the DC.format must also set the content_type property
        image = Image('testimage', format='image/jpeg')
        self.assertEqual(image.Format(), 'image/jpeg')
        self.assertEqual(image.content_type, 'image/jpeg')
        image.setFormat('image/gif')
        self.assertEqual(image.Format(), 'image/gif')
        self.assertEqual(image.content_type, 'image/gif')

    def test_ImageContentTypeUponConstruction(self):
        # Test the content type after calling the constructor with the
        # file object being passed in (http://www.zope.org/Collectors/CMF/370)
        testfile = open(TEST_JPG, 'rb')
        image = Image('testimage', file=testfile)
        testfile.close()
        self.assertEqual(image.Format(), 'image/jpeg')
        self.assertEqual(image.content_type, 'image/jpeg')

    def test_FileContentTypeUponConstruction(self):
        # Test the content type after calling the constructor with the
        # file object being passed in (http://www.zope.org/Collectors/CMF/370)
        testfile = open(TEST_JPG, 'rb')
        # Notice the cheat? File objects lack the extra intelligence that
        # picks content types from the actual file data, so it needs to be
        # helped along with a file extension...
        file = File('testfile.jpg', file=testfile)
        testfile.close()
        self.assertEqual(file.Format(), 'image/jpeg')
        self.assertEqual(file.content_type, 'image/jpeg')


class TestImageCopyPaste(PlacelessSetup, RequestTest):

    # Tests related to http://www.zope.org/Collectors/CMF/176
    # Copy/pasting an image (or file) should reset the object's workflow state.

    def setUp(self):
        PlacelessSetup.setUp(self)
        RequestTest.setUp(self)
        zcml.load_config('meta.zcml', Products.Five)
        zcml.load_config('permissions.zcml', Products.Five)
        zcml.load_config('configure.zcml', Products.GenericSetup)
        zcml.load_config('configure.zcml', Products.CMFCore)
        zcml.load_config('configure.zcml', Products.DCWorkflow)
        try:
            newSecurityManager(None, UnrestrictedUser('manager', '', ['Manager'], []))
            factory = self.root.manage_addProduct['CMFDefault'].addConfiguredSite
            factory('cmf', 'CMFDefault:default', snapshot=False)
            self.site = self.root.cmf
            self.site.invokeFactory('File', id='file')
            self.site.portal_workflow.doActionFor(self.site.file, 'publish')
            self.site.invokeFactory('Image', id='image')
            self.site.portal_workflow.doActionFor(self.site.image, 'publish')
            self.site.invokeFactory('Folder', id='subfolder')
            self.subfolder = self.site.subfolder
            self.workflow = self.site.portal_workflow
            transaction.commit(1) # Make sure we have _p_jars
        except:
            self.tearDown()
            raise

    def tearDown(self):
        noSecurityManager()
        RequestTest.tearDown(self)
        PlacelessSetup.tearDown(self)

    def test_File_CopyPasteResetsWorkflowState(self):
        # Copy/pasting a File should reset wf state to private
        cb = self.site.manage_copyObjects(['file']) 
        self.subfolder.manage_pasteObjects(cb)
        review_state = self.workflow.getInfoFor(self.subfolder.file, 'review_state')
        self.assertEqual(review_state, 'private')

    def test_File_CloneResetsWorkflowState(self):
        # Cloning a File should reset wf state to private
        self.subfolder.manage_clone(self.site.file, 'file')
        review_state = self.workflow.getInfoFor(self.subfolder.file, 'review_state')
        self.assertEqual(review_state, 'private')

    def test_File_CutPasteKeepsWorkflowState(self):
        # Cut/pasting a File should keep the wf state
        cb = self.site.manage_cutObjects(['file']) 
        self.subfolder.manage_pasteObjects(cb)
        review_state = self.workflow.getInfoFor(self.subfolder.file, 'review_state')
        self.assertEqual(review_state, 'published')

    def test_File_RenameKeepsWorkflowState(self):
        # Renaming a File should keep the wf state
        self.site.manage_renameObjects(['file'], ['file2']) 
        review_state = self.workflow.getInfoFor(self.site.file2, 'review_state')
        self.assertEqual(review_state, 'published')

    def test_Image_CopyPasteResetsWorkflowState(self):
        #  Copy/pasting an Image should reset wf state to private
        cb = self.site.manage_copyObjects(['image']) 
        self.subfolder.manage_pasteObjects(cb)
        review_state = self.workflow.getInfoFor(self.subfolder.image, 'review_state')
        self.assertEqual(review_state, 'private')

    def test_Image_CloneResetsWorkflowState(self):
        # Cloning an Image should reset wf state to private
        self.subfolder.manage_clone(self.site.image, 'image')
        review_state = self.workflow.getInfoFor(self.subfolder.image, 'review_state')
        self.assertEqual(review_state, 'private')

    def test_Image_CutPasteKeepsWorkflowState(self):
        # Cut/pasting an Image should keep the wf state
        cb = self.site.manage_cutObjects(['image']) 
        self.subfolder.manage_pasteObjects(cb)
        review_state = self.workflow.getInfoFor(self.subfolder.image, 'review_state')
        self.assertEqual(review_state, 'published')

    def test_Image_RenameKeepsWorkflowState(self):
        # Renaming an Image should keep the wf state
        self.site.manage_renameObjects(['image'], ['image2']) 
        review_state = self.workflow.getInfoFor(self.site.image2, 'review_state')
        self.assertEqual(review_state, 'published')


def test_suite():
    return TestSuite((
        makeSuite(TestImageElement),
        makeSuite(TestImageCopyPaste),
        ))
    return suite

if __name__ == '__main__':
    main(defaultTest='test_suite')

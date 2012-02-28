##############################################################################
#
# Copyright (c) 2002 Zope Corporation and Contributors. All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
""" Unit / functional tests for a CMFSite.

$Id: test_Portal.py 68523 2006-06-08 16:23:41Z efge $
"""

from unittest import TestSuite, makeSuite, main
import Testing
try:
    import Zope2
except ImportError: # BBB: for Zope 2.7
    import Zope as Zope2
Zope2.startup()

import Products
from Acquisition import aq_base
from Products.Five import zcml

from Products.CMFCore.tests.base.testcase import PlacelessSetup
from Products.CMFCore.tests.base.testcase import SecurityRequestTest
from Products.CMFCore.tests.base.testcase import WarningInterceptor


class CMFSiteTests( PlacelessSetup, SecurityRequestTest, WarningInterceptor):

    def setUp( self ):
        PlacelessSetup.setUp(self)
        SecurityRequestTest.setUp( self )
        self._trap_warning_output()
        zcml.load_config('meta.zcml', Products.Five)
        zcml.load_config('permissions.zcml', Products.Five)
        zcml.load_config('configure.zcml', Products.GenericSetup)
        zcml.load_config('configure.zcml', Products.CMFCore)
        zcml.load_config('configure.zcml', Products.DCWorkflow)

    def tearDown( self ):
        self._free_warning_output()
        SecurityRequestTest.tearDown( self )
        PlacelessSetup.tearDown(self)

    def _makeSite( self, id='testsite'):

        from Products.CMFDefault.factory import addConfiguredSite

        addConfiguredSite(self.root, id, 'CMFDefault:default', snapshot=False)
        return getattr( self.root, id )

    def _makeContent( self, site, portal_type, id='document', **kw ):

        site.invokeFactory( type_name=portal_type, id=id )
        content = getattr( site, id )

        if getattr( aq_base( content ), 'editMetadata', None ) is not None:
            content.editMetadata( **kw )

        return content

    def test_new( self ):

        site = self._makeSite()
        self.assertEqual( len( site.portal_catalog ), 0 )

    def test_MetadataCataloguing( self ):

        site = self._makeSite()
        catalog = site.portal_catalog
        site.portal_membership.memberareaCreationFlag = 0
        uid_handler = getattr(site, 'portal_uidhandler', None)

        portal_types = [ x for x in site.portal_types.listContentTypes()
                           if x not in ( 'Discussion Item'
                                       , 'CMF BTree Folder'
                                       , 'Folder'
                                       , 'Topic'
                                       ) ]

        self.assertEqual( len( catalog ), 0 )

        for portal_type in portal_types:

            doc = self._makeContent( site
                                   , portal_type=portal_type
                                   , title='Foo' )

            # in case of the CMFUid beeing installed this test
            # indexes also the site root because the 'Favorite'
            # references it by unique id
            isUidEnabledFavorite = uid_handler and portal_type == 'Favorite'
            if isUidEnabledFavorite:
                self.assertEqual( len( catalog ), 2 )
            else:
                self.assertEqual( len( catalog ), 1 )

            # find the right brain
            rid = catalog._catalog.paths.keys()[0]
            title = _getMetadata( catalog, rid )
            if isUidEnabledFavorite and title == 'Portal':
                rid = catalog._catalog.paths.keys()[1]
                title = _getMetadata( catalog, rid )
            self.assertEqual( title, 'Foo' )

            doc.editMetadata( title='Bar' )
            self.assertEqual( _getMetadata( catalog, rid ), 'Bar' )

            site._delObject( doc.getId() )
            
            if isUidEnabledFavorite:
                # unindex the site root by hand
                catalog.unindexObject(site)
                
            self.assertEqual( len( catalog ), 0 )

    def test_DocumentEditCataloguing( self ):

        site = self._makeSite()
        catalog = site.portal_catalog

        doc = self._makeContent( site
                               , portal_type='Document'
                               , title='Foo' )

        rid = catalog._catalog.paths.keys()[0]

        doc.setTitle( 'Bar' )   # doesn't reindex
        self.assertEqual( _getMetadata( catalog, rid ), 'Foo' )

        doc.edit( text_format='structured-text'
                , text='Some Text Goes Here\n\n   A paragraph\n   for you.'
                )
        self.assertEqual( _getMetadata( catalog, rid ), 'Bar' )

    def test_ImageEditCataloguing( self ):

        site = self._makeSite()
        catalog = site.portal_catalog

        doc = self._makeContent( site
                               , portal_type='Image'
                               , title='Foo' )

        rid = catalog._catalog.paths.keys()[0]

        doc.setTitle( 'Bar' )   # doesn't reindex
        self.assertEqual( _getMetadata( catalog, rid ), 'Foo' )

        doc.edit( 'GIF89a' )
        self.assertEqual( _getMetadata( catalog, rid ), 'Bar' )

    def test_FileEditCataloguing( self ):

        site = self._makeSite()
        catalog = site.portal_catalog

        doc = self._makeContent( site
                               , portal_type='File'
                               , title='Foo' )

        rid = catalog._catalog.paths.keys()[0]

        doc.setTitle( 'Bar' )   # doesn't reindex
        self.assertEqual( _getMetadata( catalog, rid ), 'Foo' )

        doc.edit( '%PDF-1.2\r' )
        self.assertEqual( _getMetadata( catalog, rid ), 'Bar' )

    def test_LinkEditCataloguing( self ):

        site = self._makeSite()
        catalog = site.portal_catalog

        doc = self._makeContent( site
                               , portal_type='Link'
                               , title='Foo' )

        rid = catalog._catalog.paths.keys()[0]

        doc.setTitle( 'Bar' )   # doesn't reindex
        self.assertEqual( _getMetadata( catalog, rid ), 'Foo' )

        doc.edit( 'http://www.example.com' )
        self.assertEqual( _getMetadata( catalog, rid ), 'Bar' )

    def test_NewsItemEditCataloguing( self ):

        site = self._makeSite()
        catalog = site.portal_catalog

        doc = self._makeContent( site
                               , portal_type='News Item'
                               , title='Foo' )

        rid = catalog._catalog.paths.keys()[0]

        doc.setTitle( 'Bar' )   # doesn't reindex
        self.assertEqual( _getMetadata( catalog, rid ), 'Foo' )

        doc.edit( '<h1>Extra!</h1>' )
        self.assertEqual( _getMetadata( catalog, rid ), 'Bar' )

    def test_manage_addCMFSite_emits_DeprecationWarning( self ):

        # This warning is recorded in *our* globals (stacklevel=2).
        registry = globals().get("__warningregistry__")

        if registry is not None:
            registry.clear()

        # Make a site the old-fashioned way
        from Products.CMFDefault.Portal import manage_addCMFSite
        id = 'emits_warning'
        manage_addCMFSite( self.root, id )
        site = getattr( self.root, id )

        # Check that a warning was raised.
        if registry is None:
            # registry only exists once a warning is generated
            registry = globals().get("__warningregistry__")
        self.assertEqual( len( registry ), 1 )
        message, category, linenoe  = registry.keys()[ 0 ]
        self.failUnless( 'manage_addCMFSite' in message, message )
        self.failUnless( category is DeprecationWarning, category )

def _getMetadata( catalog, rid, field='Title' ):
    md = catalog.getMetadataForRID( rid )
    return md[ field ]


def test_suite():
    return TestSuite((
        makeSuite(CMFSiteTests),
        ))

if __name__ == '__main__':
    main(defaultTest='test_suite')

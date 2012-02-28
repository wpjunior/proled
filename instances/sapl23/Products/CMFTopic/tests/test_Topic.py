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
""" Unit tests for Topic module.

$Id: test_Topic.py 38418 2005-09-09 08:40:13Z yuppie $
"""

from unittest import TestSuite, makeSuite, main
import Testing
try:
    import Zope2
except ImportError: # BBB: for Zope 2.7
    import Zope as Zope2
Zope2.startup()

from Acquisition import Implicit

from Products.CMFCore.tests.base.dummy import DummySite
from Products.CMFCore.tests.base.testcase import SecurityTest
from Products.CMFCore.TypesTool import FactoryTypeInformation as FTI
from Products.CMFCore.TypesTool import TypesTool
from Products.CMFTopic.Topic import factory_type_information as FTIDATA_TOPIC


class FauxBrain( Implicit ):

    def __init__( self, object ):

        self._object = object

    def getObject( self ):

        return self._object


class DummyDocument( Implicit ):

    def __init__( self, id ):

        self._id = id

    def getId( self ):

        return self._id


class DummyCatalog( Implicit ):

    def __init__( self, index_ids=() ):

        self._objects = []
        self._index_ids = index_ids
        self._indexes = {}

        for index_id in index_ids:
            self._indexes[ index_id ] = {}

    def _index( self, obj ):

        marker = object()
        self._objects.append( obj )

        rid = len( self._objects ) - 1

        for index_id in self._index_ids:

            value = getattr( obj, index_id, marker )

            if value is not marker:
                for word in value.split():
                    bucket = self._indexes[ index_id ].setdefault( word, [] )
                    bucket.append( rid )

    indexObject = _index

    def searchResults( self, REQUEST=None, **kw ):

        from sets import Set
        limit = None

        criteria = kw.copy()

        if REQUEST is not None:
            for k, v in REQUEST:
                criteria[ k ] = v

        results = Set( range( len( self._objects ) ) )

        for k, v in criteria.items():

            if k == 'sort_limit':
                limit = v

            else:
                results &= Set( self._indexes[ k ].get( v, [] ) )


        results = [ x for x in results ]

        if limit is not None:
            results = results[ :limit ]

        return [ FauxBrain( self._objects[ rid ] ) for rid in results ]


class DummySyndicationTool( Implicit ):

    def __init__( self, max_items ):

        self._max_items = max_items

    def getMaxItems( self, object ):

        return self._max_items


class TestTopic(SecurityTest):
    """ Test all the general Topic cases.
    """

    def setUp(self):
        SecurityTest.setUp(self)
        self.site = DummySite('site').__of__(self.root)

    def _makeOne(self, id, *args, **kw):
        from Products.CMFTopic.Topic import Topic

        return self.site._setObject( id, Topic(id, *args, **kw) )

    def _initSite( self, max_items=15, index_ids=() ):

        self.site.portal_catalog = DummyCatalog( index_ids )
        self.site.portal_syndication = DummySyndicationTool( max_items )

    def _initDocuments( self, **kw ):

        for k, v in kw.items():

            document = DummyDocument( k )
            document.description = v

            self.site._setObject( k, v )
            self.site.portal_catalog._index( document )

    def test_z2interfaces(self):
        from Interface.Verify import verifyClass
        from OFS.IOrderSupport import IOrderedContainer
        from webdav.WriteLockInterface import WriteLockInterface
        from Products.CMFCore.interfaces.Dynamic \
                import DynamicType as IDynamicType
        from Products.CMFCore.interfaces.Folderish \
                import Folderish as IFolderish
        from Products.CMFTopic.Topic import Topic

        verifyClass(IDynamicType, Topic)
        verifyClass(IFolderish, Topic)
        verifyClass(IOrderedContainer, Topic)
        verifyClass(WriteLockInterface, Topic)

    def test_z3interfaces(self):
        try:
            from zope.interface.verify import verifyClass
            from Products.CMFCore.interfaces import IDynamicType
            from Products.CMFCore.interfaces import IFolderish
        except ImportError:
            # BBB: for Zope 2.7
            return
        from Products.CMFTopic.Topic import Topic

        verifyClass(IDynamicType, Topic)
        verifyClass(IFolderish, Topic)

    def test_Empty( self ):
        topic = self._makeOne('top')

        query = topic.buildQuery()
        self.assertEqual( len( query ), 0 )

    def test_Simple( self ):
        topic = self._makeOne('top')
        topic.addCriterion( 'foo', 'String Criterion' )
        topic.getCriterion( 'foo' ).edit( 'bar' )

        query = topic.buildQuery()
        self.assertEqual( len(query), 1 )
        self.assertEqual( query['foo'], 'bar' )

        topic.addCriterion( 'baz', 'Integer Criterion' )
        topic.getCriterion( 'baz' ).edit( 43 )

        query = topic.buildQuery()
        self.assertEqual( len( query ), 2 )
        self.assertEqual( query[ 'foo' ], 'bar' )
        self.assertEqual( query[ 'baz' ], 43 )

    def test_Nested( self ):
        self.site._setObject( 'portal_types', TypesTool() )
        fti = FTIDATA_TOPIC[0].copy()
        self.site.portal_types._setObject( 'Topic', FTI(**fti) )
        topic = self._makeOne('top')
        topic._setPortalTypeName('Topic')

        topic.addCriterion( 'foo', 'String Criterion' )
        topic.getCriterion( 'foo' ).edit( 'bar' )

        topic.addSubtopic( 'qux' )
        subtopic = topic.qux

        subtopic.addCriterion( 'baz', 'String Criterion' )
        subtopic.getCriterion( 'baz' ).edit( 'bam' )

        query = subtopic.buildQuery()
        self.assertEqual( len( query ), 2 )
        self.assertEqual( query['foo'], 'bar' )
        self.assertEqual( query['baz'], 'bam' )

        subtopic.acquireCriteria = 0
        query = subtopic.buildQuery()
        self.assertEqual( len( query ), 1 )
        self.assertEqual( query['baz'], 'bam' )

    def test_selfIndexing(self):
        # The Topic object is CatalogAware and should be in the catalog
        # after it has beeen instantiated.
        self._initSite()
        topic = self._makeOne('top')

        # A topic without criteria will return a full catalog search result
        # set, so we should not have one result, for the Topic object itself.
        results = topic.queryCatalog()

        self.assertEquals(len(results), 1)
        self.assertEquals(results[0].getObject().getId(), topic.getId())
        self.assertEquals(results[0].getObject(), topic)

    def test_searchableText(self):
        # Test the catalog helper
        topic = self._makeOne('top')
        topic.edit(False, title='FOO', description='BAR')

        st = topic.SearchableText()
        self.failUnless(st.find('BAR') != -1)
        self.failUnless(st.find('FOO') != -1)

    def test_queryCatalog_noop( self ):

        self._initSite()
        self._initDocuments( **_DOCUMENTS )
        topic = self._makeOne('top')

        # Need to filter out the Topic object itself, which is also
        # CatalogAware and will index itself after instantiation.
        brains = [ x for x in topic.queryCatalog()
                      if x.getObject().getId() != 'top' ]

        self.assertEqual( len( brains ), len( _DOCUMENTS ) )

        objects = [ brain.getObject() for brain in brains ]

        for object in objects:
            self.failUnless( object.getId() in _DOCUMENTS.keys() )
            self.failUnless( object.description in _DOCUMENTS.values() )

    def test_queryCatalog_simple( self ):

        WORD = 'something'

        self._initSite( index_ids=( 'description', ) )
        self._initDocuments( **_DOCUMENTS )
        topic = self._makeOne('top')

        topic.addCriterion( 'description', 'String Criterion' )
        topic.getCriterion( 'description' ).edit( WORD )

        brains = topic.queryCatalog()

        self.assertEqual( len( brains )
                        , len( [ x for x in _DOCUMENTS.values()
                                  if WORD in x ] ) )

        objects = [ brain.getObject() for brain in brains ]

        for object in objects:
            self.failUnless( object.getId() in _DOCUMENTS.keys() )
            self.failUnless( object.description in _DOCUMENTS.values() )

    def test_synContentValues_simple( self ):

        self._initSite()
        self._initDocuments( **_DOCUMENTS )
        topic = self._makeOne('top')

        #brains = topic.synContentValues()
        # Need to filter out the Topic object itself, which is also
        # CatalogAware and will index itself after instantiation.
        brains = [ x for x in topic.synContentValues()
                      if x.getObject().getId() != 'top' ]

        self.assertEqual( len( brains ), len( _DOCUMENTS ) )

        objects = [ brain.getObject() for brain in brains ]

        for object in objects:
            self.failUnless( object.getId() in _DOCUMENTS.keys() )
            self.failUnless( object.description in _DOCUMENTS.values() )

    def test_synContentValues_limit( self ):

        LIMIT = 3

        self._initSite( max_items=LIMIT )
        self._initDocuments( **_DOCUMENTS )
        topic = self._makeOne('top')

        brains = topic.synContentValues()

        self.assertEqual( len( brains ), LIMIT )

        objects = [ brain.getObject() for brain in brains ]

        for object in objects:
            self.failUnless( object.getId() in _DOCUMENTS.keys() )
            self.failUnless( object.description in _DOCUMENTS.values() )


_DOCUMENTS = \
{ 'one'     : "something in the way she moves"
, 'two'     : "I don't know much about history"
, 'three'   : "something about Mary"
, 'four'    : "something tells me I'm in love"
, 'five'    : "there's a certain wonderful something"
, 'six'     : "gonna wash that man right out of my hair"
, 'seven'   : "I'm so much in love"
}


def test_suite():
    return TestSuite((
        makeSuite(TestTopic),
        ))

if __name__ == '__main__':
    main(defaultTest='test_suite')

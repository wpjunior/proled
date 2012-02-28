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
""" Unit tests for Favorites.

$Id: test_Favorite.py 37135 2005-07-08 13:24:33Z tseaver $
"""

from unittest import TestCase, TestSuite, makeSuite, main
import Testing
try:
    import Zope2
except ImportError: # BBB: for Zope 2.7
    import Zope as Zope2
Zope2.startup()

from Products.CMFCore.tests.base.dummy import DummySite
from Products.CMFCore.tests.base.dummy import DummyTool
from Products.CMFDefault.Favorite import Favorite


class FavoriteTests( TestCase ):

    def setUp( self ):
        self.site = DummySite('site')
        self.site._setObject( 'portal_membership', DummyTool() )
        self.site._setObject( 'portal_url', DummyTool() )

    def _makeOne(self, id, *args, **kw):
        return self.site._setObject( id, Favorite(id, *args, **kw) )

    def test_Empty( self ):
        utool = self.site.portal_url
        f = self._makeOne( 'foo' )

        self.assertEqual( f.getId(), 'foo' )
        self.assertEqual( f.Title(), '' )
        self.assertEqual( f.Description(), '' )
        self.assertEqual( f.getRemoteUrl(), utool.root )
        self.assertEqual( f.getObject(), self.site )
        self.assertEqual( f.getIcon(), self.site.getIcon() )
        self.assertEqual( f.getIcon(1), self.site.getIcon(1) )

    def test_CtorArgs( self ):
        utool = self.site.portal_url
        self.assertEqual( self._makeOne( 'foo'
                                       , title='Title'
                                       ).Title(), 'Title' )

        self.assertEqual( self._makeOne( 'bar'
                                       , description='Description'
                                       ).Description(), 'Description' )

        baz = self._makeOne( 'baz', remote_url='portal_url' )
        self.assertEqual( baz.getObject(), utool )
        self.assertEqual( baz.getRemoteUrl()
                        , '%s/portal_url' % utool.root )
        self.assertEqual( baz.getIcon(), utool.getIcon() )

    def test_edit( self ):
        utool = self.site.portal_url
        f = self._makeOne( 'foo' )
        f.edit( 'portal_url' )
        self.assertEqual( f.getObject(), utool )
        self.assertEqual( f.getRemoteUrl()
                        , '%s/portal_url' % utool.root )
        self.assertEqual( f.getIcon(), utool.getIcon() )

    def test_editEmpty( self ):
        utool = self.site.portal_url
        f = self._makeOne( 'gnnn' )
        f.edit( '' )
        self.assertEqual( f.getObject(), self.site )
        self.assertEqual( f.getRemoteUrl(), utool.root )
        self.assertEqual( f.getIcon(), self.site.getIcon() )


def test_suite():
    return TestSuite((
        makeSuite( FavoriteTests ),
        ))

if __name__ == '__main__':
    main(defaultTest='test_suite')

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
""" Unit tests for SortCriterion module.

$Id: test_SortC.py 37135 2005-07-08 13:24:33Z tseaver $
"""

from unittest import TestSuite, makeSuite, main
import Testing
try:
    import Zope2
except ImportError: # BBB: for Zope 2.7
    import Zope as Zope2
Zope2.startup()

from common import CriterionTestCase


class SortCriterionTests(CriterionTestCase):

    def _getTargetClass(self):
        from Products.CMFTopic.SortCriterion import SortCriterion

        return SortCriterion

    def test_Empty( self ):
        ssc = self._makeOne('foo', 'foofield')

        self.assertEqual( ssc.getId(), 'foo' )
        self.assertEqual( ssc.field, None )
        self.assertEqual( ssc.index, 'foofield' )
        self.assertEqual( ssc.Field(), 'foofield' )
        self.assertEqual( ssc.reversed, 0 )

        items = ssc.getCriteriaItems()
        self.assertEqual( len( items ), 1 )
        self.assertEqual( items[0][0], 'sort_on' )
        self.assertEqual( items[0][1], 'foofield' )

    def test_Nonempty( self ):
        ssc = self._makeOne('foo', 'foofield')

        ssc.edit( 1 )

        self.assertEqual( ssc.getId(), 'foo' )
        self.assertEqual( ssc.field, None )
        self.assertEqual( ssc.index, 'foofield' )
        self.assertEqual( ssc.Field(), 'foofield' )
        self.assertEqual( ssc.reversed, 1 )

        items = ssc.getCriteriaItems()
        self.assertEqual( len( items ), 2 )
        self.assertEqual( items[0][0], 'sort_on' )
        self.assertEqual( items[0][1], 'foofield' )
        self.assertEqual( items[1][0], 'sort_order' )
        self.assertEqual( items[1][1], 'reverse' )


def test_suite():
    return TestSuite((
        makeSuite(SortCriterionTests),
        ))

if __name__ == '__main__':
    main(defaultTest='test_suite')

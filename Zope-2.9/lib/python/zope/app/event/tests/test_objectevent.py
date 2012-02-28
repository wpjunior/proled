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
"""Object Event Tests

$Id: test_objectevent.py 30927 2005-06-25 16:58:29Z philikon $
"""
import unittest
from zope.testing import doctest

from zope.app.annotation.interfaces import IAnnotations, IAnnotatable
from zope.app.annotation.interfaces import IAttributeAnnotatable
from zope.app.annotation.attribute import AttributeAnnotations
from zope.app.dublincore.interfaces import IZopeDublinCore
from zope.app.dublincore.annotatableadapter import ZDCAnnotatableAdapter
from zope.app.event.objectevent import ObjectModifiedEvent
from zope.app.event.objectevent import ObjectAnnotationsModifiedEvent
from zope.app.event.objectevent import ObjectContentModifiedEvent
from zope.app.event import objectevent
from zope.app.container.contained import Contained, ObjectRemovedEvent
from zope.app.container.interfaces import IContained, IObjectRemovedEvent
from zope.app.container.interfaces import IObjectEvent
from zope.app.container.sample import SampleContainer
from zope.app.testing.placelesssetup import setUp, tearDown
from zope.app.testing import ztapi

    
class TestObjectModifiedEvent(unittest.TestCase):

    klass = ObjectModifiedEvent
    object = object()

    def setUp(self):
        self.event = self.klass(self.object)

    def testGetObject(self):
        self.assertEqual(self.event.object, self.object)

class TestObjectAnnotationsModifiedEvent(TestObjectModifiedEvent):
    klass = ObjectAnnotationsModifiedEvent
    
    def setUp(self):
        self.event = self.klass(self.object, deprecated_use=False)

class TestObjectContentModifiedEvent(TestObjectModifiedEvent):
    klass = ObjectContentModifiedEvent
    
    def setUp(self):
        self.event = self.klass(self.object, deprecated_use=False)
        

class TestObjectEventNotifications(unittest.TestCase):
    def setUp(self):
        self.callbackTriggered = False
        setUp()

    def testNotify(self):
        events = []

        def record(*args):
            events.append(args)

        ztapi.subscribe([IContained, IObjectRemovedEvent], None, record)

        item = Contained()
        event = ObjectRemovedEvent(item)
        objectevent.objectEventNotify(event)
        self.assertEqual([(item, event)], events)

    def testNotifyNobody(self):
        # Check that notify won't raise an exception in absence of
        # of subscribers.
        events = []
        item = Contained()
        evt = ObjectRemovedEvent(item)
        objectevent.objectEventNotify(evt)
        self.assertEqual([], events)

    def testVeto(self):
        ztapi.subscribe([IObjectEvent], None, objectevent.objectEventNotify)
        container = SampleContainer()
        item = Contained()

        # This will fire an event.
        container['Fred'] = item

        class Veto(Exception):
            pass
        
        def callback(item, event):
            self.callbackTriggered = True
            self.assertEqual(item, event.object)
            raise Veto

        ztapi.subscribe([IContained, IObjectRemovedEvent], None, callback)

        # del container['Fred'] will fire an ObjectRemovedEvent event.
        self.assertRaises(Veto, container.__delitem__, 'Fred')
        
    def tearDown(self):
        tearDown()

def setUpObjectEventDocTest(test) :
    setUp()
        
    ztapi.provideAdapter(IAttributeAnnotatable,
                                IAnnotations, AttributeAnnotations) 
    ztapi.provideAdapter(IAnnotatable,
                                IZopeDublinCore, ZDCAnnotatableAdapter)    

def tearDownObjectEventDocTest(test) :
    tearDown()

def test_suite():
    return unittest.TestSuite((
        unittest.makeSuite(TestObjectModifiedEvent),
        unittest.makeSuite(TestObjectAnnotationsModifiedEvent),
        unittest.makeSuite(TestObjectContentModifiedEvent),
        unittest.makeSuite(TestObjectEventNotifications),
        doctest.DocTestSuite("zope.app.event.objectevent",
                                       setUp=setUpObjectEventDocTest,
                                       tearDown=tearDownObjectEventDocTest,
                                       optionflags=doctest.NORMALIZE_WHITESPACE),
        ))

if __name__=='__main__':
    unittest.main(defaultTest='test_suite')

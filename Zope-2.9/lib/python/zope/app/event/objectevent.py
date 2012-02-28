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
"""In Zope3 events are used by components to inform each other
about relevant new objects and object modifications.

To keep all subscribers up to date it is indispensable that the life cycle of 
an object is accompanied by various events. 

    >>> class Sample(object) :
    ...    "Test class"

    >>> obj = Sample()
    >>> notify(ObjectCreatedEvent(obj))
    
    >>> obj.modified = True
    >>> notify(ObjectModifiedEvent(obj))
    
Zope3's Dublin Core Metadata for instance, rely on the bare
ObjectCreatedEvent and ObjectModifiedEvent to record creation and modification
times. Other event consumers like catalogs and caches may need more information 
to update themselves in an efficient manner. The necessary information can
be provided as optional modification descriptions of the ObjectModifiedEvent.

Some examples:
    
    >>> from zope.app.file import File
    >>> from zope.app.file.interfaces import IFile
    >>> file = File()
    >>> file.data = "123"
    >>> notify(ObjectModifiedEvent(obj, IFile))
    
This says that we modified something via IFile.  Note that an interface is an 
acceptable description. In fact, we might allow pretty much anything as a 
description and it depends on your needs what kind of descriptions 
you use.

In the following we use an IAttributes description to describe in more detail
which parts of an object where modified :

    >>> file.data = "456"
 
    >>> from zope.app.dublincore.interfaces import IZopeDublinCore
    >>> from zope.interface import directlyProvides
    >>> from zope.app.annotation.interfaces import IAttributeAnnotatable
    >>> directlyProvides(file, IAttributeAnnotatable) 
    
    >>> IZopeDublinCore(file).title = u"New title"
    >>> IZopeDublinCore(file).title = u"New description"
    >>> event = ObjectModifiedEvent(obj, Attributes(IFile, 'data'),
    ...                  Attributes(IZopeDublinCore, 'title', 'description'),
    ...                  )
    >>> notify(event)

This says we modified the file data and the DC title and description.


$Id: objectevent.py 40367 2005-11-25 13:32:29Z efge $
"""
__docformat__ = 'restructuredtext'

from zope.app.event.interfaces import IObjectEvent, IObjectCreatedEvent
from zope.app.event.interfaces import IObjectModifiedEvent
from zope.app.event.interfaces import IObjectCopiedEvent
from zope.app.event.interfaces import IObjectAnnotationsModifiedEvent
from zope.app.event.interfaces import IObjectContentModifiedEvent
from zope.app.event.interfaces import IAttributes, ISequence
from zope.interface import implements
from zope.event import notify
from zope.component import subscribers

# BBB Backward Compatibility (Can go away in 3.3)
import warnings 


_marker = object()


class ObjectEvent(object):
    """Something has happened to an object"""


    implements(IObjectEvent)

    def __init__(self, object):
        self.object = object


class ObjectCreatedEvent(ObjectEvent):
    """An object has been created"""

    implements(IObjectCreatedEvent)


class Attributes(object) :
    """
    Describes modified attributes of an interface.

        >>> from zope.app.dublincore.interfaces import IZopeDublinCore
        >>> desc = Attributes(IZopeDublinCore, "title", "description")
        >>> desc.interface == IZopeDublinCore
        True
        >>> 'title' in desc.attributes
        True

    """

    implements(IAttributes)

    def __init__(self, interface, *attributes) :
        self.interface = interface
        self.attributes = attributes


class Sequence(object) :
    """
    Describes modified keys of an interface.
    
        >>> from zope.app.container.interfaces import IContainer
        >>> desc = Sequence(IContainer, 'foo', 'bar')
        >>> desc.interface == IContainer
        True
        >>> desc.keys
        ('foo', 'bar')

    """
    
    implements(ISequence)
    
    def __init__(self, interface, *keys) :
        self.interface = interface
        self.keys = keys


class ObjectModifiedEvent(ObjectEvent):
    """An object has been modified"""

    implements(IObjectModifiedEvent)

    def __init__(self, object, *descriptions) :
        """
        Init with a list of modification descriptions.
        
        >>> from zope.interface import implements, Interface, Attribute
        >>> class ISample(Interface) :
        ...     field = Attribute("A test field")
        >>> class Sample(object) :
        ...     implements(ISample)
        
        >>> obj = Sample()
        >>> obj.field = 42
        >>> notify(ObjectModifiedEvent(obj, Attributes(ISample, "field")))
        
        """
        super(ObjectModifiedEvent, self).__init__(object) 
        self.descriptions = descriptions
        

def modified(object, *descriptions):
    notify(ObjectModifiedEvent(object, *descriptions))


class ObjectCopiedEvent(ObjectCreatedEvent):
    """An object has been copied"""

    implements(IObjectCopiedEvent)

    def __init__(self, object, original=None):
        super(ObjectCopiedEvent, self).__init__(object)
        self.original = original
        # BBB goes away in 3.3
        if original is None:
            warnings.warn(
                "%s with no original is deprecated and will no-longer "
                "be supported starting in Zope 3.3."
                % self.__class__.__name__,
                DeprecationWarning, stacklevel=2)


def objectEventNotify(event):
    """Event subscriber to dispatch ObjectEvents to interested adapters."""
    adapters = subscribers((event.object, event), None)
    for adapter in adapters:
        pass # getting them does the work


# BBB:  Can go away in 3.3

class ObjectAnnotationsModifiedEvent(ObjectModifiedEvent):
    """An object's annotations have been modified"""

    implements(IObjectAnnotationsModifiedEvent)

    def __init__(self, object, deprecated_use=True) :
        super(ObjectAnnotationsModifiedEvent, self).__init__(object)
        if deprecated_use :
            warnings.warn(
                "%s is deprecated and will no-longer be supported "
                "starting in Zope 3.3.  Use ObjectModifiedEvent "
                "and modification descriptors instead."
                % self.__class__.__name__,
                DeprecationWarning)


def annotationModified(object, deprecated_use=True):
    warnings.warn(
                "annotationModified is deprecated and will no-longer be "
                "supported starting in Zope 3.3.  Use modified "
                "and modification descriptors instead."
                % self.__class__.__name__,
                DeprecationWarning)
                
    notify(ObjectAnnotationsModifiedEvent(object, deprecated_use=False))


class ObjectContentModifiedEvent(ObjectModifiedEvent):
    """An object's content has been modified"""

    implements(IObjectContentModifiedEvent)

    def __init__(self, object, deprecated_use=True) :
        super(ObjectContentModifiedEvent, self).__init__(object)
        if deprecated_use :
            warnings.warn(
                "%s is deprecated and will no-longer be supported "
                "starting in Zope 3.3.  Use ObjectModifiedEvent "
                "and modification descriptors instead."
                % self.__class__.__name__,
                DeprecationWarning)


def contentModified(object, deprecated_use=True):
    warnings.warn(
                "contentModified is deprecated and will no-longer be "
                "supported starting in Zope 3.3.  Use modified "
                "and modification descriptors instead."
                % self.__class__.__name__,
                DeprecationWarning)

    notify(ObjectContentModifiedEvent(object, deprecated_use=False))

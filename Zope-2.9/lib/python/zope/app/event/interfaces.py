##############################################################################
#
# Copyright (c) 2002, 2003 Zope Corporation and Contributors.
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
"""Event-related interfaces

$Id: interfaces.py 40367 2005-11-25 13:32:29Z efge $
"""
__docformat__ = 'restructuredtext'

from zope.interface import Interface, Attribute


class IObjectEvent(Interface):
    """An event related to an object.

    The object that generated this event is not necessarily the object
    refered to by location.
    """

    object = Attribute("The subject of the event.")


class IObjectCreatedEvent(IObjectEvent):
    """An object has been created.

    The location will usually be ``None`` for this event."""


class IObjectCopiedEvent(IObjectCreatedEvent):
    """An object has been copied"""

    original = Attribute("The original from which the copy was made")


class IObjectModifiedEvent(IObjectEvent):
    """An object has been modified"""


class IModificationDescription(Interface) :
    """ Marker interface for descriptions of object modifications.

    Can be used as a parameter of an IObjectModifiedEvent."""


class IAttributes(IModificationDescription) :
    """ Describes the attributes of an interface.

    """

    interface = Attribute("The involved interface.")
    attributes = Attribute("A sequence of modified attributes.")


class ISequence(IModificationDescription) :
    """ Describes the modified keys of a sequence-like interface.

    """

    interface = Attribute("The involved interface.")
    keys = Attribute("A sequence of modified keys.")


# BBB: will go in Zope3.3

class IObjectAnnotationsModifiedEvent(IObjectModifiedEvent):
    """An object's annotations have been modified"""


class IObjectContentModifiedEvent(IObjectModifiedEvent):
    """An object's content has been modified"""

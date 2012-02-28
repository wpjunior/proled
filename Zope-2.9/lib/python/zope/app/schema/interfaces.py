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
"""TTW Schema Interfaces

$Id: interfaces.py 26006 2004-06-30 18:56:03Z mgedmin $
"""
from zope.interface import Interface
from zope.interface.interfaces import IInterface
from zope.app.container.interfaces import IAdding

class ISchemaUtility(Interface):
    pass

class ISchemaAdding(IAdding):
    pass

class IReadMutableSchema(IInterface):
    """This object represents an interface/schema that can be edited by
    managing the fields it contains."""

    def getName(name):
        """Get the name of the schema."""

class IWriteMutableSchema(Interface):
    """This object represents an interface/schema that can be edited by
    managing the fields it contains."""

    def setName(name):
        """Set the name of the schema."""

    def addField(name, field):
        """Add a field to schema."""

    def removeField(name):
        """Remove field by name from the schema.

        If the field does not exist, raise an error.
        """

    def renameField(orig_name, target_name):
        """Rename a field.

        If the target_name is already taken, raise an error.
        """

    def insertField(name, field, position):
        """Insert a field with a given name at the specified position.

        If the position does not make sense, i.e. a negative number of a
        number larger than len(self), then an error is raised.
        """

    def moveField(name, position):
        """Move a field (given by its name) to a particular position.

        If the position does not make sense, i.e. a negative number of a
        number larger than len(self), then an error is raised.
        """

    def moveField(name, position):
        """Move a field (given by its name) to a particular position.

        If the position does not make sense, i.e. a negative number of a
        number larger than len(self), then an error is raised.
        """

    def __setitem__(name, object):
        """Add the given object to the container under the given name.
        """

    def __delitem__(name):
        """Delete the named object from the container.

        Raises a KeyError if the object is not found.
        """

class IMutableSchema(IReadMutableSchema, IWriteMutableSchema):
    """This object represents an interface/schema that can be edited by
    managing the fields it contains."""

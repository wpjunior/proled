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
"""TTW Schema (as Utility)

$Id: schema.py 38178 2005-08-30 21:50:19Z mj $
"""
from types import FunctionType

from persistent import Persistent
from persistent.dict import PersistentDict
from zope.interface import Interface, implements

from zope.security.proxy import removeSecurityProxy
from zope.proxy import removeAllProxies
from zope.app import zapi
from zope.app.container.browser.adding import Adding
from zope.app.interface import PersistentInterfaceClass
from zope.app.component.site import UtilityRegistration
from zope.app.container.contained import Contained, setitem, uncontained

from zope.interface.interface import Attribute, Method, fromFunction
from zope.interface.interface import InterfaceClass
from zope.interface.exceptions import InvalidInterface
from zope.schema import getFieldsInOrder, getFieldNamesInOrder

from wrapper import Struct
from interfaces import ISchemaAdding, IMutableSchema, ISchemaUtility

class BaseSchemaUtility(InterfaceClass):

    implements(IMutableSchema, ISchemaUtility)

    def __init__(self, name='', bases=(), attrs=None,
                 __doc__=None, __module__=None):
        if not bases:
            bases = (Interface,)
        super(BaseSchemaUtility, self).__init__(name, bases,
                                            attrs, __doc__, __module__)
        self._clear()

    def _clear(self):
        self.schemaPermissions = {}
        self._attrs = {}

    def setName(self, name):
        """See zope.app.interfaces.utilities.IMutableSchema"""
        self.__name__ = name

    def addField(self, name, field):
        """See zope.app.interfaces.utilities.IMutableSchema"""
        fields = getFieldsInOrder(self)
        field_names = [n for n, f in fields]
        fields = [f for n, f in fields]
        if name in field_names:
            raise KeyError("Field %s already exists." % name)
        if fields:
            field.order = fields[-1].order + 1
        self[name] = field

    def removeField(self, name):
        """See zope.app.interfaces.utilities.IMutableSchema"""
        fields = getFieldNamesInOrder(self)
        if name not in fields:
            raise KeyError("Field %s does not exists." % name)
        del self[name]

    def renameField(self, orig_name, target_name):
        """See zope.app.interfaces.utilities.IMutableSchema"""
        fields = getFieldNamesInOrder(self)
        if orig_name not in fields:
            raise KeyError("Field %s does not exists." % orig_name)
        if target_name in fields:
            raise KeyError("Field %s already exists." % target_name)
        field = self[orig_name]
        del self[orig_name]
        field.__name__ = None
        self[target_name] = field

    def insertField(self, name, field, position):
        """See zope.app.interfaces.utilities.IMutableSchema"""
        fields = getFieldsInOrder(self)
        field_names = [n for n, f in fields]
        fields = [f for n, f in fields]
        if name in field_names:
            raise KeyError("Field %s already exists." % name)
        if not 0 <= position <= len(field_names):
            raise IndexError("Position %s out of range." % position)
        fields.insert(position, field)
        for p, f in enumerate(fields):
            if not f.order == p:
                f.order = p
        self[name] = field

    def moveField(self, name, position):
        """See zope.app.interfaces.utilities.IMutableSchema"""
        fields = getFieldsInOrder(self)
        field_names = [n for n, f in fields]
        fields = [f for n, f in fields]
        if name not in field_names:
            raise KeyError("Field %s does not exist." % name)
        if not 0 <= position <= len(field_names):
            raise IndexError("Position %s out of range." % position)
        index = field_names.index(name)
        if index == position: return
        field = fields[index]
        del fields[index]
        fields.insert(position, field)
        for p, f in enumerate(fields):
            if not f.order == p:
                f.order = p

    def __delitem__(self, name):
        uncontained(self._attrs[name], self, name)
        del self._attrs[name]

    def __setitem__(self, name, value):
        value = removeAllProxies(value)
        if isinstance(value, Attribute):
            value.interface = name
            if not value.__name__:
                value.__name__ = name
            elif isinstance(value, FunctionType):
                attrs[name] = fromFunction(value, name, name=name)
            else:
                raise InvalidInterface("Concrete attribute, %s" % name)

        setitem(self, self._attrs.__setitem__, name, value)

    # Methods copied from zope.interface.interface.InterfaceClass,
    # to avoid having to work around name mangling, which happens to be
    # ugly and undesirable.
    # Copied some methods, but not all. Only the ones that used __attrs
    # and __bases__. Changed __attrs to _attrs, which is a PersistentDict,
    # and __bases__ to getBases(), whic filters instances of InterfaceClass
    def getBases(self):
        return [b for b in self.__bases__ if isinstance(b, self.__class__)]

    def extends(self, interface, strict=True):
        """Does an interface extend another?"""
        return ((interface in self._implied)
                and
                ((not strict) or (self != interface))
                )

    def names(self, all=False):
        """Return the attribute names defined by the interface."""
        if not all:
            return self._attrs.keys()

        r = {}
        for name in self._attrs.keys():
            r[name] = 1
        for base in self.getBases():
            for name in base.names(all):
                r[name] = 1
        return r.keys()

    def namesAndDescriptions(self, all=False):
        """Return attribute names and descriptions defined by interface."""
        if not all:
            return self._attrs.items()

        r = {}
        for name, d in self._attrs.items():
            r[name] = d

        for base in self.getBases():
            for name, d in base.namesAndDescriptions(all):
                if name not in r:
                    r[name] = d

        return r.items()

    def getDescriptionFor(self, name):
        """Return the attribute description for the given name."""
        r = self.queryDescriptionFor(name)
        if r is not None:
            return r

        raise KeyError(name)

    __getitem__ = getDescriptionFor

    def queryDescriptionFor(self, name, default=None):
        """Return the attribute description for the given name."""
        r = self._attrs.get(name, self)
        if r is not self:
            return r
        for base in self.getBases():
            r = base.queryDescriptionFor(name, self)
            if r is not self:
                return r

        return default

    get = queryDescriptionFor

    def deferred(self):
        """Return a defered class corresponding to the interface."""
        if hasattr(self, "_deferred"): return self._deferred

        klass={}
        exec "class %s: pass" % self.__name__ in klass
        klass=klass[self.__name__]

        self.__d(klass.__dict__)

        self._deferred=klass

        return klass

    def __d(self, dict):

        for k, v in self._attrs.items():
            if isinstance(v, Method) and not (k in dict):
                dict[k]=v

        for b in self.getBases(): b.__d(dict)


class StructPersistentDict(PersistentDict):

    def __setitem__(self, name, value):
        if not isinstance(value, Persistent):
            value = Struct(value)
        return super(StructPersistentDict, self).__setitem__(name, value)


class SchemaUtility(BaseSchemaUtility, PersistentInterfaceClass, Contained):

    def __init__(self, name='', bases=(), attrs=None,
                 __doc__=None, __module__=None):
        if not bases:
            bases = (Interface,)
        PersistentInterfaceClass.__init__(self, name, bases,
                                          attrs, __doc__, __module__)
        self._clear()

    def _clear(self):
        self.schemaPermissions = PersistentDict()
        self._attrs = StructPersistentDict()


class SchemaAdding(Adding):

    implements(ISchemaAdding)

    menu_id = "add_schema_field"

    def add(self, content):
        name = self.contentName
        container = IMutableSchema(self.context)
        container.addField(name, content)
        return content

    def nextURL(self):
        """See zope.app.container.interfaces.IAdding"""
        return zapi.absoluteURL(self.context, self.request)+'/@@editschema.html'


class SchemaRegistration(UtilityRegistration):
    """Schema Registration

    We have a custom registration here, since we want active registrations to
    set the name of the schema.
    """

    def activated(self):
        self.component.setName(self.name)

    def deactivated(self):
        self.component.setName('<schema not activated>')

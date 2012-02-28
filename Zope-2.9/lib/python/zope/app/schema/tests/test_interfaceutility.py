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
"""Interfaces as Utilities tests

$Id: test_interfaceutility.py 29143 2005-02-14 22:43:16Z srichter $
"""
import unittest
from zope.interface import Interface, implements
from zope.interface.interface import InterfaceClass
from zope.interface.interfaces import IInterface
from zope.component.exceptions import ComponentLookupError

from zope.app import zapi
from zope.app.component.interfaces import ILocalUtility
from zope.app.component.site import UtilityRegistration
from zope.app.component.testing import PlacefulSetup
from zope.app.component.interface import getInterface, searchInterface
from zope.app.component.interfaces.registration import ActiveStatus
from zope.app.component.interfaces.registration import InactiveStatus
from zope.app.component.interfaces.registration import IRegistered
from zope.app.container.contained import Contained
from zope.app.dependable.interfaces import IDependable
from zope.app.testing import setup
from zope.app.traversing.api import traverse

class IBaz(Interface): pass

class Baz(object):
    # We implement IRegistered and IDependable directly to
    # depend as little  as possible on other infrastructure.
    implements(IBaz, ILocalUtility, IRegistered, IDependable)

    def __init__(self, name):
        self.name = name
        self._usages = []
        self._dependents = []

    def foo(self):
        return 'foo ' + self.name

    def addUsage(self, location):
        "See zope.app.registration.interfaces.IRegistered"
        if location not in self._usages:
            self._usages.append(location)

    def removeUsage(self, location):
        "See zope.app.registration.interfaces.IRegistered"
        self._usages.remove(location)

    def usages(self):
        "See zope.app.registration.interfaces.IRegistered"
        return self._usages

    def addDependent(self, location):
        "See zope.app.dependable.interfaces.IDependable"
        if location not in self._dependents:
            self._dependents.append(location)

    def removeDependent(self, location):
        "See zope.app.dependable.interfaces.IDependable"
        self._dependents.remove(location)

    def dependents(self):
        "See zope.app.dependable.interfaces.IDependable"
        return self._dependents

class Foo(InterfaceClass, Baz, Contained):

    def __init__(self, name):
        InterfaceClass.__init__(self, name, (Interface,))
        Baz.__init__(self, name)

class Bar(Foo): pass

class TestInterfaceUtility(PlacefulSetup, unittest.TestCase):

    def setUp(self):
        sm = PlacefulSetup.setUp(self, site=True)

    def test_getLocalInterface_delegates_to_globalUtility(self):
        gsm = zapi.getGlobalSiteManager()
        gsm.provideUtility(IInterface, Bar("blob"), name="blob")
        gsm.provideUtility(IBaz, Baz("global baz"))
        gsm.provideUtility(IInterface, Foo("global bob"), name="bob")

        self.assertEqual(getInterface(None, "bob").__class__, Foo)
        self.assertEqual(getInterface(None, "blob").__class__, Bar)

    def test_localInterfaceitems_filters_accordingly(self):
        bar = Bar("global")
        baz = Baz("global baz")
        foo = Foo("global bob")

        gsm = zapi.getGlobalSiteManager()
        gsm.provideUtility(IInterface, foo, name="bob")
        gsm.provideUtility(IInterface, bar)
        gsm.provideUtility(IBaz, baz)

        ifaces = searchInterface(None)
        self.assert_(len(ifaces), 2)
        for pair in [(foo), (bar)]:
            self.assert_(pair in ifaces)

        iface_utilities = gsm.getUtilitiesFor(IInterface)
        ifaces = [iface for (name, iface) in iface_utilities]

        self.assert_(len(ifaces), 2)
        for pair in [(foo), (bar)]:
            self.assert_(pair in ifaces)

        for pair in [(foo), (bar)]:
            self.assert_(pair in ifaces)

    def test_localInterfaceitems_filters_only_interfaces(self):
        bar = Bar("global")
        baz = Baz("global baz")
        foo = Foo("global bob")
        gsm = zapi.getGlobalSiteManager()
        gsm.provideUtility(IInterface, foo, name="bob")
        gsm.provideUtility(ILocalUtility, bar)
        gsm.provideUtility(IBaz, baz)

        iface_utilities = gsm.getUtilitiesFor(IInterface)
        ifaces = [iface for (name, iface) in iface_utilities]
        self.assertEqual(ifaces, [(foo)])

        iface_utilities = gsm.getUtilitiesFor(ILocalUtility)
        ifaces = [iface for (name, iface) in iface_utilities]
        self.assertEqual(ifaces, [(bar)])

        iface_utilities = gsm.getUtilitiesFor(IBaz)
        ifaces = [iface for (name, iface) in iface_utilities]
        self.assertEqual(ifaces, [(baz)])

    def test_getLocalInterface_raisesComponentLookupError(self):
        gsm = zapi.getGlobalSiteManager()
        gsm.provideUtility(IInterface, Foo("global"))
        gsm.provideUtility(IBaz, Baz("global baz"))
        gsm.provideUtility(IInterface, Foo("global bob"), name="bob")

        self.assertRaises(ComponentLookupError,
                          getInterface, None, "bobesponja")

    def test_globalsearchInterface_delegates_to_globalUtility(self):
        foo = Foo("global bob")
        bar = Bar("global")
        baz = Baz("global baz")
        gsm = zapi.getGlobalSiteManager()
        gsm.provideUtility(IInterface, bar)
        gsm.provideUtility(IBaz, baz)
        gsm.provideUtility(IInterface, foo, name="bob")

        self.assertEqual(searchInterface(None, search_string="bob"),
                         [foo])

    def test_localsearchInterface_delegates_to_globalUtility(self):
        # Same test as above!
        foo = Foo("global bob")
        bar = Bar("global")
        baz = Baz("global baz")
        gsm = zapi.getGlobalSiteManager()
        gsm.provideUtility(IInterface, bar)
        gsm.provideUtility(IBaz, baz)
        gsm.provideUtility(IInterface, foo, name="bob")

        self.assertEqual(searchInterface(None, search_string="bob"),
                         [foo])

    def test_query_get_Utility_delegates_to_global(self):
        gsm = zapi.getGlobalSiteManager()
        gsm.provideUtility(IInterface, Foo("global"))
        gsm.provideUtility(IInterface, Foo("global bob"), name="bob")

        sm = zapi.getSiteManager(self.rootFolder)
        self.assert_(gsm != sm)

        # If queryUtility works on the site manager, getUtility in zapi must
        # also work.
        self.assertEqual(sm.queryUtility(IInterface).foo(), "foo global")
        self.assertEqual(sm.queryUtility(IInterface, "bob").foo(),
                         "foo global bob")

    def test_local_utilities(self):
        gsm = zapi.getGlobalSiteManager()
        gsm.provideUtility(IInterface, Foo("global"))
        gsm.provideUtility(IInterface, Foo("global bob"), name="bob")

        sm = zapi.getSiteManager(self.rootFolder)
        default = traverse(self.rootFolder, "++etc++site/default")
        default['foo'] = Foo("local")
        foo = default['foo']
        cm = default.registrationManager

        for name in ('', 'bob'):
            registration = UtilityRegistration(name, IInterface, foo)
            cname = cm.addRegistration(registration)
            registration = traverse(cm, cname)

            gout = name and "foo global "+name or "foo global"
            self.assertEqual(sm.queryUtility(IInterface, name).foo(), gout)

            registration.status = ActiveStatus
            self.assertEqual(
                sm.queryUtility(IInterface, name).foo(), "foo local")

            registration.status = InactiveStatus
            self.assertEqual(sm.queryUtility(IInterface, name).foo(), gout)


def test_suite():
    return unittest.makeSuite(TestInterfaceUtility)

if __name__ == '__main__':
    unittest.main()

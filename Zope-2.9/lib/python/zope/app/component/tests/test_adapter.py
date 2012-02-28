##############################################################################
#
# Copyright (c) 2004 Zope Corporation and Contributors.
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
"""Registration Tests

$Id$
"""
__docformat__ = "reStructuredText"
import unittest
import transaction
from ZODB.tests.util import DB

import zope.component.testing as placelesssetup
import zope.interface
from zope.interface.adapter import AdapterRegistry
from zope.testing import doctest

from zope.app.component import interfaces
from zope.app.component.adapter import LocalAdapterRegistry, AdapterRegistration
from zope.app.testing import setup

class IF0(zope.interface.Interface):
    pass

class IF1(IF0):
    pass

class IF2(IF1):
    pass

class IB0(zope.interface.Interface):
    pass

class IB1(IB0):
    pass

class IR0(zope.interface.Interface):
    pass

class IR1(IR0):
    pass

class R1(object):
    zope.interface.implements(IR1)

class F0(object):
    zope.interface.implements(IF0)

class F2(object):
    zope.interface.implements(IF2)

# Create a picklable global registry. The pickleability of other
# global adapter registries is beyond the scope of these tests:
class GlobalAdapterRegistry(AdapterRegistry):
    def __reduce__(self):
        return 'globalAdapterRegistry'

globalAdapterRegistry = GlobalAdapterRegistry()

def test_local_adapter():
    """Local Adapter Tests

   Local surrogates and adapter registries share declarations with
   those "above" them.

   Suppose we have a global AdapterRegistry:

   >>> G = AdapterRegistry()

   we also have a local adapter registry, with G as it's base:

   >>> L1 = LocalAdapterRegistry(G)

   and so on:

   >>> L2 = LocalAdapterRegistry(G, L1)

   Now, if we declare an adapter globally:

   >>> G.register([IF1], IB1, '', 'A11G')

   we can query it locally:

   >>> L1.lookup([IF2], IB1)
   'A11G'
   
   >>> L2.lookup([IF2], IB1)
   'A11G'

   We can add local definitions:

   >>> ra011 = AdapterRegistration(required=IF0, provided=IB1, factory='A011',
   ...                             registry=L1)
   >>> ra011.status = interfaces.registration.ActiveStatus

   and use it:

   >>> L1.lookup([IF0], IB1)
   'A011'
   
   >>> L2.lookup([IF0], IB1)
   'A011'
   
   but not outside L1:

   >>> G.lookup([IF0], IB1)

   Note that it doesn't override the non-local adapter:

   >>> L1.lookup([IF2], IB1)
   'A11G'
   
   >>> L2.lookup([IF2], IB1)
   'A11G'
   
   because it was more specific.

   Let's override the adapter in L2:

   >>> ra112 = AdapterRegistration(required=IF1, provided=IB1, factory='A112',
   ...                             registry=L2)
   >>> ra112.status = interfaces.registration.ActiveStatus

   Now, in L2, we get the new adapter, because it's as specific and more
   local than the one from G:

   >>> L2.lookup([IF2], IB1)
   'A112'
   
   But we still get the old one in L1

   >>> L1.lookup([IF2], IB1)
   'A11G'
   
   Note that we can ask for less specific interfaces and still get the adapter:

   >>> L2.lookup([IF2], IB0)
   'A112'

   >>> L1.lookup([IF2], IB0)
   'A11G'

   We get the more specific adapter even if there is a less-specific
   adapter to B0:

   >>> G.register([IF1], IB1, '', 'A10G')

   >>> L2.lookup([IF2], IB0)
   'A112'

   But if we have an equally specific and equally local adapter to B0, it
   will win:

   >>> ra102 = AdapterRegistration(required=IF1, provided=IB0, factory='A102',
   ...                             registry=L2)
   >>> ra102.status = interfaces.registration.ActiveStatus

   >>> L2.lookup([IF2], IB0)
   'A102'

   We can deactivate registrations, which has the effect of deleting adapters:


   >>> ra112.status = interfaces.registration.InactiveStatus

   >>> L2.lookup([IF2], IB0)
   'A102'

   >>> L2.lookup([IF2], IB1)
   'A10G'

   >>> ra102.status = interfaces.registration.InactiveStatus

   >>> L2.lookup([IF2], IB0)
   'A10G'

   We can ask for all of the registrations :

   >>> L1.registrations() #doctest: +NORMALIZE_WHITESPACE
   (<AdapterRegistration:
        required=<InterfaceClass zope.app.component.tests.test_adapter.IF0>,
        with=(),
        provided=<InterfaceClass zope.app.component.tests.test_adapter.IB1>,
        name='',
        component='A011',
        permission=None>,)

   This shows only the local registrations in L1.
   """

def test_named_adapters():
    """
    Suppose we have a global AdapterRegistry:

    >>> G = AdapterRegistry()

    we also have a local adapter registry, with G as it's base:

    >>> L1 = LocalAdapterRegistry(G)

    and so on:

    >>> L2 = LocalAdapterRegistry(G, L1)

    Now, if we declare an adapter globally:

    >>> G.register([IF1], IB1, 'bob', 'A11G')

    we can query it locally:

    >>> L1.lookup([IF2], IB1)
    >>> L1.lookup([IF2], IB1, 'bob')
    'A11G'

    >>> L2.lookup([IF2], IB1)
    >>> L2.lookup([IF2], IB1, 'bob')
    'A11G'

    We can add local definitions:

    >>> ra011 = AdapterRegistration(required = IF0, provided=IB1,
    ...                             factory='A011', name='bob',
    ...                             registry=L1)
    >>> ra011.status = interfaces.registration.ActiveStatus

    and use it:

    >>> L1.lookup([IF0], IB1)
    >>> L1.lookup([IF0], IB1, 'bob')
    'A011'

    >>> L2.lookup([IF0], IB1)
    >>> L2.lookup([IF0], IB1, 'bob')
    'A011'

    but not outside L1:

    >>> G.lookup([IF0], IB1, 'bob')

    Note that it doesn't override the non-local adapter:

    >>> L1.lookup([IF2], IB1)
    >>> L1.lookup([IF2], IB1, 'bob')
    'A11G'

    >>> L2.lookup([IF2], IB1)
    >>> L2.lookup([IF2], IB1, 'bob')
    'A11G'

    because it was more specific.

    Let's override the adapter in L2:

    >>> ra112 = AdapterRegistration(required=IF1, provided=IB1,
    ...                             factory='A112', name='bob',
    ...                             registry=L2)
    >>> ra112.status = interfaces.registration.ActiveStatus

    Now, in L2, we get the new adapter, because it's as specific and more
    local than the one from G:

    >>> L2.lookup([IF2], IB1)
    >>> L2.lookup([IF2], IB1, 'bob')
    'A112'

    But we still get thye old one in L1

    >>> L1.lookup([IF2], IB1)
    >>> L1.lookup([IF2], IB1, 'bob')
    'A11G'

    Note that we can ask for less specific interfaces and still get the adapter:

    >>> L2.lookup([IF2], IB0)
    >>> L2.lookup([IF2], IB0, 'bob')
    'A112'

    >>> L1.lookup([IF2], IB0)
    >>> L1.lookup([IF2], IB0, 'bob')
    'A11G'

    We get the more specific adapter even if there is a less-specific
    adapter to B0:

    >>> G.register([IF1], IB1, 'bob', 'A10G')

    >>> L2.lookup([IF2], IB0)
    >>> L2.lookup([IF2], IB0, 'bob')
    'A112'

    But if we have an equally specific and equally local adapter to B0, it
    will win:

    >>> ra102 = AdapterRegistration(required = IF1, provided=IB0,
    ...                             factory='A102', name='bob',
    ...                             registry=L2)
    >>> ra102.status = interfaces.registration.ActiveStatus
    
    >>> L2.lookup([IF2], IB0)
    >>> L2.lookup([IF2], IB0, 'bob')
    'A102'

    We can deactivate registrations, which has the effect of deleting adapters:


    >>> ra112.status = interfaces.registration.InactiveStatus

    >>> L2.lookup([IF2], IB0)
    >>> L2.lookup([IF2], IB0, 'bob')
    'A102'

    >>> L2.lookup([IF2], IB1)
    >>> L2.lookup([IF2], IB1, 'bob')
    'A10G'

    >>> ra102.status = interfaces.registration.InactiveStatus

    >>> L2.lookup([IF2], IB0)
    >>> L2.lookup([IF2], IB0, 'bob')
    'A10G'
    """

def test_multi_adapters():
    """
    Suppose we have a global AdapterRegistry:

    >>> G = AdapterRegistry()

    we also have a local adapter registry, with G as it's base:

    >>> L1 = LocalAdapterRegistry(G)

    and so on:

    >>> L2 = LocalAdapterRegistry(G, L1)

    Now, if we declare an adapter globally:

    >>> G.register([IF1, IR0], IB1, 'bob', 'A11G')

    we can query it locally:

    >>> L1.lookup([IF2, IR1], IB1, 'bob')
    'A11G'

    >>> L2.lookup([IF2, IR1], IB1, 'bob')
    'A11G'

    We can add local definitions:

    >>> ra011 = AdapterRegistration(required=(IF0, IR0), provided=IB1,
    ...                             factory='A011', name='bob',
    ...                             registry=L1)
    >>> ra011.status = interfaces.registration.ActiveStatus
    
    and use it:

    >>> L1.lookup([IF0, IR1], IB1, 'bob')
    'A011'

    >>> L2.lookup([IF0, IR1], IB1, 'bob')
    'A011'

    but not outside L1:

    >>> G.lookup((IF0, IR1), IB1, 'bob')

    Note that it doesn't override the non-local adapter:

    >>> L1.lookup([IF2, IR1], IB1, 'bob')
    'A11G'

    >>> L2.lookup((IF2, IR1), IB1, 'bob')
    'A11G'

    because it was more specific.

    Let's override the adapter in L2:

    >>> ra112 = AdapterRegistration(required=(IF1, IR0), provided=IB1,
    ...                             factory='A112', name='bob',
    ...                             registry=L2)
    >>> ra112.status = interfaces.registration.ActiveStatus

    Now, in L2, we get the new adapter, because it's as specific and more
    local than the one from G:

    >>> L2.lookup((IF2, IR1), IB1, 'bob')
    'A112'

    But we still get the old one in L1

    >>> L1.lookup((IF2, IR1), IB1, 'bob')
    'A11G'

    Note that we can ask for less specific interfaces and still get
    the adapter:

    >>> L2.lookup((IF2, IR1), IB0, 'bob')
    'A112'

    >>> L1.lookup((IF2, IR1), IB0, 'bob')
    'A11G'

    We get the more specific adapter even if there is a less-specific
    adapter to B0:

    >>> G.register([IF1, IR0], IB1, 'bob', 'A10G')

    >>> L2.lookup((IF2, IR1), IB0, 'bob')
    'A112'

    But if we have an equally specific and equally local adapter to B0, it
    will win:

    >>> ra102 = AdapterRegistration(required=(IF1, IR0), provided=IB0,
    ...                             factory='A102', name='bob',
    ...                             registry=L2)
    >>> ra102.status = interfaces.registration.ActiveStatus
    
    >>> L2.lookup((IF2, IR1), IB0, 'bob')
    'A102'

    We can deactivate registrations, which has the effect of deleting adapters:

    >>> ra112.status = interfaces.registration.InactiveStatus

    >>> L2.lookup((IF2, IR1), IB0, 'bob')
    'A102'

    >>> L2.lookup((IF2, IR1), IB1, 'bob')
    'A10G'

    >>> ra102.status = interfaces.registration.InactiveStatus

    >>> L2.lookup([IF2], IB0)
    >>> L2.lookup((IF2, IR1), IB0, 'bob')
    'A10G'
    """

def test_persistence():
    """
    >>> db = DB()
    >>> conn1 = db.open()

    >>> G = globalAdapterRegistry
    >>> L1 = LocalAdapterRegistry(G)
    >>> L2 = LocalAdapterRegistry(G, L1)

    >>> conn1.root()['L1'] = L1
    >>> conn1.root()['L2'] = L2
    
    >>> G.register([IF1], IB1, 'bob', 'A11G')
    >>> L1.lookup([IF2], IB1)
    >>> L1.lookup([IF2], IB1, 'bob')
    'A11G'

    >>> L2.lookup([IF2], IB1)
    >>> L2.lookup([IF2], IB1, 'bob')
    'A11G'

    We can add local definitions:

    >>> ra011 = AdapterRegistration(required=IF0, provided=IB1,
    ...                             factory='A011', name='bob',
    ...                             registry=L1)
    >>> ra011.status = interfaces.registration.ActiveStatus

    and use it:

    >>> L1.lookup([IF0], IB1)
    >>> L1.lookup([IF0], IB1, 'bob')
    'A011'

    >>> L2.lookup([IF0], IB1)
    >>> L2.lookup([IF0], IB1, 'bob')
    'A011'

    but not outside L1:

    >>> G.lookup([IF0], IB1)

    Note that it doesn't override the non-local adapter:

    >>> L1.lookup([IF2], IB1)
    >>> L1.lookup([IF2], IB1, 'bob')
    'A11G'

    >>> L2.lookup([IF2], IB1)
    >>> L2.lookup([IF2], IB1, 'bob')
    'A11G'

    because it was more specific.

    Let's override the adapter in L2:

    >>> ra112 = AdapterRegistration(required=IF1, provided=IB1,
    ...                             factory='A112', name='bob',
    ...                             registry=L2)
    >>> ra112.status = interfaces.registration.ActiveStatus

    Now, in L2, we get the new adapter, because it's as specific and more
    local than the one from G:

    >>> L2.lookup([IF2], IB1)
    >>> L2.lookup([IF2], IB1, 'bob')
    'A112'

    But we still get the old one in L1

    >>> L1.lookup([IF2], IB1)
    >>> L1.lookup([IF2], IB1, 'bob')
    'A11G'

    Note that we can ask for less specific interfaces and still get
    the adapter:

    >>> L2.lookup([IF2], IB0)
    >>> L2.lookup([IF2], IB0, 'bob')
    'A112'

    >>> L1.lookup([IF2], IB0)
    >>> L1.lookup([IF2], IB0, 'bob')
    'A11G'

    We get the more specific adapter even if there is a less-specific
    adapter to B0:

    >>> G.register([IF0], IB0, 'bob', 'A00G')

    >>> L2.lookup([IF2], IB0)
    >>> L2.lookup([IF2], IB0, 'bob')
    'A112'

    But if we have an equally specific and equally local adapter to B0, it
    will win:

    >>> ra102 = AdapterRegistration(required=IF1, provided=IB0,
    ...                             factory='A102', name='bob',
    ...                             registry=L2)
    >>> ra102.status = interfaces.registration.ActiveStatus

    >>> L2.lookup([IF2], IB0)
    >>> L2.lookup([IF2], IB0, 'bob')
    'A102'

    >>> L1.lookup([IF2], IB0, 'bob')
    'A11G'
    >>> L1.lookup([IF2], IB1, 'bob')
    'A11G'
    >>> L2.lookup([IF2], IB0, 'bob')
    'A102'
    >>> L2.lookup([IF2], IB1, 'bob')
    'A112'

    >>> transaction.commit()

    Now, let's open another transaction:

    >>> conn2 = db.open()

    >>> L1 = conn2.root()['L1']
    >>> L2 = conn2.root()['L2']
    >>> ra112 = L2._registrations[0]
    >>> ra102 = L2._registrations[1]

    We should get the same outputs:

    >>> L1.lookup([IF2], IB0, 'bob')
    'A11G'
    >>> L1.lookup([IF2], IB1, 'bob')
    'A11G'
    >>> L2.lookup([IF2], IB0, 'bob')
    'A102'
    >>> L2.lookup([IF2], IB1, 'bob')
    'A112'
    
    We can deactivate registrations, which has the effect of deleting
    adapters:

    >>> ra112.status = interfaces.registration.InactiveStatus
    >>> ra102.status = interfaces.registration.InactiveStatus

    >>> L1.lookup([IF2], IB0, 'bob')
    'A11G'
    >>> L1.lookup([IF2], IB1, 'bob')
    'A11G'
    >>> L2.lookup([IF2], IB0, 'bob')
    'A11G'
    >>> L2.lookup([IF2], IB1, 'bob')
    'A11G'

    >>> transaction.commit()

    If we look back at the first connection, we should get the same data:

    >>> conn1.sync()
    >>> L1 = conn1.root()['L1']
    >>> L2 = conn1.root()['L2']

    We should see the result of the deactivations:
    
    >>> L1.lookup([IF2], IB0, 'bob')
    'A11G'
    >>> L1.lookup([IF2], IB1, 'bob')
    'A11G'
    >>> L2.lookup([IF2], IB0, 'bob')
    'A11G'
    >>> L2.lookup([IF2], IB1, 'bob')
    'A11G'

    Cleanup:
    >>> G.__init__()
    >>> db.close()
    """


def test_local_default():
    """
    >>> G = AdapterRegistry()
    >>> L1 = LocalAdapterRegistry(G)

    >>> r = AdapterRegistration(required=None, provided=IB1,
    ...                         factory='Adapter', registry=L1)
    >>> r.status = interfaces.registration.ActiveStatus
    >>> L1.lookup([IF2], IB1)
    'Adapter'
    """


def test_changing_next():
    """
    >>> G = AdapterRegistry()
    >>> L1 = LocalAdapterRegistry(G)
    >>> L2 = LocalAdapterRegistry(G, L1)
    >>> f2 = F2()

    >>> L2.lookup([IF2], IB1)

    >>> G.register([IF1], IB1, '', 'A11G')
    >>> L2.lookup([IF2], IB1)
    'A11G'


    >>> ra111 = AdapterRegistration(required=IF1, provided=IB1,
    ...                             factory='A111', registry=L1)
    >>> ra111.status = interfaces.registration.ActiveStatus
    >>> L2.lookup([IF2], IB1)
    'A111'

    >>> L1.next
    >>> L2.next == L1
    True
    >>> L1.subs == (L2,)
    True
    >>> L3 = LocalAdapterRegistry(G, L1)
    >>> L2.setNext(L3)
    >>> L2.next == L3
    True
    >>> L3.next == L1
    True
    >>> L1.subs == (L3,)
    True
    >>> L3.subs == (L2,)
    True

    >>> ra113 = AdapterRegistration(required=IF1, provided=IB1,
    ...                             factory='A113', registry=L3)
    >>> ra113.status = interfaces.registration.ActiveStatus

    >>> L2.lookup([IF2], IB1)
    'A113'
    >>> L2.setNext(L1)
    >>> L2.next == L1
    True
    >>> L3.next == L1
    True
    >>> L1.subs == (L3, L2)
    True
    >>> L3.subs == ()
    True
    >>> L2.lookup([IF2], IB1)
    'A111'

    """

def setUp(test):
    placelesssetup.setUp(test)
    setup.setUpAnnotations()
    setup.setUpDependable()
    setup.setUpTraversal()

def test_suite():
    return unittest.TestSuite((
        doctest.DocTestSuite(),
        doctest.DocFileSuite('../adapterregistry.txt',
                             setUp=setUp, tearDown=placelesssetup.tearDown),
        ))

if __name__ == "__main__":
    unittest.main(defaultTest='test_suite')
    

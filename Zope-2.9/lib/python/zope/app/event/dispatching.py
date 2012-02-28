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
"""Implement zope-specific event dispatching, based on subscription adapters

This package installs an event dispatcher that calls event handlers,
registered as subscription adapters providing ``None``.

So, to subscribe to an event, use a subscription adapter to ``None``:

  >>> from zope.app.testing.placelesssetup import setUp, tearDown
  >>> setUp()

  >>> class E1(object):
  ...     pass

  >>> class E2(E1):
  ...     pass

  >>> called = []
  >>> def handler1(event):
  ...     called.append(1)

  >>> def handler2(event):
  ...     called.append(2)

  >>> from zope.app.testing import ztapi
  >>> from zope.interface import implementedBy
  >>> ztapi.subscribe([implementedBy(E1)], None, handler1) # old way
  >>> ztapi.subscribe((E2,), None, handler2) # new way

  >>> from zope.event import notify

  >>> notify(E1())
  >>> called
  [1]

  >>> del called[:]
  >>> notify(E2())
  >>> called.sort()
  >>> called
  [1, 2]
  
  >>> tearDown()

$Id: dispatching.py 30927 2005-06-25 16:58:29Z philikon $
"""
__docformat__ = 'restructuredtext'

from warnings import warn
from zope.component import subscribers
import zope.event

def dispatch(*event):
    # iterating over subscribers assures they get executed
    for ignored in subscribers(event, None):
        pass

zope.event.subscribers.append(dispatch)

def publish(context, event):
    warn("Use zope.event.notify rather than zope.app.event.publish",
         DeprecationWarning, 2)
    zope.event.notify(event)

##############################################################################
#
# Copyright (c) 2002 Zope Corporation and Contributors.
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
"""Unit test logic for setting up and tearing down basic infrastructure

$Id: placelesssetup.py 30927 2005-06-25 16:58:29Z philikon $
"""

from zope.app.event.interfaces import IObjectEvent
from zope.app.event.objectevent import objectEventNotify
from zope.app.testing import ztapi

events = []

def getEvents(event_type=None, filter=None):
    r = []
    for event in events:
        if event_type is not None and not event_type.providedBy(event):
            continue
        if filter is not None and not filter(event):
            continue
        r.append(event)

    return r

def clearEvents():
    del events[:]

class PlacelessSetup(object):

    def setUp(self):
        clearEvents()
        ztapi.subscribe([None], None, events.append)
        ztapi.subscribe([IObjectEvent], None, objectEventNotify)

import zope.testing.cleanup
zope.testing.cleanup.addCleanUp(clearEvents)

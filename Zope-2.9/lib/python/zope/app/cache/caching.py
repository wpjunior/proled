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
"""Helpers for caching.

$Id: caching.py 26617 2004-07-19 03:25:41Z pruggera $
"""
__docformat__ = 'restructuredtext'

from zope.app import zapi
from zope.app.cache.interfaces import ICacheable, ICache
from zope.component import ComponentLookupError

def getCacheForObject(obj):
    """Returns the cache associated with `obj` or ``None``."""
    adapter = ICacheable(obj, None)
    if adapter is None:
        return None
    cache_id = adapter.getCacheId()
    if not cache_id:
        return None
    return zapi.getUtility(ICache, cache_id)

def getLocationForCache(obj):
    """Returns the location to be used for caching the object or ``None``."""
    try:
        return zapi.getPath(obj)
    except (ComponentLookupError, TypeError):
        return None

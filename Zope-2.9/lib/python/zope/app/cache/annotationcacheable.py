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
"""An adapter of annotatable objects.

$Id: annotationcacheable.py 26617 2004-07-19 03:25:41Z pruggera $
"""
__docformat__ = 'restructuredtext'

from zope.interface import implements
from zope.proxy import removeAllProxies

from zope.app import zapi
from zope.app.annotation.interfaces import IAnnotations
from zope.app.cache.interfaces import ICacheable, ICache

annotation_key = 'zope.app.cache.CacheManager'

class AnnotationCacheable(object):
    """Stores cache information in object's annotations."""

    implements(ICacheable)

    def __init__(self, context):
        self._context = context

    def getCacheId(self):
        annotations = IAnnotations(self._context)
        return annotations.get(annotation_key, None)

    def setCacheId(self, id):
        # Remove object from old cache
        old_cache_id = self.getCacheId()
        if old_cache_id and old_cache_id != id:
            cache = zapi.getUtility(ICache, old_cache_id)
            cache.invalidate(self._context)
        annotations = IAnnotations(removeAllProxies(self._context))
        annotations[annotation_key] = id

    cacheId = property(getCacheId, setCacheId, None, "Associated cache name")

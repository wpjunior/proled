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
"""RAM cache interface.

$Id: ram.py 29143 2005-02-14 22:43:16Z srichter $
"""
__docformat__ = 'restructuredtext'

from zope.interface import Attribute

from zope.app.cache.interfaces import ICache
from zope.app.component.interfaces.registration import IRegisterable

class IRAMCache(ICache, IRegisterable):
    """Interface for the RAM Cache."""

    maxEntries = Attribute("""A maximum number of cached values.""")

    maxAge = Attribute("""Maximum age for cached values in seconds.""")

    cleanupInterval = Attribute("""An interval between cache cleanups
    in seconds.""")

    def getStatistics():
        """Reports on the contents of a cache.

        The returned value is a sequence of dictionaries with the
        following keys:

          `path`, `hits`, `misses`, `size`, `entries`
        """

    def update(maxEntries, maxAge, cleanupInterval):
        """Saves the parameters available to the user"""

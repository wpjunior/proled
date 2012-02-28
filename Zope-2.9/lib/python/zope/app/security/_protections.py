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
# FOR A PARTICULAR PURPOSE
#
##############################################################################
"""Register protection information for some standard low-level types

$Id: _protections.py 39662 2005-10-27 02:26:46Z srichter $
"""

def protect():
    from zope.security.checker import NoProxy

    # BBB 2005/10/10 -- MessageIDs are to be removed for Zope 3.3
    import zope.deprecation
    zope.deprecation.__show__.off()
    from zope.i18nmessageid import MessageID, Message
    zope.deprecation.__show__.on()

    # Add message id types to the basic types, so their setting cannot be
    # overridden, once set. `protect()` was not guranteed to run after
    # zope.security.checker._clear, so that sometimes the proxies were not set.
    # This is not the ideal solution, but it is effective.

    # Make sure the message id gets never proxied
    # TODO because MessageIDs are mutable, this is a security hole.  This hole
    # is one of the primary reasons for the development of the Message
    # replacement.  See zope/i18nmessageid/messages.txt.
    zope.security.checker.BasicTypes[MessageID] = NoProxy
    # this, however, is not a security hole, because Messages are immutable.
    zope.security.checker.BasicTypes[Message] = NoProxy

    # add __parent__ and __name__ to always available names
    import zope.security.checker
    for name in ['__name__', '__parent__']:
        if name not in zope.security.checker._available_by_default:
            zope.security.checker._available_by_default.append(name)


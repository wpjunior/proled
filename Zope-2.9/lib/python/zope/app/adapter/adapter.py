# Copyright (c) 2003 Zope Corporation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
##############################################################################
"""Local adapter service implementation.

$Id: adapter.py 27880 2004-10-10 09:27:16Z srichter $
"""
from persistent import Persistent
from zope.deprecation import deprecated

# Hopefully noone was using this yet.
class LocalAdapterService(Persistent):
    pass

deprecated('LocalAdapterService',
           'Services have been removed. Use site manager API. '
           'The reference will be gone in Zope 3.3.')

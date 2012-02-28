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
"""Customization of zope.i18n for the Zope application server

$Id: __init__.py 39525 2005-10-20 12:28:29Z philikon $
"""
__docformat__ = 'restructuredtext'

# BBB 2005/10/10 -- MessageIDs are to be removed for Zope 3.3
import zope.deprecation
zope.deprecation.__show__.off()
from zope.i18nmessageid import MessageIDFactory, MessageFactory
zope.deprecation.__show__.on()

# import one of these as _ to create i18n messages in the zope domain
ZopeMessageIDFactory = MessageIDFactory('zope')
ZopeMessageFactory = MessageFactory('zope')

zope.deprecation.deprecated('ZopeMessageIDFactory',
                            'Mutable i18n messages ("message ids") have been '
                            'deprecated in favour of immutable ones and will '
                            'be removed in Zope 3.3.  Please use '
                            'ZopeMessageFactory instead of '
                            'ZopeMessageIDFactory.')

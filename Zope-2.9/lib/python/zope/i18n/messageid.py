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
"""Provide a backwards compatible import location for i18n message
ids.  This module will be removed from Zope 3.3.

$Id: messageid.py 39527 2005-10-20 12:34:10Z philikon $
"""
##############################################################################
# BBB 2005/10/10 -- remove the whole module for Zope 3.3
#
import zope.deprecation
zope.deprecation.__show__.off()
from zope.i18nmessageid import MessageID, MessageIDFactory
from zope.i18nmessageid import Message, MessageFactory
zope.deprecation.__show__.on()

zope.deprecation.deprecated(
    ('MessageID', 'MessageIDFactory' 'Message', 'MessageFactory'),
    "The zope.i18n.messageid module as a backwards-compatible import "
    "location for i18n message ids has been deprecated and will be "
    "removed from Zope 3.3.  Please use Message and MessageFactory "
    "from the zope.i18nmessageid package instead."
    )
#
##############################################################################

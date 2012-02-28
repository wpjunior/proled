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
"""Folder interfaces

$Id: interfaces.py 30851 2005-06-18 17:02:06Z anguenot $
"""
__docformat__ = 'restructuredtext'

from zope.app.container.interfaces import IContainer
from zope.app.traversing.interfaces import IContainmentRoot
from zope.app.component.interfaces import IPossibleSite
from zope.app.annotation.interfaces import IAttributeAnnotatable

class IFolder(IContainer, IPossibleSite, IAttributeAnnotatable):
    """The standard Zope Folder object interface."""

class IRootFolder(IFolder, IContainmentRoot):
    """The standard Zope root Folder object interface."""

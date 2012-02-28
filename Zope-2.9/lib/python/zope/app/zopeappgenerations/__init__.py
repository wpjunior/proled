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
"""Zope Application Server Generations

$Id: __init__.py 39687 2005-10-28 10:14:24Z hdima $
"""
__docformat__ = "reStructuredText"
from zope.app.generations.generations import SchemaManager
from zope.app.publication.zopepublication import ZopePublication

key = 'zope.app.zopeappgenerations'


ZopeAppSchemaManager = SchemaManager(
    minimum_generation=0,
    generation=2,
    package_name=key)


def getRootFolder(context):
    return context.connection.root().get(ZopePublication.root_name, None)

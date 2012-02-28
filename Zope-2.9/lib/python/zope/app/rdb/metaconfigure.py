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
"""'rdb' ZCML Namespace Directive Handler

$Id: metaconfigure.py 29143 2005-02-14 22:43:16Z srichter $
"""
from zope.app import zapi
from zope.app.rdb.interfaces import IZopeDatabaseAdapter


def connectionhandler(_context, name, component, dsn):
    connection = component(dsn)
    _context.action(
            discriminator = ('provideConnection', name),
            callable = provideConnection,
            args = (name, connection) )
    
def provideConnection(name, connection):
    """ Registers a database connection
    
    Uses the global site manager for registering the connection
    """
    gsm = zapi.getGlobalSiteManager()
    gsm.provideUtility(IZopeDatabaseAdapter, connection, name)


    


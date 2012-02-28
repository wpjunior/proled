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
"""'rdb' ZCML Namespace Directives

$Id: metadirectives.py 25177 2004-06-02 13:17:31Z jim $
"""
from zope.configuration.fields import GlobalObject
from zope.interface import Interface
from zope.schema import TextLine

class IProvideConnectionDirective(Interface):
    """This directive creates a globale connection to an RDBMS."""

    name = TextLine(
        title=u"Name",
        description=u"This is the name the connection will be known as.",
        required=True)

    component = GlobalObject(
        title=u"Component",
        description=u"Specifies the component that provides the connection. "
                     "This component handles one particular RDBMS.",
        required=True)

    dsn = TextLine(
        title=u"DSN",
        description=u"The DSN contains all the connection information. The"\
                    u"syntax looks as follows: \n" \
                    u"dbi://username:password@host:port/dbname;param1=value...",
        default=u"dbi://localhost/testdb",
        required=True)

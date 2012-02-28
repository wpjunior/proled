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
"""Unauthorized Exception View Class

$Id: unauthorized.py 71681 2007-01-02 13:52:00Z adamg $
"""
__docformat__ = 'restructuredtext'

from zope.app import zapi


class Unauthorized(object):

    def issueChallenge(self):
        # Set the error status to 403 (Forbidden) in the case when we don't
        # challenge the user
        self.request.response.setStatus(403)

        # make sure that squid does not keep the response in the cache
        self.request.response.setHeader('Expires', 'Mon, 26 Jul 1997 05:00:00 GMT')
        self.request.response.setHeader('Cache-Control', 'no-store, no-cache, must-revalidate')
        self.request.response.setHeader('Pragma', 'no-cache')
        
        principal = self.request.principal
        auth = zapi.principals()
        auth.unauthorized(principal.id, self.request)

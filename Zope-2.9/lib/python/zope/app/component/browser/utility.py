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
"""Use-Registration view for utilities.

$Id: utility.py 28818 2005-01-12 22:10:50Z srichter $
"""
from zope.app.component.browser.registration import AddComponentRegistration
from zope.app.component.interfaces.registration import ActiveStatus

class AddRegistration(AddComponentRegistration):
    """View for adding a utility registration.

    We could just use AddComponentRegistration, except that we need a
    custom interface widget.

    This is a view on a local utility, configured by an <addform>
    directive.
    """
    def add(self, registration):
        reg = super(AddRegistration, self).add(registration)
        reg.status = ActiveStatus
        return reg

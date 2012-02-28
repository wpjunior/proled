##############################################################################
#
# Copyright (c) 2005 Zope Corporation and Contributors.
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
"""Site Management view code

$Id: site.py 39064 2005-10-11 18:40:10Z philikon $
"""

__docformat__ = "reStructuredText"

from zope.app import zapi
from zope.app.i18n import ZopeMessageFactory as _


class UtilityRegistrationDetails(object):
    """Utility Registration Details"""

    def provided(self):
        provided = self.context.provided
        return provided.__module__ + '.' + provided.__name__

    def name(self):
        return self.context.name or _('<no name>')

    def component(self):
        url = zapi.getMultiAdapter(
            (self.context.component, self.request), name='absolute_url')
        name = zapi.name(self.context.component)
        return {'url': url, 'name': name}

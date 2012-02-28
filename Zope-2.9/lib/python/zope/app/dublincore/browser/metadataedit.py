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
"""Dublin Core Meta Data View

$Id: metadataedit.py 39064 2005-10-11 18:40:10Z philikon $
"""
__docformat__ = 'restructuredtext'

from datetime import datetime
from zope.event import notify
from zope.app.event.objectevent import ObjectModifiedEvent
from zope.app.event.objectevent import Attributes
from zope.app.i18n import ZopeMessageFactory as _
from zope.app.dublincore.interfaces import IZopeDublinCore


class MetaDataEdit(object):
    """Provide view for editing basic dublin-core meta-data."""

    def edit(self):
        request = self.request
        formatter = self.request.locale.dates.getFormatter('dateTime', 'medium')
        dc = IZopeDublinCore(self.context)
        message=''

        if 'dctitle' in request:
            dc.title = unicode(request['dctitle'])
            dc.description = unicode(request['dcdescription'])
            description = Attributes(IZopeDublinCore, 'title', 'description')
            notify(ObjectModifiedEvent(self.context, description))
            message = _("Changed data ${datetime}",
                        mapping={'datetime': formatter.format(datetime.utcnow())})

        return {
            'message': message,
            'dctitle': dc.title,
            'dcdescription': dc.description,
            'modified': (dc.modified or dc.created) and \
                        formatter.format(dc.modified or dc.created) or '',
            'created': dc.created and formatter.format(dc.created) or '',
            'creators': dc.creators
            }

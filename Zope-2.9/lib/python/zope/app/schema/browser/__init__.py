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
"""Mutable Schema (as Utility) Views

$Id: __init__.py 40422 2005-11-30 05:00:44Z fdrake $
"""
from zope.app import zapi
from zope.app.form.browser.editview import EditView
from zope.app.form.utility import setUpEditWidgets
from zope.app.i18n import ZopeMessageFactory as _
from zope.app.schema.interfaces import IMutableSchema
from zope.app.pagetemplate.viewpagetemplatefile import ViewPageTemplateFile
from zope.app.publisher.browser import BrowserView
from zope.schema import getFieldNamesInOrder, getFieldsInOrder


_msg_anErrorOccurred = _("An error occurred")

class EditSchema(BrowserView):

    edit = ViewPageTemplateFile('schema_edit.pt')
    errors = ()
    update_status = None

    def name(self):
        return self.context.getName()

    def fieldNames(self):
        return getFieldNamesInOrder(self.context)

    def fields(self):
        return [{'name': name,
                 'field': field,
                 'type': field.__class__.__name__}
                for name, field in getFieldsInOrder(self.context)]

    def update(self):
        status = ''
        container = IMutableSchema(self.context)
        request = self.request

        if 'DELETE' in request:
            if not 'ids' in request:
                self.errors = (_("Must select a field to delete"),)
                status = _msg_anErrorOccurred
            for id in request.get('ids', []):
                del container[id]
        elif 'MOVE_UP' in request or 'MOVE_DOWN' in request:
            up = request.get('MOVE_UP')
            down = request.get('MOVE_DOWN')
            name = up or down
            delta = up and -1 or 1
            names = self.fieldNames()
            if name not in names:
                #TODO variable insertion must not be expanded until
                # after the translation... preferably use mapping here
                self.errors = (_("Invalid field name: %s" % name),)
                status = _msg_anErrorOccurred
            p = names.index(name) + delta
            try:
                self.context.moveField(name, p)
            except IndexError:
                #TODO variable insertion must not be expanded until
                # after the translation... preferably use mapping here
                self.errors = (_("Invalid position: %s" % p),)
                status = _msg_anErrorOccurred
        self.update_status = status
        return status


class EditMutableSchema(EditView):

    def _get_schema(self):
        return self.context.mutableschema

    schema = property(_get_schema)

    def _setUpWidgets(self):
        adapted = self.schema(self.context)
        if adapted is not self.context:
            adapted.__parent__ = self.context
        setUpEditWidgets(self, self.schema, source=self.adapted,
                         names=self.fieldNames)

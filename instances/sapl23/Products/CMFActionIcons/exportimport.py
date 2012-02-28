##############################################################################
#
# Copyright (c) 2005 Zope Corporation and Contributors. All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""ActionIconsTool setup handlers.

$Id: exportimport.py 41534 2006-02-01 16:46:01Z efge $
"""
import os

from AccessControl import ClassSecurityInfo
from AccessControl.Permission import Permission
from Globals import InitializeClass
from Globals import package_home
from Products.PageTemplates.PageTemplateFile import PageTemplateFile

from Products.CMFCore.utils import getToolByName

from Products.GenericSetup.utils import CONVERTER
from Products.GenericSetup.utils import DEFAULT
from Products.GenericSetup.utils import ExportConfiguratorBase
from Products.GenericSetup.utils import ImportConfiguratorBase
from Products.GenericSetup.utils import KEY

from permissions import ManagePortal

_pkgdir = package_home( globals() )
_xmldir = os.path.join( _pkgdir, 'xml' )

#
#   Configurator entry points
#
_FILENAME = 'actionicons.xml'

def importActionIconsTool(context):
    """ Import cache policy maanger settings from an XML file.
    """
    site = context.getSite()
    ait = getToolByName(site, 'portal_actionicons', None)
    if ait is None:
        return 'Action icons: No tool!'

    body = context.readDataFile(_FILENAME)
    if body is None:
        return 'Action icons: Nothing to import.'

    if context.shouldPurge():
        ait.clearActionIcons()

    # now act on the settings we've retrieved
    configurator = ActionIconsToolImportConfigurator(site, 'utf-8')
    ait_info = configurator.parseXML(body)

    for action_icon in ait_info['action_icons']:
        category = action_icon['category']
        action_id = action_icon['action_id']
        if ait.queryActionInfo(category, action_id) is not None:
            ait.updateActionIcon(**action_icon)
        else:
            ait.addActionIcon(**action_icon)

    return 'Action icons settings imported.'

def exportActionIconsTool(context):
    """ Export caching policy manager settings as an XML file.
    """
    site = context.getSite()
    mhc = ActionIconsToolExportConfigurator( site ).__of__( site )
    text = mhc.generateXML()

    context.writeDataFile( _FILENAME, text, 'text/xml' )

    return 'Action icons tool settings exported.'


class ActionIconsToolExportConfigurator(ExportConfiguratorBase):
    """ Synthesize XML description of cc properties.
    """
    security = ClassSecurityInfo()

    security.declareProtected( ManagePortal, 'listActionIconInfo' )
    def listActionIconInfo(self):
        """ Return a list of mappings describing the action icons.
        """
        ait = getToolByName(self._site, 'portal_actionicons')
        for action_icon in ait.listActionIcons():
            yield {'category': action_icon.getCategory(),
                   'action_id': action_icon.getActionId(),
                   'title': action_icon.getTitle(),
                   'priority': action_icon.getPriority(),
                   'icon_expr': action_icon.getExpression(),
                  }

    security.declarePrivate('_getExportTemplate')
    def _getExportTemplate(self):

        return PageTemplateFile('aitExport.xml', _xmldir)

InitializeClass(ActionIconsToolExportConfigurator)


class ActionIconsToolImportConfigurator(ImportConfiguratorBase):

    def _getImportMapping(self):
        return {
          'action-icons':
             { 'action-icon': {KEY: 'action_icons', DEFAULT: ()} },
          'action-icon':
             { 'category':      {},
               'action_id':     {},
               'title':         {},
               'icon_expr':     {},
               'priority':      {CONVERTER: self._convertToInteger},
             },
          }

    def _convertToInteger(self, val):
        return int(val.strip())

InitializeClass(ActionIconsToolImportConfigurator)

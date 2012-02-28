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
"""Tools View

$Id: tools.py 40070 2005-11-12 18:01:00Z jukart $
"""
import zope.interface
import zope.event

from zope.app import zapi
from zope.app.component import site, interfaces, browser
from zope.app.event import objectevent
from zope.app.exception.interfaces import UserError

from zope.app.i18n import ZopeMessageFactory as _


class IToolType(zope.interface.interfaces.IInterface):
    """Interfaces implementing the tool type are considered tools."""


class IToolConfiguration(zope.interface.Interface):
    """This is an object that represents a tool configuration"""

    #title
    #
    #description
    #
    #interface
    #
    #unique


class ToolConfiguration(object):
    """ """
    zope.interface.implements(IToolConfiguration)

    def __init__(self, interface, title, description=None, unique=False,
                 folder='tools'):
        self.interface = interface
        self.title = title
        self.description = description
        self.unique = unique
        self.folder = folder


class SiteManagementView(browser.ComponentAdding):
    """A Site Management via Tools"""

    activeTool = None
    addTool = False
    addName = u''
    renameTool = False
    renameList = []
    newNames = []
    msg = u''

    def __init__(self, context, request):
        super(SiteManagementView, self).__init__(context, request)
        if 'activeTool' in request:
            request.response.setCookie('SetActiveTool', request['activeTool'],
                                       path="/")
            self.activeTool = zapi.getUtility(IToolConfiguration,
                                              request['activeTool'])
        elif 'SetActiveTool' in request:
            self.activeTool = zapi.getUtility(IToolConfiguration,
                                              request['SetActiveTool'])

    def update(self):
        """ """
        msg = u''
        if "INSTALL-SUBMIT" in self.request:
            self.install()
            msg = _(u'Tools successfully installed.')
        if "UNINSTALL-SUBMIT" in self.request:
            self.uninstall()
            msg = _(u'Tools successfully uninstalled.')
        if "ADD-TOOL-SUBMIT" in self.request:
            try:
                self.action(self.request['type_name'], self.request['id'])
            except UserError, err:
                self.addTool = True
                self.addName = self.contentName
                msg=err
        elif "CANCEL-ADD-TOOL-SUBMIT" in self.request:
            self.request.response.expireCookie('SetActiveTool')
            self.activeTool = None
        elif "ACTIVATE-SUBMIT" in self.request:
            self.changeStatus(interfaces.registration.ActiveStatus)
            msg = _(u'Tools successfully activated.')
        elif "DEACTIVATE-SUBMIT" in self.request:
            self.changeStatus(interfaces.registration.InactiveStatus)
            msg = _(u'Tools successfully deactivated.')
        elif "ADD-SUBMIT" in self.request:
            self.addTool = True
        elif "DELETE-SUBMIT" in self.request:
            if 'selected' in self.request:
                self.delete()
                msg = _(u'Tools successfully deleted.')
            else:
                msg = _(u'No tools selected.')
        elif "RENAME-SUBMIT" in self.request:
            if 'selected' in self.request:
                self.renameList = self.request['selected']
            if 'new_names' in self.request:
                self.renameList = self.request['old_names']
                self.newNames = self.request['new_names']
                try:
                    self.rename()
                except UserError, err:
                    msg=err
                else:
                    msg = _(u'Tools successfully renamed.')
        elif "RENAME-CANCEL-SUBMIT" in self.request:
            self.activeTool = None
        self.msg=msg
        return msg

    def getSiteManagementFolder(self, tool):
        """Get the site management folder for this tool."""
        sm = zapi.getSiteManager()
        if not tool.folder in sm:
            folder = site.SiteManagementFolder()
            zope.event.notify(objectevent.ObjectCreatedEvent(folder))
            sm[tool.folder] = folder
        return sm[tool.folder]

    def toolExists(self, interface, name=''):
        """Check whether a tool already exists in this site"""
        sm = zapi.getSiteManager()
        for reg in sm.registrations():
            if isinstance(reg, site.UtilityRegistration):
                if reg.name == name and reg.provided == interface:
                    return True
        return False

    def getUniqueTools(self):
        """Get unique tools info for display."""
        results = [{'name': tool.interface.getName(),
                    'title': tool.title,
                    'description': tool.description,
                    'exists': self.toolExists(tool.interface)
                    }
                   for name, tool in zapi.getUtilitiesFor(IToolConfiguration)
                   if tool.unique]
        results.sort(lambda x, y: cmp(x['title'], y['title']))
        return results

    def getToolInstances(self, tool):
        """Find every registered utility for a given tool configuration."""
        regManager = self.getSiteManagementFolder(tool).registrationManager
        return [
            {'name': reg.name,
             'url': zapi.absoluteURL(reg.component, self.request),
             'rename': tool is self.activeTool and reg.name in self.renameList,
             'renameNew': tool is self.activeTool and \
                          reg.name in self.renameList and \
                          self.newNames and \
                          self.newNames[self.renameList.index(reg.name)],
             'active': reg.status == u'Active',
            }
            for reg in regManager.values()
            if (zapi.isinstance(reg, site.UtilityRegistration) and
                reg.provided.isOrExtends(tool.interface))]

    def getTools(self):
        """Return a list of all tools"""
        results = [{'name': tool.interface.getName(),
                    'title': tool.title,
                    'description': tool.description,
                    'instances': self.getToolInstances(tool),
                    'add': tool is self.activeTool and self.addTool,
                    'addname': tool is self.activeTool and self.addTool and self.addName,
                    'rename': tool is self.activeTool and self.renameList,
                    'message': tool is self.activeTool and self.msg,
                    }
                   for name, tool in zapi.getUtilitiesFor(IToolConfiguration)
                   if not tool.unique]
        results.sort(lambda x, y: cmp(x['title'], y['title']))
        return results

    def install(self):
        tool_names = self.request['selected']
        for tool_name in tool_names:
            self.activeTool = zapi.getUtility(IToolConfiguration, tool_name)
            type_name = list(self.addingInfo())[0]['extra']['factory']
            self.action(type_name)
        self.activeTool = None

    def uninstall(self):
        type_names = self.request['selected']
        self.request.form['selected'] = [u'']
        for name, tool in zapi.getUtilitiesFor(IToolConfiguration):
            if name in type_names:
                self.activeTool = tool
                self.delete()
        self.activeTool = None

    def changeStatus(self, status):
        tool = self.activeTool
        regManager = self.context[tool.folder].registrationManager
        names = self.request.form['selected']
        for reg in regManager.values():
            if reg.provided.isOrExtends(tool.interface) and reg.name in names:
                reg.status = status

    def delete(self):
        tool = self.activeTool
        regManager = self.context[tool.folder].registrationManager
        names = self.request.form['selected']
        for reg in list(regManager.values()):
            if reg.provided.isOrExtends(tool.interface) and reg.name in names:
                component = reg.component
                reg.status = interfaces.registration.InactiveStatus
                del regManager[zapi.name(reg)]
                del zapi.getParent(component)[zapi.name(component)]

    def rename(self):
        tool = self.activeTool
        regManager = self.context[tool.folder].registrationManager
        new_names = self.request['new_names']
        old_names = self.request['old_names']
        msg=''
        for reg in regManager.values():
            if reg.provided.isOrExtends(tool.interface) and \
                   reg.name in old_names:
                old_name=reg.name
                new_name = new_names[old_names.index(old_name)]
                if new_name!=reg.name:
                    if self.toolExists(self.activeTool.interface,new_name):
                        if not msg:
                            msg=_(u'The given tool name is already being used.')
                    else:
                        orig_status = reg.status
                        reg.status = interfaces.registration.InactiveStatus
                        reg.name = new_names[old_names.index(old_name)]
                        reg.status = orig_status
                        self.renameList.remove(old_name)
                        self.newNames.remove(new_name)
                else:
                    self.renameList.remove(old_name)
                    self.newNames.remove(new_name)
        if msg:
            raise UserError(msg)

    def add(self, content):
        """See zope.app.container.interfaces.IAdding"""

        name = self.contentName
        if self.toolExists(self.activeTool.interface,name):
            raise UserError(_(u'The given tool name is already being used.'))
        
        sm = self.context

        self.context = self.getSiteManagementFolder(self.activeTool)

        self.contentName = '' # always use a unique name
        util = super(SiteManagementView, self).add(content)
        self.contentName = name

        # Add registration
        name = not self.activeTool.unique and self.contentName or u''
        registration = site.UtilityRegistration(
            name, self.activeTool.interface, util)
        self.context.registrationManager.addRegistration(registration)
        registration.status = interfaces.registration.ActiveStatus

        self.context = sm
        return util

    def nextURL(self):
        """See zope.app.container.interfaces.IAdding"""
        return (zapi.absoluteURL(self.context, self.request)
                + '/@@SiteManagement')

    def addingInfo(self):
        """See zope.app.container.interfaces.IAdding"""
        sm = self.context
        self.context = self.getSiteManagementFolder(self.activeTool)
        self._addFilterInterface = self.activeTool.interface
        results = super(SiteManagementView, self).addingInfo()
        self.context = sm
        self._addFilterInterface = None
        return results

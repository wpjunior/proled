##############################################################################
#
# Copyright (c) 2001 Zope Corporation and Contributors. All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
""" Portal class

$Id: Portal.py 40364 2005-11-24 18:23:00Z yuppie $
"""

from Globals import HTMLFile
from Globals import InitializeClass

from Products.CMFCore.PortalObject import PortalObjectBase
from Products.CMFCore import PortalFolder
from Products.CMFCore.TypesTool import FactoryTypeInformation
from Products.CMFCore.utils import getToolByName

from DublinCore import DefaultDublinCoreImpl
from permissions import AccessFuturePortalContent
from permissions import AddPortalContent
from permissions import AddPortalFolders
from permissions import DeleteObjects
from permissions import FTPAccess
from permissions import ListPortalMembers
from permissions import ListUndoableChanges
from permissions import ManagePortal
from permissions import ManageProperties
from permissions import ReplyToItem
from permissions import ReviewPortalContent
from permissions import SetOwnPassword
from permissions import SetOwnProperties
from permissions import UndoChanges
from permissions import View
from permissions import ViewManagementScreens

import Document
import Image
import File
import Link
import NewsItem
import Favorite
import DiscussionItem
import SkinnedFolder

factory_type_information = ( Document.factory_type_information
                           + Image.factory_type_information
                           + File.factory_type_information
                           + Link.factory_type_information
                           + NewsItem.factory_type_information
                           + Favorite.factory_type_information
                           + DiscussionItem.factory_type_information
                           + SkinnedFolder.factory_type_information
                           )


class CMFSite ( PortalObjectBase
              , DefaultDublinCoreImpl
              ):
    """
        The *only* function this class should have is to help in the setup
        of a new CMFSite.  It should not assist in the functionality at all.
    """
    meta_type = 'CMF Site'

    _properties = (
        {'id':'title', 'type':'string', 'mode': 'w'},
        {'id':'description', 'type':'text', 'mode': 'w'},
        )
    title = ''
    description = ''

    __ac_permissions__=( ( AddPortalContent, () )
                       , ( AddPortalFolders, () )
                       , ( ListPortalMembers, () )
                       , ( ReplyToItem, () )
                       , ( View, ('isEffective',) )
                       )

    def __init__( self, id, title='' ):
        PortalObjectBase.__init__( self, id, title )
        DefaultDublinCoreImpl.__init__( self )

    def isEffective( self, date ):
        """
            Override DefaultDublinCoreImpl's test, since we are always viewable.
        """
        return 1

    def reindexObject( self, idxs=[] ):
        """
            Override DefaultDublinCoreImpl's method (so that we can play
            in 'editMetadata').
        """
        pass

InitializeClass(CMFSite)


class PortalGenerator:

    klass = CMFSite

    def setupTools(self, p):
        """Set up initial tools"""

        addCMFCoreTool = p.manage_addProduct['CMFCore'].manage_addTool
        addCMFCoreTool('CMF Actions Tool', None)
        addCMFCoreTool('CMF Catalog', None)
        addCMFCoreTool('CMF Member Data Tool', None)
        addCMFCoreTool('CMF Skins Tool', None)
        addCMFCoreTool('CMF Types Tool', None)
        addCMFCoreTool('CMF Undo Tool', None)
        addCMFCoreTool('CMF URL Tool', None)
        addCMFCoreTool('CMF Workflow Tool', None)

        addCMFDefaultTool = p.manage_addProduct['CMFDefault'].manage_addTool
        addCMFDefaultTool('Default Discussion Tool', None)
        addCMFDefaultTool('Default Membership Tool', None)
        addCMFDefaultTool('Default Registration Tool', None)
        addCMFDefaultTool('Default Properties Tool', None)
        addCMFDefaultTool('Default Metadata Tool', None)
        addCMFDefaultTool('Default Syndication Tool', None)

        # try to install CMFUid without raising exceptions if not available
        try:
            addCMFUidTool = p.manage_addProduct['CMFUid'].manage_addTool
        except AttributeError:
            pass
        else:
            addCMFUidTool('Unique Id Annotation Tool', None)
            addCMFUidTool('Unique Id Generator Tool', None)
            addCMFUidTool('Unique Id Handler Tool', None)

    def setupMailHost(self, p):
        p.manage_addProduct['MailHost'].manage_addMailHost(
            'MailHost', smtp_host='localhost')

    def setupUserFolder(self, p):
        p.manage_addProduct['OFSP'].manage_addUserFolder()

    def setupCookieAuth(self, p):
        p.manage_addProduct['CMFCore'].manage_addCC(
            id='cookie_authentication')

    def setupMembersFolder(self, p):
        PortalFolder.manage_addPortalFolder(p, 'Members')
        p.Members.manage_addProduct['OFSP'].manage_addDTMLMethod(
            'index_html', 'Member list', '<dtml-return roster>')

    def setupRoles(self, p):
        # Set up the suggested roles.
        p.__ac_roles__ = ('Member', 'Reviewer',)

    def setupPermissions(self, p):
        # Set up some suggested role to permission mappings.
        mp = p.manage_permission

        mp(AccessFuturePortalContent, ['Reviewer','Manager',], 1)
        mp(AddPortalContent,          ['Owner','Manager',],    1)
        mp(AddPortalFolders,          ['Owner','Manager',],    1)
        mp(ListPortalMembers,         ['Member','Manager',],   1)
        mp(ListUndoableChanges,       ['Member','Manager',],   1)
        mp(ReplyToItem,               ['Member','Manager',],   1)
        mp(ReviewPortalContent,       ['Reviewer','Manager',], 1)
        mp(SetOwnPassword,            ['Member','Manager',],   1)
        mp(SetOwnProperties,          ['Member','Manager',],   1)

        # Add some other permissions mappings that may be helpful.
        mp(DeleteObjects,             ['Owner','Manager',],    1)
        mp(FTPAccess,                 ['Owner','Manager',],    1)
        mp(ManageProperties,          ['Owner','Manager',],    1)
        mp(UndoChanges,               ['Owner','Manager',],    1)
        mp(ViewManagementScreens,     ['Owner','Manager',],    1)

    def setupDefaultSkins(self, p):
        from Products.CMFCore.DirectoryView import addDirectoryViews
        from Products.CMFTopic import topic_globals
        ps = getToolByName(p, 'portal_skins')
        addDirectoryViews(ps, 'skins', globals())
        addDirectoryViews(ps, 'skins', topic_globals)
        ps.manage_addProduct['OFSP'].manage_addFolder(id='custom')
        ps.addSkinSelection('Basic',
            'custom, zpt_topic, zpt_content, zpt_generic,'
            + 'zpt_control, Images',
            make_default=1)
        ps.addSkinSelection('Nouvelle',
            'nouvelle, custom, topic, content, generic, control, Images')
        ps.addSkinSelection('No CSS',
            'no_css, custom, topic, content, generic, control, Images')
        p.setupCurrentSkin()

    def setupTypes(self, p, initial_types=factory_type_information):
        tool = getToolByName(p, 'portal_types', None)
        if tool is None:
            return
        for t in initial_types:
            fti = FactoryTypeInformation(**t)
            tool._setObject(t['id'], fti)

    def setupMimetypes(self, p):
        p.manage_addProduct[ 'CMFCore' ].manage_addRegistry()
        reg = p.content_type_registry

        reg.addPredicate( 'link', 'extension' )
        reg.getPredicate( 'link' ).edit( extensions="url, link" )
        reg.assignTypeName( 'link', 'Link' )

        reg.addPredicate( 'news', 'extension' )
        reg.getPredicate( 'news' ).edit( extensions="news" )
        reg.assignTypeName( 'news', 'News Item' )

        reg.addPredicate( 'document', 'major_minor' )
        reg.getPredicate( 'document' ).edit( major="text", minor="" )
        reg.assignTypeName( 'document', 'Document' )

        reg.addPredicate( 'image', 'major_minor' )
        reg.getPredicate( 'image' ).edit( major="image", minor="" )
        reg.assignTypeName( 'image', 'Image' )

        reg.addPredicate( 'file', 'major_minor' )
        reg.getPredicate( 'file' ).edit( major="application", minor="" )
        reg.assignTypeName( 'file', 'File' )

    def setupWorkflow(self, p):
        wftool = getToolByName(p, 'portal_workflow', None)
        if wftool is None:
            return
        try:
            from Products.DCWorkflow.Default \
                    import createDefaultWorkflowClassic
        except ImportError:
            return
        id = 'default_workflow'
        wftool._setObject( id, createDefaultWorkflowClassic(id) )

        #   These objects don't participate in workflow by default.
        wftool.setChainForPortalTypes( ('Folder', 'Topic'), () )

    def setup(self, p, create_userfolder):
        from Products.CMFTopic import Topic
        self.setupTools(p)
        self.setupMailHost(p)
        if int(create_userfolder) != 0:
            self.setupUserFolder(p)
        self.setupCookieAuth(p)
        self.setupMembersFolder(p)
        self.setupRoles(p)
        self.setupPermissions(p)
        self.setupDefaultSkins(p)

        #   SkinnedFolders are only for customization;
        #   they aren't a default type.
        default_types = tuple( filter( lambda x: x['id'] != 'Skinned Folder'
                                     , factory_type_information ) )
        self.setupTypes(p, default_types )

        self.setupTypes(p, PortalFolder.factory_type_information)
        self.setupTypes(p, Topic.factory_type_information)
        self.setupMimetypes(p)
        self.setupWorkflow(p)

    def create(self, parent, id, create_userfolder):
        id = str(id)
        portal = self.klass(id=id)
        parent._setObject(id, portal)
        # Return the fully wrapped object.
        p = parent.this()._getOb(id)
        self.setup(p, create_userfolder)
        return p

    def setupDefaultProperties(self, p, title, description,
                               email_from_address, email_from_name,
                               validate_email, default_charset=''):
        p._setProperty('email_from_address', email_from_address, 'string')
        p._setProperty('email_from_name', email_from_name, 'string')
        p._setProperty('validate_email', validate_email and 1 or 0, 'boolean')
        p._setProperty('default_charset', default_charset, 'string')
        p._setProperty('enable_permalink', 0, 'boolean')
        p.title = title
        p.description = description


manage_addCMFSiteForm = HTMLFile('dtml/addPortal', globals())
manage_addCMFSiteForm.__name__ = 'addPortal'

def manage_addCMFSite(self, id, title='Portal', description='',
                         create_userfolder=1,
                         email_from_address='postmaster@localhost',
                         email_from_name='Portal Administrator',
                         validate_email=0, default_charset='',
                         RESPONSE=None):
    """ Adds a portal instance.
    """
    from warnings import warn

    warn("manage_addCMFSite is a deprecated way to create a CMF site;  in "
         "the future, please use 'CMFDefault.factory.addConfiguredSite'.  "
         "manage_addCMFSite will be removed in CMF 2.0.",
         DeprecationWarning, 2)

    gen = PortalGenerator()
    id = id.strip()
    p = gen.create(self, id, create_userfolder)
    gen.setupDefaultProperties(p, title, description,
                               email_from_address, email_from_name,
                               validate_email, default_charset)
    if RESPONSE is not None:
        RESPONSE.redirect(p.absolute_url() + '/finish_portal_construction')

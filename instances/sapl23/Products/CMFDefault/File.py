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
""" This module implements a portal-managed File class.  It is based on
Zope's built-in File object, but modifies the behaviour slightly to
make it more Portal-friendly.

$Id: File.py 70021 2006-09-07 10:16:08Z jens $
"""

from Globals import InitializeClass
from AccessControl import ClassSecurityInfo

from Products.CMFCore.PortalContent import PortalContent

from DublinCore import DefaultDublinCoreImpl
from permissions import View
from permissions import ModifyPortalContent

from zope.interface import implements
from Products.GenericSetup.interfaces import IDAVAware

factory_type_information = (
  { 'id'             : 'File'
  , 'meta_type'      : 'Portal File'
  , 'description'    : """\
File objects can contain arbitrary downloadable files.
"""
  , 'icon'           : 'file_icon.gif'
  , 'product'        : 'CMFDefault'
  , 'factory'        : 'addFile'
  , 'immediate_view' : 'metadata_edit_form'
  , 'aliases'        : {'(Default)':'index_html',
                        'view':'file_view'}
  , 'actions'        : ( { 'id'            : 'view'
                         , 'name'          : 'View'
                         , 'action': 'string:${object_url}/file_view'
                         , 'permissions'   : (View,)
                         }
                       , { 'id'            : 'download'
                         , 'name'          : 'Download'
                         , 'action': 'string:${object_url}'
                         , 'permissions'   : (View,)
                         }
                       , { 'id'            : 'edit'
                         , 'name'          : 'Edit'
                         , 'action': 'string:${object_url}/file_edit_form'
                         , 'permissions'   : (ModifyPortalContent,)
                         }
                       , { 'id'            : 'metadata'
                         , 'name'          : 'Metadata'
                         , 'action': 'string:${object_url}/metadata_edit_form'
                         , 'permissions'   : (ModifyPortalContent,)
                         }
                       )
  }
,
)

import OFS.Image

def addFile( self
           , id
           , title=''
           , file=''
           , content_type=''
           , precondition=''
           , subject=()
           , description=''
           , contributors=()
           , effective_date=None
           , expiration_date=None
           , format='text/html'
           , language=''
           , rights=''
           ):
    """
    Add a File
    """

    # cookId sets the id and title if they are not explicity specified
    id, title = OFS.Image.cookId(id, title, file)

    self=self.this()

    # Instantiate the object and set its description.
    fobj = File( id, title, '', content_type, precondition, subject
               , description, contributors, effective_date, expiration_date
               , format, language, rights
               )
    
    # Add the File instance to self
    self._setObject(id, fobj)

    # 'Upload' the file.  This is done now rather than in the
    # constructor because the object is now in the ZODB and
    # can span ZODB objects.
    self._getOb(id).manage_upload(file)


class File(PortalContent, OFS.Image.File, DefaultDublinCoreImpl):
    """
        A Portal-managed File
    """

    implements(IDAVAware)
    __implements__ = ( PortalContent.__implements__
                     , DefaultDublinCoreImpl.__implements__
                     )
    
    meta_type='Portal File'
    effective_date = expiration_date = None
    _isDiscussable = 1
    icon = PortalContent.icon

    security = ClassSecurityInfo()

    def __init__( self
                , id
                , title=''
                , file=''
                , content_type=''
                , precondition=''
                , subject=()
                , description=''
                , contributors=()
                , effective_date=None
                , expiration_date=None
                , format=None
                , language='en-US'
                , rights=''
                ):
        OFS.Image.File.__init__( self, id, title, file
                               , content_type, precondition )
        self._setId(id)
        delattr(self, '__name__')

        # If no file format has been passed in, rely on what OFS.Image.File
        # detected. Unlike Images, which have code to try and pick the content
        # type out of the binary data, File objects only provide the correct
        # type if a "hint" in the form of a filename extension is given.
        if format is None:
            format = self.content_type 

        DefaultDublinCoreImpl.__init__( self, title, subject, description
                               , contributors, effective_date, expiration_date
                               , format, language, rights )

    # use OFS.Image.File's index_html; PortalContent's will cause some
    # circular behaviour w/ 'None' being returned as the default view
    security.declareProtected(View, 'index_html')
    index_html = OFS.Image.File.index_html

    # For old instances where bases had OFS.Image.File first,
    # the id was actually stored in __name__.
    # getId() will do the correct thing here, as id() is callable
    def id(self):
        return self.__name__

    security.declareProtected(View, 'SearchableText')
    def SearchableText(self):
        """
        SeachableText is used for full text seraches of a portal.  It
        should return a concatenation of all useful text.
        """
        return "%s %s" % (self.title, self.description)

    security.declarePrivate('manage_afterAdd')
    def manage_afterAdd(self, item, container):
        """Both of my parents have an afterAdd method"""
        OFS.Image.File.manage_afterAdd(self, item, container)
        PortalContent.manage_afterAdd(self, item, container)

    security.declarePrivate('manage_afterClone')
    def manage_afterClone(self, item):
        """Both of my parents have an afterClone method"""
        OFS.Image.File.manage_afterClone(self, item)
        PortalContent.manage_afterClone(self, item)

    security.declarePrivate('manage_beforeDelete')
    def manage_beforeDelete(self, item, container):
        """Both of my parents have a beforeDelete method"""
        PortalContent.manage_beforeDelete(self, item, container)
        OFS.Image.File.manage_beforeDelete(self, item, container)

    security.declarePrivate('_isNotEmpty')
    def _isNotEmpty(self, file):
        """ Do various checks on 'file' to try to determine non emptiness. """
        if not file:
            return 0                    # Catches None, Missing.Value, ''
        elif file and (type(file) is type('')):
            return 1
        elif getattr(file, 'filename', None):
            return 1
        elif not hasattr(file, 'read'):
            return 0
        else:
            file.seek(0,2)              # 0 bytes back from end of file
            t = file.tell()             # Report the location
            file.seek(0)                # and return pointer back to 0
            if t: return 1
            else: return 0

    security.declarePrivate('_edit')
    def _edit(self, precondition='', file=''):
        """ Perform changes for user """
        if precondition: self.precondition = precondition
        elif self.precondition: del self.precondition

        if self._isNotEmpty(file):
            self.manage_upload(file)

    security.declareProtected(ModifyPortalContent, 'edit')
    def edit(self, precondition='', file=''):
        """ Update and reindex. """
        self._edit( precondition, file )
        self.reindexObject()

    security.declareProtected(View, 'download')
    def download(self, REQUEST, RESPONSE):
        """Download this item.
        
        Calls OFS.Image.File.index_html to perform the actual transfer after
        first setting Content-Disposition to suggest a filename.
        
        This method is deprecated, use the URL of this object itself. Because
        the default view of a File object is to download, rather than view,
        this method is obsolete. Also note that certain browsers do not deal
        well with a Content-Disposition header.

        """

        RESPONSE.setHeader('Content-Disposition',
                           'attachment; filename=%s' % self.getId())
        return OFS.Image.File.index_html(self, REQUEST, RESPONSE)

    security.declareProtected(View, 'Format')
    def Format(self):
        """ Dublin Core element - resource format """
        return self.content_type

    security.declareProtected(ModifyPortalContent, 'setFormat')
    def setFormat(self, format):
        """ Dublin Core element - resource format """
        self.manage_changeProperties(content_type=format)

    security.declareProtected(ModifyPortalContent, 'PUT')
    def PUT(self, REQUEST, RESPONSE):
        """ Handle HTTP (and presumably FTP?) PUT requests """
        OFS.Image.File.PUT( self, REQUEST, RESPONSE )
        self.reindexObject()


InitializeClass(File)


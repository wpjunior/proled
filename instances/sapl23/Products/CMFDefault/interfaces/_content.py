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
""" CMFDefault content interfaces.

$Id: _content.py 38708 2005-09-30 22:53:49Z tseaver $
"""

from zope.interface import Interface
from zope.interface import Attribute


class IDocument(Interface):
    """ Textual content, in one of several formats.

    o Allowed formats include: structured text, HTML, plain text.
    """
    def CookedBody():
        """ Get the "cooked" (ready for presentation) form of the text.
        """

    def EditableBody():
        """ Get the "raw" (as edited) form of the text.
        """


class IMutableDocument(IDocument):
    """ Updatable form of IDocument.
    """
    def edit(text_format, text, file='', safety_belt=''):
        """ Update the document.

        o 'safety_belt', if passed, must match the value issued when the edit
        began.
        """


class ILink(Interface):
    """ URL as content.
    """
    def getRemoteUrl():
        """ Return the URL to which the link points, as a string.
        """


class IMutableLink(ILink):

    """ Updatable form of ILink.
    """
    def edit(remote_url):
        """ Update the link.

        o 'remote_url' should be a URL in an RFC-compatible form.

        o If 'remote_url' is unparseable by urllib, raise ValueError.
        """

##############################################################################
#
# Copyright (c) 2006 Zope Corporation and Contributors.
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
"""Unit tests for decode module.

$Id: test_decode.py 70913 2006-10-25 19:20:28Z yuppie $
"""
import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

def test_processInputs():
    """
    Testing processInputs

      >>> from zope import interface
      >>> from zope.i18n.interfaces import IUserPreferredCharsets
      >>> from Products.Five.form import EditView
      >>> class DummyResponse:
      ...     headers = {}
      ...     def setHeader(self, n, v):
      ...         self.headers[n] = v
      >>> class DummyRequest:
      ...     interface.implements(IUserPreferredCharsets)
      ...     form = {}
      ...     def getPreferredCharsets(self):
      ...         return ['iso-8859-1']
      ...     RESPONSE = DummyResponse()
      >>> class DummyEditView(EditView):
      ...     def __init__(self, context, request):
      ...         self.context = context
      ...         self.request = request
      >>> request = DummyRequest()

    Strings are converted to unicode::

      >>> request.form['foo'] = u'f\xf6\xf6'.encode('iso-8859-1')
      >>> editview = DummyEditView(None, request)
      >>> editview._processInputs()
      >>> request.form['foo'] == u'f\xf6\xf6'
      True

    Strings in lists are converted to unicode::

      >>> request.form['foo'] = [u'f\xf6\xf6'.encode('iso-8859-1')]
      >>> editview = DummyEditView(None, request)
      >>> editview._processInputs()
      >>> request.form['foo'] == [u'f\xf6\xf6']
      True

    Strings in tuples are converted to unicode::

      >>> request.form['foo'] = (u'f\xf6\xf6'.encode('iso-8859-1'),)
      >>> editview = DummyEditView(None, request)
      >>> editview._processInputs()
      >>> request.form['foo'] == (u'f\xf6\xf6',)
      True
    """

def test_suite():
    from zope.testing.doctest import DocTestSuite
    return DocTestSuite()

if __name__ == '__main__':
    framework()

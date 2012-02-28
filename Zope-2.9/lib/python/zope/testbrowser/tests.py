##############################################################################
#
# Copyright (c) 2004-2006 Zope Corporation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.0 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""Regression tests.

$Id: tests.py 71526 2006-12-11 17:12:54Z poster $
"""

import unittest
import httplib
import urllib2
from cStringIO import StringIO

import ClientCookie
import mechanize

from zope.testbrowser import browser
from zope.testing import doctest


def set_next_response(body, headers=None, status='200', reason='OK'):
    global next_response_body
    global next_response_headers
    global next_response_status
    global next_response_reason
    if headers is None:
        headers = (
            'Content-Type: text/html\r\n'
            'Content-Length: %s\r\n'
            % len(body)
            )
    next_response_body = body
    next_response_headers = headers
    next_response_status = status
    next_response_reason = reason


class FauxConnection(object):
    """A ``urllib2`` compatible connection object."""

    def __init__(self, host):
        pass

    def set_debuglevel(self, level):
        pass

    def _quote(self, url):
        # the publisher expects to be able to split on whitespace, so we have
        # to make sure there is none in the URL
        return url.replace(' ', '%20')


    def request(self, method, url, body=None, headers=None):
        if body is None:
            body = ''

        if url == '':
            url = '/'

        url = self._quote(url)

        # Construct the headers.
        header_chunks = []
        if headers is not None:
            for header in headers.items():
                header_chunks.append('%s: %s' % header)
            headers = '\n'.join(header_chunks) + '\n'
        else:
            headers = ''

        # Construct the full HTTP request string, since that is what the
        # ``HTTPCaller`` wants.
        request_string = (method + ' ' + url + ' HTTP/1.1\n'
                          + headers + '\n' + body)

        print request_string.replace('\r', '')

    def getresponse(self):
        """Return a ``urllib2`` compatible response.

        The goal of this method is to convert the Zope Publisher's response to
        a ``urllib2`` compatible response, which is also understood by
        mechanize.
        """
        return FauxResponse(next_response_body,
                            next_response_headers,
                            next_response_status,
                            next_response_reason,
                            )


class FauxResponse(object):

    def __init__(self, content, headers, status, reason):
        self.content = content
        self.status = status
        self.reason = reason
        self.msg = httplib.HTTPMessage(StringIO(headers), 0)
        self.content_as_file = StringIO(self.content)

    def read(self, amt=None):
        return self.content_as_file.read(amt)


class FauxHTTPHandler(urllib2.HTTPHandler):

    http_request = urllib2.AbstractHTTPHandler.do_request_

    def http_open(self, req):
        """Open an HTTP connection having a ``urllib2`` request."""
        # Here we connect to the publisher.
        return self.do_open(FauxConnection, req)


class FauxMechanizeBrowser(mechanize.Browser):

    handler_classes = {
        # scheme handlers
        "http": FauxHTTPHandler,

        "_http_error": urllib2.HTTPErrorProcessor,
        "_http_request_upgrade": ClientCookie.HTTPRequestUpgradeProcessor,
        "_http_default_error": urllib2.HTTPDefaultErrorHandler,

        # feature handlers
        "_authen": urllib2.HTTPBasicAuthHandler,
        "_redirect": ClientCookie.HTTPRedirectHandler,
        "_cookies": mechanize.Browser.handler_classes['_cookies'],
        "_refresh": ClientCookie.HTTPRefreshProcessor,
        "_referer": mechanize.Browser.handler_classes['_referer'],
        "_equiv": ClientCookie.HTTPEquivProcessor,
        "_seek": ClientCookie.SeekableProcessor,
        }

    default_schemes = ["http"]
    default_others = ["_http_error", "_http_request_upgrade",
                      "_http_default_error"]
    default_features = ["_authen", "_redirect", "_cookies", "_seek"]


class Browser(browser.Browser):

    def __init__(self, url=None):
        mech_browser = FauxMechanizeBrowser()
        super(Browser, self).__init__(url=url, mech_browser=mech_browser)

    def open(self, body, headers=None, status=200, reason='OK'):
        set_next_response(body, headers, status, reason)
        browser.Browser.open(self, 'http://localhost/')


def test_submit_duplicate_name():
    """

This test was inspired by bug #723 as testbrowser would pick up the wrong
button when having the same name twice in a form.

    >>> browser = Browser()

When given a form with two submit buttons that have the same name:

    >>> browser.open('''\
    ... <html><body>
    ...   <form action="." method="post" enctype="multipart/form-data">
    ...      <input type="submit" name="submit_me" value="GOOD" />
    ...      <input type="submit" name="submit_me" value="BAD" />
    ...   </form></body></html>
    ... ''') # doctest: +ELLIPSIS
    GET / HTTP/1.1
    ...

We can specify the second button through it's label/value:

    >>> browser.getControl('BAD')
    <SubmitControl name='submit_me' type='submit'>
    >>> browser.getControl('BAD').value
    'BAD'
    >>> browser.getControl('BAD').click() # doctest: +REPORT_NDIFF +ELLIPSIS
    POST / HTTP/1.1
    Content-length: ...
    Connection: close
    Content-type: multipart/form-data; boundary=...
    Host: localhost
    User-agent: Python-urllib/2.4
    <BLANKLINE>
    ...
    Content-disposition: form-data; name="submit_me"
    <BLANKLINE>
    BAD
    ...
    <BLANKLINE>

This also works if the labels have whitespace around them (this tests a
regression caused by the original fix for the above):

    >>> browser.open('''\
    ... <html><body>
    ...   <form action="." method="post" enctype="multipart/form-data">
    ...      <input type="submit" name="submit_me" value=" GOOD " />
    ...      <input type="submit" name="submit_me" value=" BAD " />
    ...   </form></body></html>
    ... ''') # doctest: +ELLIPSIS
    GET / HTTP/1.1
    ...
    >>> browser.getControl('BAD')
    <SubmitControl name='submit_me' type='submit'>
    >>> browser.getControl('BAD').value
    ' BAD '
    >>> browser.getControl('BAD').click() # doctest: +REPORT_NDIFF +ELLIPSIS
    POST / HTTP/1.1
    Content-length: ...
    Connection: close
    Content-type: multipart/form-data; boundary=...
    Host: localhost
    User-agent: Python-urllib/2.4
    <BLANKLINE>
    ...
    Content-disposition: form-data; name="submit_me"
    <BLANKLINE>
     BAD 
    ...
    <BLANKLINE>

"""


def test_suite():
    return unittest.TestSuite((
        doctest.DocTestSuite(),
        ))

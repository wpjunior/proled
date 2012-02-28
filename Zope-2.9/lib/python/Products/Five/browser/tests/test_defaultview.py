##############################################################################
#
# Copyright (c) 2004, 2005 Zope Corporation and Contributors.
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
"""Test Default View functionality

$Id: test_defaultview.py 69843 2006-08-29 14:48:01Z alecm $
"""
import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

def test_default_view():
    """
    Test default view functionality

    Let's register a couple of default views and make our stub classes
    default viewable:

      >>> import Products.Five.browser.tests
      >>> from Products.Five import zcml
      >>> zcml.load_config("configure.zcml", Products.Five)
      >>> zcml.load_config('defaultview.zcml', Products.Five.browser.tests)

    Now let's add a couple of stub objects:

      >>> from Products.Five.tests.testing.simplecontent import manage_addSimpleContent
      >>> from Products.Five.tests.testing.simplecontent import manage_addCallableSimpleContent
      >>> from Products.Five.tests.testing.simplecontent import manage_addIndexSimpleContent

      >>> manage_addSimpleContent(self.folder, 'testoid', 'Testoid')
      >>> manage_addCallableSimpleContent(self.folder, 'testcall', 'TestCall')
      >>> manage_addIndexSimpleContent(self.folder, 'testindex', 'TestIndex')

    As a last act of preparation, we create a manager login:

      >>> uf = self.folder.acl_users
      >>> uf._doAddUser('manager', 'r00t', ['Manager'], [])

    Test a simple default view:

      >>> print http(r'''
      ... GET /test_folder_1_/testoid HTTP/1.1
      ... Authorization: Basic manager:r00t
      ... ''')
      HTTP/1.1 200 OK
      ...
      The eagle has landed

    This tests whether an existing ``index_html`` method is still
    supported and called:

      >>> print http(r'''
      ... GET /test_folder_1_/testindex HTTP/1.1
      ... ''')
      HTTP/1.1 200 OK
      ...
      Default index_html called

    Disabled __call__ overriding for now.  Causese more trouble than it
    fixes.  Thus, no test here:

      #>>> print http(r'''
      #... GET /test_folder_1_/testcall HTTP/1.1
      #... ''')
      #HTTP/1.1 200 OK
      #...
      #Default __call__ called


    Clean up:

      >>> from zope.app.testing.placelesssetup import tearDown
      >>> tearDown()
    """

def test_default_method_args_marshalling():
    """\
    Test the default call method of a view, with respect to possible
    breakage of argument marshalling from other components

    This is not directly a bug in Five, just a change that enables
    components have simpler code to imitate ZPublisher's arguments
    marshalling strategy on default view methods.

    The ZPublisher marshalls arguments to called methods from the
    request based on the method's signature. This however assumes
    that it finds the real callable method. However in case of the
    autogenerated __call__ method of a view, the real method is
    wrapped. Although the publisher correctly handles this by
    looking at the __browser_default__ and applying the request on
    the real method, Plone's portal factory does not do this
    correctly, thus causing these method calls fail with TypeError,
    since no parameters will be marshalled to the browser default
    methods if within the portal factory.

    The applied fix changes the __call__ in such a way that it is
    not wrapper any more, but yields the original callable instead.
    This test simply checks that this is so, in other words this is
    a check that would have failed with the original version.

    First, we load the configuration file:

      >>> import Products.Five.tests
      >>> from Products.Five import zcml
      >>> zcml.load_config('meta.zcml', Products.Five)
      >>> zcml.load_config("permissions.zcml", Products.Five)
      >>> zcml.load_config('directives.zcml', Products.Five.tests)

    Define a view, with a single attribute and the name of the view
    is the same as the attribute. Important is that we will use the
    default browser view.

      >>> zcml.load_string('''
      ...   <configure xmlns="http://namespaces.zope.org/zope"
      ...              xmlns:browser="http://namespaces.zope.org/browser">
      ...        <browser:page
      ...            for="Products.Five.browser.tests.classes.IOne"
      ...            class="Products.Five.browser.tests.classes.ViewOne"
      ...            attribute="my_method"
      ...            name="my_method"
      ...            permission="zope2.Public"
      ...        />
      ...   </configure>
      ...   ''')

    Create a context object and a request. Provide parameters on the
    request.

      >>> from Products.Five.browser.tests.classes import One
      >>> context = One()
      >>> from zope.publisher.browser import TestRequest
      >>> request = TestRequest(form={'arg1': 'A', 'arg2': 'B', 'kw1': 'C'})

    Create the view.

      >>> from zope.component import getMultiAdapter
      >>> from zope.interface import Interface
      >>> view = getMultiAdapter((context, request), Interface, 'my_method')

    Check that the __call__ method's signature equals to the real
    method's signature. They both should yield the four parameters.

      >>> def args(method):
      ...     f = method.im_func
      ...     c = f.func_code
      ...     defaults = f.func_defaults
      ...     names = c.co_varnames[1:c.co_argcount]
      ...     return names
      >>> args(view.my_method)
      ('arg1', 'arg2', 'kw1', 'kw2')
      >>> args(view.__call__)
      ('arg1', 'arg2', 'kw1', 'kw2')

    Finally, call the view's default method. Important is, if this
    gives a TypeError then the portal factory will fail. This is in
    effect the same as the previous argument check was.

      >>> from ZPublisher.mapply import mapply
      >>> mapply(view.__call__, (), request)
      CALLED A B C D

    Clean up adapter registry and others:

      >>> from zope.testing.cleanup import cleanUp
      >>> cleanUp()
    """

def test_suite():
    from Testing.ZopeTestCase import FunctionalDocTestSuite
    return FunctionalDocTestSuite()

if __name__ == '__main__':
    framework()

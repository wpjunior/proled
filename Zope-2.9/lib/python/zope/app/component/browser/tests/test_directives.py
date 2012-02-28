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
"""Directives Tests

$Id: test_directives.py 40187 2005-11-16 23:37:25Z srichter $
"""
import unittest
from zope.interface import Interface
from zope.testing.doctestunit import DocTestSuite

from zope.app.testing.placelesssetup import setUp, tearDown

class FauxContext(object):
    def __init__(self):
        self.actions = []
        self.info = 'info'

    def action(self, **kw):
        self.actions.append(kw)

class IDummyUtility(Interface):
    """Represents a dummy utility."""

def test_toolDirective():
    r"""
    >>> from zope.app.component.browser import metaconfigure
    >>> context = FauxContext()
    >>> metaconfigure.tool(context, IDummyUtility, folder="dummy",
    ...                    title="dummy", description="the description")

    >>> iface = context.actions[0]
    >>> iface['discriminator']

    >>> iface['callable'].__module__
    'zope.app.component.interface'

    >>> iface['args'][1].getName()
    'IDummyUtility'

    >>> iface['args'][2].getName()
    'IToolType'

    >>> tool = context.actions[1]
    >>> from pprint import pprint
    >>> pprint([n for n in tool['discriminator']])
    ['utility',
     <InterfaceClass zope.app.component.browser.tools.IToolConfiguration>,
     'IDummyUtility']

    >>> tool['callable'].__module__
    'zope.app.component.metaconfigure'
    """

def test_suite():
    return unittest.TestSuite((
        DocTestSuite(setUp=setUp, tearDown=tearDown),
        ))

if __name__ == '__main__': unittest.main()

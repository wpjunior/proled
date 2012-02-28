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
"""Five-specific directive handlers

These directives are specific to Five and have no equivalents in Zope 3.

$Id: fiveconfigure.py 18581 2005-10-14 16:54:25Z regebro $
"""
from zope.interface import classImplements, classImplementsOnly, implementedBy
from zope.interface.interface import InterfaceClass
from zope.configuration.exceptions import ConfigurationError
from zope.app.component.metaconfigure import adapter
from zope.app.component.interfaces import IPossibleSite

from Products.Five.site.localsite import FiveSite

_localsite_monkies = []
def classSiteHook(class_, site_class):
    setattr(class_, 'getSiteManager',
            site_class.getSiteManager.im_func)
    setattr(class_, 'setSiteManager',
            site_class.setSiteManager.im_func)
    _localsite_monkies.append(class_)

def installSiteHook(_context, class_, site_class=None):
    if site_class is None:
        if not IPossibleSite.implementedBy(class_):
            # This is not a possible site, we need to monkey-patch it so that
            # it is.
            site_class = FiveSite
    else:
        if not IPossibleSite.implementedBy(site_class):
            raise ConfigurationError('Site class does not implement '
                                     'IPossibleClass: %s' % site_class)
    # only install the hook once
    already = getattr(class_, '_localsite_marker', False)

    if site_class is not None and not already:
        class_._localsite_marker = True
        _context.action(
            discriminator = (class_,),
            callable = classSiteHook,
            args=(class_, site_class)
            )
        _context.action(
            discriminator = (class_, IPossibleSite),
            callable = classImplements,
            args=(class_, IPossibleSite)
            )

# clean up code

def uninstallSiteHooks():
    for class_ in _localsite_monkies:
        delattr(class_, 'getSiteManager')
        delattr(class_, 'setSiteManager')
        classImplementsOnly(class_, implementedBy(class_)-IPossibleSite)
        _localsite_monkies.remove(class_)
        if getattr(class_, '_localsite_marker', False):
            delattr(class_, '_localsite_marker')

from zope.testing.cleanup import addCleanUp
addCleanUp(uninstallSiteHooks)
del addCleanUp

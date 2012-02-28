##############################################################################
#
# Copyright (c) 2004 Zope Corporation and Contributors.
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
"""Module Aliases Package

modulealiases package allows you to make module alias declarations via zcml,
e.g.::

  <modulealias
      module="some.existing.package"
      alias="some.nonexistent.package" />

$Id: metaconfigure.py 26567 2004-07-16 06:58:27Z srichter $
"""
__docformat__ = 'restructuredtext'
import sys
import types

class ModuleAliasException(Exception):
    pass

def define_module_alias(_context, module, alias):
    _context.action(
        discriminator = None,
        callable = alias_module,
        args = (module, alias, _context),
        )

def alias_module(module, alias, context):
    """ define a module alias by munging sys.modules """
    module_ob = context.resolve(module)
    alias_ob = sys.modules.get(alias)
    if not isinstance(module_ob, types.ModuleType):
        raise ModuleAliasException(
            '"module" %s does not resolve to a module' % module)

    if alias_ob is not None and alias_ob is not module_ob: 
        raise ModuleAliasException(
            '"alias" module %s already exists in sys.modules' % alias)
    
    sys.modules[alias] = module_ob


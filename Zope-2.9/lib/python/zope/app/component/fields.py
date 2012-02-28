#############################################################################
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
"""Component-related fields

$Id$
"""
__docformat__ = 'restructuredtext'

import zope.schema
from zope.component.exceptions import ComponentLookupError
from zope.configuration.exceptions import ConfigurationError
from zope.configuration.fields import GlobalObject
from zope.publisher.interfaces.browser import ILayer

from zope.app import zapi


class LayerField(GlobalObject):
    r"""This field represents a layer.

    Besides being able to look up the layer by importing it, we also try
    to look up the name in the site manager.

    >>> from zope.interface import directlyProvides
    >>> from zope.interface.interface import InterfaceClass

    >>> layer1 = InterfaceClass('layer1', (),
    ...                         __doc__='Layer: layer1',
    ...                         __module__='zope.app.layers')
    >>> directlyProvides(layer1, ILayer)

    >>> layers = None
    >>> class Resolver(object):
    ...     def resolve(self, path):
    ...         if '..' in path:
    ...             raise ValueError('Empty module name')
    ...         if (path.startswith('zope.app.layers') and
    ...             hasattr(layers, 'layer1') or
    ...             path == 'zope.app.component.fields.layer1' or
    ...             path == '.fields.layer1'):
    ...             return layer1
    ...         raise ConfigurationError('layer1')

    >>> field = LayerField()
    >>> field = field.bind(Resolver())

    Test 1: Import the layer
    ------------------------

    >>> field.fromUnicode('zope.app.component.fields.layer1') is layer1
    True

    Test 2: We have a shortcut name. Import the layer from `zope.app.layers`.
    -------------------------------------------------------------------------

    >>> from types import ModuleType as module
    >>> import sys
    >>> layers = module('layers')
    >>> old = sys.modules.get('zope.app.layers', None)
    >>> sys.modules['zope.app.layers'] = layers
    >>> setattr(layers, 'layer1', layer1)

    >>> field.fromUnicode('layer1') is layer1
    True

    >>> if old is not None:
    ...     sys.modules['zope.app.layers'] = old

    Test 3: Get the layer from the site manager
    -------------------------------------------

    >>> from zope.app.testing import ztapi
    >>> ztapi.provideUtility(ILayer, layer1, 'layer1')

    >>> field.fromUnicode('layer1') is layer1
    True

    Test 4: Import the layer by using a short name
    ----------------------------------------------

    >>> field.fromUnicode('.fields.layer1') is layer1
    True
    """

    def fromUnicode(self, u):
        name = str(u.strip())

        try:
            value = zapi.queryUtility(ILayer, name)
        except ComponentLookupError:
            # The component architecture is not up and running.
            pass
        else:
            if value is not None:
                return value

        try:
            value = self.context.resolve('zope.app.layers.'+name)
        except (ConfigurationError, ValueError), v:
            try:
                value = self.context.resolve(name)
            except ConfigurationError, v:
                raise zope.schema.ValidationError(v)

        self.validate(value)
        return value

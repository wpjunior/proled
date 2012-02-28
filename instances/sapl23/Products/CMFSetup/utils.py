##############################################################################
#
# Copyright (c) 2004 Zope Corporation and Contributors. All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
""" CMFSetup product utilities

$Id: utils.py 40769 2005-12-13 17:22:05Z efge $
"""

import os
from warnings import warn
from xml.dom.minidom import parseString as domParseString

import Products
from AccessControl import ClassSecurityInfo
from Acquisition import aq_base
from Acquisition import Implicit
from Globals import InitializeClass
from Globals import package_home
from Products.PageTemplates.PageTemplateFile import PageTemplateFile

from exceptions import BadRequest
from permissions import ManagePortal


_pkgdir = package_home( globals() )
_xmldir = os.path.join( _pkgdir, 'xml' )

CONVERTER, DEFAULT, KEY = range(3)


class ImportConfiguratorBase(Implicit):
    """ Synthesize data from XML description.
    """
    security = ClassSecurityInfo()
    security.setDefaultAccess('allow')

    def __init__(self, site, encoding=None):

        self._site = site
        self._encoding = encoding

    security.declareProtected(ManagePortal, 'parseXML')
    def parseXML(self, xml):
        """ Pseudo API.
        """
        reader = getattr(xml, 'read', None)

        if reader is not None:
            xml = reader()

        dom = domParseString(xml)
        root = dom.documentElement

        return self._extractNode(root)

    def _extractNode(self, node):

        nodes_map = self._getImportMapping()
        if node.nodeName not in nodes_map:
            nodes_map = self._getSharedImportMapping()
            if node.nodeName not in nodes_map:
                raise ValueError('Unknown node: %s' % node.nodeName)
        node_map = nodes_map[node.nodeName]
        info = {}

        for name, val in node.attributes.items():
            key = node_map[name].get( KEY, str(name) )
            if self._encoding is not None:
                val = val.encode(self._encoding)
            info[key] = val

        for child in node.childNodes:
            name = child.nodeName

            if name == '#comment':
                continue

            if not name == '#text':
                key = node_map[name].get(KEY, str(name) )
                info[key] = info.setdefault( key, () ) + (
                                                    self._extractNode(child),)

            elif '#text' in node_map:
                key = node_map['#text'].get(KEY, 'value')
                val = child.nodeValue.lstrip()
                if self._encoding is not None:
                    val = val.encode(self._encoding)
                info[key] = info.setdefault(key, '') + val

        for k, v in node_map.items():
            key = v.get(KEY, k)

            if DEFAULT in v and not key in info:
                if isinstance( v[DEFAULT], basestring ):
                    info[key] = v[DEFAULT] % info
                else:
                    info[key] = v[DEFAULT]

            elif CONVERTER in v and key in info:
                info[key] = v[CONVERTER]( info[key] )

            if key is None:
                info = info[key]

        return info

    def _getSharedImportMapping(self):

        return {
          'object':
            { 'i18n:domain':     {},
              'name':            {KEY: 'id'},
              'meta_type':       {},
              'insert-before':   {},
              'insert-after':    {},
              'property':        {KEY: 'properties', DEFAULT: ()},
              'object':          {KEY: 'objects', DEFAULT: ()},
              'xmlns:i18n':      {} },
          'property':
            { 'name':            {KEY: 'id'},
              '#text':           {KEY: 'value', DEFAULT: ''},
              'element':         {KEY: 'elements', DEFAULT: ()},
              'type':            {},
              'select_variable': {},
              'i18n:translate':  {} },
          'element':
            { 'value':           {KEY: None} },
          'description':
            { '#text':           {KEY: None, DEFAULT: ''} } }

    def _convertToBoolean(self, val):

        return val.lower() in ('true', 'yes', '1')

    def _convertToInteger(self, val):

        return int(val.strip())

    def _convertToUnique(self, val):

        assert len(val) == 1
        return val[0]

    security.declareProtected(ManagePortal, 'initObject')
    def initObject(self, parent, o_info):
        warn('CMFSetup.utils including ImportConfiguratorBase is deprecated. '
             'Please use NodeAdapterBase from GenericSetup.utils instead.',
             DeprecationWarning)

        obj_id = str(o_info['id'])
        if obj_id not in parent.objectIds():
            meta_type = o_info['meta_type']
            for mt_info in Products.meta_types:
                if mt_info['name'] == meta_type:
                    parent._setObject( obj_id, mt_info['instance'](obj_id) )
                    break
            else:
                raise ValueError('unknown meta_type \'%s\'' % obj_id)
        obj = parent._getOb(obj_id)

        if 'insert-before' in o_info:
            if o_info['insert-before'] == '*':
                parent.moveObjectsToTop(obj_id)
            else:
                try:
                    position = parent.getObjectPosition(o_info['insert-before'])
                    parent.moveObjectToPosition(obj_id, position)
                except ValueError:
                    pass
        elif 'insert-after' in o_info:
            if o_info['insert-after'] == '*':
                parent.moveObjectsToBottom(obj_id)
            else:
                try:
                    position = parent.getObjectPosition(o_info['insert-after'])
                    parent.moveObjectToPosition(obj_id, position+1)
                except ValueError:
                    pass

        [ self.initObject(obj, info) for info in o_info['objects'] ]

        if 'i18n:domain' in o_info:
            obj.i18n_domain = o_info['i18n:domain']

        [ self.initProperty(obj, info) for info in o_info['properties'] ]

    security.declareProtected(ManagePortal, 'initProperty')
    def initProperty(self, obj, p_info):
        warn('CMFSetup.utils including ImportConfiguratorBase is deprecated. '
             'Please use NodeAdapterBase from GenericSetup.utils instead.',
             DeprecationWarning)

        prop_id = p_info['id']
        prop_map = obj.propdict().get(prop_id, None)

        if prop_map is None:
            type = p_info.get('type', None)
            if type:
                val = p_info.get('select_variable', '')
                obj._setProperty(prop_id, val, type)
                prop_map = obj.propdict().get(prop_id, None)
            else:
                raise ValueError('undefined property \'%s\'' % prop_id)

        if not 'w' in prop_map.get('mode', 'wd'):
            raise BadRequest('%s cannot be changed' % prop_id)

        if prop_map.get('type') == 'multiple selection':
            prop_value = p_info['elements'] or ()
        elif prop_map.get('type') == 'boolean':
            # Make sure '0' is imported as False
            prop_value = str(p_info['value'])
            if prop_value == '0':
                prop_value = ''
        else:
            # if we pass a *string* to _updateProperty, all other values
            # are converted to the right type
            prop_value = p_info['elements'] or str( p_info['value'] )

        obj._updateProperty(prop_id, prop_value)

InitializeClass(ImportConfiguratorBase)


class ExportConfiguratorBase(Implicit):
    """ Synthesize XML description.
    """
    security = ClassSecurityInfo()
    security.setDefaultAccess('allow')

    def __init__(self, site, encoding=None):

        self._site = site
        self._encoding = encoding
        self._template = self._getExportTemplate()

    security.declareProtected(ManagePortal, 'generateXML')
    def generateXML(self, **kw):
        """ Pseudo API.
        """
        return self._template(**kw)

    #
    #   generic object and property support
    #
    _ob_nodes = PageTemplateFile('object_nodes.xml', _xmldir)
    _prop_nodes = PageTemplateFile('property_nodes.xml', _xmldir)

    security.declareProtected(ManagePortal, 'generateObjectNodes')
    def generateObjectNodes(self, obj_infos):
        """ Pseudo API.
        """
        warn('CMFSetup.utils including ExportConfiguratorBase is deprecated. '
             'Please use NodeAdapterBase from GenericSetup.utils instead.',
             DeprecationWarning)

        lines = self._ob_nodes(objects=obj_infos).splitlines()
        return '\n'.join(lines)

    security.declareProtected(ManagePortal, 'generatePropertyNodes')
    def generatePropertyNodes(self, prop_infos):
        """ Pseudo API.
        """
        warn('CMFSetup.utils including ExportConfiguratorBase is deprecated. '
             'Please use NodeAdapterBase from GenericSetup.utils instead.',
             DeprecationWarning)

        lines = self._prop_nodes(properties=prop_infos).splitlines()
        return '\n'.join(lines)

    def _extractObject(self, obj):
        warn('CMFSetup.utils including ExportConfiguratorBase is deprecated. '
             'Please use NodeAdapterBase from GenericSetup.utils instead.',
             DeprecationWarning)

        properties = []
        subobjects = []
        i18n_domain = getattr(obj, 'i18n_domain', None)

        if getattr( aq_base(obj), '_propertyMap' ):
            for prop_map in obj._propertyMap():
                prop_info = self._extractProperty(obj, prop_map)
                if i18n_domain and prop_info['id'] in ('title', 'description'):
                    prop_info['i18ned'] = ''
                if prop_info['id'] != 'i18n_domain':
                    properties.append(prop_info)

        if getattr( aq_base(obj), 'objectValues' ):
            for sub in obj.objectValues():
                subobjects.append( self._extractObject(sub) )

        return { 'id': obj.getId(),
                 'meta_type': obj.meta_type,
                 'i18n_domain': i18n_domain or None,
                 'properties': tuple(properties),
                 'subobjects': tuple(subobjects) }

    def _extractProperty(self, obj, prop_map):
        warn('CMFSetup.utils including ExportConfiguratorBase is deprecated. '
             'Please use NodeAdapterBase from GenericSetup.utils instead.',
             DeprecationWarning)

        prop_id = prop_map['id']
        prop = obj.getProperty(prop_id)

        if isinstance(prop, tuple):
            prop_value = ''
            prop_elements = prop
        elif isinstance(prop, list):
            # Backward compat for old instances that stored
            # properties as list.
            prop_value = ''
            prop_elements = tuple(prop)
        else:
            prop_value = prop
            prop_elements = ()

        if 'd' in prop_map.get('mode', 'wd') and not prop_id == 'title':
            type = prop_map.get('type', 'string')
            select_variable = prop_map.get('select_variable', None)
        else:
            type = None
            select_variable = None

        return { 'id': prop_id,
                 'value': prop_value,
                 'elements': prop_elements,
                 'type': type,
                 'select_variable': select_variable }

InitializeClass(ExportConfiguratorBase)


# BBB: old class mixing the two, will be removed in CMF 2.0
class ConfiguratorBase(ImportConfiguratorBase, ExportConfiguratorBase):
    """ Synthesize XML description.
    """
    security = ClassSecurityInfo()
    security.setDefaultAccess('allow')

    def __init__(self, site, encoding=None):
        ImportConfiguratorBase.__init__(self, site, encoding)
        ExportConfiguratorBase.__init__(self, site, encoding)

InitializeClass(ConfiguratorBase)


# BBB: deprecated DOM parsing utilities, will be removed in CMF 2.0

_marker = object()

def _queryNodeAttribute( node, attr_name, default, encoding=None ):

    """ Extract a string-valued attribute from node.

    o Return 'default' if the attribute is not present.
    """
    attr_node = node.attributes.get( attr_name, _marker )

    if attr_node is _marker:
        return default

    value = attr_node.nodeValue

    if encoding is not None:
        value = value.encode( encoding )

    return value

def _getNodeAttribute( node, attr_name, encoding=None ):

    """ Extract a string-valued attribute from node.
    """
    value = _queryNodeAttribute( node, attr_name, _marker, encoding )

    if value is _marker:
        raise ValueError, 'Invalid attribute: %s' % attr_name

    return value

def _queryNodeAttributeBoolean( node, attr_name, default ):

    """ Extract a string-valued attribute from node.

    o Return 'default' if the attribute is not present.
    """
    attr_node = node.attributes.get( attr_name, _marker )

    if attr_node is _marker:
        return default

    value = node.attributes[ attr_name ].nodeValue.lower()

    return value in ( 'true', 'yes', '1' )

def _getNodeAttributeBoolean( node, attr_name ):

    """ Extract a string-valued attribute from node.
    """
    value = node.attributes[ attr_name ].nodeValue.lower()

    return value in ( 'true', 'yes', '1' )

def _coalesceTextNodeChildren( node, encoding=None ):

    """ Concatenate all childe text nodes into a single string.
    """
    from xml.dom import Node
    fragments = []
    node.normalize()
    child = node.firstChild

    while child is not None:

        if child.nodeType == Node.TEXT_NODE:
            fragments.append( child.nodeValue )

        child = child.nextSibling

    joined = ''.join( fragments )

    if encoding is not None:
        joined = joined.encode( encoding )

    return ''.join( [ line.lstrip() for line in joined.splitlines(True) ] )

def _extractDescriptionNode(parent, encoding=None):

    d_nodes = parent.getElementsByTagName('description')
    if d_nodes:
        return _coalesceTextNodeChildren(d_nodes[0], encoding)
    else:
        return ''

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
""" CMFDefault portal_metadata tool.

$Id: MetadataTool.py 37005 2005-05-04 21:33:28Z jens $
"""

from AccessControl import ClassSecurityInfo
from AccessControl import getSecurityManager
from Globals import DTMLFile
from Globals import InitializeClass
from Globals import PersistentMapping
from OFS.SimpleItem import SimpleItem

from Products.CMFCore.ActionProviderBase import ActionProviderBase
from Products.CMFCore.interfaces.portal_metadata \
        import portal_metadata as IMetadataTool
from Products.CMFCore.utils import UniqueObject

from exceptions import MetadataError
from permissions import ManagePortal
from permissions import ModifyPortalContent
from permissions import View
from utils import _dtmldir


class MetadataElementPolicy( SimpleItem ):
    """
        Represent a type-specific policy about a particular DCMI element.
    """

    security = ClassSecurityInfo()
    #
    #   Default values.
    #
    is_required         = 0
    supply_default      = 0
    default_value       = ''
    enforce_vocabulary  = 0
    allowed_vocabulary  = ()

    def __init__(self, is_multi_valued=False):
        self.is_multi_valued = bool(is_multi_valued)

    #
    #   Mutator.
    #
    security.declareProtected(ManagePortal , 'edit')
    def edit( self
            , is_required
            , supply_default
            , default_value
            , enforce_vocabulary
            , allowed_vocabulary
            ):
        self.is_required        = bool(is_required)
        self.supply_default     = bool(supply_default)
        self.default_value      = default_value
        self.enforce_vocabulary = bool(enforce_vocabulary)
        self.allowed_vocabulary = tuple(allowed_vocabulary)

    #
    #   Query interface
    #
    security.declareProtected(View , 'isMultiValued')
    def isMultiValued( self ):
        """
            Can this element hold multiple values?
        """
        return self.is_multi_valued

    security.declareProtected(View , 'isRequired')
    def isRequired( self ):
        """
            Must this element be supplied?
        """
        return self.is_required

    security.declareProtected(View , 'supplyDefault')
    def supplyDefault( self ):
        """
            Should the tool supply a default?
        """
        return self.supply_default

    security.declareProtected(View , 'defaultValue')
    def defaultValue( self ):
        """
            If so, what is the default?
        """
        return self.default_value

    security.declareProtected(View , 'enforceVocabulary')
    def enforceVocabulary( self ):
        """
        """
        return self.enforce_vocabulary

    security.declareProtected(View , 'allowedVocabulary')
    def allowedVocabulary( self ):
        """
        """
        return self.allowed_vocabulary

InitializeClass( MetadataElementPolicy )


DEFAULT_ELEMENT_SPECS = ( ( 'Title', 0 )
                        , ( 'Description', 0 )
                        , ( 'Subject', 1 )
                        , ( 'Format', 0 )
                        , ( 'Language', 0 )
                        , ( 'Rights', 0 )
                        )


class ElementSpec( SimpleItem ):
    """
        Represent all the tool knows about a single metadata element.
    """
    security = ClassSecurityInfo()

    #
    #   Default values.
    #
    is_multi_valued = 0

    def __init__( self, is_multi_valued ):
        self.is_multi_valued  = is_multi_valued
        self.policies         = PersistentMapping()
        self.policies[ None ] = self._makePolicy()  # set default policy

    security.declarePrivate( '_makePolicy' )
    def _makePolicy( self ):
        return MetadataElementPolicy( self.is_multi_valued )

    security.declareProtected(View , 'isMultiValued')
    def isMultiValued( self ):
        """
            Is this element multi-valued?
        """
        return self.is_multi_valued

    security.declareProtected(View , 'getPolicy')
    def getPolicy( self, typ=None ):
        """
            Find the policy this element for objects whose type
            object name is 'typ';  return a default, if none found.
        """
        try:
            return self.policies[ typ ].__of__(self)
        except KeyError:
            return self.policies[ None ].__of__(self)

    security.declareProtected(View , 'listPolicies')
    def listPolicies( self ):
        """
            Return a list of all policies for this element.
        """
        res = []
        for k, v in self.policies.items():
            res.append((k, v.__of__(self)))
        return res

    security.declareProtected(ManagePortal , 'addPolicy')
    def addPolicy( self, typ ):
        """
            Add a policy to this element for objects whose type
            object name is 'typ'.
        """
        if typ is None:
            raise MetadataError, "Can't replace default policy."

        if self.policies.has_key( typ ):
            raise MetadataError, "Existing policy for content type:" + typ

        self.policies[ typ ] = self._makePolicy()

    security.declareProtected(ManagePortal, 'removePolicy')
    def removePolicy( self, typ ):
        """
            Remove the policy from this element for objects whose type
            object name is 'typ' (*not* the default, however).
        """
        if typ is None:
            raise MetadataError, "Can't remove default policy."
        del self.policies[ typ ]

InitializeClass( ElementSpec )


class MetadataTool( UniqueObject, SimpleItem, ActionProviderBase ):

    __implements__ = (IMetadataTool, ActionProviderBase.__implements__)

    id = 'portal_metadata'
    meta_type = 'Default Metadata Tool'
    _actions = ()

    #
    #   Default values.
    #
    publisher           = ''
    element_specs       = None
    #initial_values_hook = None
    #validation_hook     = None

    security = ClassSecurityInfo()

    def __init__( self
                , publisher=None
               #, initial_values_hook=None
               #, validation_hook=None
                , element_specs=DEFAULT_ELEMENT_SPECS
                ):

        self.editProperties( publisher
                          #, initial_values_hook
                          #, validation_hook
                           )

        self.element_specs = PersistentMapping()

        for name, is_multi_valued in element_specs:
            self.element_specs[ name ] = ElementSpec( is_multi_valued )

    #
    #   ZMI methods
    #
    manage_options = ( ActionProviderBase.manage_options +
                     ( { 'label'      : 'Overview'
                         , 'action'     : 'manage_overview'
                         }
                       , { 'label'      : 'Properties'
                         , 'action'     : 'propertiesForm'
                         }
                       , { 'label'      : 'Elements'
                         , 'action'     : 'elementPoliciesForm'
                         }
            # TODO     , { 'label'      : 'Types'
            #            , 'action'     : 'typesForm'
            #            }
                       )
                     + SimpleItem.manage_options
                     )

    security.declareProtected(ManagePortal, 'manage_overview')
    manage_overview = DTMLFile( 'explainMetadataTool', _dtmldir )

    security.declareProtected(ManagePortal, 'propertiesForm')
    propertiesForm = DTMLFile( 'metadataProperties', _dtmldir )

    security.declareProtected(ManagePortal, 'editProperties')
    def editProperties( self
                      , publisher=None
               # TODO , initial_values_hook=None
               # TODO , validation_hook=None
                      , REQUEST=None
                      ):
        """
            Form handler for "tool-wide" properties (including list of
            metadata elements).
        """
        if publisher is not None:
            self.publisher = publisher

        # TODO self.initial_values_hook = initial_values_hook
        # TODO self.validation_hook = validation_hook

        if REQUEST is not None:
            REQUEST[ 'RESPONSE' ].redirect( self.absolute_url()
                                        + '/propertiesForm'
                                        + '?manage_tabs_message=Tool+updated.'
                                        )

    security.declareProtected(ManagePortal, 'elementPoliciesForm')
    elementPoliciesForm = DTMLFile( 'metadataElementPolicies', _dtmldir )

    security.declareProtected(ManagePortal, 'addElementPolicy')
    def addElementPolicy( self
                        , element
                        , content_type
                        , is_required
                        , supply_default
                        , default_value
                        , enforce_vocabulary
                        , allowed_vocabulary
                        , REQUEST=None
                        ):
        """
            Add a type-specific policy for one of our elements.
        """
        if content_type == '<default>':
            content_type = None

        spec = self.getElementSpec( element )
        spec.addPolicy( content_type )
        policy = spec.getPolicy( content_type )
        policy.edit( is_required
                   , supply_default
                   , default_value
                   , enforce_vocabulary
                   , allowed_vocabulary
                   )
        if REQUEST is not None:
            REQUEST[ 'RESPONSE' ].redirect( self.absolute_url()
               + '/elementPoliciesForm'
               + '?element=' + element
               + '&manage_tabs_message=Policy+added.'
               )

    security.declareProtected(ManagePortal, 'removeElementPolicy')
    def removeElementPolicy( self
                           , element
                           , content_type
                           , REQUEST=None
                           ):
        """
            Remvoe a type-specific policy for one of our elements.
        """
        if content_type == '<default>':
            content_type = None

        spec = self.getElementSpec( element )
        spec.removePolicy( content_type )
        if REQUEST is not None:
            REQUEST[ 'RESPONSE' ].redirect( self.absolute_url()
               + '/elementPoliciesForm'
               + '?element=' + element
               + '&manage_tabs_message=Policy+removed.'
               )

    security.declareProtected(ManagePortal, 'updateElementPolicy')
    def updateElementPolicy( self
                           , element
                           , content_type
                           , is_required
                           , supply_default
                           , default_value
                           , enforce_vocabulary
                           , allowed_vocabulary
                           , REQUEST=None
                           ):
        """
            Update a policy for one of our elements ('content_type'
            will be '<default>' when we edit the default).
        """
        if content_type == '<default>':
            content_type = None
        spec = self.getElementSpec( element )
        policy = spec.getPolicy( content_type )
        policy.edit( is_required
                   , supply_default
                   , default_value
                   , enforce_vocabulary
                   , allowed_vocabulary
                   )
        if REQUEST is not None:
            REQUEST[ 'RESPONSE' ].redirect( self.absolute_url()
               + '/elementPoliciesForm'
               + '?element=' + element
               + '&manage_tabs_message=Policy+updated.'
               )


    #
    #   Element spec manipulation.
    #
    security.declareProtected(ManagePortal, 'listElementSpecs')
    def listElementSpecs( self ):
        """
            Return a list of ElementSpecs representing
            the elements managed by the tool.
        """
        res = []
        for k, v in self.element_specs.items():
            res.append((k, v.__of__(self)))
        return res

    security.declareProtected(ManagePortal, 'getElementSpec')
    def getElementSpec( self, element ):
        """
            Return an ElementSpec representing the tool's knowledge
            of 'element'.
        """
        return self.element_specs[ element ].__of__( self )

    security.declareProtected(ManagePortal, 'addElementSpec')
    def addElementSpec( self, element, is_multi_valued, REQUEST=None ):
        """
            Add 'element' to our list of managed elements.
        """
        # Don't replace.
        if self.element_specs.has_key( element ):
           return

        self.element_specs[ element ] = ElementSpec( is_multi_valued )

        if REQUEST is not None:
            REQUEST[ 'RESPONSE' ].redirect( self.absolute_url()
               + '/propertiesForm'
               + '?manage_tabs_message=Element+' + element + '+added.'
               )

    security.declareProtected(ManagePortal, 'removeElementSpec')
    def removeElementSpec( self, element, REQUEST=None ):
        """
            Remove 'element' from our list of managed elements.
        """
        del self.element_specs[ element ]

        if REQUEST is not None:
            REQUEST[ 'RESPONSE' ].redirect( self.absolute_url()
               + '/propertiesForm'
               + '?manage_tabs_message=Element+' + element + '+removed.'
               )

    security.declareProtected(ManagePortal, 'listPolicies')
    def listPolicies( self, typ=None ):
        """
            Show all policies for a given content type, or the default
            if None.
        """
        result = []
        for element, spec in self.listElementSpecs():
            result.append( ( element, spec.getPolicy( typ ) ) )
        return result

    #
    #   'portal_metadata' interface
    #
    security.declarePrivate( 'getFullName' )
    def getFullName( self, userid ):
        """
            Convert an internal userid to a "formal" name, if
            possible, perhaps using the 'portal_membership' tool.

            Used to map userid's for Creator, Contributor DCMI
            queries.
        """
        return userid   # TODO: do lookup here

    security.declarePublic( 'getPublisher' )
    def getPublisher( self ):
        """
            Return the "formal" name of the publisher of the
            portal.
        """
        return self.publisher

    security.declarePublic( 'listAllowedVocabulary' )
    def listAllowedVocabulary( self, element, content=None, content_type=None ):
        """
            List allowed keywords for a given portal_type, or all
            possible keywords if none supplied.
        """
        spec = self.getElementSpec( element )
        if content_type is None and content:
            content_type = content.getPortalTypeName()
        return spec.getPolicy( content_type ).allowedVocabulary()

    security.declarePublic( 'listAllowedSubjects' )
    def listAllowedSubjects( self, content=None, content_type=None ):
        """
            List allowed keywords for a given portal_type, or all
            possible keywords if none supplied.
        """
        return self.listAllowedVocabulary( 'Subject', content, content_type )

    security.declarePublic( 'listAllowedFormats' )
    def listAllowedFormats( self, content=None, content_type=None ):
        """
            List the allowed 'Content-type' values for a particular
            portal_type, or all possible formats if none supplied.
        """
        return self.listAllowedVocabulary( 'Format', content, content_type )

    security.declarePublic( 'listAllowedLanguages' )
    def listAllowedLanguages( self, content=None, content_type=None ):
        """
            List the allowed language values.
        """
        return self.listAllowedVocabulary( 'Language', content, content_type )

    security.declarePublic( 'listAllowedRights' )
    def listAllowedRights( self, content=None, content_type=None ):
        """
            List the allowed values for a "Rights"
            selection list;  this gets especially important where
            syndication is involved.
        """
        return self.listAllowedVocabulary( 'Rights', content, content_type )

    security.declareProtected(ModifyPortalContent, 'setInitialMetadata')
    def setInitialMetadata( self, content ):
        """
            Set initial values for content metatdata, supplying
            any site-specific defaults.
        """
        for element, policy in self.listPolicies(content.getPortalTypeName()):

            if not getattr( content, element )():

                if policy.supplyDefault():
                    setter = getattr( content, 'set%s' % element )
                    setter( policy.defaultValue() )
                elif policy.isRequired():
                    raise MetadataError, \
                          'Metadata element %s is required.' % element

        # TODO:  Call initial_values_hook, if present


    security.declareProtected(View, 'validateMetadata')
    def validateMetadata( self, content ):
        """
            Enforce portal-wide policies about DCI, e.g.,
            requiring non-empty title/description, etc.  Called
            by the CMF immediately before saving changes to the
            metadata of an object.
        """
        for element, policy in self.listPolicies(content.getPortalTypeName()):

            value = getattr( content, element )()
            if not value and policy.isRequired():
                raise MetadataError, \
                        'Metadata element %s is required.' % element

            if value and policy.enforceVocabulary():
                values = policy.isMultiValued() and value or [ value ]
                for value in values:
                    if not value in policy.allowedVocabulary():
                        raise MetadataError, \
                        'Value %s is not in allowed vocabulary for ' \
                        'metadata element %s.' % ( value, element )

        # TODO:  Call validation_hook, if present

InitializeClass( MetadataTool )

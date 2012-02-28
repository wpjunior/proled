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
"""Evolve the ZODB from Zope X3.0 to a Zope X3.1 compatible format.

$Id: evolve1.py 39687 2005-10-28 10:14:24Z hdima $
"""
__docformat__ = "reStructuredText"
import zope.deprecation

from zope.app import zapi
from zope.app.component.interfaces.registration import IRegistrationManager
from zope.app.component.interfaces.registration import IRegisterableContainer
from zope.app.error.error import ErrorReportingUtility
from zope.app.error.interfaces import IErrorReportingUtility
from zope.app.principalannotation import PrincipalAnnotationUtility
from zope.app.principalannotation.interfaces import IPrincipalAnnotationUtility
from zope.app.component.interfaces.registration import ActiveStatus
from zope.app.component.interfaces.registration import InactiveStatus 
from zope.app.zopeappgenerations import getRootFolder

# Imports that are only available via backward-compatibility
zope.deprecation.__show__.off()
from zope.component.bbb.service import IService
from zope.app.site.interfaces import ISite, IServiceRegistration
from zope.app.utility import UtilityRegistration
zope.deprecation.__show__.on()

from zope.app.generations.utility import findObjectsProviding

generation = 1

def evolve(context):
    """Evolve the ZODB from a Zope X3.0 to a X3.1 compatible format.

    - The Principal Annotation Service was replaced by the Principal
      Annotation Utility. Thus all service registrations have to be changed to
      utility registrations. 

    - The Error Reporting Service was replaced by the Error Reporting
      Utility. Thus, all service registrations have to be changed to utility
      registrations. 

    - Component-based registrations used to keep track of their components via
      the component's path. Now it stores the component directly. All
      registrations are updated to this new format.

    - Converts all service registrations to utility registrations providing
      IService, which is the method used to simulate the old service API.

    - Remove 'RegistrationManager' object from all site management folders.

    - Remove all local adapter and utility service instances. 
    """
    root = getRootFolder(context)

    for site in findObjectsProviding(root, ISite):
        sm = site.getSiteManager()

        # Remove old registration manager instances
        for rm in findObjectsProviding(sm, IRegistrationManager):
            # Make sure that we called the new registration manager
            # which will retrieve the old one, if necessary
            zapi.getParent(rm).registrationManager = rm

            # Do a hard core delete, because I want no whining and complaining
            container = zapi.getParent(rm)
            del container._SampleContainer__data[zapi.getName(rm)]

            # Make sure the new registration manager has the correct name:
            rm.__name__ = '++registrations++'
            rm.__parent__ = container

        for reg_container in findObjectsProviding(sm, IRegisterableContainer):
            manager = reg_container.registrationManager

            # Iterate through each registration and fix it up.
            for reg in tuple(manager.values()):

                # Regardless of registration type, we want to convert the
                # component path to component  
                if ('_BBB_componentPath' in reg.__dict__ and
                    reg._BBB_componentPath is not None):

                    reg.component = reg.getComponent()
                    del reg.__dict__['_BBB_componentPath']

                # Fixup and convert service registrations
                if IServiceRegistration.providedBy(reg):
                    if reg.name == 'ErrorLogging':
                        fixupErrorLogging(reg_container, reg)

                    elif reg.name == 'PrincipalAnnotation':
                        fixupPrincipalAnnotation(reg_container, reg)

                    elif reg.name in ('Utilities', 'Adapters'):
                        # Delete the registration
                        reg.status = InactiveStatus
                        del manager[zapi.name(reg)]
                        # Delete the component
                        c = reg.component
                        del zapi.getParent(c)[zapi.name(c)]

                    else:
                        # Handle all outstanding service registrations
                        # Create a new utility registration
                        new_reg = UtilityRegistration(reg.name, IService,
                                                      reg.component)
                        manager.addRegistration(new_reg)
                        new_reg.status = ActiveStatus
                        # Delete the old registration
                        reg.status = InactiveStatus
                        del manager[zapi.getName(reg)]

                # Fixup utility registrations
                else:
                    # Getting the provided interface converts the utility
                    # registration automatically from 'interface' -> 'provided'
                    reg.provided
                    # Now let's reactivate the utility, so it will be
                    # available within the new framework
                    orig = reg.status
                    reg.status = InactiveStatus
                    reg.status = orig
                    

def fixupErrorLogging(reg_container, reg):
    # Fix up Error Reporting Service --> Utility 
    # We do this by simply removing old Error Reporting Services and their
    # registrations and then add a new error reporting utility.

    errors = reg.component
    # Set the registration to unregistered and then delete it
    reg.status = InactiveStatus
    del zapi.getParent(reg)[zapi.name(reg)]
    # Get the properties from the old error reporting service and
    # delete it
    props = errors.getProperties()
    folder = zapi.getParent(errors)
    del folder._SampleContainer__data[zapi.name(errors)]
    
    # Only add a new error reporting utility, if there is none.
    if 'ErrorReporting' not in folder:
        # Create the error reporting utility and set its properties
        utility = ErrorReportingUtility()
        utility.setProperties(**props)
        folder['ErrorReporting'] = utility
        # Register the utility and set the registration active
        reg = UtilityRegistration('', IErrorReportingUtility, utility)
        reg_manager = folder.registrationManager
        key = reg_manager.addRegistration(reg)
        reg_manager[key].status = ActiveStatus
    else:
        # If there is one, then at least move the data
        folder['ErrorReporting'].__dict__.update(props)


def fixupPrincipalAnnotation(reg_container, reg):
    # Fix up Principal Annotation Service --> Utility 
    ann = reg.component
    # Set the registration to inactive and then delete it
    reg.status = InactiveStatus
    del zapi.getParent(reg)[zapi.name(reg)]
    # Get the instance dictionary from the old principal
    # annotation service and then delete the service
    props = ann.__dict__
    name = zapi.name(ann)
    folder = zapi.getParent(ann)
    del folder._SampleContainer__data[name]
    
    # Only add a new principal annotation utility, if there is none.
    utils = [obj for obj in folder.values()
             if IPrincipalAnnotationUtility.providedBy(obj)]
    if len(utils) == 0:
        # Create the principal annotation utility and set its
        # properties
        utility = PrincipalAnnotationUtility()
        utility.__dict__.update(props)
        folder[name] = utility
        # Register the utility and set the registration active
        reg = UtilityRegistration('', IPrincipalAnnotationUtility,
                                  utility)
        reg_manager = folder.getRegistrationManager() 
        key = reg_manager.addRegistration(reg)
        reg_manager[key].status = ActiveStatus
    else:
        # If there is one, then at least move the data
        utils[0].__dict__.update(props)

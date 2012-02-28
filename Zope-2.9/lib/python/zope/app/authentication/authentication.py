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
"""Pluggable Authentication Utility implementation

$Id: authentication.py 37979 2005-08-17 11:54:56Z hdima $
"""
import zope.interface

from zope import component
from zope.schema.interfaces import ISourceQueriables
from zope.app.security.interfaces import IAuthentication, PrincipalLookupError
from zope.app.location.interfaces import ILocation
from zope.app.component import queryNextUtility
from zope.app.component.site import SiteManagementFolder

from zope.app.authentication import interfaces


class PluggableAuthentication(SiteManagementFolder):

    zope.interface.implements(
        IAuthentication,
        interfaces.IPluggableAuthentication,
        ISourceQueriables)

    authenticatorPlugins = ()
    credentialsPlugins = ()

    def __init__(self, prefix=''):
        super(PluggableAuthentication, self).__init__()
        self.prefix = prefix

    def authenticate(self, request):
        authenticatorPlugins = [
            component.queryUtility(interfaces.IAuthenticatorPlugin,
                                  name, context=self)
            for name in self.authenticatorPlugins]
        for name in self.credentialsPlugins:
            credplugin = component.queryUtility(
                interfaces.ICredentialsPlugin, name, context=self)
            if credplugin is None:
                continue
            credentials = credplugin.extractCredentials(request)
            for authplugin in authenticatorPlugins:
                if authplugin is None:
                    continue
                info = authplugin.authenticateCredentials(credentials)
                if info is None:
                    continue
                principal = component.getMultiAdapter((info, request),
                    interfaces.IAuthenticatedPrincipalFactory)(self)
                principal.id = self.prefix + info.id
                return principal
        return None

    def getPrincipal(self, id):
        if not id.startswith(self.prefix):
            next = queryNextUtility(self, IAuthentication)
            if next is None:
                raise PrincipalLookupError(id)
            return next.getPrincipal(id)
        id = id[len(self.prefix):]
        for name in self.authenticatorPlugins:
            authplugin = component.queryUtility(
                interfaces.IAuthenticatorPlugin, name, context=self)
            if authplugin is None:
                continue
            info = authplugin.principalInfo(id)
            if info is None:
                continue
            principal = interfaces.IFoundPrincipalFactory(info)(self)
            principal.id = self.prefix + info.id
            return principal
        next = queryNextUtility(self, IAuthentication)
        if next is not None:
            return next.getPrincipal(self.prefix + id)
        raise PrincipalLookupError(id)

    def getQueriables(self):
        for name in self.authenticatorPlugins:
            authplugin = component.queryUtility(
                interfaces.IAuthenticatorPlugin, name, context=self)
            if authplugin is None:
                continue
            queriable = component.queryMultiAdapter((authplugin, self),
                interfaces.IQueriableAuthenticator)
            if queriable is not None:
                yield name, queriable

    def unauthenticatedPrincipal(self):
        return None

    def unauthorized(self, id, request):
        challengeProtocol = None

        for name in self.credentialsPlugins:
            credplugin = component.queryUtility(interfaces.ICredentialsPlugin,
                                                name)
            if credplugin is None:
                continue
            protocol = getattr(credplugin, 'challengeProtocol', None)
            if challengeProtocol is None or protocol == challengeProtocol:
                if credplugin.challenge(request):
                    if protocol is None:
                        return
                    elif challengeProtocol is None:
                        challengeProtocol = protocol

        if challengeProtocol is None:
            next = queryNextUtility(self, IAuthentication)
            if next is not None:
                next.unauthorized(id, request)

    def logout(self, request):
        challengeProtocol = None

        for name in self.credentialsPlugins:
            credplugin = component.queryUtility(interfaces.ICredentialsPlugin,
                                                name)
            if credplugin is None:
                continue
            protocol = getattr(credplugin, 'challengeProtocol', None)
            if challengeProtocol is None or protocol == challengeProtocol:
                if credplugin.logout(request):
                    if protocol is None:
                        return
                    elif challengeProtocol is None:
                        challengeProtocol = protocol

        if challengeProtocol is None:
            next = queryNextUtility(self, IAuthentication)
            if next is not None:
                next.logout(request)


class QuerySchemaSearchAdapter(object):
    """Performs schema-based principal searches on behalf of a PAU.

    Delegates the search to the adapted authenticator (which also provides
    IQuerySchemaSearch) and prepends the PAU prefix to the resulting principal
    IDs.
    """
    component.adapts(
        interfaces.IQuerySchemaSearch,
        interfaces.IPluggableAuthentication)

    zope.interface.implements(
        interfaces.IQueriableAuthenticator,
        interfaces.IQuerySchemaSearch,
        ILocation)

    def __init__(self, authplugin, pau):
        if ILocation.providedBy(authplugin):
            self.__parent__ = authplugin.__parent__
            self.__name__ = authplugin.__name__
        else:
            self.__parent__ = pau
            self.__name__ = ""
        self.authplugin = authplugin
        self.pau = pau
        self.schema = authplugin.schema

    def search(self, query, start=None, batch_size=None):
        for id in self.authplugin.search(query, start, batch_size):
            yield self.pau.prefix + id

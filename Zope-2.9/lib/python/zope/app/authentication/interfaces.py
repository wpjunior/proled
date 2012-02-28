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
"""Pluggable Authentication Utility Interfaces

$Id: interfaces.py 39687 2005-10-28 10:14:24Z hdima $
"""
__docformat__ = "reStructuredText"

import zope.interface
import zope.schema
from zope.app.i18n import ZopeMessageFactory as _
from zope.app.security.interfaces import ILogout
from zope.app.container.constraints import contains, containers
from zope.app.container.interfaces import IContainer


class IPlugin(zope.interface.Interface):
    """A plugin for a pluggable authentication component."""


class IPluggableAuthentication(ILogout, IContainer):
    """Provides authentication services with the help of various plugins."""

    contains(IPlugin)

    credentialsPlugins = zope.schema.List(
        title=_('Credentials Plugins'),
        value_type=zope.schema.Choice(vocabulary='CredentialsPlugins'),
        default=[],
        )

    authenticatorPlugins = zope.schema.List(
        title=_('Authenticator Plugins'),
        value_type=zope.schema.Choice(vocabulary='AuthenticatorPlugins'),
        default=[],
        )

    prefix = zope.schema.TextLine(
        title=_('Prefix'),
        default=u'',
        required=True,
        readonly=True,
        )

    def logout(request):
        """Performs a logout by delegating to its authentictor plugins."""


class ICredentialsPlugin(IPlugin):
    """Handles credentials extraction and challenges per request."""

    containers(IPluggableAuthentication)

    challengeProtocol = zope.interface.Attribute(
        """A challenge protocol used by the plugin.

        If a credentials plugin works with other credentials pluggins, it
        and the other cooperating plugins should specify a common (non-None)
        protocol. If a plugin returns True from its challenge method, then
        other credentials plugins will be called only if they have the same
        protocol.
        """)

    def extractCredentials(request):
        """Ties to extract credentials from a request.

        A return value of None indicates that no credentials could be found.
        Any other return value is treated as valid credentials.
        """

    def challenge(request):
        """Possibly issues a challenge.

        This is typically done in a protocol-specific way.

        If a challenge was issued, return True, otherwise return False.
        """

    def logout(request):
        """Possibly logout.

        If a logout was performed, return True, otherwise return False.
        """

class IAuthenticatorPlugin(IPlugin):
    """Authenticates a principal using credentials.

    An authenticator may also be responsible for providing information
    about and creating principals.
    """
    containers(IPluggableAuthentication)

    def authenticateCredentials(credentials):
        """Authenticates credentials.

        If the credentials can be authenticated, return an object that provides
        IPrincipalInfo. If the plugin cannot authenticate the credentials,
        returns None.
        """

    def principalInfo(id):
        """Returns an IPrincipalInfo object for the specified principal id.

        If the plugin cannot find information for the id, returns None.
        """

class IPasswordManager(zope.interface.Interface):
    """Password manager."""

    def encodePassword(password):
        """Return encoded data for the password."""

    def checkPassword(storedPassword, password):
        """Return whether the password coincide with the storedPassword."""

class IPrincipalInfo(zope.interface.Interface):
    """Minimal information about a principal."""

    id = zope.interface.Attribute("The principal id.")

    title = zope.interface.Attribute("The principal title.")

    description = zope.interface.Attribute("A description of the principal.")


class IPrincipalFactory(zope.interface.Interface):
    """A principal factory."""

    def __call__(authentication):
        """Creates a principal.

        The authentication utility that called the factory is passed
        and should be included in the principal-created event.
        """


class IFoundPrincipalFactory(IPrincipalFactory):
    """A found principal factory."""


class IAuthenticatedPrincipalFactory(IPrincipalFactory):
    """An authenticated principal factory."""


class IPrincipalCreated(zope.interface.Interface):
    """A principal has been created."""

    principal = zope.interface.Attribute("The principal that was created")

    authentication = zope.interface.Attribute(
        "The authentication utility that created the principal")

    info = zope.interface.Attribute("An object providing IPrincipalInfo.")


class IAuthenticatedPrincipalCreated(IPrincipalCreated):
    """A principal has been created by way of an authentication operation."""

    request = zope.interface.Attribute(
        "The request the user was authenticated against")


class AuthenticatedPrincipalCreated:
    """
    >>> from zope.interface.verify import verifyObject
    >>> event = AuthenticatedPrincipalCreated("authentication", "principal",
    ...     "info", "request")
    >>> verifyObject(IAuthenticatedPrincipalCreated, event)
    True
    """

    zope.interface.implements(IAuthenticatedPrincipalCreated)

    def __init__(self, authentication, principal, info, request):
        self.authentication = authentication
        self.principal = principal
        self.info = info
        self.request = request


class IFoundPrincipalCreated(IPrincipalCreated):
    """A principal has been created by way of a search operation."""


class FoundPrincipalCreated:
    """
    >>> from zope.interface.verify import verifyObject
    >>> event = FoundPrincipalCreated("authentication", "principal",
    ...     "info")
    >>> verifyObject(IFoundPrincipalCreated, event)
    True
    """

    zope.interface.implements(IFoundPrincipalCreated)

    def __init__(self, authentication, principal, info):
        self.authentication = authentication
        self.principal = principal
        self.info = info


class IQueriableAuthenticator(zope.interface.Interface):
    """Indicates the authenticator provides a search UI for principals."""


class IQuerySchemaSearch(zope.interface.Interface):
    """An interface for searching using schema-constrained input."""

    schema = zope.interface.Attribute("""
        The schema that constrains the input provided to the search method.

        A mapping of name/value pairs for each field in this schema is used
        as the query argument in the search method.
        """)

    def search(query, start=None, batch_size=None):
        """Returns an iteration of principal IDs matching the query.

        query is a mapping of name/value pairs for fields specified by the
        schema.

        If the start argument is provided, then it should be an
        integer and the given number of initial items should be
        skipped.

        If the batch_size argument is provided, then it should be an
        integer and no more than the given number of items should be
        returned.
        """

class IGroupAdded(zope.interface.Interface):
    """A group has been added."""

    group = zope.interface.Attribute("""The group that was defined""")


class GroupAdded:
    """
    >>> from zope.interface.verify import verifyObject
    >>> event = GroupAdded("group")
    >>> verifyObject(IGroupAdded, event)
    True
    """

    zope.interface.implements(IGroupAdded)

    def __init__(self, group):
        self.group = group

    def __repr__(self):
        return "<GroupAdded %r>" % self.group.id

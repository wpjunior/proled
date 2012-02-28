from zope.app.component.site import UtilityRegistration
from zope.app.security.interfaces import IAuthentication
from zope.app.authentication.interfaces import ICredentialsPlugin
from zope.app.authentication.interfaces import IAuthenticatorPlugin

def pluggableAuthenticationRegistration(view, component):
    return UtilityRegistration(u'', IAuthentication, component)

def credentialsPluginRegistration(view, name, component):
    return UtilityRegistration(name, ICredentialsPlugin, component)

def authenticatorPluginRegistration(view, name, component):
    return UtilityRegistration(name, IAuthenticatorPlugin, component)


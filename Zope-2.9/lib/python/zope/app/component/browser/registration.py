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
"""General registry-related views

$Id: registration.py 40187 2005-11-16 23:37:25Z srichter $
"""
import warnings

from zope.security.proxy import removeSecurityProxy

from zope.app import zapi
from zope.app.container.browser.adding import Adding
from zope.app.container.interfaces import INameChooser
from zope.app.form.browser.widget import SimpleInputWidget
from zope.app.i18n import ZopeMessageFactory as _
from zope.app.publisher.browser import BrowserView
from zope.app.component import interfaces
from zope.app.component.interfaces.registration import ActiveStatus
from zope.app.component.interfaces.registration import InactiveStatus

class RegistrationView(BrowserView):
    """View for registerable objects that have at most one registration.

    If the object has more than one registration, this performs a
    redirection to the 'registrations.html' view.
    """
    def __init__(self, context, request):
        super(RegistrationView, self).__init__(context, request)
        useconfig = interfaces.registration.IRegistered(self.context)
        self.registrations = useconfig.registrations()

    def update(self):
        """Make changes based on the form submission."""
        if len(self.registrations) > 1:
            self.request.response.redirect("registrations.html")
            return
        if "deactivate" in self.request:
            self.registrations[0].status = InactiveStatus
        elif "activate" in self.request:
            if not self.registrations:
                # create a registration:
                self.request.response.redirect("addRegistration.html")
                return
            self.registrations[0].status = ActiveStatus

    def active(self):
        return self.registrations[0].status == ActiveStatus

    def registered(self):
        return bool(self.registrations)

    def registration(self):
        """Return the first registration.

        If there are no registrations, raises an error.
        """
        return {'url': zapi.absoluteURL(self.registrations[0], self.request),
                'details': zapi.queryMultiAdapter(
                    (self.registrations[0], self.request), name='details')
                }


class Registered(object):
    """View for registerable objects with more than one registration."""

    def registrations(self):
        registered = interfaces.registration.IRegistered(self.context)
        return [
            {'name': zapi.name(reg),
             'url': zapi.absoluteURL(reg, self.request),
             'status': reg.status,
             'details': zapi.queryMultiAdapter((reg, self.request),
                                               name='details')}
            for reg in registered.registrations()]


#############################################################################
# BBB: Only for backward compatibility. 12/07/2004
class ComponentPathWidget(SimpleInputWidget):
    """Widget for displaying component paths

    The widget doesn't actually allow editing. Rather it gets the
    value by inspecting its field's context. If the context is an
    IComponentRegistration, then it just gets its value from the
    component using the field's name. Otherwise, it uses the path to
    the context.
    """

    def __init__(self, *args, **kw):
        warnings.warn(
            "Use of `ComponentPathWidget` deprecated, since the "
            "registration code now uses the component directly instead "
            "of using the component's path.",
            DeprecationWarning, stacklevel=2,
            )
        super(ComponentPathWidget, self).__init__(*args, **kw)

    def __call__(self):
        """See zope.app.browser.interfaces.form.IBrowserWidget"""
        # Render as a link to the component
        field = self.context
        context = field.context
        if interfaces.registration.IRegistration.providedBy(context):
            # It's a registration object. Just get the corresponding attr
            path = getattr(context, field.__name__)
            # The path may be relative; then interpret relative to ../..
            if not path.startswith("/"):
                context = zapi.traverse(context, "../..")
            component = zapi.traverse(context, path)
        else:
            # It must be a component that is about to be configured.
            component = context
            # Always use a relative path (just the component name)
            path = zapi.name(context)

        url = zapi.absoluteURL(component, self.request)

        return ('<a href="%s/@@SelectedManagementView.html">%s</a>'
                % (url, path))

    def hidden(self):
        """See zope.app.browser.interfaces.form.IBrowserWidget"""
        return ''

    def hasInput(self):
        """See zope.app.form.interfaces.IWidget"""
        return 1

    def getInputValue(self):
        """See zope.app.form.interfaces.IWidget"""
        field = self.context
        context = field.context
        if interfaces.registration.IRegistration.providedBy(context):
            # It's a registration object. Just get the corresponding attr
            path = getattr(context, field.getName())
        else:
            # It must be a component that is about to be configured.
            # Always return a relative path (just the component name)
            path = zapi.name(context)

        return path
#############################################################################


class ComponentWidget(SimpleInputWidget):
    """Widget for displaying/entering component paths that point to components.

    The widget doesn't actually allow editing. Rather it gets the
    value by inspecting its field's context. If the context is an
    IComponentRegistration, then it just gets its value from the
    component using the field's name. Otherwise, it uses the path to
    the context.
    """

    def __call__(self):
        """See zope.app.browser.interfaces.form.IBrowserWidget"""
        # Render as a link to the component
        field = self.context
        context = field.context
        if interfaces.registration.IRegistration.providedBy(context):
            # It's a registration object. Just get the corresponding attr
            component = getattr(context, field.__name__)
            path = zapi.getPath(component)
        else:
            # It must be a component that is about to be configured.
            component = context
            # Always use a relative path (just the component name)
            path = zapi.name(context)

        url = zapi.absoluteURL(component, self.request)

        return ('<a href="%s/@@SelectedManagementView.html">%s</a>'
                % (url, path))

    def hidden(self):
        """See zope.app.browser.interfaces.form.IBrowserWidget"""
        return ''

    def hasInput(self):
        """See zope.app.form.interfaces.IWidget"""
        return 1

    def getInputValue(self):
        """See zope.app.form.interfaces.IWidget"""
        field = self.context
        context = field.context
        if interfaces.registration.IRegistration.providedBy(context):
            # It's a registration object. Just get the corresponding attr
            return getattr(context, field.getName())

        # It must be a component that is about to be configured.
        return context


class AddComponentRegistration(BrowserView):
    """View for adding component registrations

    This class is used to define registration add forms.  It provides
    the ``add`` and ``nextURL`` methods needed when creating add forms
    for non-IAdding objects.  We need this here because registration
    add forms are views of the component being configured.
    """

    def add(self, registration):
        """Add a registration

        We are going to add the registration to the local
        registration manager. We don't want to hard code the name of
        this, so we'll simply scan the containing folder and add the
        registration to the first registration manager we find.
        """
        component = self.context

        # Get the registration manager for this folder
        rm = component.__parent__.registrationManager
        rm.addRegistration(registration)
        return registration

    def nextURL(self):
        return "@@SelectedManagementView.html"


class RegistrationAdding(Adding):
    """Adding subclass for adding registrations."""
    menu_id = "add_registration"

    def nextURL(self):
        return zapi.absoluteURL(self.context, self.request)


class EditRegistration(BrowserView):
    """A view on a registration manager, used by registrations.pt."""

    def update(self):
        """Perform actions depending on user input."""

        if 'keys' in self.request:
            k = self.request['keys']
        else:
            k = []

        msg = 'You must select at least one item to use this action'

        if 'remove_submit' in self.request:
            if not k: return msg
            self.remove_objects(k)
        elif 'refresh_submit' in self.request:
            pass # Nothing to do

        return ''

    def remove_objects(self, key_list):
        """Unregister and remove the directives from the container."""
        container = self.context
        for name in key_list:
            container[name].status = InactiveStatus
            del container[name]

    def registrationInfo(self):
        """Render View for each directives."""
        return [
            {'name': name,
             'url': zapi.absoluteURL(reg, self.request),
             'active': reg.status == ActiveStatus,
             'details': zapi.queryMultiAdapter((reg, self.request),
                                               name='details')}
            for name, reg in self.context.items()]

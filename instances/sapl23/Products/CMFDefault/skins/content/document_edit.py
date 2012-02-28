## Script (Python) "document_edit"
##parameters=text_format, text, file='', SafetyBelt='', change_and_view=''
##title=Edit a document
##
from Products.PythonScripts.standard import urlencode
from Products.CMFDefault.exceptions import EditingConflict
from Products.CMFDefault.exceptions import IllegalHTML
from Products.CMFDefault.exceptions import ResourceLockedError
from Products.CMFDefault.utils import scrubHTML

try:
    text = scrubHTML( text ) # Strip Javascript, etc.
    context.edit( text_format
                , text
                , file
                , safety_belt=SafetyBelt
                )
except (ResourceLockedError, EditingConflict, IllegalHTML), msg:
    message = msg
    action_id = 'edit'
else:
    message = 'Document changed.'
    if change_and_view:
        action_id = 'view'
    else:
        action_id = 'edit'

target = '%s/%s' % ( context.absolute_url(),
                     context.getTypeInfo().getActionById(action_id) )
query = urlencode( {'portal_status_message': message} )
context.REQUEST.RESPONSE.redirect( '%s?%s' % (target, query) )

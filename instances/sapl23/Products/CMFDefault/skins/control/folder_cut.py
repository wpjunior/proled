## Script (Python) "folder_cut"
##title=Cut objects from a folder and copy to the clipboard
##parameters=
REQUEST=context.REQUEST
if REQUEST.has_key('ids'):
  context.manage_cutObjects(REQUEST['ids'], REQUEST)
  return REQUEST.RESPONSE.redirect(context.absolute_url() + '/folder_contents?portal_status_message=Item(s)+Cut.')
else:
  return REQUEST.RESPONSE.redirect(context.absolute_url() + '/folder_contents?portal_status_message=Please+select+one+or+more+items+to+cut+first.')

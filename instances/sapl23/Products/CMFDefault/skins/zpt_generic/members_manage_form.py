##parameters=b_start=0, ids=(), members_new='', members_delete=''
##
from ZTUtils import Batch
from Products.CMFCore.utils import getToolByName
from Products.CMFDefault.utils import html_marshal

mtool = getToolByName(script, 'portal_membership')
rtool = getToolByName(script, 'portal_registration')


form = context.REQUEST.form
if members_delete and \
        context.validateMemberIds(**form) and \
        context.members_delete_control(**form) and \
        context.setRedirect(mtool, 'global/manage_members', b_start=b_start):
    return
elif members_new and \
        context.setRedirect(rtool, 'user/join', b_start=b_start):
    return


options = {}

target = mtool.getActionInfo('global/manage_members')['url']

members = mtool.listMembers()
batch_obj = Batch(members, 25, b_start, orphan=0)
items = []
for member in batch_obj:
    member_id = member.getId()
    login_time = member.getProperty('login_time')
    member_login = login_time == '2000/01/01' and '---' or login_time.Date()
    member_home = mtool.getHomeUrl(member_id, verifyPermission=0)
    items.append( {'checkbox': 'cb_%s' % member_id,
                   'email': member.getProperty('email'),
                   'login': member_login,
                   'id': member_id,
                   'home': member_home } )
navigation = context.getBatchNavigation(batch_obj, target,
                                        'member', 'members')
options['batch'] = { 'listItemInfos': tuple(items),
                     'navigation': navigation }

hidden_vars = []
for name, value in html_marshal(b_start=b_start):
    hidden_vars.append( {'name': name, 'value': value} )
buttons = []
buttons.append( {'name': 'members_new', 'value': 'New...'} )
if items:
    buttons.append( {'name': 'members_delete', 'value': 'Delete'} )
options['form'] = { 'action': target,
                    'listHiddenVarInfos': tuple(hidden_vars),
                    'listButtonInfos': tuple(buttons) }

return context.members_manage_template(**options)

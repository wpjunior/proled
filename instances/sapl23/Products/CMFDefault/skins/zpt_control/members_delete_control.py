##parameters=ids, **kw
##title=Delete members
##
from Products.CMFCore.utils import getToolByName

mtool = getToolByName(script, 'portal_membership')

mtool.deleteMembers(ids,REQUEST=context.REQUEST)

return context.setStatus( True, 'Selected member%s deleted.' %
                                ( len(ids) != 1 and 's' or '' ) )

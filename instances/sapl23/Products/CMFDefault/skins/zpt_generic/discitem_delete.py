#
# discitem_delete
#
parent = context.inReplyTo()
talkback = context.portal_discussion.getDiscussionFor(parent)
talkback.deleteReply( context.getId() )
 
context.REQUEST['RESPONSE'].redirect( '%s?portal_status_message=Reply+deleted'
                                    % parent.absolute_url()
                                    )

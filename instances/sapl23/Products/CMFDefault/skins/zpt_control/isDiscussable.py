## Script (Python) "isDiscussable"
##title=Return whether the context is discussable or not.
##parameters=
# this script is deprecated; *metadata_edit_form no longer depends on it
if hasattr(context, 'allow_discussion'):
    return context.allow_discussion
else:
    return None

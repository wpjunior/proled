##parameters=ids, delta, **kw
##
subset_ids = [ obj.getId() for obj in context.listFolderContents() ]
try:
    try:
        attempt = context.moveObjectsUp(ids, delta, subset_ids=subset_ids)
    except TypeError:
        # Zope 2.7.0
        attempt = context.moveObjectsUp(ids, delta)
    if attempt:
        return context.setStatus( True, '%d item%s moved up.' %
                                    ( attempt, (attempt != 1 and 's' or '') ) )
    else:
        return context.setStatus(False, 'Nothing to change.')
except ValueError, errmsg:
    return context.setStatus(False, 'ValueError: %s' % errmsg)

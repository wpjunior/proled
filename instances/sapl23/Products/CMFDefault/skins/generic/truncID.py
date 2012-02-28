## Script (Python) "truncID.py $Revision: 34933 $"
##parameters=objID, size 
##title=return truncated objID
##
if len(objID) > size:
    return objID[:size] + '...'
else:
   return objID

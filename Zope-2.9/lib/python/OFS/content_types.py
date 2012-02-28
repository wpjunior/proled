##############################################################################
#
# Copyright (c) 2002 Zope Corporation and Contributors. All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE
#
##############################################################################
"""A utility module for content-type handling.

$Id: content_types.py 41015 2005-12-24 04:55:14Z andreasjung $
"""

import warnings
warnings.warn('Using OFS.content_types is deprecated (will be removed in Zope '
              '2.11). Instead use zope.app.contenttypes.', 
              DeprecationWarning,
              stacklevel=2) 

from zope.app.content_types import text_type, guess_content_type, add_files

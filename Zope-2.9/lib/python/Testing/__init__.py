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
"""
Set up testing environment

$Id: __init__.py 40222 2005-11-18 15:46:28Z andreasjung $
"""
import os

import App.config

cfg = App.config.getConfiguration()

# Set testinghome to the Testing package directory
cfg.testinghome = os.path.dirname(__file__)

# Make sure this change is propogated to all the legacy locations for
# this information.
App.config.setConfiguration(cfg)

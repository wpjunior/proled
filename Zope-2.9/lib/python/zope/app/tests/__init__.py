#
# This file is necessary to make this directory a package.

##############################################################################
# BBB: backward-comptibility; 12/18/2004

import sys
from zope.deprecation.deprecation import DeprecationProxy
import zope.app

def deprecate(module):
    depmodule = DeprecationProxy(module)
    depmodule.deprecate(module.__dict__.keys(),
                        'The testing support code moved from zope.app.tests '
                        'to zope.app.testing. This reference go away in Zope '
                        'X3.3.')
    return depmodule


from zope.app.testing import placelesssetup
sys.modules['zope.app.tests.placelesssetup'] = deprecate(placelesssetup)
from zope.app.testing import setup
sys.modules['zope.app.tests.setup'] = deprecate(setup)
from zope.app.testing import dochttp
sys.modules['zope.app.tests.dochttp'] = deprecate(dochttp)
from zope.app.testing import functional
sys.modules['zope.app.tests.functional'] = deprecate(functional)
from zope.app.testing import ztapi
sys.modules['zope.app.tests.ztapi'] = deprecate(ztapi)
#############################################################################

import unittest
from zope.testing import doctest
from zope.app.testing.setup import placefulSetUp
from zope.app.testing.setup import placefulTearDown

def setUp(self):
    placefulSetUp(True)

def tearDown(self):
    placefulTearDown()

def test_suite():
    return unittest.TestSuite((
        doctest.DocFileSuite('../tools.txt',
                             setUp=setUp,
                             tearDown=tearDown),
    ))

if __name__=='main':
    unittest.main(defaultTest='test_suite')


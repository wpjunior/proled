"""Tests of the 'partial' annotatable adapter.

"""
__docformat__ = "reStructuredText"

import zope.testing.doctest

import zope.app.annotation.attribute
import zope.app.annotation.interfaces
import zope.app.testing.placelesssetup
import zope.app.testing.ztapi


def setUp(test):
    zope.app.testing.placelesssetup.setUp(test)
    zope.app.testing.ztapi.provideAdapter(
        zope.app.annotation.interfaces.IAttributeAnnotatable,
        zope.app.annotation.interfaces.IAnnotations,
        zope.app.annotation.attribute.AttributeAnnotations)

def tearDown(test):
    zope.app.testing.placelesssetup.tearDown(test)


def test_suite():
    return zope.testing.doctest.DocFileSuite(
        "partial.txt", setUp=setUp, tearDown=tearDown)

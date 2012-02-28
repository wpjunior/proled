##############################################################################
#
# Copyright (c) 2001, 2002 Zope Corporation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""Provide persistent wrappers for objects that cannot derive from
persistence for some reason.

$Id$
"""
from persistent import Persistent, GHOST
from zope.interface import implementedBy
from zope.security.checker import selectChecker

class SecurityDescriptor(object):
    """ SecurityDescriptor is used by Struct to return the
    checker for the proxied object when its an instance,
    and return the checker for the Struct class, when its a class
    """

    def __get__(self, inst, cls=None):
        if inst is None:
            return selectChecker(cls)
        else:
            # This is *VERY* tricky. There is a possibility that
            # the object was loaded, but not active by the time
            # __proxied__ needs to be accessed, which results
            # in an AttributeError here, which is swallowed
            # somewere inside the security machinery,
            # and then the object ends up using _defaultChecker
            #
            # Added the same code below, in ClassDescriptor,
            # though I'm not sure it is really needed there.
            if inst._p_state == GHOST:
                inst._p_activate()
            return selectChecker(inst.__proxied__)

class ClassDescriptor(object):
    """ ClassDescriptor is used by Struct to return the
    real class for Struct when a class is being used, and return
    the proxied object's class when its an instance.
    """

    def __get__(self, inst, cls=None):
        if inst is None:
            return cls
        else:
            if inst._p_state == GHOST:
                inst._p_activate()
            return inst.__proxied__.__class__


# Put those attributes in a list so its easier to add/remove
# when needed.
struct_attrs = ['__proxied__',
                '__dict__',
                '__reduce_ex__',
                '__reduce__',
                '__getstate__',
                '__setstate__',
                '__Security_checker__']

class Struct(Persistent):
  """Wraps a non-persistent object, assuming that *all* changes are
  made through external attribute assignments.
  """

  # TODO to do this right and expose both IPersistent and the
  # underlying object's interfaces, we'd need to use a specialized
  # descriptor.  This would create to great a dependency on
  # zope.interface.

  __class__ = ClassDescriptor()
  __Security_checker__ = SecurityDescriptor()


  def __init__(self, o):
      self.__proxied__ = o

  def __getattribute__(self, name):
      if name.startswith('_p_') or name in struct_attrs:
          v = Persistent.__getattribute__(self, name)
          # Handle descriptors here, eg: __Security_checker__
          # is a descriptor for Struct objects.
          if hasattr(v, '__get__'):
              return v.__get__(self, type(self))
          return v
      # TODO This is butt ugly. See the comment on SecurityDescriptor.
      if self._p_state == GHOST:
          self._p_activate()
      proxied = self.__proxied__
      v = getattr(proxied, name)
      # And also handle descriptors for the proxied object,
      # but using the proxied object on __get__ calls.
      if hasattr(v, '__get__'):
          # We should call it only if it came from the class,
          # otherwise its a descriptor being used as an instance
          # attribute, so just return it.
          if (hasattr(proxied, '__class__') and
              getattr(proxied.__class__, name) is v):
              return v.__get__(proxied, type(proxied))
      return v

  def __setattr__(self, name, v):
      if name.startswith('_p_') or name in struct_attrs:
          return Persistent.__setattr__(self, name, v)
      # Set _p_changed before calling the mutator on the
      # proxied object, so we have the object marked
      # as dirty even if an exception takes place later.
      self._p_changed = 1
      setattr(self.__proxied__, name, v)

  def __delattr__(self, name):
      if name.startswith('_p_') or name in struct_attrs:
          return Persistent.__delattr__(self, name)
      # Set _p_changed before deleting the attribute. See
      # comment above, on __setattr__
      self._p_changed = 1
      delattr(self.__proxied__, name, v)


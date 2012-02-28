##############################################################################
# Copyright (c) 2003 Zope Corporation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
##############################################################################
"""Demo file-system implementation, for testing

$Id: demofs.py 27459 2004-09-07 01:45:52Z shane $
"""
execute = 1
read = 2
write = 4

class File(object):
    type = 'f'
    modified=None

    def __init__(self):
        self.access = {'anonymous': read}

    def accessable(self, user, access=read):
        return (user == 'root'
                or (self.access.get(user, 0) & access)
                or (self.access.get('anonymous', 0) & access)
                )

    def grant(self, user, access):
        self.access[user] = self.access.get(user, 0) | access

    def revoke(self, user, access):
        self.access[user] = self.access.get(user, 0) ^ access

class Directory(File):

    type = 'd'

    def __init__(self):
        super(Directory, self).__init__()
        self.files = {}

    def get(self, name, default=None):
        return self.files.get(name, default)

    def __getitem__(self, name):
        return self.files[name]

    def __setitem__(self, name, v):
        self.files[name] = v

    def __delitem__(self, name):
        del self.files[name]

    def __contains__(self, name):
        return name in self.files

    def __iter__(self):
        return iter(self.files)

# Copyright (c) 2013 Alon Swartz <alon@turnkeylinux.org>
#
# This file is part of OctoHub.
#
# OctoHub is free software; you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software
# Foundation; either version 3 of the License, or (at your option) any later
# version.

class AttrDict(dict):
    """Attribute Dictionary (set and access attributes 'pythonically')"""
    def __getattr__(self, name):
        if name in self:
            return self[name]
        raise AttributeError('no such attribute: %s' % name)

    def __setattr__(self, name, val):
        self[name] = val


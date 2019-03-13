# py23 compatible
from __future__ import print_function
from __future__ import division
from __future__ import unicode_literals
from __future__ import absolute_import

import sys

class NoneDict(dict):
    """
    None dict is a dict that returns None on key it does not have
    """

    def __init__(self, other):
        for key in other:
            self[key] = other[key]

    def __getitem__(self, key):
        if key not in self:
            return None
        return dict.__getitem__(self, key)


def _fix_all(list):
    """
    2 to 3 compatiblity helper method dealing with __all__ and str/unicode
    """
    if sys.version_info >= (3, 0):
        return list
    return [str(x) for x in list]


def get_input(prompt=""):
    """
    2 to 3 compatiblity helper method dealing with raw_input -> input
    """
    if sys.version_info >= (3, 0):
        return input(prompt)
    else:
        return raw_input(prompt)


def to_raw(str):
    """
    2 to 3 compatiblity helper method dealing with str->bytes
    """
    if sys.version_info >= (3, 0):
        return str.encode("utf-8")
    else:
        return str


def to_str(raw):
    """
    2 to 3 compatiblity helper method dealing with bytes->str
    """
    if sys.version_info >= (3, 0):
        return raw.decode("utf-8")
    else:
        return raw


class Counter(object):
    def __init__(self):
        self.state = 0

    def get(self):
        s = self.state
        self.state += 1
        return s

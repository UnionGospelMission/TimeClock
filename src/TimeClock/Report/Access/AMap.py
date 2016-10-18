import types

from zope.interface import implementer

from TimeClock.Report.IAccess.IAMap import IAMap
from TimeClock.Util.registerAdapter import adapter
from TimeClock.Utils import coerce


@adapter(type(None), IAMap)
@adapter(dict, IAMap)
@implementer(IAMap)
class AMap(object):
    __slots__ = '_other'

    @coerce
    def __init__(self, other: dict=None):
        if other is None:
            other = {}
        self._other = other.copy()

    def get(self, key):
        return self._other[key]

    def set(self, key, value):
        self._other[key] = value

    def iter(self):
        yield from self._other.items()

    def __contains__(self, item):
        return item in self._other

    def __str__(self):
        return str(self._other)

    def __repr__(self):
        return repr(self._other)

    def copy(self):
        return self._other.copy()

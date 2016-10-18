import time

from zope.interface import Interface
from zope.interface.interface import InterfaceClass


class Log(object):
    __slots__ = ['_parent']

    def __init__(self, parent):
        self._parent = parent

    def log(self, level, obj):
        if isinstance(obj, InterfaceClass):
            obj = '<Interface attributes=[%s]>' % str.join(', ', obj.names())
        msg = '%02f %s:  %r' % (time.time(), level, obj)
        self._parent.log(msg)

    def progress(self, progress):
        if hasattr(self._parent, 'progress'):
            self._parent.progress(progress)

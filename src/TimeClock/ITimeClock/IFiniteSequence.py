from collections.abc import Iterable

from twisted.python.components import registerAdapter
from zope.interface.common.sequence import IFiniteSequence as ifs
from zope.interface.interface import InterfaceClass


class iface_mixin(InterfaceClass):
    def implementedBy(self, obj):
        if issubclass(obj, (list, tuple)):
            return True
        return super().implementedBy(obj)

    def providedBy(self, obj):
        if isinstance(obj, (list, tuple)):
            return True
        return super().providedBy(obj)


IFiniteSequence = iface_mixin("IFiniteSequence", (ifs,), {})


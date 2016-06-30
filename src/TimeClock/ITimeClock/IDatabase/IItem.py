from zope.interface import Interface

from TimeClock.Util import fromMethod


class IItem(Interface):
    @fromMethod
    def powerUp(object, iface):
        pass

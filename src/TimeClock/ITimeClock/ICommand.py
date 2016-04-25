from zope.interface import Interface, Attribute

from TimeClock.ITimeClock.IDatabase.IPermission import IPermission
from TimeClock.ITimeClock.IDatabase.IPerson import IPerson
from TimeClock.Util import fromFunction
from TimeClock.Util.subclass import Subclass
from TimeClock.Utils import overload


class ICommand(Interface):
    name = Attribute("name")

    @overload
    def hasPermission(caller: IPerson) -> bool:
        pass

    @fromFunction
    @overload
    def hasPermission(permissions: [IPermission]) -> bool:
        pass

    def execute(caller: Subclass[Interface], *parameters: object):
        pass

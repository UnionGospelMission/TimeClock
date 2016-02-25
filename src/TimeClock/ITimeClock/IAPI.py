from zope.interface import Interface, Attribute

from TimeClock.ITimeClock.IDatabase.IPermission import IPermission
from TimeClock.ITimeClock.ICommand import ICommand
from TimeClock.Util import fromFunction
from TimeClock.Utils import overload


class IAPI(Interface):
    name = Attribute("name")
    @overload
    def getCommands() -> [ICommand]:
        pass
    @fromFunction
    @overload
    def getCommands(permissions: [IPermission]) -> [ICommand]:
        pass
    def __getitem__(value: str) -> ICommand:
        pass
    @overload
    def getCommandNames() -> [str]:
        pass
    @fromFunction
    @overload
    def getCommandNames(permissions: [IPermission]) -> [str]:
        pass

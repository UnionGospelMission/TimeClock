from zope.interface import implementer

from TimeClock import AD
from TimeClock.Database.Commands.CommandEvent import CommandEvent
from TimeClock.ITimeClock.ICommand import ICommand
from TimeClock.ITimeClock.IDatabase.IEmployee import IEmployee
from TimeClock.ITimeClock.IDatabase.IItem import IItem
from TimeClock.ITimeClock.IDatabase.IPermission import IPermission
from TimeClock.ITimeClock.IEvent.IEventBus import IEventBus
from TimeClock.Utils import coerce, overload
from axiom.item import Item
from axiom.attributes import text


@implementer(ICommand, IItem)
class Login(Item):
    def getArguments(self) -> [object]:
        return ["caller", "employee", "password"]
    name = text()
    @coerce
    def hasPermission(self, permissions: [IPermission]) -> bool:
        return True
    @overload
    def execute(self, caller: object, eid: int, pw: str):
        c = CommandEvent(caller, self, eid)
        r = IEventBus("Commands").postEvent(c)
        if r:
            e = IEmployee(eid)
            if e.alternate_authentication:
                assert(e.alternate_authentication.authenticate(e, pw))
            else:
                AD.authenticate(e, pw)
    @overload
    def execute(self, caller: object, adid: str, pw: str):
        c = CommandEvent(caller, self, adid)
        if IEventBus("Commands").postEvent(c):
            e = IEmployee(adid)
            if e.alternate_authentication:
                assert (e.alternate_authentication.authenticate(e, pw))
            else:
                AD.authenticate(e, pw)
    @overload
    def execute(self, caller: IEmployee, *parameters: object):
        raise NotImplementedError("%s called with invalid parameters" % self.name)

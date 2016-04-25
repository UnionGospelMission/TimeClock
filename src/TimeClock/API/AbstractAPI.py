from functools import partial

from zope.interface import implementer

from TimeClock.ITimeClock.IAPI import IAPI
from TimeClock.ITimeClock.ICommand import ICommand
from TimeClock.ITimeClock.IDatabase.IEmployee import IEmployee
from TimeClock.ITimeClock.IDatabase.IPermission import IPermission
from TimeClock.Util import BoundFunction
from TimeClock.Utils import overload


@implementer(IAPI)
class APIProxy(object):
    def __init__(self, api, employee):
        self.api = api
        self.employee = employee
    def __getattr__(self, attr):
        val = getattr(self.api, attr)
        if isinstance(val, BoundFunction):
            oself = val.oself
            if ICommand.providedBy(oself):
                return partial(val, self.employee)
        if ICommand.providedBy(val):
            return partial(val, self.employee)
        return val
    def getCommandShortNames(self, *a):
        o=[]
        for i in self.getCommandNames(*a):
            n = i.title().replace(' ', '')
            o.append(n[0].lower() + n[1:])
        return o


class AbstractAPI(object):
    @overload
    def getCommands(self) -> [ICommand]:
        return self.powerupsFor(ICommand)
    @overload
    def getCommands(self, employee: IEmployee) -> [ICommand]:
        o = []
        for c in self.powerupsFor(ICommand):
            if c.hasPermission(employee):
                o.append(c)
        return o
    @overload
    def getCommands(self, permissions: [IPermission]) -> [ICommand]:
        o = []
        for c in self.powerupsFor(ICommand):
            if c.hasPermission(permissions):
                o.append(c)
        return o
    def __getitem__(self, value: str) -> ICommand:
        return next(c for c in self.powerupsFor(ICommand) if c.name == value)
    @overload
    def getCommandNames(self) -> [str]:
        return (c.name for c in self.powerupsFor(ICommand))
    @overload
    def getCommandNames(self, permissions: [IPermission]) -> [str]:
        return (c.name for c in self.powerupsFor(ICommand) if c.hasPermission(permissions))
    def __getattr__(self, item):
        if '_' in item:
            return super(AbstractAPI, self).__getattribute__(item)
        for i in self.getCommandNames():
            n = i.title().replace(' ', '')
            if item == n[0].lower() + n[1:]:
                return self[i].execute
        return super(AbstractAPI, self).__getattribute__(item)
    def apiFor(self, employee: IEmployee) -> IAPI:
        return APIProxy(self, employee)

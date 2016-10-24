from zope.interface import implementer

from TimeClock.Database.Commands.CommandEvent import CommandEvent
from TimeClock.ITimeClock.ICommand import ICommand
from TimeClock.ITimeClock.IDatabase.IAdministrator import IAdministrator
from TimeClock.ITimeClock.IDatabase.IItem import IItem
from TimeClock.ITimeClock.IDatabase.ISupervisedBy import ISupervisedBy
from TimeClock.ITimeClock.IDatabase.ISupervisee import ISupervisee
from TimeClock.ITimeClock.IEvent.IEventBus import IEventBus
from TimeClock.Utils import overload
from axiom.item import Item

from axiom.attributes import text

from TimeClock.ITimeClock.IDatabase.IEmployee import IEmployee
from TimeClock.ITimeClock.IDatabase.IPermission import IPermission
from TimeClock.ITimeClock.IDatabase.IPerson import IPerson
from TimeClock.ITimeClock.IDatabase.ISupervisor import ISupervisor


@implementer(ICommand, IItem)
class SetSupervisor(Item):
    name = text()

    @overload
    def hasPermission(self, caller: IPerson) -> bool:
        return self.hasPermission(caller.getPermissions())

    @overload
    def hasPermission(self, permissions: [IPermission]) -> bool:
        return True

    @overload
    def execute(self, caller: IAdministrator, employee: IEmployee, supervisor: ISupervisor):
        c = CommandEvent(caller, self, employee, supervisor)
        IEventBus("Commands").postEvent(c)

        if not supervisor:
            for sup in employee.getSupervisors():
                sup.powerDown(employee, ISupervisee)
                employee.powerDown(sup, ISupervisedBy)
        else:
            supervisor.powerUp(employee, ISupervisee)
            employee.powerUp(supervisor, ISupervisedBy)

    @overload
    def execute(self, caller: IAdministrator, employee: IEmployee, supervisor: type(None)):
        c = CommandEvent(caller, self, employee, supervisor)
        IEventBus("Commands").postEvent(c)
        if not supervisor:
            for sup in employee.getSupervisors():
                sup.powerDown(employee, ISupervisee)
                employee.powerDown(sup, ISupervisedBy)
        else:
            supervisor.powerUp(employee, ISupervisee)
            employee.powerUp(supervisor, ISupervisedBy)

    @overload
    def execute(self, caller: IPerson, *parameters: object):
        print(44, caller, parameters)
        raise NotImplementedError("%s called with invalid parameters" % self.name)

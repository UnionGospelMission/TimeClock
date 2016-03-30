from zope.interface import Attribute, implementer, Interface

from TimeClock.Database.Commands.CommandEvent import CommandEvent
from TimeClock.ITimeClock.ICommand import ICommand
from TimeClock.ITimeClock.IDatabase.IAdministrator import IAdministrator
from TimeClock.ITimeClock.IDatabase.ISubAccount import ISubAccount
from TimeClock.ITimeClock.IDatabase.IEmployee import IEmployee
from TimeClock.ITimeClock.IDatabase.IItem import IItem
from TimeClock.ITimeClock.IDatabase.IPermission import IPermission
from TimeClock.ITimeClock.IDatabase.IPerson import IPerson
from TimeClock.ITimeClock.IEvent.IEventBus import IEventBus
from TimeClock.Util import NULL
from TimeClock.Utils import overload
from axiom.item import Item
from axiom.attributes import text
from TimeClock.Solomon.Solomon import getEmployees


@implementer(ICommand, IItem)
class CheckForNewEmployees(Item):
    name = text()
    def hasPermission(self, permissions: [IPermission]):
        return True
    @overload
    def execute(self, caller: IPerson):
        caller = IAdministrator(caller)

        c = CommandEvent(caller, self)
        IEventBus("Commands").postEvent(c)
        return self.store.transact(self.doCheckForEmployees)
    def doCheckForEmployees(self):
        o = []
        for emp in getEmployees():
            n_emp = IEmployee(int(emp['EmpId']), None)
            if not n_emp:
                print("adding new employee", emp['EmpId'])
                n_emp = IEmployee(NULL)
                n_emp.employee_id = int(emp['EmpId'])
                a = ISubAccount(emp['DfltExpSub'], None)
                if a:
                    a.powerUp(n_emp, IEmployee)
                    n_emp.powerUp(a, ISubAccount)
                o.append(n_emp)
            else:
                print(45, n_emp)
                if n_emp.active_directory_name is None and n_emp.alternate_authentication is None:
                    o.append(n_emp)
        return o
    @overload
    def execute(self, caller: IPerson, *parameters: object):
        print(42, caller, parameters)
        raise NotImplementedError("%s called with invalid parameters" % self.name)

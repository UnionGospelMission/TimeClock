from TimeClock.Axiom.Store import Store
from TimeClock.Database.Employee import Employee
from TimeClock.ITimeClock.IDatabase.IEmployee import IEmployee
from TimeClock.ITimeClock.IDatabase.IPermission import IPermission
from TimeClock.Utils import overload
from ...ITimeClock.IDatabase.IWorkLocation import IWorkLocation


@overload
def findEmployee(eid: int) -> IEmployee:
    return Store.findFirst(Employee, Employee.employee_id == eid)


@overload
def findEmployee(adid: str) -> IEmployee:
    return Store.findFirst(Employee, Employee.active_directory_name == adid)


def newEmployee(_):
    from TimeClock.Axiom.Store import Store
    e = Employee(store=Store)
    e.powerUp(IPermission("Clock In"), IPermission)
    return e


IWorkLocation['getEmployees'].annotations['return'] = [IEmployee]

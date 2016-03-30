from twisted.python.components import registerAdapter

from TimeClock.Axiom.Store import Store
from TimeClock.Utils import overload
from TimeClock.Database.Employee import Employee, IEmployee


@overload
def findEmployee(eid: int) -> IEmployee:
    return Store.findFirst(Employee, Employee.employee_id==eid)


@overload
def findEmployee(adid: str) -> IEmployee:
    return Store.findFirst(Employee, Employee.active_directory_name==adid)

registerAdapter(findEmployee, int, IEmployee)
registerAdapter(findEmployee, str, IEmployee)

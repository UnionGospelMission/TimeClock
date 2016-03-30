from twisted.python.components import registerAdapter

from TimeClock.Database.Employee import IEmployee
from TimeClock.Database.Reflection.Employee import findEmployee, newEmployee
from TimeClock.Util import Null


registerAdapter(findEmployee, int, IEmployee)
registerAdapter(findEmployee, str, IEmployee)
registerAdapter(newEmployee, Null, IEmployee)

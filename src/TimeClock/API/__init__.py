from ..Database.API.AdministratorAPI import AdministratorAPI
from ..Database.API.EmployeeAPI import EmployeeAPI
from ..Database.API.SupervisorAPI import SupervisorAPI
from ..Database.API.PublicAPI import PublicAPI
from ..ITimeClock.ICommand import ICommand

from ..Axiom.Store import Store

from .Commands import MakeSupervisor, MakeAdministrator, AddToArea, NewEmployee, ClockIn, NewArea, ClockOut


PublicAPI = Store.findOrCreate(PublicAPI, name="Public API")
EmployeeAPI = Store.findOrCreate(EmployeeAPI, name="Employee API")
SupervisorAPI = Store.findOrCreate(SupervisorAPI, name="Supervisor API")
AdministratorAPI = Store.findOrCreate(AdministratorAPI, name="Administrator API")


AdministratorAPI.powerUp(MakeAdministrator, ICommand)
AdministratorAPI.powerUp(MakeSupervisor, ICommand)
AdministratorAPI.powerUp(AddToArea, ICommand)
AdministratorAPI.powerUp(NewEmployee, ICommand)
AdministratorAPI.powerUp(NewArea, ICommand)

AdministratorAPI.powerUp(ClockIn, ICommand)

SupervisorAPI.powerUp(ClockIn, ICommand)

EmployeeAPI.powerUp(ClockIn, ICommand)

AdministratorAPI.powerUp(ClockOut, ICommand)

SupervisorAPI.powerUp(ClockOut, ICommand)

EmployeeAPI.powerUp(ClockOut, ICommand)


from ..Database.TimeEntry import TimeEntry
from ..Database.EntryType import EntryType
from ..Database.TimePeriod import TimePeriod

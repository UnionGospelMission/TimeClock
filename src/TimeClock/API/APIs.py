from TimeClock.Axiom import Store
from TimeClock.Database.API.AdministratorAPI import AdministratorAPI
from TimeClock.Database.API.EmployeeAPI import EmployeeAPI
from TimeClock.Database.API.PublicAPI import PublicAPI
from TimeClock.Database.API.SupervisorAPI import SupervisorAPI


from .Commands import MakeSupervisor, MakeAdministrator, AddToArea, CheckForNewEmployees, ClockIn, NewArea, ClockOut, EditTime, \
    ApproveTime, Login, ViewHours, ViewAverageHours, ViewEmployees, AssumeRole, SetSupervisor, SetWorkLocations, \
    SetSubAccounts, ChangePassword
from ..Database.API.AdministratorAPI import AdministratorAPI
from ..Database.API.EmployeeAPI import EmployeeAPI
from ..Database.API.PublicAPI import PublicAPI
from ..Database.API.SupervisorAPI import SupervisorAPI

from ..ITimeClock.ICommand import ICommand


PublicAPI = Store.Store.findOrCreate(PublicAPI, name="Public API")
EmployeeAPI = Store.Store.findOrCreate(EmployeeAPI, name="Employee API")
SupervisorAPI = Store.Store.findOrCreate(SupervisorAPI, name="Supervisor API")
AdministratorAPI = Store.Store.findOrCreate(AdministratorAPI, name="Administrator API")

# Note:  Removing a command from this list will not remove it from an existing database
# You must also call API.powerDown(command, ICommand)

PublicAPI.powerUp(Login, ICommand)

AdministratorAPI.powerUp(MakeAdministrator, ICommand)
AdministratorAPI.powerUp(MakeSupervisor, ICommand)
AdministratorAPI.powerUp(AddToArea, ICommand)
AdministratorAPI.powerUp(CheckForNewEmployees, ICommand)
AdministratorAPI.powerUp(NewArea, ICommand)
AdministratorAPI.powerUp(ApproveTime, ICommand)
AdministratorAPI.powerUp(EditTime, ICommand)
AdministratorAPI.powerUp(ClockOut, ICommand)
AdministratorAPI.powerUp(ViewHours, ICommand)
AdministratorAPI.powerUp(ViewAverageHours, ICommand)
AdministratorAPI.powerUp(ViewEmployees, ICommand)
AdministratorAPI.powerUp(AssumeRole, ICommand)
AdministratorAPI.powerUp(ClockIn, ICommand)
AdministratorAPI.powerUp(SetSupervisor, ICommand)
AdministratorAPI.powerUp(SetWorkLocations, ICommand)
AdministratorAPI.powerUp(SetSubAccounts, ICommand)
AdministratorAPI.powerUp(ChangePassword, ICommand)

EmployeeAPI.powerUp(ClockIn, ICommand)
EmployeeAPI.powerUp(ClockOut, ICommand)
EmployeeAPI.powerUp(ViewHours, ICommand)
EmployeeAPI.powerUp(ViewAverageHours, ICommand)
EmployeeAPI.powerUp(ChangePassword, ICommand)


SupervisorAPI.powerUp(ClockOut, ICommand)
SupervisorAPI.powerUp(ViewHours, ICommand)
SupervisorAPI.powerUp(ViewAverageHours, ICommand)
SupervisorAPI.powerUp(ViewEmployees, ICommand)
SupervisorAPI.powerUp(AssumeRole, ICommand)
SupervisorAPI.powerUp(ClockIn, ICommand)
SupervisorAPI.powerUp(EditTime, ICommand)
SupervisorAPI.powerUp(ApproveTime, ICommand)
SupervisorAPI.powerUp(ChangePassword, ICommand)


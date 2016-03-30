from TimeClock.Axiom import Store
from TimeClock.Database.API.AdministratorAPI import AdministratorAPI
from TimeClock.Database.API.EmployeeAPI import EmployeeAPI
from TimeClock.Database.API.PublicAPI import PublicAPI
from TimeClock.Database.API.SupervisorAPI import SupervisorAPI


PublicAPI = Store.Store.findOrCreate(PublicAPI, name="Public API")
EmployeeAPI = Store.Store.findOrCreate(EmployeeAPI, name="Employee API")
SupervisorAPI = Store.Store.findOrCreate(SupervisorAPI, name="Supervisor API")
AdministratorAPI = Store.Store.findOrCreate(AdministratorAPI, name="Administrator API")

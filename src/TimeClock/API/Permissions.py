from TimeClock.Axiom import Store
from TimeClock.Database.Permissions import Permission


MakeSupervisor = Store.Store.findOrCreate(Permission, name="Make Supervisor")
NewEmployee = Store.Store.findOrCreate(Permission, name="New Employee")
ClockIn = Store.Store.findOrCreate(Permission, name="Clock In")
NewArea = Store.Store.findOrCreate(Permission, name="New SubAccount")
AssignArea = Store.Store.findOrCreate(Permission, name="Assign SubAccount")

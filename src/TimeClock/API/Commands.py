from ..Database.Commands.MakeSupervisor import MakeSupervisor
from ..Database.Commands.AddToArea import AddToArea
from ..Database.Commands.NewEmployee import NewEmployee
from ..Database.Commands.MakeAdministrator import MakeAdministrator
from ..Database.Commands.ClockIn import ClockIn
from ..Database.Commands.NewArea import NewArea
from ..Database.Commands.ClockOut import ClockOut

from ..Axiom.Store import Store


MakeSupervisor = Store.findOrCreate(MakeSupervisor, name="Make Supervisor")
MakeAdministrator = Store.findOrCreate(MakeAdministrator, name="Make Administrator")
AddToArea = Store.findOrCreate(AddToArea, name="Add to Area")
NewEmployee = Store.findOrCreate(NewEmployee, name="New Employee")
ClockIn = Store.findOrCreate(ClockIn, name="Clock In")
NewArea = Store.findOrCreate(NewArea, name="New Area")
ClockOut = Store.findOrCreate(ClockOut, name="Clock Out")

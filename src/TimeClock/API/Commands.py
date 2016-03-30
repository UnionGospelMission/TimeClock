from TimeClock.Database.Commands.ChangeAuthentication import ChangeAuthentication
from TimeClock.Database.Commands.AssumeRole import AssumeRole
from TimeClock.Database.Commands.CheckForNewEmployees import CheckForNewEmployees
from TimeClock.Database.Commands.SetSubAccounts import SetSubAccounts
from TimeClock.Database.Commands.SetSupervisor import SetSupervisor
from TimeClock.Database.Commands.SetWorkLocations import SetWorkLocations
from TimeClock.Database.Commands.ViewEmployees import ViewEmployees
from TimeClock.Database.Commands.ViewAverageHours import ViewAverageHours
from TimeClock.Database.Commands.ApproveTime import ApproveTime
from TimeClock.Database.Commands.EditTime import EditTime
from TimeClock.Database.Commands.Login import Login
from ..Database.Commands.MakeSupervisor import MakeSupervisor
from ..Database.Commands.AddToArea import AddToArea
from ..Database.Commands.MakeAdministrator import MakeAdministrator
from ..Database.Commands.ClockIn import ClockIn
from ..Database.Commands.NewArea import NewArea
from ..Database.Commands.ClockOut import ClockOut
from ..Database.Commands.ViewHours import ViewHours

from ..Axiom import Store


MakeSupervisor = Store.Store.findOrCreate(MakeSupervisor, name="Make Supervisor")
MakeAdministrator = Store.Store.findOrCreate(MakeAdministrator, name="Make Administrator")
AddToArea = Store.Store.findOrCreate(AddToArea, name="Add to SubAccount")
CheckForNewEmployees = Store.Store.findOrCreate(CheckForNewEmployees, name="Check For New Employees")
ClockIn = Store.Store.findOrCreate(ClockIn, name="Clock In")
NewArea = Store.Store.findOrCreate(NewArea, name="New SubAccount")
ClockOut = Store.Store.findOrCreate(ClockOut, name="Clock Out")
ApproveTime = Store.Store.findOrCreate(ApproveTime, name="Approve Time")
Login = Store.Store.findOrCreate(Login, name="Login")
EditTime = Store.Store.findOrCreate(EditTime, name="Edit Time")
ViewHours = Store.Store.findOrCreate(ViewHours, name="View Hours")
ViewAverageHours = Store.Store.findOrCreate(ViewAverageHours, name="View Average Hours")
ViewEmployees = Store.Store.findOrCreate(ViewEmployees, name="View Employees")
AssumeRole = Store.Store.findOrCreate(AssumeRole, name="Assume Role")
SetSupervisor = Store.Store.findOrCreate(SetSupervisor, name="Set Supervisor")
SetWorkLocations = Store.Store.findOrCreate(SetWorkLocations, name="Set Work Locations")
SetSubAccounts = Store.Store.findOrCreate(SetSubAccounts, name="Set Sub Accounts")
ChangePassword = Store.Store.findOrCreate(ChangeAuthentication, name="Change Password")




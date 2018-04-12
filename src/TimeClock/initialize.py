from TimeClock.AD import runWithConnection
from TimeClock.Database.API.API import API
from TimeClock.Database.Commands import ScheduleTimeOff
from TimeClock.Database.Commands.ApproveTimeOff import ApproveTimeOff
from TimeClock.Database.Commands.ScheduleTimeOff import ScheduleTimeOff
from TimeClock.Database.Commands.AssignTask import AssignTask
from TimeClock.Database.Commands.CreateTask import CreateTask
from TimeClock.Database.Commands.ManageSubAccounts import ManageSubAccounts
from TimeClock.Database.Commands.ManageWorkLocations import ManageWorkLocations
from TimeClock.Database.Commands.SetSupervisorSubAccounts import SetSupervisorSubAccounts
from TimeClock.Database.Commands.ViewBenefits import ViewBenefits
from TimeClock.Database.Commands.ViewReports import ViewReports
from TimeClock.Database.Permissions import Permission
from TimeClock.ITimeClock.IAPI import IAPI
from TimeClock.ITimeClock.ICommand import ICommand
from TimeClock.ITimeClock.ISolomonEmployee import ISolomonEmployee
from TimeClock.Utils import coerce
from .Database.File import File
from .Database.Logger import Logger
from .Database.StaticAuthenticationMethod import StaticAuthenticationMethod
from .ITimeClock.IDatabase.IAdministrator import IAdministrator
from .ITimeClock.IDatabase.IEmployee import IEmployee
from .ITimeClock.IDatabase.ISubAccount import ISubAccount
from .ITimeClock.IDatabase.IWorkLocation import IWorkLocation
from .ITimeClock.IEvent.IDatabaseEvent.ICommandEvent import ICommandEvent
from .ITimeClock.IEvent.IEventBus import IEventBus
from .Solomon import Solomon
from .Util import NULL

from axiom import store
from twisted.python import usage

from .Database.Commands.ChangeAuthentication import ChangeAuthentication
from .Database.Commands.AssumeRole import AssumeRole
from .Database.Commands.CheckForNewEmployees import CheckForNewEmployees
from .Database.Commands.SetSubAccounts import SetSubAccounts
from .Database.Commands.SetSupervisor import SetSupervisor
from .Database.Commands.SetWorkLocations import SetWorkLocations
from .Database.Commands.ViewEmployees import ViewEmployees
from .Database.Commands.ViewAverageHours import ViewAverageHours
from .Database.Commands.ApproveTime import ApproveTime
from .Database.Commands.EditTime import EditTime
from .Database.Commands.Login import Login
from .Database.Commands.AsyncLogin import AsyncLogin
from .Database.Commands.MakeSupervisor import MakeSupervisor
from .Database.Commands.AddToArea import AddToArea
from .Database.Commands.MakeAdministrator import MakeAdministrator
from .Database.Commands.ClockIn import ClockIn
from .Database.Commands.NewArea import NewArea
from .Database.Commands.ClockOut import ClockOut
from .Database.Commands.ViewHours import ViewHours

try:
    from ldap3 import Connection
except ImportError:
    Connection = object


def initializeCommands(Store: store.Store):
    Store.powerUp(Store.findOrCreate(MakeSupervisor, name="Make Supervisor"), ICommand)
    Store.powerUp(Store.findOrCreate(MakeAdministrator, name="Make Administrator"), ICommand)
    Store.powerUp(Store.findOrCreate(AddToArea, name="Add to SubAccount"), ICommand)
    Store.powerUp(Store.findOrCreate(CheckForNewEmployees, name="Check For New Employees"), ICommand)
    Store.powerUp(Store.findOrCreate(ClockIn, name="Clock In"), ICommand)
    Store.powerUp(Store.findOrCreate(NewArea, name="New SubAccount"), ICommand)
    Store.powerUp(Store.findOrCreate(ClockOut, name="Clock Out"), ICommand)
    Store.powerUp(Store.findOrCreate(ApproveTime, name="Approve Time"), ICommand)
    Store.powerUp(Store.findOrCreate(Login, name="Login"), ICommand)
    Store.powerUp(Store.findOrCreate(AsyncLogin), ICommand)
    Store.powerUp(Store.findOrCreate(EditTime, name="Edit Time"), ICommand)
    Store.powerUp(Store.findOrCreate(ViewHours, name="View Hours"), ICommand)
    Store.powerUp(Store.findOrCreate(ViewAverageHours, name="View Average Hours"), ICommand)
    Store.powerUp(Store.findOrCreate(ViewEmployees, name="View Employees"), ICommand)
    Store.powerUp(Store.findOrCreate(AssumeRole, name="Assume Role"), ICommand)
    Store.powerUp(Store.findOrCreate(SetSupervisor, name="Set Supervisor"), ICommand)
    Store.powerUp(Store.findOrCreate(SetWorkLocations, name="Set Work Locations"), ICommand)
    Store.powerUp(Store.findOrCreate(SetSubAccounts, name="Set Sub Accounts"), ICommand)
    Store.powerUp(Store.findOrCreate(ChangeAuthentication, name="Change Password"), ICommand)
    Store.powerUp(Store.findOrCreate(ViewReports, name="View Reports"), ICommand)
    Store.powerUp(Store.findOrCreate(ManageSubAccounts, name="Manage Sub Accounts"), ICommand)
    Store.powerUp(Store.findOrCreate(ManageWorkLocations, name="Manage Work Locations"), ICommand)
    Store.powerUp(Store.findOrCreate(CreateTask), ICommand)
    Store.powerUp(Store.findOrCreate(AssignTask), ICommand)
    Store.powerUp(Store.findOrCreate(ScheduleTimeOff), ICommand)
    Store.powerUp(Store.findOrCreate(ApproveTimeOff), ICommand)
    Store.powerUp(Store.findOrCreate(ViewBenefits), ICommand)
    Store.powerUp(Store.findOrCreate(SetSupervisorSubAccounts), ICommand)


def commandFinder(Store: store.Store):
    def findCommand(name: str):
        for i in Store.powerupsFor(ICommand):
            if i.name == name or i.name.replace(' ', '') == name:
                return i
    return findCommand


def initializeAPIs(Store: store.Store):
    PublicAPI = Store.findOrCreate(API, name="Public API")
    Store.powerUp(PublicAPI, IAPI)

    EmployeeAPI = Store.findOrCreate(API, name="Employee API")
    Store.powerUp(EmployeeAPI, IAPI)

    SupervisorAPI = Store.findOrCreate(API, name="Supervisor API")
    Store.powerUp(SupervisorAPI, IAPI)

    AdministratorAPI = Store.findOrCreate(API, name="Administrator API")
    Store.powerUp(AdministratorAPI, IAPI)
    findCommand = commandFinder(Store)
    PublicAPI.powerUp(findCommand("Login"), ICommand)
    PublicAPI.powerUp(findCommand("AsyncLogin"), ICommand)

    AdministratorAPI.powerUp(findCommand("MakeAdministrator"), ICommand)
    AdministratorAPI.powerUp(findCommand("MakeSupervisor"), ICommand)
    AdministratorAPI.powerUp(findCommand("AddToArea"), ICommand)
    AdministratorAPI.powerUp(findCommand("CheckForNewEmployees"), ICommand)
    AdministratorAPI.powerUp(findCommand("NewArea"), ICommand)
    AdministratorAPI.powerUp(findCommand("ApproveTime"), ICommand)
    AdministratorAPI.powerUp(findCommand("EditTime"), ICommand)
    AdministratorAPI.powerUp(findCommand("ClockOut"), ICommand)
    AdministratorAPI.powerUp(findCommand("ViewHours"), ICommand)
    AdministratorAPI.powerUp(findCommand("ViewAverageHours"), ICommand)
    AdministratorAPI.powerUp(findCommand("ViewEmployees"), ICommand)
    AdministratorAPI.powerUp(findCommand("AssumeRole"), ICommand)
    AdministratorAPI.powerUp(findCommand("ClockIn"), ICommand)
    AdministratorAPI.powerUp(findCommand("SetSupervisor"), ICommand)
    AdministratorAPI.powerUp(findCommand("SetWorkLocations"), ICommand)
    AdministratorAPI.powerUp(findCommand("SetSubAccounts"), ICommand)
    AdministratorAPI.powerUp(findCommand("ChangePassword"), ICommand)
    AdministratorAPI.powerUp(findCommand("ViewReports"), ICommand)
    AdministratorAPI.powerUp(findCommand("AssignTask"), ICommand)
    AdministratorAPI.powerUp(findCommand("CreateTask"), ICommand)
    AdministratorAPI.powerUp(findCommand("ManageSubAccounts"), ICommand)
    AdministratorAPI.powerUp(findCommand("ManageWorkLocations"), ICommand)
    AdministratorAPI.powerUp(findCommand("ScheduleTimeOff"), ICommand)
    AdministratorAPI.powerUp(findCommand("ApproveTimeOff"), ICommand)
    AdministratorAPI.powerUp(findCommand("ViewBenefits"), ICommand)
    AdministratorAPI.powerUp(findCommand("SetSupervisorSubAccounts"), ICommand)
    sv = findCommand("ScheduleVacation")
    if sv:
        for api in [AdministratorAPI, EmployeeAPI, SupervisorAPI]:
            if sv in api.powerupsFor(ICommand):
                api.powerDown(sv, ICommand)
        sv.deleteFromStore(Store)
    sv = findCommand("ApproveVacation")
    if sv:
        for api in [AdministratorAPI, EmployeeAPI, SupervisorAPI]:
            if sv in api.powerupsFor(ICommand):
                api.powerDown(sv, ICommand)
        sv.deleteFromStore(Store)

    EmployeeAPI.powerUp(findCommand("ClockIn"), ICommand)
    EmployeeAPI.powerUp(findCommand("ClockOut"), ICommand)
    EmployeeAPI.powerUp(findCommand("ViewHours"), ICommand)
    EmployeeAPI.powerUp(findCommand("ViewAverageHours"), ICommand)
    EmployeeAPI.powerUp(findCommand("ChangePassword"), ICommand)
    EmployeeAPI.powerUp(findCommand("ScheduleTimeOff"), ICommand)
    EmployeeAPI.powerUp(findCommand("ViewBenefits"), ICommand)

    SupervisorAPI.powerUp(findCommand("ClockOut"), ICommand)
    SupervisorAPI.powerUp(findCommand("ViewHours"), ICommand)
    SupervisorAPI.powerUp(findCommand("ViewAverageHours"), ICommand)
    # SupervisorAPI.powerUp(findCommand("ViewEmployees"), ICommand)
    SupervisorAPI.powerUp(findCommand("AssumeRole"), ICommand)
    SupervisorAPI.powerUp(findCommand("ClockIn"), ICommand)
    SupervisorAPI.powerUp(findCommand("EditTime"), ICommand)
    SupervisorAPI.powerUp(findCommand("ApproveTime"), ICommand)
    SupervisorAPI.powerUp(findCommand("ChangePassword"), ICommand)
    SupervisorAPI.powerUp(findCommand("AssignTask"), ICommand)
    SupervisorAPI.powerUp(findCommand("CreateTask"), ICommand)
    SupervisorAPI.powerUp(findCommand("ScheduleTimeOff"), ICommand)
    SupervisorAPI.powerUp(findCommand("ApproveTimeOff"), ICommand)
    SupervisorAPI.powerUp(findCommand("ViewBenefits"), ICommand)


def initializeWorkLocations(Store: store.Store):
    for i in Solomon.getWorkLocations():
        IWorkLocation(i['WrkLocId'])


def initializeSubAccounts(Store: store.Store):
    for i in Solomon.getSubAccounts():
        ISubAccount(int(i['Sub']))


def initializePermissions(Store: store.Store):
    Permission(store=Store, name="Create Task")
    Permission(store=Store, name="Assign Task")
    Permission(store=Store, name="Make Supervisor")
    Permission(store=Store, name="New Employee")
    Permission(store=Store, name="Clock In")
    Permission(store=Store, name="New SubAccount")
    Permission(store=Store, name="Assign SubAccount")


def initializeDB(Store: store.Store, options: usage.Options):
    username = options.get('username')
    password = options.get('password')
    employees = commandFinder(Store)("Check For New Employees").doCheckForEmployees()
    for emp in employees:
        un = runWithConnection(findUsername, username, password, args=(emp, options))
        if un:
            emp.active_directory_name = un


@coerce
def findUsername(conn, emp: IEmployee, options: usage.Options) -> str:
    ise = ISolomonEmployee(emp)
    name = ise.name
    if '~' in name:
        name = name.split('~')
        ln = name[0]
        fn = name[1].split()[0]
    else:
        name = name.split()
        fn = name[0]
        ln = name[-1]
    if conn.search('dc=ugm, dc=local', '(&(givenName=%s) (sn=%s))' % (fn, ln), attributes=['sAMAccountName']):
        if len(conn.response) == 4 and 'attributes' in conn.response[0]:
            if conn.response[0]['attributes']['sAMAccountName']:
                return conn.response[0]['attributes']['sAMAccountName'][0]
        if options.get('resolve'):
            print("AD username not found for %s, searching by last name only" % ise.name)
            if conn.search('dc=ugm, dc=local', '(&(givenName=*) (sn=%s))' % (ln,), attributes=['sAMAccountName',
                                                                                               'givenName',
                                                                                               'sn']):
                while len(conn.response) > 3:
                    resp = conn.response.pop(0)
                    if 'attributes' not in resp:
                        break
                    print("Possible match found")
                    print("FN:", resp['attributes']['givenName'])
                    print("LN:", resp['attributes']['sn'])
                    if 'Y' in input("Is this a match? (yN)").upper():
                        return resp['attributes']['sAMAccountName'][0]
            if options.get('resolve') == 'firstname':
                print("AD username not found, searching by first name only")
                if conn.search('dc=ugm, dc=local', '(&(givenName=%s) (sn=*))' % (fn,),
                               attributes=['sAMAccountName', 'givenName', 'sn']):
                    while len(conn.response) > 3:
                        resp = conn.response.pop(0)
                        if 'attributes' not in resp:
                            break
                        print("Possible match found")
                        print("FN:", resp['attributes']['givenName'])
                        print("LN:", resp['attributes']['sn'])
                        if 'Y' in input("Is this a match? (yN)").upper():
                            return resp['attributes']['sAMAccountName'][0]


def initialize(db: store.Store, options: usage.Options):
    initializers = []
    initializePermissions(db)
    adm = IEmployee(1, None)
    if not adm:
        adm = IEmployee(NULL)
        adm.employee_id = 1
        adm.alternate_authentication = StaticAuthenticationMethod(store=adm.store).setPassword("xyzzy")
        adm1 = IAdministrator(NULL)
        adm1.employee = adm
        adm.powerUp(adm1, IAdministrator)

    if db.filesdir:
        l = Logger(store=db.store)

        l.file = File(store=db.store, path=db.store.filesdir.child('Commands.log').path)
        l.flags = 1 | 2 | 4 | 8
        l.name = "Command Logger"
        IEventBus("Commands").powerUp(l, ICommandEvent)
        initializers = [initializeCommands, initializeAPIs]

    if Solomon.pymssql:
        initializers.append(initializeSubAccounts)
        initializers.append(initializeWorkLocations)
        initializers.append(lambda d: initializeDB(d, options))
    else:
        wl = IWorkLocation(NULL)
        wl.description = 'test'
        wl.workLocationID = "TST"
        sa = ISubAccount(NULL)
        sa.name = 'test'
        sa.sub = 1
    db.transact(lambda: [i(db) for i in initializers])

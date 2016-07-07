from zope.interface import implements, implementer

from TimeClock.API.APIs import PublicAPI
from TimeClock.Axiom import Store
from TimeClock.Database.Employee import Employee
from TimeClock.Database.Event.ClockInOutEvent import ClockInOutEvent
from TimeClock.Exceptions import PermissionDenied
from TimeClock.ITimeClock.IDatabase.IEmployee import IEmployee
from TimeClock.ITimeClock.IEvent.IDatabaseEvent import IDatabaseEvent
from TimeClock.ITimeClock.IEvent.IEvent import IEvent
from TimeClock.ITimeClock.IEvent.IEventBus import IEventBus
from TimeClock.ITimeClock.IEvent.IEventHandler import IEventHandler
from TimeClock.ITimeClock.ISolomonEmployee import ISolomonEmployee
from TimeClock.Utils import overload
from TimeClock.Web.TimeClockPage import TimeClockPage
from nevow import inevow, tags
from nevow.context import WovenContext
from nevow.loaders import xmlfile

from nevow.athena import LivePage, LiveElement, LiveFragment, expose


path = __file__.rsplit('/', 1)[0]


class LoginPage(LivePage):
    def renderHTTP(self, ctx):
        __builtins__['ctx'] = ctx
        return super().renderHTTP(ctx)

    def __init__(self, *a):
        super(LoginPage, self).__init__(*a)
        self.jsModules.mapping['LoginPage'] = path + '/JS/Login.js'
        self.jsModules.mapping['jquery'] = path + '/JS/jquery/__init__.js'
        self.jsModules.mapping['redirect'] = path + '/JS/redirect.js'
    docFactory = xmlfile(path + "/Pages/Login.html")

    @implementer(IEventHandler)
    class ClockedInFragment(LiveFragment):
        jsClass = "LoginPage.ClockedIn"
        docFactory = xmlfile(path + "/Pages/GenericCommand.xml", "GenericCommandPattern")
        def powerUp(self, object, iface):
            pass
        def __init__(self, parent, ctx):
            super().__init__()
            self.parent = parent
            self.setFragmentParent(parent)
        @overload
        def handleEvent(self, event: ClockInOutEvent):
            if event.clockedIn:
                self.callRemote("clockedIn", event.employee.employee_id, ISolomonEmployee(event.employee).name);
            else:
                self.callRemote("clockedOut", event.employee.employee_id, ISolomonEmployee(event.employee).name);

        @overload
        def handleEvent(self, event: IEvent):
            pass
        def render_class(self, *a):
            return 'ClockedIn'
        def render_genericCommand(self, ctx: WovenContext, data):
            IEventBus("Database").register(self, IDatabaseEvent)
            checkedIn = Store.Store.query(Employee, Employee.timeEntry!=None)
            ret = tags.table(border='1px solid black')[
                tags.thead()[
                    tags.tr()[
                        tags.th(colspan=2)['Currently Clocked In']
                    ],
                    tags.tr()[
                        tags.th()['Employee ID'],
                        tags.th()['Employee Name']
                    ]
                ],
                tags.tbody(id='employeeList', border='1px solid black') [
                    [tags.tr()[tags.td()[i.employee_id], tags.td()[ISolomonEmployee(i).name]] for i in checkedIn]
                ]
            ]
            for p in self.preprocessors:
                ret = p(ret)
            return ret

    class LoginFragment(LiveFragment):
        jsClass = "LoginPage.Login"
        docFactory = xmlfile(path + "/Pages/Login.html", "LoginPattern")
        def __init__(self, parent, ctx):
            super().__init__()
            self.parent = parent
            self.setFragmentParent(parent)
        @expose
        def quickValidate(self, func, username, password):
            if username.isdigit():
                username = int(username)
            employee = IEmployee(username, None)
            if employee is None:
                return "access denied"

            try:
                PublicAPI.login(employee, username, password)
            except PermissionDenied as e:
                return "access denied"
            if func == 'clockIn':
                ise = ISolomonEmployee(employee)
                if employee.timeEntry:
                    return "Already clocked in"
                employee.clockIn(ise.defaultSubAccount, ise.defaultWorkLocation)

            elif func == 'clockOut':
                if not employee.timeEntry:
                    return "Already clocked out"
                employee.clockOut()
            return 'access granted'

        @expose
        def validate(self, username, password):
            if username.isdigit():
                username = int(username)
            employee = IEmployee(username, None)
            if employee is None:
                return "access denied"
            try:
                PublicAPI.login(employee, username, password)
            except PermissionDenied as e:
                return "access denied"
            newPage = TimeClockPage(employee)
            return newPage.pageId

    render_clockedInList = lambda self, *x: self.ClockedInFragment(self, *x)

    render_LoginPage = lambda self, *x: self.LoginFragment(self, *x)

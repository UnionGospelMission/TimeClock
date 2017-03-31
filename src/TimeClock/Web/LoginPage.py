from TimeClock.API.APIs import PublicAPI
from TimeClock.Exceptions import PermissionDenied
from TimeClock.ITimeClock.IDatabase.IEmployee import IEmployee
from TimeClock.ITimeClock.ISolomonEmployee import ISolomonEmployee
from TimeClock.Web.TimeClockPage import TimeClockPage
from TimeClock.Web.TimeClockStationPage import TimeClockStationPage
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
            if employee.alternate_authentication and employee.alternate_authentication.expired:
                return "Please login to enable quick actions"
            try:
                PublicAPI.login(employee, username, password)
            except PermissionDenied as e:
                return "access denied"
            if func == 'clockIn':
                ise = ISolomonEmployee(employee)
                if employee.timeEntry:
                    return "Already clocked in"
                dsa = ise.defaultSubAccount
                dwl = ise.defaultWorkLocation
                if not dsa.active:
                    return "Default sub account is disabled, please log in to clock in"
                if not dwl.active:
                    return "Default work location is disabled, please log in to clock in"
                employee.clockIn(dsa, dwl)

            elif func == 'clockOut':
                if not employee.timeEntry:
                    return "Already clocked out"
                employee.clockOut()
            return 'access granted'
        @expose
        def tcs(self, username, password):
            if username.isdigit():
                username = int(username)
            employee = IEmployee(username, None)
            if employee is None:
                return "access denied"
            try:
                PublicAPI.login(employee, username, password)
            except PermissionDenied as e:
                return "access denied"
            newPage = TimeClockStationPage()
            return newPage.pageId
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

    render_LoginPage = lambda self, *x: self.LoginFragment(self, *x)

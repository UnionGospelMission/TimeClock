from TimeClock.API.APIs import PublicAPI
from TimeClock.Exceptions import PermissionDenied
from TimeClock.ITimeClock.IDatabase.IEmployee import IEmployee
from TimeClock.ITimeClock.ISolomonEmployee import ISolomonEmployee
from TimeClock.Web.TimeClockPage import TimeClockPage
from nevow.loaders import xmlfile

from nevow.athena import LivePage, LiveElement, LiveFragment, expose


path = __file__.rsplit('/', 1)[0]


class LoginPage(LivePage):
    def __init__(self, *a):
        super(LoginPage, self).__init__(*a)
        self.jsModules.mapping['LoginPage'] = path + '/JS/Login.js'
        self.jsModules.mapping['jQuery'] = path + '/JS/jQuery.js'
        self.jsModules.mapping['redirect'] = path + '/JS/redirect.js'
    docFactory = xmlfile(path + "/Pages/Login.html")

    class LoginFragment(LiveFragment):
        jsClass = "LoginPage.Login"
        docFactory = xmlfile(path + "/Pages/Login.html", "LoginPattern")
        def __init__(self, parent, ctx):
            self.parent = parent
            self.setFragmentParent(parent)
        @expose
        def quickValidate(self, func, username, password):
            if username.isdigit():
                username = int(username)
            employee = IEmployee(username, None)
            if employee is None:
                return "access denied"
            PublicAPI.login(employee, username, password)
            if func == 'clockIn':
                ise = ISolomonEmployee(employee)
                employee.clockIn(ise.defaultSubAccount, ise.defaultWorkLocation)
            elif func == 'clockOut':
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

    render_LoginPage = lambda self, *x: self.LoginFragment(self, *x)

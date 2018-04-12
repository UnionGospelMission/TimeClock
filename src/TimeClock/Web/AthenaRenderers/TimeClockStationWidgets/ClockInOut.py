from TimeClock.API.APIs import PublicAPI
from TimeClock.Axiom import Transaction
from TimeClock.Exceptions import PermissionDenied
from TimeClock.ITimeClock.IDatabase.ISubAccount import ISubAccount
from TimeClock.ITimeClock.IDatabase.IWorkLocation import IWorkLocation
from TimeClock.ITimeClock.ISolomonEmployee import ISolomonEmployee
from TimeClock.Utils import coerce, getAllSubAccounts, getAllWorkLocations
from TimeClock.Web.AthenaRenderers.Abstract.AbstractHideable import AbstractHideable
from TimeClock.Web.AthenaRenderers.Abstract.AbstractRenderer import AbstractRenderer, path
from nevow import tags
from nevow.athena import expose
from nevow.context import WovenContext
from nevow.loaders import xmlfile


class ClockInOut(AbstractRenderer, AbstractHideable):
    jsClass = "TimeClock.TimeClockStation.ClockedInOut"
    label = 'Clock In or Out'
    docFactory = xmlfile(path + "/Pages/GenericCommand.xml", "GenericCommandPattern")
    visible = True
    subAccount = None
    workLocation = None

    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.setFragmentParent(parent)

    def render_class(self, *a):
        return 'ClockInOut'

    def getSubs(self):
        return [tags.option(value=None)['All Employees']] + [tags.option(value=i.sub)[i.name] for i in getAllSubAccounts() if i.active]

    def getLocs(self):
        return [tags.option(value=None)['All Employees']] + [tags.option(value=i.workLocationID)[i.description] for i in getAllWorkLocations() if i.active]

    def render_genericCommand(self, ctx: WovenContext, data):
        ret = [
            tags.select(id='subAccount', style='display:block')[
                [self.getSubs(),
                 tags.Tag('athena:handler')(handler='selectSubAccount', event='onchange')]
            ],
            tags.select(id='workLocation', style='display:block')[
                [self.getLocs(),
                 tags.Tag('athena:handler')(handler='selectWorkLocation', event='onchange')]
            ],
            tags.br(),
            tags.input(id='password', type='password', placeholder='password'),
            tags.input(id='clockInOut', type='button', value='ClockInOut')[tags.Tag('athena:handler')(event='onclick', handler='clockInOut')]
        ]
        return self.preprocess(ret)

    @expose
    def selectWorkLocation(self, wloc):
        if wloc == 'All Employees':
            self.workLocation = None
        else:
            self.workLocation = IWorkLocation(wloc)
        self.parent.refresh(self.workLocation, self.subAccount)

    @expose
    def selectSubAccount(self, sub):
        if sub == 'All Employees':
            self.subAccount = None
        else:
            self.subAccount = ISubAccount(sub)
        self.parent.refresh(self.workLocation, self.subAccount)

    @expose
    @Transaction
    def clockIn(self, empRenderer: int, passwd: str):
        emp = self.page.getWidget(empRenderer).getEmployee()
        if emp.alternate_authentication and emp.alternate_authentication.expired:
            self.callRemote('alert', "<div>Your password is expired, please log in and reset your password</div>")
        else:
            def clockIn(valid):
                if valid:
                    ise = ISolomonEmployee(emp)
                    dsa = ise.defaultSubAccount
                    dwl = ise.defaultWorkLocation
                    if not dsa.active:
                        self.callRemote('alert', "<div>Default sub account is disabled, please log in to clock in</div>")
                        return
                    if not dwl.active:
                        self.callRemote('alert', "<div>Default work location is disabled, please log in to clock in</div>")
                        return
                    emp.clockIn(dsa, dwl)
                else:
                    self.callRemote('alert', "<div>Invalid username or password</div>")
            return PublicAPI.asyncLogin(emp, emp.employee_id, passwd).addCallback(clockIn).addErrback(
                lambda *_: self.callRemote('alert', "<div>Invalid username or password</div>"))
    @expose
    @Transaction
    def clockOut(self, empRenderer: int, passwd: str):
        emp = self.page.getWidget(empRenderer).getEmployee()

        def clockOut(valid):
            if valid:
                emp.clockOut()
            else:
                self.callRemote('alert', "<div>Invalid username or password</div>")
        return PublicAPI.asyncLogin(emp, emp, passwd).addCallback(clockOut).addErrback(
            lambda *_: self.callRemote('alert', "<div>Invalid username or password</div>"))

from twisted.python.components import registerAdapter
from zope.interface import implementer

from TimeClock.Axiom.Store import Store
from TimeClock.Database.Commands.SetSupervisor import SetSupervisor
from TimeClock.Database.Commands.SetWorkLocations import SetWorkLocations
from TimeClock.Database.Employee import Employee
from TimeClock.Database.Supervisor import Supervisor
from TimeClock.Database.WorkLocation import WorkLocation
from TimeClock.ITimeClock.IDatabase.IAdministrator import IAdministrator
from TimeClock.ITimeClock.IDatabase.IEmployee import IEmployee
from TimeClock.ITimeClock.IDatabase.ISupervisor import ISupervisor
from TimeClock.ITimeClock.IDatabase.IWorkLocation import IWorkLocation
from TimeClock.ITimeClock.ISolomonEmployee import ISolomonEmployee
from TimeClock.ITimeClock.IWeb.IAthenaRenderable import IAthenaRenderable
from TimeClock.Solomon.Solomon import ACTIVE
from TimeClock.Web.AthenaRenderer.AbstractCommandRenderer import AbstractCommandRenderer
from TimeClock.Web.AthenaRenderer.AbstractRenderer import path
from TimeClock.Web.AthenaRenderer.ListRenderer import ListRenderer
from nevow.athena import expose
from nevow.loaders import xmlfile
from nevow import tags as T


@implementer(IAthenaRenderable)
class SetWorkLocationRenderer(AbstractCommandRenderer):
    docFactory = xmlfile(path + "/Pages/SetWorkLocationRenderer.xml", 'SetWorkLocationPattern')
    jsClass = "TimeClock.WorkLocation"
    sup = None
    loclist = None
    emp = None
    emplist = None
    locations = None
    def render_formArguments(self, ctx, data):

        # @TODO: Move supervisor, administrator, and employee lookups to database util, add command for it
        if self.employee.isAdministrator():
            locs = []
            self.locations = locations = list(Store.query(WorkLocation))
            for loc in locations:
                locs.append({1: loc.description, 2: loc.workLocationID})
            e = [{"Name": ISolomonEmployee(i).name, "Employee ID": i.employee_id}
                 for i in Store.query(Employee)
                 if ISolomonEmployee(i).status == ACTIVE]
            self.loclist = ListRenderer(locs)
            self.emplist = ListRenderer(e)
            self.loclist.prepare(self, callback=None, title="Locations")
            self.emplist.prepare(self, callback=self.empSelected, title="Employees")

            eimp = T.input(id="employeeID", name="employeeID", disabled="")
            self.loclist.visible = True
            self.emplist.visible = True
            ret = [eimp, T.br(), T.input(type='button', value='Load Employee List')[
                T.Tag('athena:handler')(event='onclick', handler='loadEmployeeList')], self.loclist]
            for p in self.preprocessors:
                ret = p(ret)
            return ret
    @expose
    def loadEmployeeList(self):
        return self.emplist
    @expose
    def refresh(self):
        fa = self.render_formArguments(None, None)
        self.callRemote('refreshLists', self.emplist, self.loclist)
    def empSelected(self, idx):
        self.emp = IEmployee(self.emplist.list[int(idx)]['Employee ID'])
        selected = []
        for loc in self.emp.getWorkLocations():
            selected.append(self.locations.index(loc))
        self.callRemote("setEmp", self.emp.employee_id, selected)
        self.emplist.hide()
    @expose
    def runCommand(self, args):
        self.command.execute(IAdministrator(self.employee),
                             IEmployee(int(args[0])), [IWorkLocation(a.strip()) for a in args[1]])
        self.refresh()


registerAdapter(SetWorkLocationRenderer, SetWorkLocations, IAthenaRenderable)

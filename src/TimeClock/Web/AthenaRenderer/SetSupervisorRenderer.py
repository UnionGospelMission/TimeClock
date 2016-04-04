from twisted.python.components import registerAdapter
from zope.interface import implementer

from TimeClock.Axiom.Store import Store
from TimeClock.Database.Commands.SetSupervisor import SetSupervisor
from TimeClock.Database.Employee import Employee
from TimeClock.Database.Supervisor import Supervisor
from TimeClock.ITimeClock.IDatabase.IAdministrator import IAdministrator
from TimeClock.ITimeClock.IDatabase.IEmployee import IEmployee
from TimeClock.ITimeClock.IDatabase.ISupervisor import ISupervisor
from TimeClock.ITimeClock.ISolomonEmployee import ISolomonEmployee
from TimeClock.ITimeClock.IWeb.IAthenaRenderable import IAthenaRenderable
from TimeClock.Web.AthenaRenderer.AbstractCommandRenderer import AbstractCommandRenderer
from TimeClock.Web.AthenaRenderer.AbstractRenderer import path
from TimeClock.Web.AthenaRenderer.ListRenderer import ListRenderer
from nevow.athena import expose
from nevow.loaders import xmlfile
from nevow import tags as T


@implementer(IAthenaRenderable)
class SetSupervisorRenderer(AbstractCommandRenderer):
    docFactory = xmlfile(path + "/Pages/SetSupervisor.xml", 'SetSupervisorPattern')
    jsClass = "TimeClock.SetSupervisor"
    sup = None
    suplist = None
    emp = None
    emplist = None
    def render_formArguments(self, ctx, data):
        # @TODO: Move supervisor, administrator, and employee lookups to database util, add command for it
        if self.employee.isAdministrator():
            s = []
            supervisors = Store.query(Supervisor)
            for sup in supervisors:
                if ISupervisor(sup.employee, None) is sup:
                    s.append({"Name": ISolomonEmployee(sup.employee).name, "Employee ID": sup.employee.employee_id})
            e = [({"Name": ISolomonEmployee(i).name, "Employee ID": i.employee_id, 'Current Supervisor': i.supervisor.employee.employee_id if i.supervisor else None}) for i in Store.query(Employee) if ISolomonEmployee(i).status == 'A']
            self.suplist = ListRenderer(s)
            self.emplist = ListRenderer(e)
            self.suplist.prepare(self, callback=self.supSelected, title="Supervisors")
            self.emplist.prepare(self, callback=self.empSelected, title="Employees")
            simp = T.input(id="supervisorID", name="supervisorID", disabled="")
            eimp = T.input(id="employeeID", name="employeeID", disabled="")
            self.suplist.visible = True
            self.emplist.visible = True
            ret = [eimp,
                   simp,
                   T.br(),
                   T.input(type='button', value='Load Employee List')[
                       T.Tag('athena:handler')(event='onclick', handler='loadEmployeeList')],
                   self.suplist]
            for p in self.preprocessors:
                ret = p(ret)
            return ret
    @expose
    def loadEmployeeList(self):
        return self.emplist
    @expose
    def refresh(self):
        fa = self.render_formArguments(None, None)
        self.callRemote('refreshLists', self.suplist, self.emplist)
    def supSelected(self, idx):
        self.sup = ISupervisor(IEmployee(self.suplist.list[int(idx)]['Employee ID']))
        self.suplist.hide()
        self.callRemote("setSup", self.sup.employee.employee_id)
    def empSelected(self, idx):
        self.emp = IEmployee(self.emplist.list[int(idx)]['Employee ID'])
        self.callRemote("setEmp", self.emp.employee_id)
        self.emplist.hide()
    @expose
    def runCommand(self, args):
        self.command.execute(IAdministrator(self.employee),
                             IEmployee(int(args[0])), (ISupervisor(IEmployee(int(args[1])))))
        self.refresh()


registerAdapter(SetSupervisorRenderer, SetSupervisor, IAthenaRenderable)

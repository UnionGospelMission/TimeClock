from collections import OrderedDict

from TimeClock.Axiom.Store import Store
from TimeClock.Database.SubAccount import SubAccount
from TimeClock.Database.Commands.ViewEmployees import ViewEmployees
from TimeClock.ITimeClock.IDatabase.IAdministrator import IAdministrator
from TimeClock.ITimeClock.IDatabase.ISubAccount import ISubAccount
from TimeClock.ITimeClock.IDatabase.IEmployee import IEmployee
from TimeClock.ITimeClock.IDatabase.ISupervisor import ISupervisor
from TimeClock.ITimeClock.ISolomonEmployee import ISolomonEmployee
from TimeClock.Util.DateTime import DateTime
from TimeClock.Utils import coerce
from TimeClock.Web.AthenaRenderer.AbstractCommandRenderer import AbstractCommandRenderer
from TimeClock.Web.AthenaRenderer.Calendar import Calendar
from nevow.athena import expose

from nevow.loaders import xmlfile
from twisted.python.components import registerAdapter
from zope.interface import implementer

from TimeClock.ITimeClock.IWeb.IAthenaRenderable import IAthenaRenderable
from TimeClock.Web.AthenaRenderer.AbstractRenderer import path
from nevow.tags import input, select, option


@implementer(IAthenaRenderable)
class ViewEmployeesRenderer(AbstractCommandRenderer):
    docFactory = xmlfile(path + "/Pages/ActionItem.xml", 'ActionItemPattern')
    jsClass = "TimeClock.ViewEmployees"
    def render_formArguments(self, ctx, idata):
        if IAdministrator(self.employee, None):
            s = select(name="area")[
                [option(id='all')["all"]]
            ]
            if self.employee.isSupervisor():
                _ = s[
                    option(id="mine")["mine"]
                ]


            for a in Store.query(SubAccount):
                _ = s[option(id=a.sub)[a.name]]
            return s
        return []

    @expose
    def runCommand(self, args):
        args = self.processArgs(args)
        if args:
            if args[0] == 'mine':
                o = list(self.command.execute(ISupervisor(self.employee)))
            else:
                if args[0] == 'all':
                    a = None
                else:
                    a = ISubAccount(args[0])
                o = list(super().execute(a))
        else:
            o = list(super().execute())
        l = []
        for i in o:
            l.append(OrderedDict(EmployeeID=i.employee_id, Name=ISolomonEmployee(i).name))

        print(37, l)
        iar = IAthenaRenderable(l)
        iar.prepare(self, title="Employees", callback=lambda idx: [print(55, idx), self.employeeSelected(l[idx])][1])
        iar.visible = True
        return iar
    @coerce
    def employeeSelected(self, employeeDict: OrderedDict):
        print(60, employeeDict)
        iar = IAthenaRenderable(IEmployee(employeeDict['EmployeeID']))
        iar.prepare(self)
        return iar


registerAdapter(ViewEmployeesRenderer, ViewEmployees, IAthenaRenderable)

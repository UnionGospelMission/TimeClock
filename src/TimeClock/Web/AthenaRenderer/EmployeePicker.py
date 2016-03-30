from zope.interface import implementer

import TimeClock.Utils
from TimeClock import Util
from TimeClock.ITimeClock.IDatabase.IEmployee import IEmployee
from TimeClock.ITimeClock.IDatabase.ISupervisor import ISupervisor
from TimeClock.ITimeClock.ISolomonEmployee import ISolomonEmployee
from TimeClock.ITimeClock.IWeb.IAthenaRenderable import IAthenaRenderable
from TimeClock.Web.AthenaRenderer.AbstractRenderer import path, AbstractRenderer
from TimeClock.Web.AthenaRenderer.ListRenderer import ListRenderer
from nevow import tags
from nevow.athena import expose
from nevow.context import WovenContext
from nevow.loaders import xmlfile


@implementer(IAthenaRenderable)
class EmployeePicker(AbstractRenderer):
    docFactory = xmlfile(path + "/Pages/EmployeePicker.xml", 'EmployeePickerPattern')
    jsClass = "TimeClock.EmployeePicker"
    list = None
    def __init__(self, parent, employees: [IEmployee], callback, limit=1):
        self.prepare(parent)
        self.visible = True
        if employees is None:
            employees = TimeClock.Utils.getAllEmployees()
        self.employees = employees
        self.callback = callback
        self.limit = limit
    def render_formArguments(self, ctx: WovenContext, data):
        self.list = lr = ListRenderer([{'Name': ISolomonEmployee(i).name, 'Employee ID': i.employee_id}
                                       for i in self.employees],
                                      limit=self.limit)
        lr.prepare(self, self.showDetails, "Employees")
        lr.visible = True
        return tags.input(type='button', value='Load Employee List')[tags.Tag("athena:handler")(event="onclick", handler="loadEmployeeList")]
    def render_actionName(self, ctx: WovenContext, data):
        return "Select Employee"
    def showDetails(self, idx):
        iar = IAthenaRenderable(self.employees[int(idx)])
        iar.prepare(self)
        return iar
    @expose
    def loadEmployeeList(self):
        return self.list
    @expose
    def runCallback(self, args):
        emps = [self.employees[int(i)] for i in args]
        self.callback(emps)
        self.hide()

from twisted.python.components import registerAdapter
from zope.interface import implementer

from TimeClock.API.CalendarData import CalendarData
from TimeClock.Database.Commands.ApproveTime import ApproveTime
from TimeClock.ITimeClock.IDatabase.IAdministrator import IAdministrator
from TimeClock.ITimeClock.IDatabase.IEmployee import IEmployee
from TimeClock.ITimeClock.IDatabase.ISupervisor import ISupervisor
from TimeClock.ITimeClock.IDatabase.ITimePeriod import ITimePeriod
from TimeClock.ITimeClock.IDateTime import IDateTime
from TimeClock.ITimeClock.IWeb.IAthenaRenderable import IAthenaRenderable
from TimeClock.Util.DateTime import DateTime
from TimeClock.Web.AthenaRenderer.AbstractCommandRenderer import AbstractCommandRenderer
from TimeClock.Web.AthenaRenderer.AbstractRenderer import path
from TimeClock.Web.AthenaRenderer.Calendar import Calendar
from TimeClock.Web.AthenaRenderer.EmployeePicker import EmployeePicker
from nevow import tags
from nevow.athena import expose
from nevow.loaders import xmlfile


@implementer(IAthenaRenderable)
class ApproveTimeRenderer(AbstractCommandRenderer):
    docFactory = xmlfile(path + '/Pages/ApproveTime.xml', 'ApproveTimePattern')
    jsClass = 'TimeClock.ApproveTime'
    shifts = None
    _employee = None
    eid = None
    shiftRenderer = None
    def render_formArguments(self, ctx, data):
        st = tags.input(type='date', id='startDate')
        et = tags.input(type='date', id='endDate')
        if IAdministrator(self.employee, None):
            self.eid = eid = EmployeePicker(self, None, self.pickEmployee)
        else:
            self.eid = eid = EmployeePicker(self, ISupervisor(self.employee).getEmployees(), self.pickEmployee)
        return st, et, eid
    def pickEmployee(self, employees: [IEmployee]):
        self._employee = employees[0]
        self.callRemote("selectEmployee", self._employee.employee_id)
        self.eid.hide()
    def actionName(self, *args):
        return "Lookup Times"
    @expose
    def runCommand(self, args):
        self._employee = emp = IEmployee(int(args[4]))
        st = DateTime.get(args[0]).replace(minutes=args[1])
        et = DateTime.get(args[2]).replace(days=1).replace(minutes=args[3])
        self.shifts = [i for i in emp.viewHours(st, et) if not i.approved and i.endTime(False)]
        shifts = [{'Start Time': str(i.startTime().asLocalTime()), 'Duration': str(i.duration())}
                  for i in self.shifts
                  ]
        lr = Calendar()
        lr.setData(self.ShiftData(self.shifts))
        lr.prepare(self)
        lr.visible = True
        self.shiftRenderer = lr
        return lr
    @expose
    def approveShifts(self, args):
        a = []
        for arg in args:
            arg = int(arg)
            arg = self.shifts[arg]
            a.append(arg)
        emp = IAdministrator(self.employee, None) or ISupervisor(self.employee, None) or self.employee
        self.eid.list.show()
        self.eid.show()
        self.shiftRenderer.callRemote("onClose")
        return self.command.execute(emp, self._employee, a)
    class ShiftData(object):
        def __init__(self, shifts: [ITimePeriod]):
            self.shifts = shifts
            self.cd = CalendarData(shifts)
        def getData(self, date: IDateTime):
            entries = self.cd.between(date.date(), date.date().replace(days=1))
            o = []
            for entry in entries:
                o.append("Clock In: ")
                o.append(entry.startTime().asLocalTime().strftime("%H:%M"))
                o.append(tags.br())
                o.append("Clock Out: ")
                o.append(entry.endTime().asLocalTime().strftime("%H:%M"))
                o.append(tags.br())
                o.append("Duration: ")
                o.append(str(entry.duration()).split('.')[0])
            return o


registerAdapter(ApproveTimeRenderer, ApproveTime, IAthenaRenderable)

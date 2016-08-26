from twisted.python.components import registerAdapter
from zope.interface import implementer

from TimeClock.Axiom import Transaction
from TimeClock.Axiom.Store import Store
from TimeClock.Database import Commands
from TimeClock.Database.Employee import Employee
from TimeClock.ITimeClock.IDatabase.IEntryType import IEntryType
from TimeClock.ITimeClock.IDatabase.ISupervisor import ISupervisor
from TimeClock.ITimeClock.IDatabase.ITimeEntry import ITimeEntry
from TimeClock.ITimeClock.IDateTime import IDateTime
from TimeClock.ITimeClock.IEvent.IEvent import IEvent
from TimeClock.ITimeClock.IEvent.IEventBus import IEventBus
from TimeClock.ITimeClock.IEvent.IEventHandler import IEventHandler
from TimeClock.ITimeClock.IEvent.IWebEvent.ITimeEntryChangedEvent import ITimeEntryChangedEvent
from TimeClock.ITimeClock.ISolomonEmployee import ISolomonEmployee
from TimeClock.ITimeClock.IWeb.IAthenaRenderable import IAthenaRenderable
from TimeClock.ITimeClock.IWeb.IListRow import IListRow
from TimeClock.Solomon import Solomon
from TimeClock.Utils import coerce, overload
from TimeClock.Web.AthenaRenderers.Abstract.AbstractHideable import AbstractHideable
from TimeClock.Web.AthenaRenderers.Abstract.AbstractRenderer import AbstractRenderer, path
from TimeClock.Web.AthenaRenderers.Commands import AbstractCommandRenderer
from TimeClock.Web.AthenaRenderers.Commands.ApproveShifts import ApproveShifts
from TimeClock.Web.AthenaRenderers.Objects.EmployeeRenderer import EmployeeRenderer
from TimeClock.Web.AthenaRenderers.Widgets.List import List
from TimeClock.Web.AthenaRenderers.Widgets.ListToListSelector import ListToListSelector
from TimeClock.Web.AthenaRenderers.Widgets.SaveList import SaveList
from TimeClock.Web.Events.TimeEntryCreatedEvent import TimeEntryCreatedEvent
from nevow import tags, loaders
from nevow.athena import expose
from nevow.context import WovenContext
from nevow.loaders import xmlfile


@implementer(IEventHandler)
class ApproveTimeOff(ApproveShifts):
    jsClass = 'TimeClock.Commands.ApproveTimeOff'
    name = 'Approve Time Off'
    def getEmployees(self):
        if self.employee.isAdministrator():
            employees = [i for i in list(Store.query(Employee)) if ISolomonEmployee(i).status == Solomon.ACTIVE]
        elif self.employee.isSupervisor():
            employees = [i for i in list(Store.query(Employee, Employee.supervisor == ISupervisor(self.employee))) if
                         ISolomonEmployee(i).status == Solomon.ACTIVE]
        else:
            employees = []
        return employees
    def __init__(self, cmd):
        super().__init__(cmd)
        self.name = cmd.name
        self.entryTypes = (
            IEntryType("Vacation"),
            IEntryType("Illness"),
            IEntryType("Personal"),
        )

    def render_class(self, ctx: WovenContext, data):
        IEventBus("Web").register(self, ITimeEntryChangedEvent)
        return "ApproveTimeOff"
    def render_genericCommand_(self, ctx: WovenContext, data):

        employees = []
        self.l1 = l1 = List(employees, ["Employee ID", "Name"])
        self.l2 = l2 = List([], ["Work Location", "Sub Account", "Date", "Entry Type", "Duration", "Approved", "Denied"])
        self.ltl = ltl = ListToListSelector(l1, l2)
        ltl.mappingReturnsNewElements = True
        ltl.prepare(self)
        ltl.visible = True
        ltl.closeable = False
        ltl.getMappingFor = self.getMappingFor
        ltl.setMappingFor = self.setMappingFor
        l2.setSelectable(False)

        startTime = tags.input(id='startTime', placeholder='Start Time')[tags.Tag('athena:handler')(event='onchange', handler='timeWindowChanged')]
        endTime = tags.input(id='endTime', placeholder='End Time')[
            tags.Tag('athena:handler')(event='onchange', handler='timeWindowChanged')]
        self.preprocess([startTime, endTime])
        return [startTime, endTime, ltl]
    @coerce
    def getMappingFor(self, e: EmployeeRenderer):
        if self.employee.isAdministrator() or e.getEmployee() in ISupervisor(self.employee).getEmployees():
            self.selected = e.getEmployee()
        else:
            return []
        o = []
        timeOffTypes = IEntryType("Vacation"), IEntryType("Illness"), IEntryType("Personal")
        shifts = list(i for i in self.selected.powerupsFor(ITimeEntry) if i.type in timeOffTypes and not i.denied)
        if self.startTime:
            startTime = IDateTime(self.startTime)
        else:
            startTime = None
        if self.endTime:
            endTime = IDateTime(self.endTime)
        else:
            endTime = None
        for shift in shifts:
            if not ((startTime and shift.endTime() < startTime) or (endTime and shift.startTime() > endTime)):
                s = IListRow(shift)
                s.prepare(self.l2)
                o.append(s)
        o.append(SaveList(6).prepare(self.l2))
        return self.preprocess(o)

    @Transaction
    def setMappingFor(self, s: EmployeeRenderer, accounts: [EmployeeRenderer]):
        pass


# registerAdapter(ApproveTimeOff, Commands.ApproveTimeOff.ApproveTimeOff, IAthenaRenderable)


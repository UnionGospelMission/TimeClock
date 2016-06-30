from twisted.python.components import registerAdapter
from zope.interface import implementer

from TimeClock import Exceptions
from TimeClock.Axiom import Transaction
from TimeClock.Axiom.Store import Store
from TimeClock.Database import Commands
from TimeClock.Database.Commands.ApproveTime import ApproveTime
from TimeClock.Database.Employee import Employee
from TimeClock.Database.Supervisor import Supervisor
from TimeClock.ITimeClock.IDatabase.IAdministrator import IAdministrator
from TimeClock.ITimeClock.IDatabase.IEmployee import IEmployee
from TimeClock.ITimeClock.IDatabase.ISupervisor import ISupervisor
from TimeClock.ITimeClock.IDatabase.ITimeEntry import ITimeEntry
from TimeClock.ITimeClock.IEvent.IEvent import IEvent
from TimeClock.ITimeClock.IEvent.IEventBus import IEventBus
from TimeClock.ITimeClock.IEvent.IEventHandler import IEventHandler
from TimeClock.ITimeClock.IEvent.IWebEvent.IEmployeeChangedEvent import IEmployeeChangedEvent
from TimeClock.ITimeClock.IEvent.IWebEvent.ITimeEntryChangedEvent import ITimeEntryChangedEvent
from TimeClock.ITimeClock.ISolomonEmployee import ISolomonEmployee
from TimeClock.ITimeClock.IWeb.IAthenaRenderable import IAthenaRenderable
from TimeClock.ITimeClock.IWeb.IListRow import IListRow
from TimeClock.Utils import coerce, overload
from TimeClock.Web.AthenaRenderers.Abstract.AbstractHideable import AbstractHideable
from TimeClock.Web.AthenaRenderers.Abstract.AbstractRenderer import AbstractRenderer, path
from TimeClock.Web.AthenaRenderers.Objects.EmployeeRenderer import EmployeeRenderer
from TimeClock.Web.AthenaRenderers.Objects.TimeEntryRenderer import TimeEntryRenderer
from TimeClock.Web.AthenaRenderers.Objects.WorkLocationRenderer import WorkLocationRenderer
from TimeClock.Web.AthenaRenderers.Widgets.List import List
from TimeClock.Web.AthenaRenderers.Widgets.ListToListSelector import ListToListSelector
from TimeClock.Web.AthenaRenderers.Widgets.SaveList import SaveList
from TimeClock.Web.Events.SupervisorAssignmentChangedEvent import SupervisorAssignmentChangedEvent
from TimeClock.Web.Events.TimeEntryCreatedEvent import TimeEntryCreatedEvent
from TimeClock.Web.Events.WorkLocationAssignmentChangedEvent import WorkLocationAssignmentChangedEvent
from nevow import tags, loaders
from nevow.context import WovenContext
from nevow.loaders import xmlfile
from nevow.stan import directive


@implementer(IEventHandler)
class ApproveShifts(AbstractRenderer, AbstractHideable):
    docFactory = xmlfile(path + "/Pages/GenericCommand.xml", "GenericCommandPattern")
    jsClass = 'TimeClock.Commands.ApproveShifts'
    workLocations = None
    name = 'Approve Shifts'
    selected = None
    ltl = None
    l1 = None
    l2 = None
    @overload
    def handleEvent(self, evt: TimeEntryCreatedEvent):
        if evt.timeEntry.employee is self.ltl.element:
            self.l2.addRow(evt.timeEntry)
    @overload
    def handleEvent(self, event: IEvent):
        pass
    def render_class(self, ctx: WovenContext, data):
        IEventBus("Web").register(self, ITimeEntryChangedEvent)
        return "ApproveShifts"
    def render_genericCommand(self, ctx: WovenContext, data):
        if self.employee.isAdministrator():
            employees = [i for i in list(Store.query(Employee)) if ISolomonEmployee(i).status == 'A']
        elif self.employee.isSupervisor():
            employees = [i for i in list(Store.query(Employee, Employee.supervisor == ISupervisor(self.employee))) if ISolomonEmployee(i).status == 'A']
        else:
            employees = []
        self.l1 = l1 = List(employees, ["Employee ID", "Name"])
        self.l2 = l2 = List([], ["Work Location", "Sub Account", "Start Time", "End Time", "Duration", "Approved"])
        self.ltl = ltl = ListToListSelector(l1, l2)
        ltl.mappingReturnsNewElements = True
        ltl.prepare(self)
        ltl.visible = True
        ltl.closeable = False
        ltl.getMappingFor = self.getMappingFor
        ltl.setMappingFor = self.setMappingFor
        l2.setSelectable(False)
        return ltl

    @coerce
    def getMappingFor(self, e: EmployeeRenderer):
        if self.employee.isAdministrator() or e.getEmployee() in ISupervisor(self.employee).getEmployees():
            self.selected = e.getEmployee()
        else:
            return []
        o = []
        shifts = self.selected.powerupsFor(ITimeEntry)

        for shift in shifts:
            s = IListRow(shift)
            s.prepare(self.l2)
            o.append(s)
        o.append(SaveList(6).prepare(self.l2))
        return self.preprocess(o)

    @Transaction
    def setMappingFor(self, s: EmployeeRenderer, accounts: [EmployeeRenderer]):
        pass


registerAdapter(ApproveShifts, ApproveTime, IAthenaRenderable)

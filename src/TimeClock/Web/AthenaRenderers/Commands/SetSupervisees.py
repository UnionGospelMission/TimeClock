from twisted.python.components import registerAdapter
from zope.interface import implementer

from TimeClock import Exceptions
from TimeClock.Axiom import Transaction
from TimeClock.Axiom.Store import Store
from TimeClock.Database import Commands
from TimeClock.Database.Employee import Employee
from TimeClock.Database.Supervisor import Supervisor
from TimeClock.ITimeClock.IDatabase.IAdministrator import IAdministrator
from TimeClock.ITimeClock.IDatabase.IEmployee import IEmployee
from TimeClock.ITimeClock.IDatabase.ISupervisee import ISupervisee
from TimeClock.ITimeClock.IDatabase.ISupervisor import ISupervisor
from TimeClock.ITimeClock.IEvent.IEvent import IEvent
from TimeClock.ITimeClock.IEvent.IEventBus import IEventBus
from TimeClock.ITimeClock.IEvent.IEventHandler import IEventHandler
from TimeClock.ITimeClock.IEvent.IWebEvent.IEmployeeChangedEvent import IEmployeeChangedEvent
from TimeClock.ITimeClock.IEvent.IWebEvent.ISupervisorCreatedRemovedEvent import ISupervisorCreatedRemovedEvent
from TimeClock.ITimeClock.ISolomonEmployee import ISolomonEmployee
from TimeClock.ITimeClock.IWeb.IAthenaRenderable import IAthenaRenderable
from TimeClock.ITimeClock.IWeb.IListRow import IListRow
from TimeClock.Solomon import Solomon
from TimeClock.Utils import coerce, overload
from TimeClock.Web.AthenaRenderers.Abstract.AbstractHideable import AbstractHideable
from TimeClock.Web.AthenaRenderers.Abstract.AbstractRenderer import AbstractRenderer, path
from TimeClock.Web.AthenaRenderers.Commands import AbstractCommandRenderer
from TimeClock.Web.AthenaRenderers.Objects.EmployeeRenderer import EmployeeRenderer
from TimeClock.Web.AthenaRenderers.Objects.WorkLocationRenderer import WorkLocationRenderer
from TimeClock.Web.AthenaRenderers.Widgets.List import List
from TimeClock.Web.AthenaRenderers.Widgets.ListToListSelector import ListToListSelector
from TimeClock.Web.Events.SupervisorAssignmentChangedEvent import SupervisorAssignmentChangedEvent
from TimeClock.Web.Events.SupervisorCreatedEvent import SupervisorCreatedEvent
from TimeClock.Web.Events.SupervisorRemovedEvent import SupervisorRemovedEvent
from TimeClock.Web.Events.WorkLocationAssignmentChangedEvent import WorkLocationAssignmentChangedEvent
from nevow.athena import expose
from nevow.context import WovenContext
from nevow.loaders import xmlfile


@implementer(IEventHandler)
class SetSupervisees(AbstractCommandRenderer, AbstractHideable):
    docFactory = xmlfile(path + "/Pages/GenericCommand.xml", "GenericCommandPattern")
    jsClass = 'TimeClock.Commands'
    workLocations = None
    name = 'Set Supervisees'
    selected = None
    ltl = None
    loaded = False
    @expose
    def load(self, active: bool = True, inactive: bool = False):
        if not self.loaded:
            self.ltl.l2.list = [IListRow(i).prepare(self.ltl.l2) for i in list(Store.query(Employee)) if
                                ISolomonEmployee(i).status == Solomon.ACTIVE]
            self.ltl.l2.callRemote('select', self.ltl.l2.list, True)
            self.loaded = True

    @overload
    def handleEvent(self, event: SupervisorAssignmentChangedEvent):
        if event.employee.supervisor and event.employee.supervisor is self.selected:
            self.ltl.callRemote("refresh");
    @overload
    def handleEvent(self, event: SupervisorCreatedEvent):
        iar = IListRow(event.employee)
        self.ltl.l1.addRow(iar)

    @overload
    def handleEvent(self, event: SupervisorRemovedEvent):
        self.ltl.l1.removeRow(event.employee)

    @overload
    def handleEvent(self, event: IEvent):
        pass

    def render_class(self, ctx: WovenContext, data):
        IEventBus("Web").register(self, IEmployeeChangedEvent)
        IEventBus("Web").register(self, ISupervisorCreatedRemovedEvent)
        return "SetSupservisors"
    def render_genericCommand(self, ctx: WovenContext, data):
        sups = []
        for sup in Store.query(Supervisor):
            if sup.employee and ISupervisor(sup.employee, None) is sup:
                sups.append(sup.employee)

        l2 = List([], ["Employee ID", "Name"])
        l1 = List(sups, ["Supervisor ID", "Name"])
        self.ltl = ltl = ListToListSelector(l1, l2)
        ltl.prepare(self)
        ltl.visible = True
        ltl.closeable = False
        ltl.getMappingFor = self.getMappingFor
        ltl.setMappingFor = self.setMappingFor
        return ltl

    @coerce
    def getMappingFor(self, e: EmployeeRenderer):
        self.selected = ISupervisor(IEmployee(e.getEmployee()), None)
        if not self.selected:
            return []

        o = []
        employees = self.selected.getEmployees()

        for emp in employees:
            for i in self.ltl.liveFragmentChildren[1].liveFragmentChildren:
                if isinstance(i, EmployeeRenderer):
                    if i.getEmployee() is emp:
                        o.append(i)
        return o

    @Transaction
    def setMappingFor(self, s: EmployeeRenderer, accounts: [EmployeeRenderer]):
        if not s or not s.getEmployee():
            raise Exceptions.DatabasException("No supervisor selected")
        sup = ISupervisor(s.getEmployee(), None)
        if not sup:
            raise Exceptions.DatabasException("%s is not a supervisor" % s.name)
        for emp in sup.getEmployees():
            emp.supervisor = None
            sup.powerDown(emp, ISupervisee)
        if self.args[0].hasPermission(self.employee):
            for e in accounts:
                try:
                    oldsup = e.getEmployee().supervisor
                    newsup = sup
                    self.args[0].execute(IAdministrator(self.employee), e.getEmployee(), newsup)
                    e = SupervisorAssignmentChangedEvent(e.getEmployee(), oldsup)
                    IEventBus("Web").postEvent(e)
                    if e.cancelled:
                        raise Exceptions.DatabaseChangeCancelled()
                except Exceptions.DatabaseChangeCancelled:
                    continue



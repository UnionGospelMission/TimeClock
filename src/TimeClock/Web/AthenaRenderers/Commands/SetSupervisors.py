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
class SetSupervisors(AbstractCommandRenderer, AbstractHideable):
    docFactory = xmlfile(path + "/Pages/GenericCommand.xml", "GenericCommandPattern")
    jsClass = 'TimeClock.Commands'
    workLocations = None
    name = 'Set Supervisors'
    selected = None
    ltl = None
    loaded = False

    @expose
    def load(self, active: bool = True, inactive: bool = False):
        if not self.loaded:
            self.ltl.l1.list = [IListRow(i).prepare(self.ltl.l1) for i in list(Store.query(Employee)) if ISolomonEmployee(i).status == Solomon.ACTIVE]
            self.ltl.l1.callRemote('select', self.ltl.l1.list, True)
            self.loaded = True

    @overload
    def handleEvent(self, event: SupervisorAssignmentChangedEvent):
        if event.employee is self.selected:
            self.ltl.callRemote("refresh");
    @overload
    def handleEvent(self, event: SupervisorCreatedEvent):
        iar = IListRow(event.employee)
        self.ltl.l2.addRow(iar)

    @overload
    def handleEvent(self, event: SupervisorRemovedEvent):
        self.ltl.l2.removeRow(event.employee)
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

        l1 = List([], ["Employee ID", "Name"])
        l2 = List(sups, ["Supervisor ID", "Name"])
        l2.limit = 1
        self.ltl = ltl = ListToListSelector(l1, l2)
        ltl.prepare(self)
        ltl.visible = True
        ltl.closeable = False
        ltl.getMappingFor = self.getMappingFor
        ltl.setMappingFor = self.setMappingFor
        return ltl

    @coerce
    def getMappingFor(self, e: EmployeeRenderer):
        self.selected = IEmployee(e.getEmployee())
        sup = self.selected.supervisor
        if sup and (not sup.employee or not ISupervisor(sup.employee, None)):
            self.selected.supervisor = None
            sup = None
        if not sup:
            return []
        for i in self.ltl.liveFragmentChildren[1].liveFragmentChildren:
            if isinstance(i, EmployeeRenderer):
                if i.getEmployee() is sup.employee:
                    return [i]

    @Transaction
    def setMappingFor(self, e: EmployeeRenderer, accounts: [EmployeeRenderer]):
        if not e:
            raise Exceptions.DatabasException("No employee selected")
        if self.args[0].hasPermission(self.employee):
            oldsup = e.getEmployee().supervisor
            if len(accounts) > 1:
                raise Exceptions.DatabasException("Employee cannot have more than one supervisor")
            if not accounts:
                self.args[0].execute(IAdministrator(self.employee), e.getEmployee(), None)
            else:
                newsup = ISupervisor(accounts[0].getEmployee())
                self.args[0].execute(IAdministrator(self.employee), e.getEmployee(), newsup)
            e = SupervisorAssignmentChangedEvent(e.getEmployee(), oldsup)
            IEventBus("Web").postEvent(e)
            if e.cancelled:
                raise Exceptions.DatabaseChangeCancelled()


registerAdapter(SetSupervisors, Commands.SetSupervisor.SetSupervisor, IAthenaRenderable)

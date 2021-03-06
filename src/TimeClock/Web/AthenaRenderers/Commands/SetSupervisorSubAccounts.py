from TimeClock.Database.Supervisor import Supervisor
from TimeClock.ITimeClock.IDatabase.ISupervisor import ISupervisor
from TimeClock.ITimeClock.IEvent.IWebEvent.ISupervisorCreatedRemovedEvent import ISupervisorCreatedRemovedEvent
from TimeClock.Web.Events.SupervisorCreatedEvent import SupervisorCreatedEvent
from TimeClock.Web.Events.SupervisorRemovedEvent import SupervisorRemovedEvent
from twisted.python.components import registerAdapter
from zope.interface import implementer

from TimeClock import Exceptions
from TimeClock.Axiom import Transaction
from TimeClock.Axiom.Store import Store
from TimeClock.Database.Commands.SetSupervisorSubAccounts import SetSupervisorSubAccounts as sssa
from TimeClock.Database.Employee import Employee
from TimeClock.Database.SubAccount import SubAccount
from TimeClock.ITimeClock.IDatabase.IAdministrator import IAdministrator
from TimeClock.ITimeClock.IDatabase.IEmployee import IEmployee
from TimeClock.ITimeClock.IEvent.IEvent import IEvent
from TimeClock.ITimeClock.IEvent.IEventBus import IEventBus
from TimeClock.ITimeClock.IEvent.IEventHandler import IEventHandler
from TimeClock.ITimeClock.IEvent.IWebEvent.IEmployeeChangedEvent import IEmployeeChangedEvent
from TimeClock.ITimeClock.ISolomonEmployee import ISolomonEmployee
from TimeClock.ITimeClock.IWeb.IAthenaRenderable import IAthenaRenderable
from TimeClock.ITimeClock.IWeb.IListRow import IListRow
from TimeClock.Solomon import Solomon
from TimeClock.Utils import coerce, overload
from TimeClock.Web.AthenaRenderers.Abstract.AbstractHideable import AbstractHideable
from TimeClock.Web.AthenaRenderers.Abstract.AbstractRenderer import AbstractRenderer, path
from TimeClock.Web.AthenaRenderers.Commands import AbstractCommandRenderer
from TimeClock.Web.AthenaRenderers.Objects.EmployeeRenderer import EmployeeRenderer
from TimeClock.Web.AthenaRenderers.Objects.SubAccountRenderer import SubAccountRenderer
from TimeClock.Web.AthenaRenderers.Widgets.List import List
from TimeClock.Web.AthenaRenderers.Widgets.ListToListSelector import ListToListSelector
from TimeClock.Web.Events.SubAccountAssignmentChangedEvent import SubAccountAssignmentChangedEvent
from nevow.athena import expose
from nevow.context import WovenContext
from nevow.loaders import xmlfile


@implementer(IEventHandler)
class SetSupervisorSubAccounts(AbstractCommandRenderer, AbstractHideable):
    docFactory = xmlfile(path + "/Pages/GenericCommand.xml", "GenericCommandPattern")
    jsClass = 'TimeClock.Commands'
    subaccounts = None
    name = 'Set Supervisor Sub Accounts'
    selected = None
    ltl = None
    loaded = False

    @expose
    def load(self, active: bool = True, inactive: bool = False):
        if not self.loaded:
            self.ltl.l1.list = [IListRow(i.employee).prepare(self.ltl.l1) for i in list(Store.query(Supervisor)) if
                                ISolomonEmployee(i.employee).status == Solomon.ACTIVE and ISupervisor(i.employee, None) is i]
            self.ltl.l1.callRemote('select', self.ltl.l1.list, True)
            self.loaded = True

    @overload
    def handleEvent(self, event: SubAccountAssignmentChangedEvent):
        if self.selected and event.employee is self.selected.employee:
            self.ltl.callRemote("refresh")

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
        return "SetSupervisorSubAccounts"

    def render_genericCommand(self, ctx: WovenContext, data):
        l1 = List([], ["Employee ID", "Name"])
        l2 = List([i for i in list(Store.query(SubAccount)) if i.active], ["Sub Account", "Name", "Active"])
        self.ltl = ltl = ListToListSelector(l1, l2)
        ltl.closeable = False
        ltl.prepare(self)
        ltl.visible = True
        ltl.getMappingFor = self.getMappingFor
        ltl.setMappingFor = self.setMappingFor
        return ltl

    @coerce
    def getMappingFor(self, e: EmployeeRenderer):
        self.selected = ISupervisor(e.getEmployee())
        o = []
        sa = self.selected.getSubAccounts()
        for sub in sa:
            for i in self.ltl.liveFragmentChildren[1].liveFragmentChildren:
                if i.getSub() is sub:
                    o.append(i)
                    break
        return o

    @Transaction
    def setMappingFor(self, e: EmployeeRenderer, accounts: [SubAccountRenderer]):
        # @TODO: add event hook
        if self.args[0].hasPermission(self.employee):
            p = ISupervisor(e.getEmployee()).getSubAccounts()
            self.args[0].execute(IAdministrator(self.employee), ISupervisor(e.getEmployee()), [i.getSub() for i in accounts])
            e = SubAccountAssignmentChangedEvent(e.getEmployee(), p)
            IEventBus("Web").postEvent(e)
            if e.cancelled:
                raise Exceptions.DatabaseChangeCancelled()


registerAdapter(SetSupervisorSubAccounts, sssa, IAthenaRenderable)

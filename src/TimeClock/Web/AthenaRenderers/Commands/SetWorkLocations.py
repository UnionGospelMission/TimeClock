from twisted.python.components import registerAdapter
from zope.interface import implementer

from TimeClock import Exceptions
from TimeClock.Axiom import Transaction
from TimeClock.Axiom.Store import Store
from TimeClock.Database.Commands.SetWorkLocations import SetWorkLocations as ssa
from TimeClock.Database.Employee import Employee
from TimeClock.Database.WorkLocation import WorkLocation
from TimeClock.ITimeClock.IDatabase.IAdministrator import IAdministrator
from TimeClock.ITimeClock.IDatabase.IEmployee import IEmployee
from TimeClock.ITimeClock.IEvent.IEvent import IEvent
from TimeClock.ITimeClock.IEvent.IEventBus import IEventBus
from TimeClock.ITimeClock.IEvent.IEventHandler import IEventHandler
from TimeClock.ITimeClock.IEvent.IWebEvent.IEmployeeChangedEvent import IEmployeeChangedEvent
from TimeClock.ITimeClock.IWeb.IAthenaRenderable import IAthenaRenderable
from TimeClock.Utils import coerce, overload
from TimeClock.Web.AthenaRenderers.Abstract.AbstractHideable import AbstractHideable
from TimeClock.Web.AthenaRenderers.Abstract.AbstractRenderer import AbstractRenderer, path
from TimeClock.Web.AthenaRenderers.Objects.EmployeeRenderer import EmployeeRenderer
from TimeClock.Web.AthenaRenderers.Objects.WorkLocationRenderer import WorkLocationRenderer
from TimeClock.Web.AthenaRenderers.Widgets.List import List
from TimeClock.Web.AthenaRenderers.Widgets.ListToListSelector import ListToListSelector
from TimeClock.Web.Events.WorkLocationAssignmentChangedEvent import WorkLocationAssignmentChangedEvent
from nevow.context import WovenContext
from nevow.loaders import xmlfile


@implementer(IEventHandler)
class SetWorkLocations(AbstractRenderer, AbstractHideable):
    docFactory = xmlfile(path + "/Pages/GenericCommand.xml", "GenericCommandPattern")
    jsClass = 'TimeClock.Commands'
    workLocations = None
    name = 'Set Work Locations'
    selected = None
    ltl = None

    @overload
    def handleEvent(self, event: WorkLocationAssignmentChangedEvent):
        print(39, event.employee, self.selected)
        if event.employee is self.selected:
            self.ltl.callRemote("refresh");

    @overload
    def handleEvent(self, event: IEvent):
        pass

    def render_class(self, ctx: WovenContext, data):
        IEventBus("Web").register(self, IEmployeeChangedEvent)
        return "SetWorkLocations"
    def render_genericCommand(self, ctx: WovenContext, data):
        l1 = List(list(Store.query(Employee)), ["Employee ID", "Name"])
        l2 = List(list(Store.query(WorkLocation)), ["Sub Account", "Name", "Active"])
        self.ltl = ltl = ListToListSelector(l1, l2)
        ltl.closeable = False
        ltl.prepare(self)
        ltl.visible = True
        ltl.getMappingFor = self.getMappingFor
        ltl.setMappingFor = self.setMappingFor
        return ltl

    @coerce
    def getMappingFor(self, e: EmployeeRenderer):
        self.selected = IEmployee(e.getEmployee())
        o = []
        sa = self.selected.getWorkLocations()
        for sub in sa:
            for i in self.ltl.liveFragmentChildren[1].liveFragmentChildren:
                if i.getWLoc() is sub:
                    o.append(i)
                    break
        return o

    @Transaction
    def setMappingFor(self, e: EmployeeRenderer, accounts: [WorkLocationRenderer]):
        # @TODO: add event hook
        print(48, e, accounts)
        if self.args[0].hasPermission(self.employee):
            p = e.getEmployee().getWorkLocations()
            self.args[0].execute(IAdministrator(self.employee), e.getEmployee(), [i.getWLoc() for i in accounts])
            e = WorkLocationAssignmentChangedEvent(e.getEmployee(), p)
            IEventBus("Web").postEvent(e)
            if e.cancelled:
                raise Exceptions.DatabaseChangeCancelled()


registerAdapter(SetWorkLocations, ssa, IAthenaRenderable)

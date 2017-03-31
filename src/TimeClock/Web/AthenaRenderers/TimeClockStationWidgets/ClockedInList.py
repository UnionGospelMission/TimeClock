from zope.interface import implementer

from TimeClock.Database.Employee import Employee
from TimeClock.Database.Event.ClockInOutEvent import ClockInOutEvent
from TimeClock.ITimeClock.IEvent.IDatabaseEvent import IDatabaseEvent
from TimeClock.ITimeClock.IEvent.IEvent import IEvent
from TimeClock.ITimeClock.IEvent.IEventBus import IEventBus
from TimeClock.ITimeClock.IEvent.IEventHandler import IEventHandler
from TimeClock.ITimeClock.ISolomonEmployee import ISolomonEmployee
from TimeClock.ITimeClock.IWeb.IListRow import IListRow
from TimeClock.Solomon import Solomon
from TimeClock.Utils import overload, getAllEmployees
from TimeClock.Web.AthenaRenderers.Abstract.AbstractHideable import AbstractHideable
from TimeClock.Web.AthenaRenderers.Abstract.AbstractRenderer import AbstractRenderer, path
from TimeClock.Web.AthenaRenderers.Widgets.List import List
from nevow import tags
from nevow.context import WovenContext
from nevow.loaders import xmlfile


@implementer(IEventHandler)
class ClockedInList(AbstractRenderer, AbstractHideable):
    jsClass = "TimeClock.TimeClockStation.ClockedIn"
    label = 'Currently Clocked In'
    docFactory = xmlfile(path + "/Pages/GenericCommand.xml", "GenericCommandPattern")
    lst = None
    visible = True
    wloc = None
    sub = None

    def powerUp(self, obj, iface):
        pass

    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.setFragmentParent(parent)

    @overload
    def handleEvent(self, event: ClockInOutEvent):
        if self.wloc:
            if event.employee not in self.wloc.getEmployees():
                return
        if self.sub:
            if event.employee not in self.sub.getEmployees():
                return
        if not self.lst:
            return
        if not event.clockedIn:
            self.lst.removeRow(event.employee)
        else:
            self.lst.addRow(IListRow(event.employee).setKeys("name"))

    @overload
    def handleEvent(self, event: IEvent):
        pass

    def render_class(self, *a):
        return 'ClockedIn'

    def getEmpList(self, wloc=None, sub=None):
        self.wloc = wloc
        self.sub = sub
        if wloc and sub:
            wemployees = wloc.getEmployees()
            semployees = sub.getEmployees()
            return [i for i in wemployees if i in semployees and i.timeEntry]
        if wloc:
            wemployees = wloc.getEmployees()
            return [i for i in wemployees if i.timeEntry]
        if sub:
            semployees = sub.getEmployees()
            return [i for i in semployees if i.timeEntry]
        return [i for i in getAllEmployees() if ISolomonEmployee(i).status == Solomon.ACTIVE and i.timeEntry]

    def render_genericCommand(self, ctx: WovenContext, data):
        IEventBus("Database").register(self, IDatabaseEvent)
        empList = self.getEmpList()
        self.lst = List([IListRow(i).setKeys("name") for i in empList], ['Employee Name'])
        self.lst.prepare(self)
        self.lst.visible = True
        self.lst.name = "Clocked In"
        self.lst.selectable = True
        self.lst.limit = 1
        return self.lst

    def refresh(self, wloc, subaccount):
        empList = self.getEmpList(wloc, subaccount)
        empList = [IListRow(i).prepare(self.lst).setKeys("name") for i in empList]
        self.lst.callRemote('select', empList, True)
        self.lst.list = list(empList)


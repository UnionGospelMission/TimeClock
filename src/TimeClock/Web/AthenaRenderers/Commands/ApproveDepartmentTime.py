import types
import time
from collections import defaultdict

import datetime

from TimeClock.ITimeClock.IDatabase.ISupervisedBy import ISupervisedBy
from twisted.python.reflect import qual

import twisted.internet.threads
from TimeClock.Util.IterateInReactor import IterateInReactor
from TimeClock.Web.AthenaRenderers.Objects.WorkLocationRenderer import WorkLocationRenderer
from axiom.item import _PowerupConnector

from twisted.internet import reactor

import TimeClock
from TimeClock.Database.TimeEntry import TimeEntry
from TimeClock.Database.TimePeriod import TimePeriod
from TimeClock.Util.DateTime import DateTime
from TimeClock.Web.AthenaRenderers.Widgets.StaticListRow import StaticListRow
from axiom.attributes import AND, OR
from twisted.python.components import registerAdapter
from zope.interface import implementer

from TimeClock.Axiom import Transaction
from TimeClock.Axiom.Store import Store
from TimeClock.Database.EntryType import EntryType
from TimeClock.Database.Commands.ApproveTime import ApproveTime
from TimeClock.Database.Employee import Employee
from TimeClock.ITimeClock.IDatabase.IAdministrator import IAdministrator
from TimeClock.ITimeClock.IDatabase.IEntryType import IEntryType
from TimeClock.ITimeClock.IDatabase.ISupervisor import ISupervisor
from TimeClock.ITimeClock.IDatabase.ITimeEntry import ITimeEntry
from TimeClock.ITimeClock.IDatabase.ITimePeriod import ITimePeriod
from TimeClock.ITimeClock.IDateTime import IDateTime
from TimeClock.ITimeClock.IEvent.IEvent import IEvent
from TimeClock.ITimeClock.IEvent.IEventBus import IEventBus
from TimeClock.ITimeClock.IEvent.IEventHandler import IEventHandler
from TimeClock.ITimeClock.IEvent.IWebEvent.ITimeEntryChangedEvent import ITimeEntryChangedEvent
from TimeClock.ITimeClock.ISolomonEmployee import ISolomonEmployee
from TimeClock.ITimeClock.IWeb.IAthenaRenderable import IAthenaRenderable
from TimeClock.ITimeClock.IWeb.IListRow import IListRow
from TimeClock.Solomon import Solomon
from TimeClock.Util import NULL
from TimeClock.Utils import coerce, overload
from TimeClock.Web.AthenaRenderers.Abstract.AbstractHideable import AbstractHideable
from TimeClock.Web.AthenaRenderers.Abstract.AbstractRenderer import AbstractRenderer, path
from TimeClock.Web.AthenaRenderers.Commands import AbstractCommandRenderer
from TimeClock.Web.AthenaRenderers.Objects.EmployeeRenderer import EmployeeRenderer
from TimeClock.Web.AthenaRenderers.Widgets.List import List
from TimeClock.Web.AthenaRenderers.Widgets.ListToListSelector import ListToListSelector
from TimeClock.Web.AthenaRenderers.Widgets.SaveList import SaveList
from TimeClock.Web.Events.TimeEntryChangedEvent import TimeEntryChangedEvent
from TimeClock.Web.Events.TimeEntryCreatedEvent import TimeEntryCreatedEvent
from nevow import tags
from nevow.athena import expose
from nevow.context import WovenContext
from nevow.loaders import xmlfile


@implementer(IEventHandler)
class ApproveDepartmentTime(AbstractCommandRenderer, AbstractHideable):
    docFactory = xmlfile(path + "/Pages/GenericCommand.xml", "GenericCommandPattern")
    jsClass = 'TimeClock.Commands.ApproveDepartmentTime'
    workLocations = None
    name = 'Approve Department Time'
    selected = None
    ltl = None
    l1 = None
    l2 = None
    startTime = DateTime.today().replace(weeks=-1)
    endTime = None
    loaded = False

    @expose
    def startTimeChanged(self, startTime):
        self.startTime = startTime

    @expose
    def endTimeChanged(self, endTime):
        self.endTime = endTime

    @expose
    def timeWindowChanged(self, startTime, endTime):
        self.startTime = startTime
        self.endTime = endTime

    def getEmployees(self):
        if self.employee.isAdministrator():
            employees = [i for i in list(Store.query(Employee)) if ISolomonEmployee(i).status == Solomon.ACTIVE]
        elif self.employee.isSupervisor():
            sup = ISupervisor(self.employee)
            employees = [i for i in sup.getEmployees() if ISolomonEmployee(i).status == Solomon.ACTIVE]
        else:
            employees = []
        return employees

    def getLocations(self):
        locations = set()
        for emp in self.getEmployees():
            locations.update(list(emp.getWorkLocations()))
        return locations

    @expose
    def load(self, active: bool = True, inactive: bool = False):
        if not self.loaded:
            self.ltl.l1.list = [IListRow(i).prepare(self.ltl.l1) for i in self.getLocations()]
            self.ltl.l1.callRemote('select', self.ltl.l1.list, True)
            self.loaded = True

    def __init__(self, cmd):
        super().__init__(cmd)
        self.startTime = DateTime.today().replace(weeks=-1)
        self.endTime = DateTime.today().replace(days=1)

    @overload
    def handleEvent(self, evt: TimeEntryCreatedEvent):
        if evt.timeEntry.workLocation is self.selected:
            self.l2.addRow(evt.timeEntry)

    @overload
    def handleEvent(self, evt: TimeEntryChangedEvent):
        if evt.timeEntry.denied:
            self.l2.removeRow(evt.timeEntry)

    @overload
    def handleEvent(self, event: IEvent):
        pass

    def render_class(self, ctx: WovenContext, data):
        IEventBus("Web").register(self, ITimeEntryChangedEvent)
        return "ApproveDepartmentTime"

    def render_genericCommand(self, ctx: WovenContext, data):

        locations = []
        self.l1 = l1 = List(locations, ["Work Location"])
        self.l2 = l2 = List([], ["Entry Type", "Employee", "Sub Account", "Start Time", "End Time", "Shift Duration", "Daily Total", "Approved", "Denied"])
        self.ltl = ltl = ListToListSelector(l1, l2)
        ltl.mappingReturnsNewElements = True
        ltl.prepare(self)
        ltl.visible = True
        ltl.closeable = False
        ltl.getMappingFor = self.getMappingFor
        ltl.setMappingFor = self.setMappingFor
        l2.setSelectable(False)

        startTime = tags.input(id='startTime', placeholder='Start Time')#[tags.Tag('athena:handler')(event='onchange', handler='timeWindowChanged')]
        endTime = tags.input(id='endTime', placeholder='End Time')

        self.preprocess([startTime, endTime])
        return [startTime, endTime, tags.br(), ltl]

    @coerce
    def getMappingFor(self, e: WorkLocationRenderer):
        self.selected = e._workLocation

        isAdm = self.employee.isAdministrator()

        store = self.employee.store

        q = AND(
            TimeEntry.workLocation==self.selected,
            TimeEntry.type==EntryType.storeID,
            EntryType.active==True,
            TimeEntry.period==TimePeriod.storeID,
            TimeEntry.employee==Employee.storeID,
            _PowerupConnector.interface==str(qual(ISupervisedBy)),
            _PowerupConnector.item==Employee.storeID,
            TimeEntry.approved==False,
            TimeEntry.denied==False

        )
        q.conditions = list(q.conditions)

        if self.endTime:
            q.conditions.append(
                TimePeriod._startTime <= IDateTime(self.endTime)
            )

        if self.startTime:
            q.conditions.append(
                OR(
                    TimePeriod._endTime >= IDateTime(self.startTime),
                    TimePeriod._endTime==None
                )
            )

        if not isAdm:
            q.conditions.append(TimeEntry.denied==False)
            q.conditions.append(_PowerupConnector.powerup == ISupervisor(self.employee))

        self.__class__.q = q

        shifts = (i[0] for i in store.query((TimeEntry, TimePeriod, EntryType, Employee, _PowerupConnector), q, sort=TimePeriod._startTime.asc))
        return IterateInReactor(self.prepareShifts(shifts))

    def prepareShifts(self, shifts):
        o = []
        for shift in shifts:
            # if not ((startTime and shift.endTime() < startTime) or (endTime and shift.startTime() > endTime)):
            s = IListRow(shift)
            s.showEmployee()
            s.prepare(self.l2)
            o.append(s)
            yield s
        yield SaveList(8).prepare(self.l2)

    @Transaction
    def setMappingFor(self, s: EmployeeRenderer, accounts: [EmployeeRenderer]):
        pass

import types
import time
from collections import defaultdict

import datetime

import twisted.internet.threads
from TimeClock.Util.IterateInReactor import IterateInReactor

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
class ApproveShifts(AbstractCommandRenderer, AbstractHideable):
    docFactory = xmlfile(path + "/Pages/GenericCommand.xml", "GenericCommandPattern")
    jsClass = 'TimeClock.Commands.ApproveShifts'
    workLocations = None
    name = 'Approve Shifts'
    selected = None
    ltl = None
    l1 = None
    l2 = None
    startTime = DateTime.today().replace(day=1).replace(months=-1)
    endTime = None
    loaded = False

    def getEmployees(self):
        if self.employee.isAdministrator():
            employees = [i for i in list(Store.query(Employee)) if ISolomonEmployee(i).status == Solomon.ACTIVE]
        elif self.employee.isSupervisor():
            sup = ISupervisor(self.employee)
            employees = [i for i in sup.getEmployees() if ISolomonEmployee(i).status == Solomon.ACTIVE]
        else:
            employees = []
        return employees

    @expose
    def load(self, active: bool = True, inactive: bool = False):
        if not self.loaded:
            self.ltl.l1.list = [IListRow(i).prepare(self.ltl.l1) for i in self.getEmployees()]
            self.ltl.l1.callRemote('select', self.ltl.l1.list, True)
            self.loaded = True

    def __init__(self, cmd):
        super().__init__(cmd)
        self.name = cmd.name
        if isinstance(cmd, ApproveTime):
            self.entryType = IEntryType("Work")
            self.entryTypes = self.entryTypes = tuple(
                self.args[0].store.query(EntryType, EntryType.active == True)
            )
        self.startTime = DateTime.today().replace(day=1).replace(months=-1)

    @overload
    def handleEvent(self, evt: TimeEntryCreatedEvent):
        if evt.timeEntry.employee is self.selected:
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
        return "ApproveShifts"

    def render_genericCommand(self, ctx: WovenContext, data):

        employees = []
        self.l1 = l1 = List(employees, ["Employee ID", "Name"])
        self.l2 = l2 = List([], ["Entry Type", "Work Location", "Sub Account", "Start Time", "End Time", "Shift Duration", "Daily Total", "Approved", "Denied"])
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
        addTime = [
            tags.input(id='addTime', type='button', value='Add Time Entry')[
                tags.Tag('athena:handler')(event='onclick', handler='addTime')],
            tags.select(id='newTimeType')[
                [tags.option(id=et.getTypeName())[et.getTypeName()] for et in self.entryTypes]
                ]
            ]
        if not IAdministrator(self.employee, None):
            addTime = ''

        self.preprocess([startTime, endTime, addTime])
        return [startTime, endTime, tags.br(), addTime, ltl]

    @expose
    @Transaction
    def addTime(self, typ):
        typ = IEntryType(typ)
        if IAdministrator(self.employee) and self.selected is not self.employee:
            if self.selected:
                ise = ISolomonEmployee(self.selected)
                a = ITimeEntry(NULL)
                a.subAccount = ise.defaultSubAccount
                a.workLocation = ise.defaultWorkLocation
                a.employee = self.selected
                a.period = ITimePeriod(NULL)
                a.type = typ
                a.period.end(a.period.startTime())
                self.selected.powerUp(a, ITimeEntry)
                e = TimeEntryCreatedEvent(a)
                IEventBus("Web").postEvent(e)
            else:
                raise Exception("No Employee Selected")
        else:
            raise Exception("Permission Denied")

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

    def addTotals(self, lst):
        out = []
        def render_listRow(self, ctx: WovenContext, data=None):
            r = self.old_render_listRow(ctx, data)
            r[1](style='opacity: 0')
            r[2](style='opacity: 0')
            r[3](style='opacity: 0')
            r[4](style='opacity: 0')
            r[7](style='opacity: 0')
            r[8](style='opacity: 0')
            return r
        totals = defaultdict(datetime.timedelta)
        total = datetime.timedelta()
        for s in lst:
            s = s.getEntry()
            totals[s.type.getTypeName()] += s.duration()
            total += s.duration()
        for typ in totals:
            ts = totals[typ].total_seconds()
            subtotal_row = IListRow(TimeEntry(employee=Employee(), type=EntryType(name='Subtotal: %s' % typ), period=TimePeriod(_startTime=IDateTime(0), _endTime=IDateTime(0).replace(seconds=ts))))
            out.append(subtotal_row)
            subtotal_row.prepare(self.l2)
            subtotal_row.old_render_listRow = subtotal_row.render_listRow
            subtotal_row.render_listRow = types.MethodType(render_listRow, subtotal_row)

        ts = total.total_seconds()
        total_row = IListRow(TimeEntry(employee=Employee(), type=EntryType(name='Total'), period=TimePeriod(_startTime=IDateTime(0), _endTime=IDateTime(0).replace(seconds=ts))))
        total_row.old_render_listRow = total_row.render_listRow
        total_row.render_listRow = types.MethodType(render_listRow, total_row)
        total_row.prepare(self.l2)
        TimeClock.total_row = total_row
        out.append(total_row)
        return out

    @coerce
    def getMappingFor(self, e: EmployeeRenderer):
        if self.employee.isAdministrator() or e.getEmployee() in ISupervisor(self.employee).getEmployees():
            self.selected = e.getEmployee()
        else:
            return []

        isAdm = self.employee.isAdministrator()

        store = self.employee.store

        q = AND(
            TimeEntry.employee==self.selected,
            TimeEntry.type==EntryType.storeID,
            EntryType.active==True,
            TimeEntry.period==TimePeriod.storeID,

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

        shifts = (i[0] for i in store.query((TimeEntry, TimePeriod, EntryType), q, sort=TimePeriod._startTime.asc))
        return IterateInReactor(self.prepareShifts(shifts))

    def prepareShifts(self, shifts):
        o = []
        for shift in shifts:
            # if not ((startTime and shift.endTime() < startTime) or (endTime and shift.startTime() > endTime)):
            s = IListRow(shift)
            s.prepare(self.l2)
            o.append(s)
            yield s
        yield from self.addTotals(o)
        yield SaveList(8).prepare(self.l2)

    @Transaction
    def setMappingFor(self, s: EmployeeRenderer, accounts: [EmployeeRenderer]):
        pass


registerAdapter(ApproveShifts, ApproveTime, IAthenaRenderable)

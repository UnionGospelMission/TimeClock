import time

import datetime
import types
from collections import defaultdict

import TimeClock
from TimeClock.Database.Employee import Employee
from TimeClock.Database.EntryType import EntryType
from TimeClock.Database.TimeEntry import TimeEntry
from TimeClock.Database.TimePeriod import TimePeriod
from TimeClock.Util.DateTime import DateTime
from twisted.python.components import registerAdapter
from zope.interface import implementer

from TimeClock.Database import Commands
from TimeClock.ITimeClock.IDatabase.IEntryType import IEntryType
from TimeClock.ITimeClock.IDatabase.ITimeEntry import ITimeEntry
from TimeClock.ITimeClock.IDateTime import IDateTime
from TimeClock.ITimeClock.IEvent.IEvent import IEvent
from TimeClock.ITimeClock.IEvent.IEventBus import IEventBus
from TimeClock.ITimeClock.IEvent.IEventHandler import IEventHandler
from TimeClock.ITimeClock.IEvent.IWebEvent.ITimeEntryChangedEvent import ITimeEntryChangedEvent
from TimeClock.ITimeClock.IWeb.IAthenaRenderable import IAthenaRenderable
from TimeClock.ITimeClock.IWeb.IListRow import IListRow
from TimeClock.Utils import overload
from TimeClock.Web.AthenaRenderers.Abstract.AbstractHideable import AbstractHideable
from TimeClock.Web.AthenaRenderers.Abstract.AbstractRenderer import AbstractRenderer, path
from TimeClock.Web.AthenaRenderers.Commands import AbstractCommandRenderer
from TimeClock.Web.AthenaRenderers.Widgets.List import List
from TimeClock.Web.Events.TimeEntryCreatedEvent import TimeEntryCreatedEvent
from nevow import tags
from nevow.athena import expose
from nevow.context import WovenContext
from nevow.loaders import xmlfile


@implementer(IAthenaRenderable, IEventHandler)
class ViewHours(AbstractCommandRenderer, AbstractHideable):
    docFactory = xmlfile(path + "/Pages/GenericCommand.xml", "GenericCommandPattern")
    jsClass = 'TimeClock.Commands.ViewShifts'
    subaccounts = None
    name = 'View Shifts'
    loaded = False
    startTime = DateTime.today().replace(day=1).replace(months=-1)
    endTime = None

    @expose
    def load(self):
        if not self.loaded:
            self.loaded = True
            startTime = self.startTime or IDateTime(0)
            endTime = self.endTime or None
            l = [IListRow(i).prepare(self.l) for i in self.getEntries() if not (i.endTime() < startTime or (endTime and i.startTime() > endTime))]
            for i in l:
                self.l.addRow(i)
            self.loaded = True
    l = None

    @overload
    def handleEvent(self, evt: TimeEntryCreatedEvent):
        if evt.timeEntry.employee is self.employee and evt.timeEntry.type == IEntryType("Work"):
            self.l.addRow(evt.timeEntry)

    @overload
    def handleEvent(self, event: IEvent):
        pass

    def render_genericCommand(self, ctx: WovenContext, data):
        IEventBus("Web").register(self, ITimeEntryChangedEvent)
        self.l = l = List([], ["Entry Type", "Work Location", "Sub Account", "Start Time", "End Time", "Duration", "Approved", "Denied"])
        l.closeable = False
        l.prepare(self)
        l.visible = True
        startTime = tags.input(id='startTime', placeholder='Start Time')
        #[
         #   tags.Tag('athena:handler')(event='onchange', handler='timeWindowChanged')]
        endTime = tags.input(id='endTime', placeholder='End Time')
        #[
         #   tags.Tag('athena:handler')(event='onchange', handler='timeWindowChanged')]
        self.preprocess([startTime, endTime])
        return [startTime, endTime, l]

    def getEntries(self):
        l = sorted(list(i for i in self.employee.powerupsFor(ITimeEntry)), key=(lambda p: p.period._startTime if p.period else TimeClock.Util.DateTime.DateTime.fromtimestamp(0)))
        self.addTotals(l)
        return l

    @expose
    def timeWindowChanged(self, startTime, endTime):
        if startTime:
            self.startTime = startTime = IDateTime(startTime)
        else:
            self.startTime = startTime = IDateTime(0)
        if endTime:
            self.endTime = endTime = IDateTime(endTime)
        else:
            self.endTime = None
        entries = [IListRow(i).prepare(self.l) for i in self.getEntries() if not (i.endTime() < startTime or (endTime is not None and i.startTime() > endTime))]
        self.l.list = entries
        return entries

    def addTotals(self, lst: [ITimeEntry]):
        def render_listRow(self, ctx: WovenContext, data=None):
            r = self.old_render_listRow(ctx, data)
            r[1](style='opacity: 0')
            r[2](style='opacity: 0')
            r[3](style='opacity: 0')
            r[4](style='opacity: 0')
            r[6](style='opacity: 0')
            r[7](style='opacity: 0')
            return r
        totals = defaultdict(datetime.timedelta)
        total = datetime.timedelta()
        for s in lst:
            if s.type:
                totals[s.type.getTypeName()] += s.duration()
            total += s.duration()
        for typ in totals:
            ts = totals[typ].total_seconds()
            subtotal_row = IListRow(TimeEntry(employee=Employee(), type=EntryType(name='Subtotal: %s' % typ), period=TimePeriod(_startTime=IDateTime(self.startTime or 0), _endTime=IDateTime(self.startTime or 0).replace(seconds=ts))))
            lst.append(subtotal_row)
            subtotal_row.prepare(self.l)
            subtotal_row.old_render_listRow = subtotal_row.render_listRow
            subtotal_row.render_listRow = types.MethodType(render_listRow, subtotal_row)
            subtotal_row.endTime = subtotal_row._timeEntry.endTime
            subtotal_row.startTime = subtotal_row._timeEntry.startTime

        ts = total.total_seconds()
        te = TimeEntry(employee=Employee(), type=EntryType(name='Total'), period=TimePeriod(_startTime=IDateTime(self.startTime or 0), _endTime=IDateTime(self.startTime or 0).replace(seconds=ts)))
        total_row = IListRow(te)
        total_row.old_render_listRow = total_row.render_listRow
        total_row.render_listRow = types.MethodType(render_listRow, total_row)
        total_row.prepare(self.l)
        total_row.endTime = total_row._timeEntry.endTime
        total_row.startTime = total_row._timeEntry.startTime
        TimeClock.total_row = total_row
        lst.append(total_row)





registerAdapter(ViewHours, Commands.ViewHours.ViewHours, IAthenaRenderable)

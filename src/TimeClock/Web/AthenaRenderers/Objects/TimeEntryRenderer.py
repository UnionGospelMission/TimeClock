import re
import time

import arrow
import dateutil.parser

from TimeClock import Exceptions
from TimeClock.Database.TimeEntry import TimeEntry
from TimeClock.Database.TimePeriod import TimePeriod
from TimeClock.ITimeClock.IDatabase.ICalendarData import ICalendarData
from TimeClock.Web.Utils import formatTimeDelta
from axiom.attributes import AND, OR
from twisted.python.components import registerAdapter
from zope.interface import implementer, directlyProvides

from TimeClock import Utils
from TimeClock.Axiom import Transaction
from TimeClock.Exceptions import DatabaseChangeCancelled
from TimeClock.ITimeClock.IDatabase.IEntryType import IEntryType
from TimeClock.ITimeClock.IDatabase.ISubAccount import ISubAccount
from TimeClock.ITimeClock.IDatabase.ISupervisor import ISupervisor
from TimeClock.ITimeClock.IDatabase.ITimeEntry import ITimeEntry
from TimeClock.ITimeClock.IDatabase.IWorkLocation import IWorkLocation
from TimeClock.ITimeClock.IEvent.IEvent import IEvent
from TimeClock.ITimeClock.IEvent.IEventBus import IEventBus
from TimeClock.ITimeClock.IEvent.IEventHandler import IEventHandler
from TimeClock.ITimeClock.IEvent.IWebEvent.ITimeEntryChangedEvent import ITimeEntryChangedEvent
from TimeClock.ITimeClock.IWeb.IAthenaRenderable import IAthenaRenderable
from TimeClock.ITimeClock.IWeb.IListRow import IListRow
from TimeClock.Utils import overload, coerce
from TimeClock.Web.AthenaRenderers.Abstract.AbstractExpandable import AbstractExpandable
from TimeClock.Web.AthenaRenderers.Abstract.AbstractHideable import AbstractHideable
from TimeClock.Web.AthenaRenderers.Abstract.AbstractRenderer import AbstractRenderer, path
from TimeClock.Web.Events.TimeEntryChangedEvent import TimeEntryChangedEvent

from nevow import inevow
from nevow.athena import expose
from nevow.context import WovenContext
from nevow.loaders import xmlfile
from nevow import tags as T


class _RenderListRowMixin(AbstractExpandable):
    length = 9
    _workLocation = None
    _showEmployee = False
    ctr = -1

    def render_searchclass(self, ctx, data):
        self.ctr += 1
        bc = 'timeEntry-%i' % self.ctr
        return bc

    def render_rowclass(self, ctx, data):
        if self._timeEntry.original:
            return 'te-modified'
        return ''

    def showEmployee(self):
        self._showEmployee = True

    def render_listRow(self, ctx: WovenContext, data=None):
        IEventBus("Web").register(self, ITimeEntryChangedEvent)
        listCell = inevow.IQ(ctx).patternGenerator("listCell")
        original = self._timeEntry.original
        self.expanded = False
        st = self._timeEntry.period.startTime()
        et = self._timeEntry.period.endTime(False)
        ctx.fillSlots('index', self._timeEntry.storeID)
        approved = T.input(id='approved', type='checkbox', checked=self._timeEntry.approved)[
            T.Tag('athena-handler')(event='onchange', handler='approvedClicked')
        ]
        te_type = T.input(id='entryType', type='text', disabled=True, value=self._timeEntry.type.name)
        if self._timeEntry.workLocation:
            WLs = self._timeEntry.getEmployee().getWorkLocations()
            missing = False
            if self._timeEntry.workLocation not in WLs:
                WLs.append(self._timeEntry.workLocation)
                missing = True
            workLocationID = T.select(id='workLocation', value=self._timeEntry.workLocation.workLocationID)[
                [T.option(value=i.workLocationID, selected=self._timeEntry.workLocation == i)[i.description] for i in
                 WLs]
            ]
            if missing:
                workLocationID(style='background-color:red')
        else:
            workLocationID = T.input(id='workLocation', disabled=True, value='None')
        if self._timeEntry.subAccount:
            SAs = list(self._timeEntry.getEmployee().getSubAccounts())
            missing = False
            if self._timeEntry.subAccount not in SAs:
                SAs.append(self._timeEntry.subAccount)
                missing = True
            subAccount = T.select(id='subAccount', value=self._timeEntry.subAccount.sub)[
                [T.option(value=i.sub, selected=self._timeEntry.subAccount==i)[i.name] for i in SAs]
            ]
            if missing:
                subAccount(style='background-color:red')
        else:
            subAccount = T.input(id='subAccount', disabled=True, value="None")
        duration = T.input(id='duration', value=formatTimeDelta(self._timeEntry.period.duration()))
        if self._timeEntry.type == IEntryType("Work"):
            ET = T.input(id='endTime', value=et.strftime('%Y-%m-%d %H:%M:%S %Z') if et else 'None')
            et = listCell(data=dict(listItem=ET))
            reject = T.input(id='denied', type='checkbox', checked=self._timeEntry.denied)[
                T.Tag('athena-handler')(event='onchange', handler='deniedClicked')
            ]

            rj = listCell(data=dict(listItem=reject))
            duration(disabled=True)
        else:
            ET = T.input(style='display:none', id='entryType', value=self._timeEntry.type.getTypeName())
            et = listCell(data=dict(listItem=ET))
            reject = T.input(id='denied', type='checkbox', checked=self._timeEntry.denied)
            rj = listCell(data=dict(listItem=reject))

        startTime = T.input(id='startTime', value=st.strftime('%Y-%m-%d %H:%M:%S %Z') if st else 'None')
        if self._timeEntry.employee.timeEntry is self._timeEntry:
            ET(disabled=True)
        if not self.employee.isAdministrator() or self.parent.selectable or self.employee is self._timeEntry.employee:

            workLocationID(disabled=True)
            subAccount(disabled=True)
            startTime(disabled=True)
            ET(disabled=True)
            duration(disabled=True)
            if self._timeEntry.denied or \
                    self._timeEntry.approved or \
                    not self.employee.isSupervisor() or \
                    self._timeEntry.employee not in ISupervisor(self.employee).getEmployees() or \
                    self._timeEntry.subAccount not in ISupervisor(self.employee).getSubAccounts() or \
                    self.parent.selectable or \
                    self.employee is self._timeEntry.employee:
                reject(disabled=True)
                approved(disabled=True)
        startday = self._timeEntry.startTime().date()
        endday = startday.replace(hours=23, minutes=59, seconds=59)

        store = self._timeEntry.store
        q = AND(
            TimeEntry.period==TimePeriod.storeID,
            TimeEntry.employee==self._timeEntry.employee,
            TimeEntry.denied==False,
            TimePeriod._startTime <= endday,
            OR(TimePeriod._endTime >= startday,
               TimePeriod._endTime==None
            )
        )
        if store:
            entries = ICalendarData([i[0] for i in store.query((TimeEntry, TimePeriod), q)]).between(startday, endday)
        else:
            entries = ICalendarData([])

        lastEntryOfDay = entries.entries and entries.entries[-1].startTime() == self._timeEntry.startTime()
        if lastEntryOfDay:
            total = T.input(id='total', value=formatTimeDelta(entries.sumBetween(startday, endday)))
            total(disabled=True)
            total = listCell(data=dict(listItem=total))
        else:
            total = listCell(data=dict(listItem=""))(style='opacity: 0')
        self.preprocess([approved, workLocationID, subAccount, startTime, ET, duration, reject, total])
        r = [listCell(data=dict(listItem=te_type)),
             listCell(data=dict(listItem=workLocationID if not self._showEmployee else T.input(disabled=True, value=self._timeEntry.employee.name))),
             listCell(data=dict(listItem=subAccount)),
             listCell(data=dict(listItem=startTime)),
             et,
             listCell(data=dict(listItem=duration)),
             total,
             listCell(data=dict(listItem=approved)),
             rj]
        if original and original.period:
            workLocationID(title=original.workLocation.description)
            subAccount(title=original.subAccount.name)
            startTime(title=original.startTime().strftime('%Y-%m-%d %H:%M:%S %Z'))
            ET(title=original.endTime(False).strftime('%Y-%m-%d %H:%M:%S %Z') if original.endTime(False) else 'None')
        return r

    def __conform__(self, iface):
        if iface == IListRow:
            self.docFactory = self.listDocFactory
            directlyProvides(self, IListRow)
            self.visible = True
            return self

    @staticmethod
    def listRow(e):
        return IListRow(TimeEntryRenderer(e))


@implementer(IEventHandler)
class TimeEntryRenderer(AbstractRenderer, AbstractHideable, _RenderListRowMixin):
    docFactory = xmlfile(path + '/Pages/TimeEntry.xml', 'TimeEntryPattern')
    listDocFactory = xmlfile(path + '/Pages/List.xml', 'liveListRow', ignoreDocType=True)
    tableDocFactory = xmlfile(path + '/Pages/TimeEntry.xml', 'TimeEntryTablePattern')
    jsClass = 'TimeClock.Objects.TimeEntryRenderer'
    cssModule = "jquery.ui.datetimepicker"
    commands = None
    visible = True

    def getEntry(self):
        return self._timeEntry

    def powerUp(self, obj, iface):
        self.powerups[iface] = self.powerups.get(iface, [])
        self.powerups[iface].append(obj)

    @overload
    def handleEvent(self, event: ITimeEntryChangedEvent):
        if event.timeEntry is self._timeEntry:
            d = self._timeEntry.persistentValues()
            d['startTime'] = self._timeEntry.startTime().strftime('%Y-%m-%d %H:%M:%S %Z') if self._timeEntry.startTime() else 'None'
            d['endTime'] = self._timeEntry.endTime(False).strftime('%Y-%m-%d %H:%M:%S %Z') if self._timeEntry.endTime(False) else 'None'
            d['duration'] = formatTimeDelta(self._timeEntry.period.duration())
            if d['workLocation']:
                d['workLocation'] = d['workLocation'].workLocationID
            if d['subAccount']:
                d['subAccount'] = d['subAccount'].sub
            d['entryType'] = self._timeEntry.type.name
            changed = event.previous_values
            keys = list(changed.keys())
            keys.append('duration')
            self.callRemote("newValues", {k: d[k] for k in keys})

    @overload
    def handleEvent(self, event: IEvent):
        pass

    @coerce
    def __init__(self, sa: ITimeEntry):
        super().__init__()
        self._timeEntry = sa
        self.powerups = {}

    @property
    def name(self):
        return "Time Entry"

    def render_timeEntryTable(self, ctx, data):
        r = self.tableDocFactory.load(ctx, self.preprocessors)
        return r

    def data_timeEntryData(self, ctx, data):
        return self._timeEntry.persistentValues()

    def render_timeEntryDetails(self, ctx, data):
        IEventBus("Web").register(self, ITimeEntryChangedEvent)
        st = self._timeEntry.period.startTime()
        et = self._timeEntry.period.endTime(False)
        row = inevow.IQ(ctx).patternGenerator('timeEntryDataPattern')
        o = []
        approved = T.input(id='approved', type='checkbox', checked=self._timeEntry.approved)
        workLocationID = T.input(id='workLocation', value=self._timeEntry.workLocation.workLocationID)
        subAccount = T.input(id='subAccount', value=self._timeEntry.subAccount.sub)
        startTime = T.input(id='startTime', type='text', value=st.strftime('%Y-%m-%d %H:%M:%S %Z') if st else 'None')
        endTime = T.input(id='endTime', type='text', value=et.strftime('%Y-%m-%d %H:%M:%S %Z') if et else 'None')
        duration = T.input(id='duration', value=formatTimeDelta(self._timeEntry.period.duration()), disabled=True)
        save = T.input(type='button', value='Save Changes')[
            T.Tag("athena:handler")(event='onclick', handler='saveClicked')]

        if not self.employee.isAdministrator() or self.employee is self._timeEntry.employee:
            approved(disabled=True)
            workLocationID(disabled=True)
            subAccount(disabled=True)
            startTime(disabled=True)
            endTime(disabled=True)
            duration(disabled=True)
            if not self.employee.isSupervisor() or self._timeEntry.employee not in ISupervisor(self.employee).getEmployees():
                save = ''

        o.append(row(data=dict(rowName="Work Location", rowValue=workLocationID)))
        o.append(row(data=dict(rowName="Sub Account", rowValue=subAccount)))
        o.append(row(data=dict(rowName="Start Time", rowValue=startTime)))
        o.append(row(data=dict(rowName="End Time", rowValue=endTime)))
        o.append(row(data=dict(rowName="Duration", rowValue=duration)))
        o.append(row(data=dict(rowName="Approved", rowValue=approved)))

        if save:
            o.append(row(data=dict(rowName="Save Changes", rowValue=save)))
        self.preprocess([approved, workLocationID, subAccount, startTime, endTime, duration])
        return o

    def doCompare(self, keys, vals):
        approved = vals.get('approved', self._timeEntry.approved)
        denied = vals.get('denied', self._timeEntry.denied)
        if approved and denied:
            raise Exceptions.DatabasException("Time entry cannot be both approved and denied")
        oldVals = {}
        for key in keys:
            if key not in vals:
                continue
            oldv = getattr(self._timeEntry, key)
            if key == 'duration':
                key = 'endTime'
                vals[key] = self._timeEntry.startTime()
                hour, minute, second = vals['duration'].split(':')
                vals[key] = vals[key].replace(hours=int(hour), minutes=int(minute), seconds=int(second))
                val = self._timeEntry.endTime(False)
                if val.replace(microsecond=0) != vals[key].replace(microsecond=0):
                    oldVals[key] = val
                    self._timeEntry.period.end(vals[key])
                continue
            elif key == 'workLocation':
                if vals[key] and vals[key] != 'None':
                    val = IWorkLocation(vals[key])
                else:
                    val = None
            elif key == 'subAccount':
                if vals[key] and vals[key] != 'None':
                    val = ISubAccount(int(vals[key]))
                else:
                    val = None
            elif key == 'startTime':
                oldv = self._timeEntry.period.startTime()
                val = (Utils.getIDateTime(vals[key]))
                if oldv.replace(microsecond=0) != val.replace(microsecond=0):
                    self._timeEntry.period.start(val)
                    oldVals[key] = oldv
                continue
            elif key == 'endTime':
                oldv = self._timeEntry.period.endTime(False)
                val = (Utils.getIDateTime(vals[key]))
                if oldv.replace(microsecond=0) != val.replace(microsecond=0):
                    self._timeEntry.period.end(val)
                    oldVals[key] = oldv
                continue
            elif key == 'approved' or key == 'denied':
                val = vals[key]
            if getattr(self._timeEntry, key) != val:
                oldVals[key] = getattr(self._timeEntry, key)
                setattr(self._timeEntry, key, val)
        return oldVals

    @expose
    @Transaction
    def saveClicked(self, args):
        if not self._timeEntry.store:
            return
        if self.employee is self._timeEntry.getEmployee():
            return
        oldVals = {}
        keys = []
        sup = ISupervisor(self.employee, None)
        original = self._timeEntry.original or self._timeEntry.copy()
        if self.employee.isAdministrator() and self.employee is not self._timeEntry.employee:
            keys = ['workLocation', 'subAccount', 'startTime', 'endTime', 'approved', 'denied']
            if self._timeEntry.type != IEntryType("Work"):
                keys[3] = 'duration'
        elif sup and self._timeEntry.employee in sup.getEmployees() and not self._timeEntry.approved:
            keys = ['approved', 'denied']
        if not self._timeEntry.endTime(False):
            if 'approved' in keys:
                keys.remove('approved')
            if 'endTime' in keys:
                keys.remove('endTime')
            if 'denied' in keys:
                keys.remove('denied')
        oldVals.update(self.doCompare(keys, args))
        if oldVals:
            ov = oldVals.copy()
            ov.pop('approved', None)
            ov.pop('denied', None)
            if ov:
                if not original.store:
                    original.period.store = self._timeEntry.store
                    original.store = self._timeEntry.store
                    self._timeEntry.original = original

            e = TimeEntryChangedEvent(self._timeEntry, oldVals)
            IEventBus("Web").postEvent(e)
            if e.cancelled:
                raise DatabaseChangeCancelled(e.retval)

registerAdapter(TimeEntryRenderer.listRow, ITimeEntry, IListRow)
registerAdapter(TimeEntryRenderer, ITimeEntry, IAthenaRenderable)

import re
import time

import arrow
import dateutil.parser
from twisted.python.components import registerAdapter
from zope.interface import implementer, directlyProvides

from TimeClock.Axiom import Transaction
from TimeClock.Exceptions import DatabaseChangeCancelled
from TimeClock.ITimeClock.IDatabase.ISubAccount import ISubAccount
from TimeClock.ITimeClock.IDatabase.ISupervisor import ISupervisor
from TimeClock.ITimeClock.IDatabase.ITimeEntry import ITimeEntry
from TimeClock.ITimeClock.IDatabase.IWorkLocation import IWorkLocation
from TimeClock.ITimeClock.IDateTime import IDateTime
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


tzpattern = re.compile('([A-Z0-9a-z]{3})$')


class _RenderListRowMixin(AbstractExpandable):
    length = 6
    _workLocation = None
    ctr = -1
    def render_searchclass(self, ctx, data):
        self.ctr += 1
        return 'timeEntry-%i' % self.ctr
    def render_listRow(self, ctx: WovenContext, data=None):
        IEventBus("Web").register(self, ITimeEntryChangedEvent)
        listCell = inevow.IQ(ctx).patternGenerator("listCell")
        self.expanded = False
        st = self._timeEntry.period.startTime()
        et = self._timeEntry.period.endTime(False)
        ctx.fillSlots('index', self._timeEntry.storeID)
        approved = T.input(id='approved', type='checkbox', checked=self._timeEntry.approved)
        workLocationID = T.input(id='workLocation', value=self._timeEntry.workLocation.workLocationID)
        subAccount = T.input(id='subAccount', value=self._timeEntry.subAccount.sub)
        startTime = T.input(id='startTime', value=st.strftime('%Y-%m-%d %H:%M:%S %Z') if st else 'None')
        endTime = T.input(id='endTime', value=et.strftime('%Y-%m-%d %H:%M:%S %Z') if et else 'None')
        duration = T.input(id='duration', value=str(self._timeEntry.period.duration()))

        if not self.employee.isAdministrator() or self.parent.selectable:
            approved(disabled=True)
            workLocationID(disabled=True)
            subAccount(disabled=True)
            startTime(disabled=True)
            endTime(disabled=True)
            duration(disabled=True)

        self.preprocess([approved, workLocationID, subAccount, startTime, endTime, duration])
        r = [listCell(data=dict(listItem=workLocationID)),
             listCell(data=dict(listItem=subAccount)),
             listCell(data=dict(listItem=startTime)),
             listCell(data=dict(listItem=endTime)),
             listCell(data=dict(listItem=duration)),
             listCell(data=dict(listItem=approved))]
        return r
    def __conform__(self, iface):
        if iface == IListRow:
            self.docFactory = self.listDocFactory
            directlyProvides(self, IListRow)
            return self
    @staticmethod
    def listRow(e):
        return IListRow(TimeEntryRenderer(e))


@implementer(IEventHandler)
class TimeEntryRenderer(AbstractRenderer, AbstractHideable, _RenderListRowMixin):
    docFactory = xmlfile(path + '/Pages/TimeEntry.xml', 'TimeEntryPattern')
    listDocFactory = xmlfile(path + '/Pages/List.xml', 'liveListRow', ignoreDocType=True)
    tableDocFactory = xmlfile(path + '/Pages/TimeEntry.xml', 'TimeEntryTablePattern')
    jsClass = 'TimeClock.Objects.TimeEntryRenderer';
    cssModule = "jquery.ui.datetimepicker"
    commands = None
    visible = True
    def getWLoc(self):
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
            d['duration'] = str(self._timeEntry.period.duration())
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
        duration = T.input(id='duration', value=str(self._timeEntry.period.duration()), disabled=True)
        save = T.input(type='button', value='Save Changes')[
            T.Tag("athena:handler")(event='onclick', handler='saveClicked')]

        if not self.employee.isAdministrator():
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
        oldVals = {}
        default_tzoffset = (arrow.get(time.localtime()) - arrow.get(time.gmtime())).total_seconds() / 60
        if default_tzoffset > 0:
            default_tzoffsetstr = '%02i:%02i' % (int(default_tzoffset / 60), int(default_tzoffset) % 60)
        else:
            default_tzoffsetstr = '%03i:%02i' % (int(default_tzoffset / 60), int(default_tzoffset) % 60)
        for key in keys:
            if key not in vals:
                continue
            oldv = getattr(self._timeEntry, key)
            if key == 'workLocation':
                val = IWorkLocation(vals[key])
            elif key == 'subAccount':
                val = ISubAccount(int(vals[key]))
            elif key == 'startTime':
                oldv = self._timeEntry.period.startTime()
                tz = tzpattern.search(vals[key])
                if tz:
                    tz = tz.group(0)
                    tzoffset = dateutil.parser.parse('1970-01-01 00:00:00 %s' % tz).utcoffset().total_seconds() / 60
                    if tzoffset > 0:
                        tzoffsetstr = '%02i:%02i' % (int(tzoffset / 60), int(tzoffset) % 60)
                    else:
                        tzoffsetstr = '%03i:%02i' % (int(tzoffset / 60), int(tzoffset) % 60)
                    val = IDateTime(vals[key].replace(tz, '').strip() + tzoffsetstr)
                else:
                    val = IDateTime(vals[key].strip() + default_tzoffsetstr)

                if oldv.strftime('%Y-%m-%d %H:%M:%S %Z') != val.strftime('%Y-%m-%d %H:%M:%S %Z'):
                    self._timeEntry.period.start(val)
                    oldVals[key] = oldv
                continue
            elif key == 'endTime':
                oldv = self._timeEntry.period.endTime(False)

                tz = tzpattern.search(vals[key])
                if tz:
                    tz = tz.group(0)
                    tzoffset = dateutil.parser.parse('1970-01-01 00:00:00 %s' % tz).utcoffset().total_seconds() / 60
                    if tzoffset > 0:
                        tzoffsetstr = '%02i:%02i' % (int(tzoffset / 60), int(tzoffset) % 60)
                    else:
                        tzoffsetstr = '%03i:%02i' % (int(tzoffset / 60), int(tzoffset) % 60)
                    val = IDateTime(vals[key].replace(tz, '').strip() + tzoffsetstr)
                else:
                    val = IDateTime(vals[key].strip() + default_tzoffsetstr)
                if oldv.strftime('%Y-%m-%d %H:%M:%S %Z') != val.strftime('%Y-%m-%d %H:%M:%S %Z'):
                    self._timeEntry.period.end(val)
                    oldVals[key] = oldv
                continue
            elif key == 'approved':
                val = vals[key]
            if getattr(self._timeEntry, key) != val:
                oldVals[key] = getattr(self._timeEntry, key)
                setattr(self._timeEntry, key, val)
        return oldVals

    @expose
    @Transaction
    def saveClicked(self, args):
        oldVals = {}
        keys = []
        sup = ISupervisor(self.employee, None)
        if self.employee.isAdministrator():
            keys = ['workLocation', 'subAccount', 'startTime', 'endTime', 'approved']
        elif sup and self._timeEntry.employee in sup.getEmployees():
            keys = ['approved']
        if not self._timeEntry.endTime(False):
            if 'approved' in keys:
                keys.remove('approved')
            if 'endTime' in keys:
                keys.remove('endTime')
        oldVals.update(self.doCompare(keys, args))
        if oldVals:
            e = TimeEntryChangedEvent(self._timeEntry, oldVals)
            IEventBus("Web").postEvent(e)
            if e.cancelled:
                raise DatabaseChangeCancelled(e.retval)

registerAdapter(TimeEntryRenderer.listRow, ITimeEntry, IListRow)
registerAdapter(TimeEntryRenderer, ITimeEntry, IAthenaRenderable)

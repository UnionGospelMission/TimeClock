from twisted.python.components import registerAdapter
from zope.interface import implementer, directlyProvides

from TimeClock.Axiom import Transaction
from TimeClock.Exceptions import DatabaseChangeCancelled
from TimeClock.ITimeClock.IDatabase.ISubAccount import ISubAccount
from TimeClock.ITimeClock.IDatabase.IWorkLocation import IWorkLocation
from TimeClock.ITimeClock.IEvent.IEvent import IEvent
from TimeClock.ITimeClock.IEvent.IEventBus import IEventBus
from TimeClock.ITimeClock.IEvent.IEventHandler import IEventHandler
from TimeClock.ITimeClock.IEvent.IWebEvent.ISubAccountChangedEvent import ISubAccountChangedEvent
from TimeClock.ITimeClock.IEvent.IWebEvent.IWorkLocationChangedEvent import IWorkLocationChangedEvent
from TimeClock.ITimeClock.IWeb.IAthenaRenderable import IAthenaRenderable
from TimeClock.ITimeClock.IWeb.IListRow import IListRow
from TimeClock.Utils import overload, coerce
from TimeClock.Web.AthenaRenderers.Abstract.AbstractExpandable import AbstractExpandable
from TimeClock.Web.AthenaRenderers.Abstract.AbstractHideable import AbstractHideable
from TimeClock.Web.AthenaRenderers.Abstract.AbstractRenderer import AbstractRenderer, path
from TimeClock.Web.Events.SubAccountChangedEvent import SubAccountChangedEvent
from TimeClock.Web.Events.WorkLocationChangedEvent import WorkLocationChangedEvent

from nevow import inevow
from nevow.athena import expose
from nevow.context import WovenContext
from nevow.loaders import xmlfile
from nevow import tags as T




class _RenderListRowMixin(AbstractExpandable):
    length = 3
    _workLocation = None
    ctr = -1
    def render_searchclass(self, ctx, data):
        self.ctr += 1
        return 'workLocation-%i' % self.ctr
    def render_listRow(self, ctx: WovenContext, data=None):
        IEventBus("Web").register(self, IWorkLocationChangedEvent)
        listCell = inevow.IQ(ctx).patternGenerator("listCell")
        self.expanded = False
        ctx.fillSlots('index', self._workLocation.workLocationID)
        active = T.input(id='active', type='checkbox', checked=self._workLocation.active)
        workLocationID = T.input(id='name', value=self._workLocation.workLocationID, disabled=True)
        descr = T.input(id='description', value=self._workLocation.description)

        if not self.employee.isAdministrator() or self.parent.selectable:
            active(disabled=True)
            workLocationID(disabled=True)
            descr(disabled=True)

        self.preprocess([active, workLocationID, descr])
        r = [listCell(data=dict(listItem=descr)),
             listCell(data=dict(listItem=workLocationID)),
             listCell(data=dict(listItem=active))]
        return r
    def __conform__(self, iface):
        if iface == IListRow:
            self.docFactory = self.listDocFactory
            directlyProvides(self, IListRow)
            return self
    @staticmethod
    def listRow(e):
        return IListRow(WorkLocationRenderer(e))


@implementer(IEventHandler)
class WorkLocationRenderer(AbstractRenderer, AbstractHideable, _RenderListRowMixin):
    docFactory = xmlfile(path + '/Pages/WorkLocation.xml', 'WorkLocationPattern')
    listDocFactory = xmlfile(path + '/Pages/List.xml', 'liveListRow')
    tableDocFactory = xmlfile(path + '/Pages/WorkLocation.xml', 'WorkLocationTablePattern')
    jsClass = 'TimeClock.Objects.WorkLocationRenderer';

    commands = None
    visible = True
    def getWLoc(self):
        return self._workLocation

    def powerUp(self, obj, iface):
        self.powerups[iface] = self.powerups.get(iface, [])
        self.powerups[iface].append(obj)
    @overload
    def handleEvent(self, event: IWorkLocationChangedEvent):
        if event.workLocation is self._workLocation:
            d = self._workLocation.persistentValues()
            changed = event.previous_values
            self.callRemote("newValues", {k: d[k] for k in changed.keys()})
    @overload
    def handleEvent(self, event: IEvent):
        pass

    @coerce
    def __init__(self, sa: IWorkLocation):
        super().__init__()
        self._workLocation = sa
        self.powerups = {}

    @property
    def name(self):
        return self._workLocation.name

    def render_workLocationTable(self, ctx, data):
        r = self.tableDocFactory.load(ctx, self.preprocessors)
        return r

    def data_workLocationData(self, ctx, data):
        return self._workLocation.persistentValues()

    def render_workLocationDetails(self, ctx, data):
        IEventBus("Web").register(self, IWorkLocationChangedEvent)
        row = inevow.IQ(ctx).patternGenerator('workLocationDataPattern')
        o = []
        active = T.input(id='active', type='checkbox', checked=self._workLocation.active)
        workLocationID = T.input(id='name', value=self._workLocation.workLocationID, disabled=True)
        descr = T.input(id='description', value=self._workLocation.description)
        save = T.input(type='button', value='Save Changes')[T.Tag("athena:handler")(event='onclick', handler='saveClicked')]

        o.append(row(data=dict(rowName="Work Location", rowValue=workLocationID)))
        o.append(row(data=dict(rowName="Description", rowValue=descr)))
        o.append(row(data=dict(rowName="Active", rowValue=active)))

        if not self.employee.isAdministrator():
            active(disabled=True)
            workLocationID(disabled=True)
            descr(disabled=True)
            save = ''
        else:
            o.append(row(data=dict(rowName="Save Changes", rowValue=save)))
        self.preprocess([active, workLocationID, descr, save])
        return o

    def doCompare(self, keys, vals):
        oldVals = {}
        for key in keys:
            if key not in vals:
                continue
            oldv = getattr(self._workLocation, key)
            if oldv is not None:
                typ = type(oldv)
                if typ is not type(vals[key]):
                    vals[key] = typ(vals[key])
            else:
                if vals[key].isdigit():
                    vals[key] = int(vals[key])
            if getattr(self._workLocation, key) != vals[key]:
                oldVals[key] = getattr(self._workLocation, key)
                setattr(self._workLocation, key, vals[key])
        return oldVals

    @expose
    @Transaction
    def saveClicked(self, args):
        oldVals = {}
        keys = []
        if self.employee.isAdministrator():
            keys = ['description', 'active']
        oldVals.update(self.doCompare(keys, args))
        if oldVals:
            e = WorkLocationChangedEvent(self._workLocation, oldVals)
            IEventBus("Web").postEvent(e)
            if e.cancelled:
                raise DatabaseChangeCancelled(e.retval)


registerAdapter(WorkLocationRenderer.listRow, IWorkLocation, IListRow)
registerAdapter(WorkLocationRenderer, IWorkLocation, IAthenaRenderable)

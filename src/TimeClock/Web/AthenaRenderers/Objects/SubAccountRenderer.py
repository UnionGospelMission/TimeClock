from twisted.python.components import registerAdapter
from zope.interface import implementer, directlyProvides

from TimeClock.Axiom import Transaction
from TimeClock.Exceptions import DatabaseChangeCancelled
from TimeClock.ITimeClock.IDatabase.ISubAccount import ISubAccount
from TimeClock.ITimeClock.IEvent.IEvent import IEvent
from TimeClock.ITimeClock.IEvent.IEventBus import IEventBus
from TimeClock.ITimeClock.IEvent.IEventHandler import IEventHandler
from TimeClock.ITimeClock.IEvent.IWebEvent.ISubAccountChangedEvent import ISubAccountChangedEvent
from TimeClock.ITimeClock.IWeb.IAthenaRenderable import IAthenaRenderable
from TimeClock.ITimeClock.IWeb.IListRow import IListRow
from TimeClock.Utils import overload, coerce
from TimeClock.Web.AthenaRenderers.Abstract.AbstractExpandable import AbstractExpandable
from TimeClock.Web.AthenaRenderers.Abstract.AbstractHideable import AbstractHideable
from TimeClock.Web.AthenaRenderers.Abstract.AbstractRenderer import AbstractRenderer, path
from TimeClock.Web.Events.SubAccountChangedEvent import SubAccountChangedEvent

from nevow import inevow
from nevow.athena import expose
from nevow.context import WovenContext
from nevow.loaders import xmlfile
from nevow import tags as T


instances = []


class _RenderListRowMixin(AbstractExpandable):
    length = 3
    _subAccount = None
    ctr = -1
    def render_searchclass(self, ctx, data):
        self.ctr += 1
        return 'subAccount-%i' % self.ctr
    def render_listRow(self, ctx: WovenContext, data=None):
        IEventBus("Web").register(self, ISubAccountChangedEvent)
        listCell = inevow.IQ(ctx).patternGenerator("listCell")
        self.expanded = False
        self.length = 2
        ctx.fillSlots('index', self._subAccount.sub)
        active = T.input(id='active', type='checkbox', checked=self._subAccount.active)
        name = T.input(id='name', value=self.name)
        sub = T.input(id='sub', value=self._subAccount.sub, disabled=True)

        if not self.employee.isAdministrator() or self.parent.selectable:
            active(disabled=True)
            name(disabled=True)
            sub(disabled=True)

        self.preprocess([active, name, sub])
        r = [listCell(data=dict(listItem=sub)),
             listCell(data=dict(listItem=name)),
             listCell(data=dict(listItem=active))]
        return r
    def __conform__(self, iface):
        if iface == IListRow:
            self.docFactory = self.listDocFactory
            directlyProvides(self, IListRow)
            return self
    @staticmethod
    def listRow(e):
        return IListRow(SubAccountRenderer(e))


@implementer(IEventHandler)
class SubAccountRenderer(AbstractRenderer, AbstractHideable, _RenderListRowMixin):
    docFactory = xmlfile(path + '/Pages/SubAccount.xml', 'SubAccountPattern')
    listDocFactory = xmlfile(path + '/Pages/List.xml', 'liveListRow')
    tableDocFactory = xmlfile(path + '/Pages/SubAccount.xml', 'SubAccountTablePattern')
    jsClass = 'TimeClock.Objects.SubAccountRenderer';

    commands = None
    visible = True
    def getSub(self):
        return self._subAccount

    def powerUp(self, obj, iface):
        self.powerups[iface] = self.powerups.get(iface, [])
        self.powerups[iface].append(obj)
    @overload
    def handleEvent(self, event: ISubAccountChangedEvent):
        if event.subAccount is self._subAccount:
            d = self._subAccount.persistentValues()
            changed = event.previous_values
            self.callRemote("newValues", {k: d[k] for k in changed.keys()})
    @overload
    def handleEvent(self, event: IEvent):
        pass

    @coerce
    def __init__(self, sa: ISubAccount):
        super().__init__()
        instances.append(self)
        self._subAccount = sa
        self.powerups = {}

    @property
    def name(self):
        return self._subAccount.name

    def render_subAccountTable(self, ctx, data):
        r = self.tableDocFactory.load(ctx, self.preprocessors)
        return r

    def data_subAccountData(self, ctx, data):
        return self._subAccount.persistentValues()

    def render_subAccountDetails(self, ctx, data):
        IEventBus("Web").register(self, ISubAccountChangedEvent)
        row = inevow.IQ(ctx).patternGenerator('subAccountDataPattern')
        o = []
        active = T.input(id='active', type='checkbox', checked=self._subAccount.active)
        name = T.input(id='name', value=self.name)
        sub = T.input(id='sub', value=self._subAccount.sub, disabled=True)
        save = T.input(type='button', value='Save Changes')[T.Tag("athena:handler")(event='onclick', handler='saveClicked')]

        o.append(row(data=dict(rowName="Sub Account", rowValue=sub)))
        o.append(row(data=dict(rowName="Name", rowValue=name)))
        o.append(row(data=dict(rowName="Active", rowValue=active)))

        if not self.employee.isAdministrator():
            active(disabled=True)
            name(disabled=True)
            sub(disabled=True)
            save = ''
        else:
            o.append(row(data=dict(rowName="Save Changes", rowValue=save)))
        self.preprocess([active, name, sub, save])
        return o

    def doCompare(self, keys, vals):
        oldVals = {}
        for key in keys:
            if key not in vals:
                continue
            oldv = getattr(self._subAccount, key)
            if oldv is not None:
                typ = type(oldv)
                if typ is not type(vals[key]):
                    vals[key] = typ(vals[key])
            else:
                if vals[key].isdigit():
                    vals[key] = int(vals[key])
            if getattr(self._subAccount, key) != vals[key]:
                oldVals[key] = getattr(self._subAccount, key)
                setattr(self._subAccount, key, vals[key])
        return oldVals

    @expose
    @Transaction
    def saveClicked(self, args):
        oldVals = {}
        keys = []
        if self.employee.isAdministrator():
            keys = ['name', 'active']
        oldVals.update(self.doCompare(keys, args))
        if oldVals:
            e = SubAccountChangedEvent(self._subAccount, oldVals)
            IEventBus("Web").postEvent(e)
            if e.cancelled:
                raise DatabaseChangeCancelled(e.retval)


registerAdapter(SubAccountRenderer.listRow, ISubAccount, IListRow)
registerAdapter(SubAccountRenderer, ISubAccount, IAthenaRenderable)

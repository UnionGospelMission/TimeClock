from twisted.python.components import registerAdapter
from zope.interface import implementer, directlyProvides

from TimeClock.Axiom import Transaction
from TimeClock.Axiom.Store import Store
from TimeClock.Exceptions import DatabaseChangeCancelled
from TimeClock.ITimeClock.IDatabase.IAdministrator import IAdministrator
from TimeClock.ITimeClock.IDatabase.IEmployee import IEmployee
from TimeClock.ITimeClock.IDatabase.IPerson import IPerson
from TimeClock.ITimeClock.IDatabase.ISupervisor import ISupervisor
from TimeClock.ITimeClock.IEvent.IEvent import IEvent
from TimeClock.ITimeClock.IEvent.IEventBus import IEventBus
from TimeClock.ITimeClock.IEvent.IEventHandler import IEventHandler
from TimeClock.ITimeClock.IEvent.IWebEvent.IEmployeeChangedEvent import IEmployeeChangedEvent
from TimeClock.ITimeClock.ISolomonEmployee import ISolomonEmployee
from TimeClock.ITimeClock.IWeb.IAthenaRenderable import IAthenaRenderable
from TimeClock.ITimeClock.IWeb.IListRow import IListRow
from TimeClock.Util import NULL
from TimeClock.Utils import overload
from TimeClock.Web.AthenaRenderers.Abstract.AbstractExpandable import AbstractExpandable
from TimeClock.Web.AthenaRenderers.Abstract.AbstractHideable import AbstractHideable
from TimeClock.Web.AthenaRenderers.Abstract.AbstractRenderer import AbstractRenderer, path
from TimeClock.Web.Events.EmployeeChangedEvent import EmployeeChangedEvent
from TimeClock.Web.Events.SupervisorCreatedEvent import SupervisorCreatedEvent
from TimeClock.Web.Events.SupervisorRemovedEvent import SupervisorRemovedEvent
from TimeClock.Web.LiveFragment import LiveFragment

from TimeClock.Web.Utils import employee_attributes
from nevow import inevow
from nevow.athena import expose
from nevow.context import WovenContext
from nevow.loaders import xmlfile
from nevow import tags as T
from nevow.stan import Tag


instances = []


class _RenderListRowMixin(AbstractExpandable):
    length = 2
    ctr = -1
    def render_searchclass(self, ctx, data):
        self.ctr += 1
        return 'employee-%i' % self.ctr
    def render_listRow(self, ctx: WovenContext, data=None):
        listCell = inevow.IQ(ctx).patternGenerator("listCell")
        self.expanded = False
        ctx.fillSlots('index', self._employee.employee_id)
        if self.length == 3:
            r = [
                listCell(data=dict(listItem='►'))(id='expand-button')[
                    T.Tag("athena:handler")(event='onclick', handler='expand')],
                listCell(data=dict(listItem='▼'))(style='display:none', id='unexpand-button')[
                    T.Tag("athena:handler")(event='onclick', handler='expand')],
            ]
        else:
            r = []

        r.extend([listCell(data=dict(listItem=self._employee.employee_id))[Tag('athena:handler')(event='ondblclick', handler='expand')],
                  listCell(data=dict(listItem=self.name))[Tag('athena:handler')(event='ondblclick', handler='expand')],
                ])
        if not self.parent.selectable:
            r.append(T.td(style='display:none', id='expanded')[self.tableDocFactory.load(ctx, self.preprocessors)])
        return r
    def __conform__(self, iface):
        if iface == IListRow:
            self.docFactory = self.listDocFactory
            directlyProvides(self, IListRow)
            return self
    @staticmethod
    def listRow(e):
        return IListRow(EmployeeRenderer(e))


@implementer(IEventHandler)
class EmployeeRenderer(AbstractRenderer, AbstractHideable, _RenderListRowMixin):
    docFactory = xmlfile(path + '/Pages/Employee.xml', 'EmployeePattern')
    listDocFactory = xmlfile(path + '/Pages/List.xml', 'liveListRow')
    tableDocFactory = xmlfile(path + '/Pages/Employee.xml', 'EmployeeTablePattern')
    jsClass = 'TimeClock.Objects.EmployeeRenderer';

    commands = None
    visible = False

    def getEmployee(self):
        return self._employee

    @overload
    def handleEvent(self, event: EmployeeChangedEvent):
        if event.employee is self._employee:
            d = self.data_employeeData(None, None)
            d['isAdministrator'] = self._employee.isAdministrator()
            d['isSupervisor'] = self._employee.isSupervisor()
            d['payByTask'] = self._employee.hourly_by_task
            changed = event.previous_values
            if 'hourly_by_task' in changed:
                changed['payByTask'] = changed.pop('hourly_by_task')
            self.callRemote("newValues", {k: d[k] for k in changed.keys()})
    @overload
    def handleEvent(self, event: IEvent):
        pass

    def __init__(self, person: IPerson):
        super().__init__()
        instances.append(self)
        self._employee = IEmployee(person)
        self.powerups = {}

    @property
    def solomonEmployee(self):
        return ISolomonEmployee(self._employee)

    @property
    def name(self):
        return self.solomonEmployee.name

    def render_employeeTable(self, ctx, data):
        r = self.tableDocFactory.load(ctx, self.preprocessors)
        return r
    def data_employeeData(self, ctx, data):
        d = self.solomonEmployee.record.copy()
        d.update(self._employee.persistentValues())
        return d
    def render_employeeDetails(self, ctx, data):
        IEventBus("Web").register(self, IEmployeeChangedEvent)
        row = inevow.IQ(ctx).patternGenerator('employeeDataPattern')
        o = []
        for k, e in employee_attributes.items():
            i, c = e
            if not c:
                def c(x):
                    return x
            if k == 'active_directory_name':
                t = Tag('input')(id=k, value=c(data[-1][k]))
                if not self.employee.isAdministrator():
                    t(disabled=True)
                v = self.preprocess([t])
                o.append(row(data=dict(rowName=i, rowValue=v)))
            elif k.startswith('emergency_contact'):
                v = self.preprocess([Tag('input')(id=k, value=c(data[-1][k]))])
                o.append(row(data=dict(rowName=i, rowValue=v)))
            else:
                o.append(row(data=dict(rowName=i, rowValue=c(data[-1][k]))))

        isAdm = T.input(type='checkbox', id='isAdministrator')
        if IAdministrator(self._employee, None):
            isAdm(checked=True)
        if not self.employee.isAdministrator():
            isAdm(disabled=True)
        isSup = T.input(type='checkbox', id='isSupervisor')
        if ISupervisor(self._employee, None):
            isSup(checked=True)
        if not self.employee.isAdministrator():
            isSup(disabled=True)
        pbt = T.input(type='checkbox', id='payByTask')
        if self._employee.hourly_by_task:
            pbt(checked=True)
        if not self.employee.isAdministrator():
            pbt(disabled=True)
        o.extend([row(data=dict(rowName='Is Supervisor', rowValue=isSup)), row(data=dict(rowName='Is Administrator', rowValue=isAdm)), row(data=dict(rowName='Pay By Task', rowValue=pbt))])
        self.preprocess([isSup, isAdm, pbt])
        save = row(data=dict(rowName='Save', rowValue=self.preprocess([T.input(type='button', value='Save Changes')[
            T.Tag("athena:handler")(event='onclick', handler='saveClicked')
        ]])))
        o.append(save)

        return self.preprocess(o)
    def render_employeeActions(self, ctx, data):
        if IAdministrator(self.employee, None) and self._employee.active_directory_name is None:
            row = inevow.IQ(ctx).patternGenerator('employeeActionPattern')
            import TimeClock.API.Commands
            from ..Commands.SetPassword import SetPassword
            sp = SetPassword(TimeClock.API.Commands.ChangePassword)
            sp.prepare(self)
            sp._employee = self._employee
            sp.currentPW = []
            sp.visible = True
            ctx.fillSlots('rowName', 'Set Password')
            ctx.fillSlots('rowValue', sp)
            return row(data={})
        else:
            return ""

    def showCommand(self, idx):
        c = self.commands[int(idx)]['value']
        if c.visible:
            c.hide()
        else:
            c.show()

    def doCompare(self, keys, vals):
        oldVals = {}
        for key in keys:
            if key not in vals:
                continue
            if getattr(self._employee, key) != vals[key]:
                oldVals[key] = getattr(self._employee, key)
                setattr(self._employee, key, vals[key])
        return oldVals

    @expose
    @Transaction
    def saveClicked(self, args):
        oldVals = {}
        keys = []
        if self.employee is self._employee:
            keys = ['emergency_contact_name', 'emergency_contact_phone']
        if self.employee.isAdministrator():
            if 'payByTask' in args:
                args['hourly_by_task'] = args['payByTask']
            keys = ['emergency_contact_name', 'emergency_contact_phone', 'active_directory_name', 'hourly_by_task']

        oldVals.update(self.doCompare(keys, args))

        if self.employee.isAdministrator():
            if 'isSupervisor' in args:
                isSup = args['isSupervisor']
                if isSup and not self._employee.isSupervisor():
                    s = ISupervisor(NULL)
                    s.employee = self._employee
                    self._employee.powerUp(s, ISupervisor)
                    oldVals['isSupervisor'] = False
                    e = SupervisorCreatedEvent(self._employee, s)
                    IEventBus("Web").postEvent(e)
                    if e.cancelled:
                        raise DatabaseChangeCancelled(e.retval)
                if (not isSup) and self._employee.isSupervisor():
                    s = ISupervisor(self._employee)
                    self._employee.powerDown(s, ISupervisor)
                    oldVals['isSupervisor'] = True
                    e = SupervisorRemovedEvent(self._employee, s)
                    IEventBus("Web").postEvent(e)
                    if e.cancelled:
                        raise DatabaseChangeCancelled(e.retval)
            if 'isAdministrator' in args:
                isSup = args['isAdministrator']
                if isSup and not self._employee.isAdministrator():
                    s = IAdministrator(NULL)
                    s.employee = self._employee
                    self._employee.powerUp(s, IAdministrator)
                    oldVals['isAdministrator'] = False
                if (not isSup) and self._employee.isAdministrator():
                    s = IAdministrator(self._employee)
                    self._employee.powerDown(s, IAdministrator)
                    oldVals['isAdministrator'] = True
        if oldVals:
            e = EmployeeChangedEvent(self._employee, oldVals)
            IEventBus("Web").postEvent(e)
            if e.cancelled:
                raise DatabaseChangeCancelled(e.retval)
    def prepare(self, parent: LiveFragment, force: bool = False):
        super().prepare(parent)
        if hasattr(parent, 'cols'):
            self.length = max(min(len(parent.cols), 3), 2)


registerAdapter(EmployeeRenderer.listRow, IEmployee, IListRow)
registerAdapter(EmployeeRenderer, IEmployee, IAthenaRenderable)

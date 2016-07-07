from twisted.python.components import registerAdapter
from zope.component import getUtilitiesFor, getUtility
from zope.interface import implementer, directlyProvides

from TimeClock.Axiom import Transaction
from TimeClock.Exceptions import DatabaseChangeCancelled, ReportCancelled
from TimeClock.ITimeClock.IDatabase.ISupervisor import ISupervisor
from TimeClock.ITimeClock.IEvent.IEvent import IEvent
from TimeClock.ITimeClock.IEvent.IEventBus import IEventBus
from TimeClock.ITimeClock.IEvent.IEventHandler import IEventHandler
from TimeClock.ITimeClock.IEvent.IWebEvent.IReportChangedEvent import IReportChangedEvent
from TimeClock.ITimeClock.IReport.IFormatterFactory import IFormatterFactory
from TimeClock.ITimeClock.IWeb.IAthenaRenderable import IAthenaRenderable
from TimeClock.ITimeClock.IWeb.IListRow import IListRow
from TimeClock.Report.DynamicReport import DynamicReport
from TimeClock.Utils import overload, coerce
from TimeClock.Web.AthenaRenderers.Abstract.AbstractExpandable import AbstractExpandable
from TimeClock.Web.AthenaRenderers.Abstract.AbstractHideable import AbstractHideable
from TimeClock.Web.AthenaRenderers.Abstract.AbstractRenderer import AbstractRenderer, path
from TimeClock.Web.Events.PostReportRunEvent import PostReportRunEvent
from TimeClock.Web.Events.PreReportRunEvent import PreReportRunEvent
from TimeClock.Web.Events.ReportChangedEvent import ReportChangedEvent
from nevow import inevow
from nevow import tags as T
from nevow.athena import expose
from nevow.context import WovenContext
from nevow.loaders import xmlfile
from nevow import flat


class _RenderListRowMixin(AbstractExpandable):
    length = 6
    _workLocation = None
    ctr = -1
    def render_searchclass(self, ctx, data):
        self.ctr += 1
        return 'report-%i' % self.ctr
    def getArgs(self):
        args = []
        for argName, argType in self._report.getArgs():
            arg = T.input(id=argName, placeholder=argName)
            if argType == 'int':
                arg(type='number', step=1)
            elif argType == 'float':
                arg(type='number', step=0.001)
            elif argType == 'str':
                arg(type='text')
            elif argType == 'IDateTime':
                arg(type='text', class_='IDateTime')
            args.append(arg)
        return args
    def render_listRow(self, ctx: WovenContext, data=None):
        IEventBus("Web").register(self, IReportChangedEvent)
        listCell = inevow.IQ(ctx).patternGenerator("listCell")
        self.expanded = False
        ctx.fillSlots('index', self._report.storeID)
        name = T.input(id='name', value=self._report.name)
        description = T.input(id='description', value=self._report.getDescription())
        args = T.div(id='arguments')[self.getArgs()]

        code = T.div(id='editor', style="height: 1000px; width: 1000px; text-align: left")[self._report.code]
        save = T.input(id='save', type='button', value='Save')[T.Tag('athena:handler')(event='onclick', handler='saveClicked')]
        run = T.input(id='run', type='button', value='Run')[T.Tag('athena:handler')(event='onclick', handler='runReport')]
        format_ = T.select(id='format')[
            [T.option(value=i[0])[i[0]] for i in getUtilitiesFor(IFormatterFactory)]
        ]
        self.preprocess([name, description, args, run, code, save, format_])
        r = [
            listCell(data=dict(listItem='►'))(id='expand-button')[
                T.Tag("athena:handler")(event='onclick', handler='expand')],
            listCell(data=dict(listItem='▼'))(style='display:none', id='unexpand-button')[
                T.Tag("athena:handler")(event='onclick', handler='expand')],
            listCell(data=dict(listItem=name)),
            listCell(data=dict(listItem=description)),
            listCell(data=dict(listItem=args)),
            listCell(data=dict(listItem=format_)),
            listCell(data=dict(listItem=run)),
            listCell(data=dict(listItem=[code, save]))(id='expanded', style='display:none')
        ]
        return r
    def __conform__(self, iface):
        if iface == IListRow:
            self.docFactory = self.listDocFactory
            directlyProvides(self, IListRow)
            return self
    @staticmethod
    def listRow(e):
        return IListRow(DynamicReportRenderer(e))


@implementer(IEventHandler)
class DynamicReportRenderer(AbstractRenderer, AbstractHideable, _RenderListRowMixin):
    docFactory = xmlfile(path + '/Pages/Report.xml', 'ReportPattern')
    listDocFactory = xmlfile(path + '/Pages/List.xml', 'liveListRow', ignoreDocType=True)
    tableDocFactory = xmlfile(path + '/Pages/Report.xml', 'ReportTablePattern')
    jsClass = 'TimeClock.Objects.DynamicReportRenderer';
    cssModule = "jquery.ui.datetimepicker"
    commands = None
    visible = True
    def getReport(self):
        return self._report

    def powerUp(self, obj, iface):
        pups = self.powerups[iface] = self.powerups.get(iface, [])
        pups.append(obj)

    @overload
    def handleEvent(self, event: IReportChangedEvent):
        if event.report is self._report:
            d = dict(code=self._report.code, name=self._report.name, description=self._report.getDescription(), args=flat.flatten(self.getArgs()).decode('charmap'))
            changed = event.previous_values
            keys = list(changed.keys())
            self.callRemote("newValues", {k: d[k] for k in keys})
    @overload
    def handleEvent(self, event: IEvent):
        pass

    @coerce
    def __init__(self, sa: DynamicReport):
        super().__init__()
        self._report = sa
        self.powerups = {}

    @property
    def name(self):
        return "Time Entry"

    def render_reportTable(self, ctx, data):
        r = self.tableDocFactory.load(ctx, self.preprocessors)
        return r

    def data_reportData(self, ctx, data):
        return self._report.persistentValues()

    def render_reportDetails(self, ctx, data):
        IEventBus("Web").register(self, IReportChangedEvent)
        row = inevow.IQ(ctx).patternGenerator('reportDataPattern')

        o = []
        name = T.input(id='name', value=self._report.name)
        description = T.input(id='description', value=self._report.getDescription())
        args = T.input(id='arguments', value=self._report.getArgs())
        save = T.input(type='button', value='Save Changes')[
            T.Tag("athena:handler")(event='onclick', handler='saveClicked')]

        o.append(row(data=dict(rowName="Report Name", rowValue=name)))
        o.append(row(data=dict(rowName="Description", rowValue=description)))
        o.append(row(data=dict(rowName="Arguments", rowValue=args)))

        if save:
            o.append(row(data=dict(rowName="Save Changes", rowValue=save)))
        self.preprocess([name, description, args])
        return o

    def doCompare(self, keys, vals):
        oldVals = {}
        for k in keys:
            if k in vals:
                if getattr(self._report, k) != vals[k]:
                    oldVals[k] = getattr(self._report, k)
                    if k == 'code':
                        oldVals['args'] = self._report.getArgs()
                    setattr(self._report, k, vals[k])
        return oldVals

    @expose
    @Transaction
    def saveClicked(self, args):
        if not self._report.store:
            self._report.store = self.employee.store
        oldVals = {}
        keys = []
        sup = ISupervisor(self.employee, None)
        if self.employee.isAdministrator():
            keys = ['name', 'description', 'code']
        oldVals.update(self.doCompare(keys, args))
        if oldVals:
            e = ReportChangedEvent(self._report, oldVals)
            IEventBus("Web").postEvent(e)
            if e.cancelled:
                raise DatabaseChangeCancelled(e.retval)

    @expose
    def runReport(self, format_, args):
        mime = {'csv': 'text/csv', 'json': 'text/json'}.get(format_, 'text/ascii')
        formatter = getUtility(IFormatterFactory, format_)()
        e = PreReportRunEvent(self._report, formatter, args, self.employee)
        IEventBus("Web").postEvent(e)
        if e.cancelled:
            raise ReportCancelled(e.retval)
        report = self._report.runReport(formatter, args).decode('charmap'), mime
        e = PostReportRunEvent(self._report, formatter, args, report, self.employee)
        IEventBus("Web").postEvent(e)
        if e.cancelled:
            raise ReportCancelled(e.retval)
        return e.result

registerAdapter(DynamicReportRenderer.listRow, DynamicReport, IListRow)
registerAdapter(DynamicReportRenderer, DynamicReport, IAthenaRenderable)

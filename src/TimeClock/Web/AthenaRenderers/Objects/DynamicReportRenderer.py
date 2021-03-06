from TimeClock.Axiom.Store import Store
from TimeClock.Report.Log import Log
from twisted.python.components import registerAdapter
from zope.component import getUtilitiesFor, getUtility
from zope.interface import implementer, directlyProvides

from TimeClock import Utils
from TimeClock.Axiom import Transaction
from TimeClock.Exceptions import DatabaseChangeCancelled, ReportCancelled
from TimeClock.ITimeClock.IDatabase.ISupervisor import ISupervisor
from TimeClock.ITimeClock.IEvent.IEvent import IEvent
from TimeClock.ITimeClock.IEvent.IEventBus import IEventBus
from TimeClock.ITimeClock.IEvent.IEventHandler import IEventHandler
from TimeClock.ITimeClock.IEvent.IWebEvent.IReportChangedEvent import IReportChangedEvent
from TimeClock.ITimeClock.IEvent.IWebEvent.IReportEditedEvent import IReportEditedEvent
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
from TimeClock.Web.Events.ReportEditedEvent import ReportEditedEvent
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

    def render_rowclass(self, ctx, data):
        return ''

    def render_searchclass(self, ctx, data):
        self.ctr += 1
        return 'report-%i' % self.ctr

    def getArgs(self):
        args = []
        for arg_t_n_d in self._report.getArgs():
            argName = arg_t_n_d[0]
            argType = arg_t_n_d[1]
            if len(arg_t_n_d) == 3:
                argDefault = arg_t_n_d[2]
            else:
                argDefault = ''
            arg = T.input(name=argName, placeholder=argName, title=argName, class_='Argument')
            if argType == 'int':
                arg(type='number', step=1, value=argDefault or 0)
            elif argType == 'float':
                arg(type='number', step=0.001, value=argDefault or 0)
            elif argType == 'str':
                arg(type='text', value=argDefault)
            elif argType == 'IDateTime':
                arg(type='text', class_='IDateTime Argument', value=argDefault)
            elif argType == 'bool':
                arg(type='checkbox')
                if argDefault:
                    arg(checked=True)
                arg = T.label()[arg, argName]
            elif argType == 'IAWorkLocation':
                from TimeClock.Database.WorkLocation import WorkLocation
                l = [T.option(value='None', selected=True)['None']] + [T.option(value=i.workLocationID)[i.description] for i in
                                                                     list(Store.query(WorkLocation)) if i.active]
                arg = T.select(name=argName, placeholder=argName, title=argName, value='None', class_='Argument')[l]
            elif argType == 'IASubAccount':
                from TimeClock.Database.SubAccount import SubAccount
                l = [T.option(value='None', selected=True)['None']] + [T.option(value=i.name)[i.name] for i in
                                                                     list(Store.query(SubAccount)) if i.active]
                arg = T.select(name=argName, placeholder=argName, title=argName, value='None', class_='Argument')[l]

            args.append(arg)
        return self.preprocess(args)

    def render_listRow(self, ctx: WovenContext, data=None):
        IEventBus("Web").register(self, IReportChangedEvent)
        IEventBus("Web").register(self, IReportEditedEvent)
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
            self.visible = True
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
    tempValue = None
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
    def handleEvent(self, event: IReportEditedEvent):
        if event.report is self._report:
            if self.tempValue != event.new_code:
                self.callRemote("newValues", {'code': event.new_code})
                self.tempValue = event.new_code

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
        IEventBus("Web").register(self, IReportEditedEvent)
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
    def editorChanged(self, val):
        if self.tempValue == val:
            return
        e = ReportEditedEvent(self._report, val)
        IEventBus("Web").postEvent(e)

    @expose
    @Transaction
    def saveClicked(self, args):
        if not self._report.store:
            self._report.store = self.employee.store
        oldVals = {}
        keys = []
        if self.employee.isAdministrator():
            keys = ['name', 'description', 'code']
        oldVals.update(self.doCompare(keys, args))
        if oldVals:
            e = ReportChangedEvent(self._report, oldVals)
            IEventBus("Web").postEvent(e)
            if e.cancelled:
                raise DatabaseChangeCancelled(e.retval)

    def log(self, msg):
        self.parent.parent.callRemote('log', msg)

    def progress(self, progress):
        self.parent.parent.callRemote('progress', progress)

    @expose
    def runReport(self, format_, args):
        mime = {'csv': 'text/csv', 'json': 'text/json', 'xml': 'text/xml', 'xls':'application/vnd.ms-excel', 'widget':'livefragment'}.get(format_, 'text/ascii')
        formatter = getUtility(IFormatterFactory, format_)()
        log = Log(self)
        e = PreReportRunEvent(self._report, formatter, args, self.employee)
        if e.cancelled:
            raise ReportCancelled(e.retval)
        IEventBus("Web").postEvent(e)
        args = list(args)
        params = self._report.getArgs()
        print(252, params)
        print(253, args)
        for idx, param in enumerate(params):
            if isinstance(param, tuple) and len(param) == 2:
                ptype = param[1]
                if ptype == 'IDateTime':
                    args[idx] = Utils.getIDateTime(args[idx])
        self._report.runReport(formatter, args, log, callback=self.callback(mime, formatter, args))

    def callback(self, mime, formatter, args):
        def cb(report):
            if isinstance(report, bytes):
                report = report.decode('charmap')
            else:
                report.prepare(self)
            e = PostReportRunEvent(self._report, formatter, args, [report, mime], self.employee)
            IEventBus("Web").postEvent(e)
            if e.cancelled:
                raise ReportCancelled(e.retval)
            self.callRemote('displayReport', e.result)
        return cb

registerAdapter(DynamicReportRenderer.listRow, DynamicReport, IListRow)
registerAdapter(DynamicReportRenderer, DynamicReport, IAthenaRenderable)

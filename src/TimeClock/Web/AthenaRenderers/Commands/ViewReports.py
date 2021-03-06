from twisted.python.components import registerAdapter
from zope.interface import implementer

from TimeClock.Axiom import Store, Transaction
from TimeClock.Database import Commands
from TimeClock.ITimeClock.IEvent.IEvent import IEvent
from TimeClock.ITimeClock.IEvent.IEventBus import IEventBus
from TimeClock.ITimeClock.IEvent.IEventHandler import IEventHandler
from TimeClock.ITimeClock.IEvent.IWebEvent.IReportChangedEvent import IReportChangedEvent
from TimeClock.ITimeClock.IWeb.IAthenaRenderable import IAthenaRenderable
from TimeClock.ITimeClock.IWeb.IListRow import IListRow
from TimeClock.Report.DynamicReport import DynamicReport
from TimeClock.Utils import overload
from TimeClock.Web.AthenaRenderers.Abstract.AbstractHideable import AbstractHideable
from TimeClock.Web.AthenaRenderers.Abstract.AbstractRenderer import AbstractRenderer, path
from TimeClock.Web.AthenaRenderers.Commands import AbstractCommandRenderer
from TimeClock.Web.AthenaRenderers.Widgets.List import List
from TimeClock.Web.AthenaRenderers.Widgets.SaveList import SaveList
from TimeClock.Web.Events.ReportCreatedEvent import ReportCreatedEvent
from nevow import tags
from nevow.athena import expose
from nevow.context import WovenContext
from nevow.loaders import xmlfile


@implementer(IAthenaRenderable, IEventHandler)
class ViewReports(AbstractCommandRenderer, AbstractHideable):
    docFactory = xmlfile(path + "/Pages/GenericCommand.xml", "GenericCommandPattern")
    jsClass = 'TimeClock.Commands.ViewReports'
    subaccounts = None
    name = 'View Reports'
    l = None

    @overload
    def handleEvent(self, evt: ReportCreatedEvent):
        self.l.addRow(IListRow(evt.report))

    @overload
    def handleEvent(self, event: IEvent):
        pass

    def render_genericCommand(self, ctx: WovenContext, data):
        IEventBus("Web").register(self, IReportChangedEvent)
        self.l = l = List(list(Store.Store.query(DynamicReport)), ["", "Report Name", "Report Description", "Report Arguments", 'Format', 'Run Report'])
        l.closeable = False
        l.addRow(SaveList(6, start=1))
        l.prepare(self)
        l.visible = True
        newReport = tags.input(type='button', value='New Report')[tags.Tag('athena:handler')(event='onclick', handler='newReport')]
        self.preprocess([newReport])
        log = self.preprocess([tags.div(id='log', class_='log')])
        return newReport, l, log

    @expose
    @Transaction
    def newReport(self):
        r = DynamicReport(name='new report')
        e = ReportCreatedEvent(r)
        IEventBus("Web").postEvent(e)


registerAdapter(ViewReports, Commands.ViewReports.ViewReports, IAthenaRenderable)

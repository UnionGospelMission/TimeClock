import time
from twisted.python.components import registerAdapter
from zope.interface import implementer

from TimeClock.Axiom.Store import Store
from TimeClock.Database import Commands
from TimeClock.Database.Employee import Employee
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
from TimeClock.Web.AthenaRenderers.Widgets.SaveList import SaveList
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
    @expose
    def load(self):
        if not self.loaded:
            self.loaded = True
            l = [IListRow(i) for i in self.getEntries()]
            for i in l:
                self.l.addRow(i)
            self.loaded = True
    l = None
    @overload
    def handleEvent(self, evt: TimeEntryCreatedEvent):
        if evt.timeEntry.employee is self.employee:
            self.l.addRow(evt.timeEntry)
    @overload
    def handleEvent(self, event: IEvent):
        pass
    def render_genericCommand(self, ctx: WovenContext, data):
        IEventBus("Web").register(self, ITimeEntryChangedEvent)
        self.l = l = List([], ["Work Location", "Sub Account", "Start Time", "End Time", "Duration", "Approved"])
        l.closeable = False
        l.addRow(SaveList(6))
        l.prepare(self)
        l.visible = True
        startTime = tags.input(id='startTime', placeholder='Start Time')[
            tags.Tag('athena:handler')(event='onchange', handler='timeWindowChanged')]
        endTime = tags.input(id='endTime', placeholder='End Time')[
            tags.Tag('athena:handler')(event='onchange', handler='timeWindowChanged')]
        self.preprocess([startTime, endTime])
        return [startTime, endTime, l]
    def getEntries(self):
        return list(i for i in self.employee.powerupsFor(ITimeEntry) if i.type == IEntryType("Work"))
    @expose
    def timeWindowChanged(self, startTime, endTime):
        if startTime:
            startTime = IDateTime(startTime)
        else:
            startTime = IDateTime(0)
        if endTime:
            endTime = IDateTime(endTime)
        else:
            endTime = IDateTime(time.time())
        entries = [IListRow(i).prepare(self.l) for i in self.getEntries() if not (i.endTime() < startTime or i.startTime() > endTime)]
        self.l.list = entries
        return entries






registerAdapter(ViewHours, Commands.ViewHours.ViewHours, IAthenaRenderable)

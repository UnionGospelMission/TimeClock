from twisted.python.components import registerAdapter
from zope.interface import implementer

from TimeClock.Database import Commands
from TimeClock.Axiom import Transaction
from TimeClock.Database.Event.ClockInOutEvent import ClockInOutEvent
from TimeClock.Exceptions import DatabaseChangeCancelled
from TimeClock.ITimeClock.IEvent.IDatabaseEvent import IDatabaseEvent
from TimeClock.ITimeClock.IEvent.IEvent import IEvent
from TimeClock.ITimeClock.IEvent.IEventBus import IEventBus
from TimeClock.ITimeClock.IEvent.IEventHandler import IEventHandler
from TimeClock.ITimeClock.IEvent.IWebEvent.ISubAccountChangedEvent import ISubAccountChangedEvent
from TimeClock.ITimeClock.IEvent.IWebEvent.IWebEvent import IWebEvent
from TimeClock.ITimeClock.IEvent.IWebEvent.IWorkLocationChangedEvent import IWorkLocationChangedEvent
from TimeClock.ITimeClock.ISolomonEmployee import ISolomonEmployee
from TimeClock.ITimeClock.IWeb.IAthenaRenderable import IAthenaRenderable
from TimeClock.Utils import overload
from TimeClock.Web.AthenaRenderers.Abstract.AbstractHideable import AbstractHideable
from TimeClock.Web.AthenaRenderers.Abstract.AbstractRenderer import AbstractRenderer, path
from TimeClock.Web.AthenaRenderers.Commands import AbstractCommandRenderer
from TimeClock.Web.Events.SubAccountAssignmentChangedEvent import SubAccountAssignmentChangedEvent
from TimeClock.Web.Events.TimeEntryChangedEvent import TimeEntryChangedEvent
from TimeClock.Web.Events.TimeEntryCreatedEvent import TimeEntryCreatedEvent
from TimeClock.Web.Events.WorkLocationAssignmentChangedEvent import WorkLocationAssignmentChangedEvent
from nevow import tags
from nevow.athena import expose
from nevow.context import WovenContext
from nevow.loaders import xmlfile
from nevow import flat


@implementer(IEventHandler)
class ClockInOut(AbstractCommandRenderer, AbstractHideable):
    docFactory = xmlfile(path + "/Pages/GenericCommand.xml", "GenericCommandPattern")
    jsClass = 'TimeClock.Commands.ClockInOut'
    workLocations = None
    name = 'Clock In / Clock Out'
    selected = None
    ltl = None
    _employee = None

    def prepare(self, *a, **kw):
        super().prepare(*a, **kw)
        self._employee = self.employee

    @overload
    def handleEvent(self, event: SubAccountAssignmentChangedEvent):
        if event.employee is self._employee:
            self.refresh()

    @overload
    def handleEvent(self, event: ISubAccountChangedEvent):
        subAccount = event.subAccount
        if subAccount in self._employee.getSubAccounts():
            self.refresh()

    @overload
    def handleEvent(self, event: WorkLocationAssignmentChangedEvent):
        if event.employee is self._employee:
            self.refresh()

    @overload
    def handleEvent(self, event: IWorkLocationChangedEvent):
        workLocation = event.workLocation
        if workLocation in self._employee.getWorkLocations():
            self.refresh()

    @overload
    def handleEvent(self, event: ClockInOutEvent):
        if event.employee is self._employee:
            if event.clockedIn:
                self.callRemote("clockedIn");
            else:
                self.callRemote("clockedOut");

    @overload
    def handleEvent(self, event: IEvent):
        pass

    def render_class(self, ctx: WovenContext, data):
        IEventBus("Database").register(self, IDatabaseEvent)
        IEventBus("Web").register(self, IWebEvent)
        return "ClockInOut"

    def getSubs(self, se):
        subs = []
        for a in self._employee.getSubAccounts():
            o = tags.option(value=a.sub)[a.name]
            if se.defaultSubAccount == a:
                o(selected='')
            subs.append(o)
        return subs

    def getWLocs(self, se):
        locs = []
        for b in self._employee.getWorkLocations():
            o = tags.option(value=b.workLocationID)[b.description]
            if se.defaultWorkLocation == b:
                o(selected='')
            locs.append(o)
        return locs

    def refresh(self):
        se = ISolomonEmployee(self._employee)
        self.callRemote('refresh', flat.flatten(self.getSubs(se)).decode('charmap'), flat.flatten(self.getWLocs(se)).decode('charmap'))

    def render_genericCommand(self, ctx: WovenContext, data):
        se = ISolomonEmployee(self._employee)
        s = tags.select(id="sub")[self.getSubs(se)]

        w = tags.select(id='wloc')[self.getWLocs(se)]


        sub = tags.input(type='button', value='Clock In')[
            tags.Tag('athena:handler')(event='onclick', handler='doClockIn')
        ]

        out = tags.input(type='button', value='Clock Out', id='clockout')[
            tags.Tag('athena:handler')(event='onclick', handler='doClockOut')
        ]
        d = tags.div(id='clockin')[s, w, sub]

        if self._employee.timeEntry:
            d(style='display:none')
        else:
            out(style='display:none')

        return self.preprocess([d, out])
    @expose
    @Transaction
    def clockIn(self, sub, wloc):
        self._employee.getAPI().clockIn(sub, wloc)
        e = TimeEntryCreatedEvent(self._employee.timeEntry)
        IEventBus("Web").postEvent(e)
        if e.cancelled:
            raise DatabaseChangeCancelled(e.retval)
    @expose
    @Transaction
    def clockOut(self):
        te = self._employee.timeEntry
        self._employee.getAPI().clockOut(self._employee)
        e = TimeEntryChangedEvent(te, {'endTime': None})
        IEventBus("Web").postEvent(e)
        if e.cancelled:
            raise DatabaseChangeCancelled(e.retval)


registerAdapter(ClockInOut, Commands.ClockIn.ClockIn, IAthenaRenderable)
registerAdapter(ClockInOut, Commands.ClockOut.ClockOut, IAthenaRenderable)

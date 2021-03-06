import base64

import time

from TimeClock.Web.AthenaRenderers.Commands.ApproveDepartmentTime import ApproveDepartmentTime
from TimeClock.Web.AthenaRenderers.Commands.ApproveShifts import ApproveShifts
from twisted.internet.defer import Deferred

from TimeClock.Web.AthenaRenderers.Commands.SetPassword import SetPassword
from nevow import tags
from twisted.internet import reactor
from zope.interface import implementer

from TimeClock.Database.Commands.SetSupervisor import SetSupervisor
from TimeClock.Database.Event.ClockInOutEvent import ClockInOutEvent
from TimeClock.ITimeClock.IDatabase.IAdministrator import IAdministrator
from TimeClock.ITimeClock.IDatabase.ICalendarData import ICalendarData
from TimeClock.ITimeClock.IDatabase.IEmployee import IEmployee
from TimeClock.ITimeClock.IEvent.IDatabaseEvent import IDatabaseEvent
from TimeClock.ITimeClock.IEvent.IEvent import IEvent
from TimeClock.ITimeClock.IEvent.IEventBus import IEventBus
from TimeClock.ITimeClock.IEvent.IEventHandler import IEventHandler
from TimeClock.ITimeClock.ISolomonEmployee import ISolomonEmployee
from TimeClock.ITimeClock.IWeb.IAthenaRenderable import IAthenaRenderable
from TimeClock.Util.DateTime import DateTime
from TimeClock.Web.AthenaRenderers.Commands.SetSupervisees import SetSupervisees

from TimeClock.Web.LiveFragment import LiveFragment
from .MappingResource import MappingResource
from TimeClock.Web.Utils import formatShortName
from nevow.athena import LivePage, expose, AutoJSPackage, AutoCSSPackage, _collectPackageBelow
from nevow.context import WovenContext
from nevow.loaders import xmlfile


path = __file__.rsplit('/', 1)[0]


def getId() -> str:
    with open('/dev/urandom', 'rb') as f:
        return base64.b64encode(f.read(256)).decode('charmap')


def Renderer(cls):
    def render_cls(self, ctx):
        return cls(self, ctx)
    return render_cls


def getActionItems(self, ctx):
    e = IAthenaRenderable(self.employee)
    e.visible = False
    e.getName = lambda *a: "My Profile"
    o = [e]
    p = self.employee.getPermissions()
    for i in self.api.getCommands(self.employee):
        if i.hasPermission(p) or IAdministrator(self.employee, None):
            iar = IAthenaRenderable(i, None)
            if iar:
                if self.employee.alternate_authentication and self.employee.alternate_authentication.expired:
                    if not isinstance(iar, SetPassword):
                        continue
                    else:
                        o = []
                        iar.visible = True
                if isinstance(iar, SetPassword) and self.employee.active_directory_name and not self.employee.alternate_authentication.expired:
                    iar.visible = True
                o.append(iar)
            if isinstance(i, SetSupervisor):
                o.append(SetSupervisees(i))
            if isinstance(iar, ApproveShifts):
                o.append(ApproveDepartmentTime(i))
    from TimeClock.Web.AthenaRenderers.Widgets.TimeClockStation import TimeClockStation
    o.append(TimeClockStation())
    return o


class TimeClockPage(LivePage):
    cssModule = 'TimeClock'
    docFactory = xmlfile(path + "/Pages/TimeClock.html")
    pages = {}
    LONG_CALL_TIME = 1

    def action_call(self, ctx, requestId, method, objectID, args, kwargs):
        startTime = time.time()
        try:
            return super().action_call(ctx, requestId, method, objectID, args, kwargs)
        finally:
            endTime = time.time()
            if endTime - startTime > self.LONG_CALL_TIME:
                print("extremely long remote call: %2f seconds" % (endTime-startTime))
                print(method, self._localObjects[objectID], args, kwargs)


    def renderHTTP(self, ctx):
        resp = super().renderHTTP(ctx)
        return resp

    def getWidget(self, idx):
        return self._localObjects[idx]

    def getAllWidgets(self):
        return self._localObjects.copy()

    def child_jsmodule(self, ctx):
        return MappingResource(self.jsModules.mapping)

    def child_cssmodule(self, ctx):
        return MappingResource(self.cssModules.mapping)

    def __init__(self, employee: IEmployee):
        super().__init__()
        self.employee = employee
        self.pageId = getId()
        self.pages[self.pageId] = self
        self.jsModules.mapping.update(AutoJSPackage(path + '/JS/').mapping)
        self.cssModules.mapping.update(AutoCSSPackage(path + '/CSS/').mapping)
        self.creationTime = time.time()

    @implementer(IEventHandler)
    class MenuPane(LiveFragment):
        def powerUp(self, obj, iface):
            pass
        updateTime = None
        docFactory = xmlfile(path + "/Pages/TimeClock.html", "MenuPattern")
        jsClass = "TimeClock.MenuPane"

        def handleEvent(self, event: IEvent):
            if isinstance(event, ClockInOutEvent):
                if event.employee is self.employee:
                    if event.clockedIn:
                        self.callRemote('clockedIn')
                    else:
                        self.callRemote('clockedOut')

        def __init__(self, parent, ctx: WovenContext):
            super().__init__()
            self.parent = parent
            self.parent.menu = self
            self.employee = self.parent.employee
            self.api = self.employee.getAPI()

            self.setFragmentParent(parent)
            IEventBus("Database").register(self, IDatabaseEvent)

        def render_employeeName(self, ctx):
            return ISolomonEmployee(self.employee).name

        def render_workedToday(self, ctx):
            today = DateTime.today()
            tomorrow = today.replace(days=1)
            cd = ICalendarData(self.employee.viewHours(today, tomorrow))
            o = cd.sumBetween(today, tomorrow).total_seconds()
            return "%i:%02i" % (o // 3600, o // 60 % 60)

        def render_workedThisWeek(self, ctx):
            today = DateTime.today()
            first_day_of_this_week = today.replace(days=-((today.weekday() + 1) % 7))
            first_day_of_next_week = first_day_of_this_week.replace(days=7)
            cd = ICalendarData(self.employee.viewHours(first_day_of_this_week, first_day_of_next_week))
            o = cd.sumBetween(first_day_of_this_week, first_day_of_next_week).total_seconds()
            delay = 60
            if self.employee.timeEntry:
                delay -= o % 60

            reactor.callLater(delay, self.updateTime)
            return "%i:%02i" % (o // 3600, o // 60 % 60)

        def render_showRemainingTime(self, ctx):
            ise = ISolomonEmployee(self.employee, None)
            if ise:
                pg = ise.payGrpId
                if pg in ['REGHR', 'REGFT']:
                    return 'display: inline;'
            return 'display: none;'

        def render_remainingThisWeek(self, ctx):
            today = DateTime.today()
            first_day_of_this_week = today.replace(days=-((today.weekday() + 1) % 7))
            first_day_of_next_week = first_day_of_this_week.replace(days=7)
            cd = ICalendarData(self.employee.viewHours(first_day_of_this_week, first_day_of_next_week))
            o = cd.sumBetween(first_day_of_this_week, first_day_of_next_week).total_seconds()
            delay = 60
            if self.employee.timeEntry:
                delay -= o % 60
            o = 60 * 60 * 40 - o
            if o < 0:
                o = 0
            return "%i:%02i" % (o // 3600, o // 60 % 60)

        def updateTime(self):
            worked = self.render_workedThisWeek(None)
            self.callRemote("updateTime", worked, self.render_workedToday(None), self.render_remainingThisWeek(None))

        def detached(self):
            super()
            self.updateTime = lambda *a: None

        def render_menuItem(self, args):
            request, tag, data = args
            o = []
            for d in data:
                if self.employee.timeEntry and d == "Clock In":
                    style = "display:none"
                elif not self.employee.timeEntry and d == "Clock Out":
                    style = "display:none"
                else:
                    style = ""
                o.append(tag.clone()(id='athenaid:1-' + formatShortName(d), name=formatShortName(d), style=style)[tags.div()[d]])
            return o

        def render_clockedInOut(self, ctx):
            if self.employee.timeEntry:
                return 'In'
            return 'Out'

        def data_menuItem(self, ctx, idata):
            o = []
            for a in getActionItems(self, ctx):
                if a.getName() not in o:
                    o.append(a.getName())
            return o

        def hideClockIn(self):
            self.callRemote("hideClockIn")

        def hideClockOut(self):
            self.callRemote("hideClockOut")

        @expose
        def navigate(self, element):
            self.parent.action.navigate(element)

    render_MenuPane = Renderer(MenuPane)

    class ActionPane(LiveFragment):
        docFactory = xmlfile(path + "/Pages/TimeClock.html", "ActionPattern")
        jsClass = "TimeClock.ActionPane"

        @property
        def employee(self):
            return self.parent.employee

        def __init__(self, parent, ctx):
            super().__init__()
            self.parent = parent
            self.parent.action = self
            self.api = self.employee.getAPI()
            self.selectedElement = None
            self.setFragmentParent(parent)
            self.elements = {}

        def render_ActionItems(self, ctx):
            o = []
            for iar in getActionItems(self, ctx):
                i = iar.getName()
                if 'Clock In' in i:
                    if self.selectedElement:
                        continue
                    self.elements['clockInOut'] = iar
                    self.selectedElement = iar
                else:
                    self.elements[formatShortName(i)] = iar
                iar.prepare(self)
                iar.topLevel()
                iar.visible = False
                o.append(iar)
            if not self.selectedElement:
                self.selectedElement = list(self.elements.values())[-1]
            if self.employee.alternate_authentication and self.employee.alternate_authentication.expired:
                for ele in self.elements:
                    if isinstance(self.elements[ele], SetPassword):
                        self.selectedElement = self.elements[ele]
                        self.selectedElement.visible = True
                        break
            self.selectedElement.visible = True
            d = [Deferred().addCallback(lambda v: o.pop(0)) for i in o]

            def cb():
                if d:
                    d.pop(0).callback(None)
                    reactor.callLater(0.001, cb)
            reactor.callLater(0.001, cb)
            return o

        @expose
        def navigate(self, element):
            self.selectedElement = self.elements[element]
    render_ActionPane = Renderer(ActionPane)

import base64

from TimeClock.Database.Commands.ChangeAuthentication import ChangeAuthentication
from TimeClock.ITimeClock.IDatabase.IAdministrator import IAdministrator
from TimeClock.ITimeClock.IDatabase.ICalendarData import ICalendarData
from TimeClock.ITimeClock.IDatabase.IEmployee import IEmployee
from TimeClock.ITimeClock.ISolomonEmployee import ISolomonEmployee
from TimeClock.ITimeClock.IWeb.IAthenaRenderable import IAthenaRenderable
from TimeClock.Util.DateTime import DateTime
from TimeClock.Web.AthenaRenderer.Calendar import Calendar
from TimeClock.Web.AthenaRenderer.Editor import Editor
from TimeClock.Web.AthenaRenderer.ListRenderer import ListRenderer
from TimeClock.Web.AthenaRenderer.ManageSubAccounts import ManageSubAccounts
from TimeClock.Web.LiveFragment import LiveFragment
from nevow.athena import LivePage, expose
from nevow.context import WovenContext
from nevow.loaders import xmlfile
from twisted.internet import reactor
import os


path = __file__.rsplit('/', 1)[0]


def getId() -> str:
    with open('/dev/urandom', 'rb') as f:
        return base64.b64encode(f.read(256)).decode('charmap')


def Renderer(cls):
    def render_cls(self, ctx):
        return cls(self, ctx)
    return render_cls


def formatShortName(n):
    n=n.title().replace(' ', '')
    return n[0].lower() + n[1:]


def getActionItems(self, ctx):
    o = []
    p = self.employee.getPermissions()
    for i in self.api.getCommands():
        if isinstance(i, ChangeAuthentication) and self.employee.active_directory_name:
            continue
        if i.hasPermission(p) or IAdministrator(self.employee, None):
            iar = IAthenaRenderable(i, None)
            if iar:
                o.append(iar)
    if IAdministrator(self.employee, None):
        o.append(ManageSubAccounts())
    return o




class TimeClockPage(LivePage):
    pages = {}
    def __init__(self, employee: IEmployee):
        super(TimeClockPage, self).__init__(employee)
        self.employee = employee
        self.pageId = getId()
        self.pages[self.pageId] = self
        self.jsModules.mapping['TimeClock'] = path + '/JS/TimeClock.js'
        self.jsModules.mapping['mode-python.js'] = path + '/JS/mode-python.js'
        self.jsModules.mapping['theme-twilight.js'] = path + '/JS/theme-twilight.js'
        self.cssModules.mapping['jquery-ui'] = path + '/CSS/jquery-ui.css'
        for f in os.listdir(path + '/JS'):
            self.jsModules.mapping['TimeClock.' + f.rsplit('.js', 1)[0]] = path + '/JS/' + f
            self.jsModules.mapping[f.rsplit('.js', 1)[0]] = path + '/JS/' + f
    docFactory = xmlfile(path + "/Pages/TimeClock.html")

    class MenuPane(LiveFragment):
        docFactory = xmlfile(path + "/Pages/TimeClock.html", "MenuPattern")
        jsClass = "TimeClock.MenuPane"
        def __init__(self, parent, ctx: WovenContext):
            self.parent = parent
            self.parent.menu = self
            self.employee = self.parent.employee
            self.api = self.employee.getAPI()

            self.setFragmentParent(parent)
        def render_employeeName(self, ctx):
            return ISolomonEmployee(self.employee).name
        def render_workedThisWeek(self, ctx):
            today = DateTime.today()
            first_day_of_this_week = today.replace(days=-((today.weekday() + 1) % 7))
            first_day_of_next_week = first_day_of_this_week.replace(days=7)
            cd = ICalendarData(self.employee.viewHours(first_day_of_this_week, first_day_of_next_week))
            o = 0
            for i in cd:
                o += i.duration().seconds

            delay = 60
            if self.employee.timeEntry:
                delay -= o % 60

            reactor.callLater(delay, self.updateTime)
            return "%i:%02i" % (o // 3600, o // 60 % 60)
        def updateTime(self):
            worked = self.render_workedThisWeek(None)
            self.callRemote("updateTime", worked)

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
                o.append(tag.clone()(id='athenaid:1-' + formatShortName(d), name=formatShortName(d), style=style)[d])
            return o
        def data_menuItem(self, ctx, idata):
            o = getActionItems(self, ctx)
            return [i.name for i in o]
        def hideClockIn(self):
            self.callRemote("hideClockIn")
        def hideClockOut(self):
            self.callRemote("hideClockOut")
        @expose
        def navigate(self, element):
            print(84, element)
            self.parent.action.navigate(element)

    render_MenuPane = Renderer(MenuPane)
    class ActionPane(LiveFragment):
        docFactory = xmlfile(path + "/Pages/TimeClock.html", "ActionPattern")
        jsClass = "TimeClock.ActionPane"
        def __init__(self, parent, ctx):
            self.parent = parent
            self.parent.action = self
            self.employee = parent.employee
            self.api = self.employee.getAPI()
            self.selectedElement = None
            self.setFragmentParent(parent)
            self.elements = {}
        def render_ActionItems(self, ctx):
            o = getActionItems(self, ctx)
            for iar in o:
                i = iar.name
                self.elements[formatShortName(i)] = iar
                if i == 'Clock In' and not self.employee.timeEntry:
                    self.selectedElement = iar
                elif i == "Clock Out" and self.employee.timeEntry:
                    self.selectedElement = iar
                iar.prepare(self)
            return o

        @expose
        def navigate(self, element):
            if self.selectedElement:
                self.selectedElement.hide()
            self.selectedElement = self.elements[element]
            self.elements[element].show()
    render_ActionPane = Renderer(ActionPane)



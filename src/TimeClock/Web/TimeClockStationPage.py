from twisted.internet import reactor

import nevow
from TimeClock import API
from TimeClock.Util.DateTime import DateTime
from TimeClock.Utils import overload
from TimeClock.Web.AthenaRenderers.TimeClockStationWidgets.ClockedInList import ClockedInList
from TimeClock.Web.AthenaRenderers.TimeClockStationWidgets.ClockInOut import ClockInOut
from TimeClock.Web.AthenaRenderers.TimeClockStationWidgets.ClockedOutList import ClockedOutList
from TimeClock.Web.TimeClockPage import TimeClockPage, path
from nevow.athena import LiveElement
from nevow.context import WovenContext
from nevow.inevow import IRequest
from nevow.loaders import xmlfile
from nevow.page import renderer, Element


class FakeEmployee(object):
    @staticmethod
    def getAPI():
        return API.APIs.PublicAPI


class TimeClockStationPage(Element, TimeClockPage):
    docFactory = xmlfile(path + "/Pages/TimeClockStation.html")
    cssModule = "jquery.ui.datetimepicker"
    class MenuElement(LiveElement):
        jsClass = 'TimeClock.TimeClockStation.Menu'
        def __init__(self, parent):
            super().__init__()
            self.setFragmentParent(parent)
        docFactory = xmlfile(path + "/Pages/TimeClockStation.html", "MenuPattern")
        @renderer
        def currentTime(self, rq: IRequest, tag):
            o = (DateTime.now() - DateTime.today()).total_seconds()
            delay = 60 - o % 60
            reactor.callLater(delay, self.updateTime)
            return "%i:%02i" % (o // 3600, o // 60 % 60)
        def updateTime(self):
            o = self.currentTime(None, None)
            self.callRemote("updateTime", o)
    class ActionsElement(LiveElement):
        docFactory = xmlfile(path + "/Pages/TimeClockStation.html", "ActionPattern")
        jsClass = 'TimeClock.TimeClockStation.Action'

        def __init__(self, parent):
            super().__init__()
            self.setFragmentParent(parent)
        def refresh(self, wloc, subaccount):
            self.liveFragmentChildren[1].refresh(wloc, subaccount)
            self.liveFragmentChildren[2].refresh(wloc, subaccount)
        @renderer
        def ClockedIn(self, rq: IRequest, tag):
            return ClockedInList(self)
        @renderer
        def ClockedOut(self, rq: IRequest, tag):
            return ClockedOutList(self)
        @renderer
        def ClockInOut(self, rq: IRequest, tag):
            return ClockInOut(self)

    Menu = renderer(lambda self, rq: self.MenuElement(self))
    Action = renderer(lambda self, rq: self.ActionsElement(self))
    def __init__(self):
        super().__init__()
        TimeClockPage.__init__(self, FakeEmployee)
    @overload
    def renderer(self, ctx: WovenContext, name: str):
        return self.renderer(name)
    @overload
    def renderer(self, name: str):
        try:
            return super().renderer(name)
        except nevow.errors.MissingRenderMethod as e:
            if hasattr(self, 'render_' + name):
                return getattr(self, 'render_' + name)
            raise


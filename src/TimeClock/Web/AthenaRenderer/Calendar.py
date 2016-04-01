from twisted.python.components import registerAdapter

from TimeClock.ITimeClock.IDatabase.ICalendarData import ICalendarData
from TimeClock.ITimeClock.IDatabase.ITimePeriod import ITimePeriod
from TimeClock.Web.AthenaRenderer.CalendarDay import CalendarDay
from nevow.athena import expose

from nevow.inevow import IData

from nevow import flat, inevow

from TimeClock.Util.DateTime import DateTime
from nevow.context import WovenContext

from TimeClock.Web.AthenaRenderer.AbstractRenderer import AbstractRenderer
from nevow.loaders import xmlstr, xmlfile
from zope.interface import implementer
from TimeClock.ITimeClock.IDateTime import IDate

from TimeClock.ITimeClock.IWeb.IAthenaRenderable import IAthenaRenderable
from TimeClock.Web.LiveFragment import LiveFragment


path = __file__.rsplit('/', 2)[0]

months = {1: "January",
          2: "February",
          3: "March",
          4: "April",
          5: "May",
          6: "June",
          7: "July",
          8: "August",
          9: "September",
          10: "October",
          11: "November",
          12: "December"}


class Calendar(AbstractRenderer):
    startDate = None
    endDate = None
    data = None
    docFactory = xmlfile(path + "/Pages/Calendar.xml", "CalendarPattern")
    name = 'Calendar'
    jsClass = "TimeClock.Calendar"
    def setStartDate(self, date: IDate):
        self.startDate = date
    def setEndDate(self, date: IDate):
        self.endDate = date
    def render_calendar(self, ctx: WovenContext, idata: IData):
        o = []
        monthRow = inevow.IQ(ctx).patternGenerator("monthRow")
        weekDayRow = inevow.IQ(ctx).patternGenerator("weekDayRow")
        weekDataRow = inevow.IQ(ctx).patternGenerator("weekDataRow")
        if self.startDate:
            startDate = self.startDate
        else:
            startDate = DateTime.today().replace(day=1)
        if self.endDate:
            endDate = self.endDate.replace(days=1)
        else:
            endDate = DateTime.today().nextMonth(day=1)
        week = []
        for day in DateTime.daysBetween(startDate, endDate):
            if isinstance(day, tuple):
                if week:
                    o.append(weekDayRow(data=week))
                    o.append(weekDataRow(data=week))
                    week = []
                ctx.fillSlots("Month", months[day[1]])
                o.append(monthRow(data=months[day[1]]))
            else:
                week.append(day)
                if day.weekday() == 5:
                    o.append(weekDayRow(data=week))
                    o.append(weekDataRow(data=week))
                    week = []
        if week:
            o.append(weekDayRow(data=week))
            o.append(weekDataRow(data=week))
        return o
    def render_month(self, ctx, data):
        pg = inevow.IQ(ctx).patternGenerator("monthCell")
        return pg(data=dict(month=data))
    def render_weekDay(self, ctx, data):
        pg = inevow.IQ(ctx).patternGenerator("day")
        o = []
        if len(data) != 7:
            for c in range((data[0].weekday() + 1) % 7):
                o.append(pg(data=dict(day="", ordinal=0)))
        for s in data:
            o.append(pg(data=dict(day=s.day, ordinal=s.toordinal())))
        return o
    def render_weekData(self, ctx, data):
        pg = inevow.IQ(ctx).patternGenerator("dayData")
        o = []

        if len(data) != 7:
            for c in range((data[0].weekday() + 1) % 7):
                o.append(pg(data=dict(dayData="", ordinal=0)))
        for s in data:
            if self.data:
                dayData = self.data.getData(s)
            else:
                dayData = ""
            o.append(pg(data=dict(dayData=dayData, ordinal=s.toordinal())))
        return o
    def setData(self, data):
        self.data = data
    @expose
    def zoomOnDay(self, day):
        pass
        # day=DateTime.fromordinal(int(day))
        # return CalendarDay(day).prepare(self)
    @classmethod
    def fromTimePeriod(cls, tp: ITimePeriod):
        self = cls()
        self.setStartDate(tp.startTime().date())
        self.setEndDate(tp.endTime().date())
        return self
    @classmethod
    def fromCalendarData(cls, cd: ICalendarData):
        self = cls()
        self.setStartDate(cd.startTime())
        self.setEndDate(cd.endTime())
        self.setData(cd)
        return self


registerAdapter(Calendar.fromTimePeriod, ITimePeriod, IAthenaRenderable)
registerAdapter(Calendar.fromCalendarData, ICalendarData, IAthenaRenderable)

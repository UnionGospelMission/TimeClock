from TimeClock.Util.DateTime import DateTime
from nevow import inevow
from nevow.context import WovenContext
from nevow.inevow import IData
from nevow.loaders import xmlfile

from .AbstractRenderer import AbstractRenderer, path


class CalendarDay(AbstractRenderer):
    def __init__(self, day: DateTime):
        self.day=day
    docFactory = xmlfile(path + "/Pages/CalendarDay.xml", "CalendarDayPattern")
    def render_day(self, ctx: WovenContext, idata: IData):
        o = []
        dateRow = inevow.IQ(ctx).patternGenerator("date")
        hourRow = inevow.IQ(ctx).patternGenerator("hour")
        o.append(dateRow(data=self.day))
        for hour in range(24):
            o.append(hourRow(data=hour))
        return o
    def render_date(self, ctx: WovenContext, data):
        pg = inevow.IQ(ctx).patternGenerator("dateCell")
        return pg(data=dict(date="%i-%i" % (data.month, data.day)))
    def render_hour(self, ctx: WovenContext, data):
        pg = inevow.IQ(ctx).patternGenerator("hourCell")
        return pg(data=dict(hour=data))

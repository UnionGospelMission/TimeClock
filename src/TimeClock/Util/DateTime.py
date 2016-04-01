import datetime
from pytz import timezone, utc
from tzlocal import get_localzone
from zope.interface import implementer

from TimeClock.ITimeClock.IDateTime import IDateTime
from TimeClock.Utils import coerce
from arrow import Arrow, get


@implementer(IDateTime)
class DateTime(Arrow):
    def date(self):
        return DateTime.fromdate(super(DateTime, self).date(), self.tzinfo)
    @classmethod
    @coerce
    def daysBetween(cls, startDate: IDateTime, endDate: IDateTime):
        d = startDate.date()
        endDate = endDate.date()
        month = None
        while d < endDate:
            if d.month != month:
                month = d.month
                yield ("New Month", month)
            yield d
            d = d.replace(days=1)
    @classmethod
    def today(cls):
        return cls.now().date()
    def nextMonth(self, *, day=None):
        if day is None:
            day = self.day
        return self.date().replace(months=1).replace(day=day)
    @classmethod
    def get(cls, expr):
        return DateTime.fromdatetime(get(expr))

    def astimezone(self, tz):
        return self.fromdatetime(super().astimezone(tz))

    def asLocalTime(self):
        return self.astimezone(get_localzone())

from zope.interface.common.idatetime import IDateTime, IDate, ITimeDelta


class IDateTime(IDateTime):
    def replace(year, years, month, months, day, days, hour, hours, minute, minutes, second, seconds, microsecond, microseconds, tzinfo):
        pass

    def daysBetween(startDate: IDateTime, endDate: IDateTime) -> [IDateTime]:
        pass

    def asLocalTime() -> IDateTime:
        pass

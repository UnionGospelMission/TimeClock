from zope.interface import Interface
from TimeClock.ITimeClock.IDateTime import ITimeDelta, IDateTime

from TimeClock.ITimeClock.IDatabase.IItem import IItem
from TimeClock.Util import fromFunction
from TimeClock.Utils import overload


class ITimePeriod(IItem):
    def startTime() -> IDateTime:
        pass

    def endTime(now: bool=True) -> IDateTime:
        pass

    @overload
    def start():
        pass

    @overload
    def start(t: float):
        pass

    @fromFunction
    @overload
    def start(t: IDateTime):
        pass

    @overload
    def end():
        pass

    @overload
    def end(t: float):
        pass

    @fromFunction
    @overload
    def end(t: IDateTime):
        pass

    def duration() -> ITimeDelta:
        pass




from zope.interface import Interface

from TimeClock.ITimeClock.IReport.IFormat import IFormat


class IFormatterFactory(Interface):
    def __call__() -> IFormat:
        pass

from zope.interface import Interface, Attribute

from TimeClock.ITimeClock.IReport import IFormat


class IReport(Interface):
    name = Attribute("name")

    def runReport(format: IFormat) -> bytes:
        pass

    def getDescription() -> str:
        pass


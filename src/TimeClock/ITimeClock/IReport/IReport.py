from zope.interface import Interface, Attribute

from TimeClock.ITimeClock.IReport.IFormat import IFormat


class IReport(Interface):
    name = Attribute("name")

    def runReport(formatter: IFormat, parameters: [object]) -> bytes:
        pass

    def getDescription() -> str:
        pass

    def getArgs() -> [str]:
        pass

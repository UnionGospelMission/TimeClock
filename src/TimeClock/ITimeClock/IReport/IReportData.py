from zope.interface import Interface


class IReportData(Interface):
    def __getitem__(self, item) -> object:
        pass

    def getColumns() -> [str]:
        pass

    def getValues() -> [object]:
        pass

    def __iter__() -> [tuple]:
        pass

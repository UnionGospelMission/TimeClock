from zope.interface import Interface


class IReportData(Interface):
    def __getitem__(i) -> object:
        pass

    def __iter__() -> [tuple]:
        pass

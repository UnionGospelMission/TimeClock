from zope.interface import Attribute

from TimeClock.ITimeClock.IDatabase.IItem import IItem


class IFile(IItem):
    path = Attribute("path")

    def open(mode: str):
        pass

    def read(size: int=None):
        pass

    def write(txt: str):
        pass

    def seek(offset: int):
        pass

    def close():
        pass

    def __enter__():
        pass

    def __exit__():
        pass

    def flush():
        pass

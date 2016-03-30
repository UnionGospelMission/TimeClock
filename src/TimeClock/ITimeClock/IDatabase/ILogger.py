from zope.interface import Attribute

from TimeClock.ITimeClock.IDatabase.IItem import IItem


class ILogger(IItem):
    name = Attribute('name')
    flags = Attribute('flags')
    file = Attribute('file')

    def log(level: int, message: str):
        pass

    def warn(message: str):
        pass

    def info(message: str):
        pass

    def debug(message: str):
        pass

    def error(message: str):
        pass

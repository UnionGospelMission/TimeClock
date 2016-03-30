from zope.interface import implementer

from TimeClock.ITimeClock.IDatabase.IEmployee import IEmployee


@implementer(IEmployee)
class EmployeeProxy(object):
    def __init__(self, user, target):
        self.__user = user
        self.__target = target
    def __getattribute__(self, item):
        if item.startswith('_'):
            return super().__getattribute__(item)
        if item in dir(self.__target):
            return getattr(self.__target, item)
        return super().__getattribute__(item)
    def __getattr__(self, item):
        return getattr(self.__target, item)

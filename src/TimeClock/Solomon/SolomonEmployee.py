from zope.interface import implementer

from TimeClock.ITimeClock.IDatabase.IEmployee import IEmployee
from TimeClock.ITimeClock.IDatabase.ISolomonEmployee import ISolomonEmployee


@implementer(ISolomonEmployee)
class SolomonEmployee(object):
    def __init__(self, employee: IEmployee):
        self.employee=employee
        self.record =

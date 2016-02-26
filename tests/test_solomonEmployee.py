from unittest import TestCase

from TimeClock.ITimeClock.IDatabase.IEmployee import IEmployee
from TimeClock.ITimeClock.ISolomonEmployee import ISolomonEmployee
from TimeClock.Util import NULL


class SolomonTester(TestCase):
    def testSEmployee(self):
        e = IEmployee(NULL)
        e.employee_id = 1001
        se = ISolomonEmployee(e)
        print(13, se.defaultArea)


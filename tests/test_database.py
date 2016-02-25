from unittest import TestCase

from zope.interface.verify import verifyClass

from TimeClock.Database import Employee, Area
from TimeClock.Database.Supervisor import Supervisor
from TimeClock.ITimeClock.IDatabase.IArea import IArea
from TimeClock.ITimeClock.IDatabase.IEmployee import IEmployee
from TimeClock.ITimeClock.IDatabase.ISupervisor import ISupervisor


class DatabaseTester(TestCase):
    def test_employee(self):
        self.assert_(verifyClass(IEmployee, Employee))
    def test_area(self):
        self.assert_(verifyClass(IArea, Area))
    def test_supervisor(self):
        self.assert_(verifyClass(ISupervisor, Supervisor))

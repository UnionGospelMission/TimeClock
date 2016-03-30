from unittest import TestCase

from zope.interface.verify import verifyClass

from TimeClock.Database import Employee, SubAccount
from TimeClock.Database.Supervisor import Supervisor
from TimeClock.ITimeClock.IDatabase.ISubAccount import ISubAccount
from TimeClock.ITimeClock.IDatabase.IEmployee import IEmployee
from TimeClock.ITimeClock.IDatabase.ISupervisor import ISupervisor


class DatabaseTester(TestCase):
    def test_employee(self):
        self.assert_(verifyClass(IEmployee, Employee))
    def test_area(self):
        self.assert_(verifyClass(ISubAccount, SubAccount))
    def test_supervisor(self):
        self.assert_(verifyClass(ISupervisor, Supervisor))

from unittest import TestCase

from zope.interface.common.idatetime import ITimeDelta
import os

from TimeClock.Database.Area import Area
from TimeClock.Database.Employee import Employee
from TimeClock.Axiom.Store import Store


from TimeClock.Exceptions import InvalidTransformation


s = Store

a = Area(store=s, name="test area")


class EmployeeTester(TestCase):
    def test_clockIn(self):
        employee = Employee(store=s)
        a.addEmployee(employee)
        employee.clockIn(a)
        with self.assertRaises(InvalidTransformation):
            employee.clockIn(a)
        employee.clockOut()

    def test_clockOut(self):
        employee = Employee(store=s)
        a.addEmployee(employee)
        with self.assertRaises(InvalidTransformation):
            employee.clockOut()
        employee.clockIn(a)
        self.assert_(ITimeDelta.providedBy(employee.clockOut().period.duration()))
#
#

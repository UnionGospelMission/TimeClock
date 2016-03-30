import os
from unittest import TestCase

from TimeClock.ITimeClock.IDatabase.IEmployee import IEmployee
from TimeClock.ITimeClock.ISolomonEmployee import ISolomonEmployee
from TimeClock.Util import NULL


e = IEmployee(NULL)
e.employee_id = 1001

if 'SOLOMONUSER' in os.environ:

    class SolomonTester(TestCase):
        def testSEmployee(self):
            se = ISolomonEmployee(e)
            self.assertEqual(se.defaultArea.name, 'General and Administrative')

        def testSEBenefits(self):
            se = ISolomonEmployee(e)
            self.assertEqual(len(se.getBenefits()), 3)


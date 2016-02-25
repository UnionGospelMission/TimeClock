from unittest import TestCase

from zope.interface.verify import verifyObject

from TimeClock.API.ConsoleAdministrator import ConsoleAdministrator
from TimeClock.Exceptions import InvalidTransformation
from TimeClock.ITimeClock.IDatabase.IAdministrator import IAdministrator
from TimeClock.ITimeClock.IDatabase.IEmployee import IEmployee
from TimeClock.ITimeClock.IDatabase.ISupervisor import ISupervisor


class ConsoleTester(TestCase):
    def test_admin(self):
        self.assert_(verifyObject(IEmployee, ConsoleAdministrator))
        self.assert_(verifyObject(ISupervisor, ConsoleAdministrator))
        self.assert_(verifyObject(IAdministrator, ConsoleAdministrator))

    def test_useAdmin(self):
        api = ConsoleAdministrator.getAPI()
        jane = api['New Employee'].execute(ConsoleAdministrator, 1,
                                           emergency_contact_name="John Doe",
                                           emergency_contact_phone="509-xxx-xxxx",
                                           active_directory_name="jane.doe",
                                           alternate_authentication=None,
                                           supervisor=None,
                               )

        john = api['New Employee'].execute(ConsoleAdministrator, 2,
                                           emergency_contact_name="Jane Doe",
                                           emergency_contact_phone="509-xxx-xxxx",
                                           active_directory_name="john.doe",
                                           alternate_authentication=None,
                                           supervisor=None,
                               )

        api['Make Supervisor'].execute(ConsoleAdministrator, jane)
        sup = ISupervisor(jane)
        sup.addEmployee(john)
        self.assertEqual(ISupervisor(jane).getEmployees(), (john,))

        with self.assertRaises(InvalidTransformation) as am:
            api.clockOut(john)

        self.assertEqual(am.exception.args[0], 'User not currently clocked in')

        area1 = api.newArea(ConsoleAdministrator, "Area 1")
        with self.assertRaises(InvalidTransformation) as am:
            api.newArea(ConsoleAdministrator, "Area 1")

        self.assertEqual(am.exception.args[0], 'Area named Area 1 already exists')

        with self.assertRaises(InvalidTransformation) as am:
             api.clockIn(john, area1)

        self.assertEqual(am.exception.args[0], 'User not authorized to work in area')

        api.addToArea(ConsoleAdministrator, john, area1)

        api.clockIn(john, area1)

        with self.assertRaises(InvalidTransformation) as am:
            api.clockIn(john, area1)

        self.assertEqual(am.exception.args[0], 'User already clocked in')

        api.clockOut(john)

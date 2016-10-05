from zope.interface import Attribute

from TimeClock.Report.IAccess.IAbstractAccessible import IAbstractAccessible


class IAEmployee(IAbstractAccessible):
    employee_id = Attribute('employee_id')
    def getSubAccounts() -> [IASubAccount]:
        pass

    def getWorkLocations() -> [IAWorkLocation]:
        pass

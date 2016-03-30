from zope.interface import Interface, Attribute

from TimeClock.ITimeClock.IDatabase.IBenefit import IBenefit


class ISolomonEmployee(Interface):
    name = Attribute("name")
    defaultSubAccount = Attribute("defaultArea")
    phone = Attribute("Phone")
    defaultWorkLocation = Attribute("defaultWorkLocation")

    def getBenefits() -> [IBenefit]:
        pass

    def getAvailableBenefits() -> dict:
        pass

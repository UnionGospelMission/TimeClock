from zope.interface import Interface, Attribute


class ISolomonEmployee(Interface):
    name = Attribute("name")
    defaultArea = Attribute("defaultArea")
    phone = Attribute("Phone")
    defaultWorkLocation = Attribute("defaultWorkLocation")


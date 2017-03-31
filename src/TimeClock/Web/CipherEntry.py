from zope.interface import Interface, Attribute, implementer

from axiom.attributes import text
from axiom.item import Item


class ICipherEntry(Interface):
    entry = Attribute("entry")


@implementer(ICipherEntry)
class CipherEntry(Item):
    entry = text()


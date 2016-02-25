from zope.interface import implementer

from TimeClock.API.AbstractAPI import AbstractAPI
from TimeClock.ITimeClock.IAPI import IAPI
from axiom.attributes import text
from axiom.item import Item


@implementer(IAPI)
class PublicAPI(AbstractAPI, Item):
    name = text()



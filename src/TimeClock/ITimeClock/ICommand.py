from zope.interface import Interface, Attribute

from TimeClock.ITimeClock.IDatabase.IPermission import IPermission
from TimeClock.Util.subclass import Subclass


class ICommand(Interface):
    name = Attribute("name")
    def hasPermission(permissions:[IPermission]) -> bool:
        pass
    def execute(caller: Subclass[Interface], *parameters:object):
        pass

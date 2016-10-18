from zope.interface import Attribute

from TimeClock.ITimeClock.ITimeDelta import ITimeDelta
from TimeClock.Report.IAccess.IAbstractAccessible import IAbstractAccessible


class IATimeEntry(IAbstractAccessible):
    startTime = Attribute("startTime")
    endTime = Attribute("endTime")
    entryType = Attribute("entryType")
    subAccount = Attribute("subAccount")
    workLocation = Attribute("workLocation")
    duration = Attribute("duration")
    approved = Attribute("approved")
    denied = Attribute("denied")

    def truncate(startTime, endTime) -> ITimeDelta:
        """
        Returns a copy of the time entry truncated to fit inside the window specified
        """

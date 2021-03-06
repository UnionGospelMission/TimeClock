from ..ITimeClock.IDateTime import IDateTime

from twisted.python.components import registerAdapter

from axiom.attributes import integer, MICRO

from ..Util.DateTime import DateTime, utc, zonename


registerAdapter(DateTime.fromtimestamp, float, IDateTime)
registerAdapter(DateTime.fromtimestamp, int, IDateTime)

EPOCH = IDateTime(0.0).astimezone(utc)


class datetime(integer):
    """
        An in-database representation of IDateTime.
        """
    def coercer(self, value):
        if value is None:
            return value
        return IDateTime(value).to(zonename)

    def infilter(self, pyval, oself, store):
        if pyval is None:
            return None
        return integer.infilter(self,
                                int((pyval - EPOCH).total_seconds() * MICRO),
                                oself,
                                store)

    def outfilter(self, dbval, oself):
        if dbval is None:
            return None
        return DateTime.fromtimestamp(dbval / MICRO).to(zonename)

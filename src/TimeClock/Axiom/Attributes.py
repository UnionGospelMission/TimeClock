from zope.interface.common.idatetime import IDateTime

from twisted.python.components import registerAdapter

from axiom.attributes import integer, MICRO

from datetime import datetime


registerAdapter(datetime.fromtimestamp, float, IDateTime)
registerAdapter(datetime.fromtimestamp, int, IDateTime)

EPOCH = IDateTime(0.0)


class datetime(integer):
    """
        An in-database representation of IDateTime.
        """
    def coercer(self, value):
        if value is None:
            return value
        return IDateTime(value)

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
        return IDateTime(dbval / MICRO)

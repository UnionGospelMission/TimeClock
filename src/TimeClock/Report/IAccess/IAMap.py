from TimeClock.Report.IAccess.IAbstractAccessible import IAbstractAccessible


class IAMap(IAbstractAccessible):
    def set(key, value):
        """
        like self[key] = value
        """

    def get(key):
        """
        like self[key]
        """

    def iter():
        """
        generator which yields (key, value) tuples
        """

    def __contains__(item):
        """
        checks if self[item] exists
        """

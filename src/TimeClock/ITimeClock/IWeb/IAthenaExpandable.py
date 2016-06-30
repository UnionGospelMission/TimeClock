from zope.interface import Interface, Attribute


class IAthenaExpandable(Interface):
    expanded = Attribute("expanded")

    def expand():
        pass

    def shrink():
        pass

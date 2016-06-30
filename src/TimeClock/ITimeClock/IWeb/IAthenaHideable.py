from zope.interface import Interface, Attribute


class IAthenaHideable(Interface):
    visible = Attribute("visible")

    def hide():
        pass

    def show():
        pass

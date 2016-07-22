class bbf:
    pass


class BoundFunction(bbf):
    def __init__(self, oself, func):
        self.oself = oself
        self.__func__ = func
    def __call__(self, *a, **kw):
        return self.__func__(self.oself, *a, **kw)
    def __repr__(self):
        return "<BoundFunction %r of %r>" % (self.__func__, self.oself)

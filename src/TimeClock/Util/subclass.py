_issubclass = issubclass

class subclass(object):
    def __init__(self, cls):
        self.cls=cls
    def __getitem__(self, item):
        return subclass(item)

Subclass = subclass(None)


def issubclass(obj, cls):
    try:
        return _issubclass(obj, cls)
    except TypeError:
        return False

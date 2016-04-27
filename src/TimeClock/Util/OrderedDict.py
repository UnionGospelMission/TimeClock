from collections import OrderedDict


class OrderedDict(OrderedDict):
    def __init__(self, *args, **kw):
        super().__init__(*args)
        keys = list(kw)
        keys.sort()
        for k in keys:
            self[k] = kw[k]

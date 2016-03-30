from TimeClock.Utils import coerce


class AbstractEvent(object):
    cancellable = True
    cancelled = False
    finished = False
    retval = True

    def __setattr__(self, key, value):
        if key == 'cancelable':
            raise TypeError("can't set attribute cancellable")
        super(AbstractEvent, self).__setattr__(key, value)

    @coerce
    def cancel(self) -> bool:
        if not self.cancellable:
            raise ValueError("event not cancellable")
        self.cancelled = True
        return self.cancelled

    @coerce
    def setReturn(self, retval: object) -> bool:
        self.retval = retval
        return True

    @coerce
    def setFinished(self, finished: bool) -> bool:
        self.finished = finished

    @coerce
    def getFinished(self) -> bool:
        return self.finished

    def getReturn(self) -> object:
        return self.retval

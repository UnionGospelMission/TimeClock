from twisted.internet.defer import Deferred

from twisted.internet import reactor

class IterateInReactor(Deferred):
    def __init__(self, iterator, delay=0):
        super().__init__()
        self.iterator = iter(iterator)
        self.output = []
        self.delay = delay
        reactor.callLater(delay, self.iterate)

    def iterate(self):
        sigil = object()
        n = next(self.iterator, sigil)
        if n is not sigil:
            self.output.append(n)
            reactor.callLater(self.delay, self.iterate)
        else:
            self.callback(self.output)

from axiom.scripts import axiomatic

class alwaysEqual(object):
    __hash__=object.__hash__
    def __eq__(self, other):
        return True
    def __len__(self):
        o=axiomatic.Options()
        o.parseOptions()

class Ignore(object):
    def parseOptions(self, *_):
        pass

class Options(axiomatic.Options):
    subCommands = ((alwaysEqual(), None, Ignore, ""),)


o=Options()
o.parseOptions()


def run(argv=None):
    o1 = axiomatic.Options()
    o1.store = o.getStore()
    try:
        o1.parseOptions(argv)
    except axiomatic.usage.UsageError as e:
        raise SystemExit(str(e))

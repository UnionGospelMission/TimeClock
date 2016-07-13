import sys
from axiom.scripts import axiomatic


class alwaysEqual(object):
    __hash__ = object.__hash__
    def __eq__(self, other):
        return True
    def __len__(self):
        return 1


class Ignore(object):
    def parseOptions(self, *_):
        pass


class Options(axiomatic.Options):
    subCommands = ((alwaysEqual(), None, Ignore, ""),)


if '--help' not in sys.argv and '-h' not in sys.argv:
    o = Options()
    o.parseOptions()
else:
    axiomatic.Options().parseOptions()


def run(argv=None):
    o1 = axiomatic.Options()
    o1.store = o.getStore()
    try:
        o1.parseOptions(argv)
    except axiomatic.usage.UsageError as e:
        raise SystemExit(str(e))

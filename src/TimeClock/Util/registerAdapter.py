import twisted.python.components


def adapter(original, target):
    def doRegister(cls):
        twisted.python.components.registerAdapter(cls, original, target)
        return cls
    return doRegister

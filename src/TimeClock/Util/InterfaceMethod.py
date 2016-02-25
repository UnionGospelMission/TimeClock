from zope.interface.exceptions import BrokenImplementation
from zope.interface.interface import Method


class AnnotatedMethod(Method):
    def __init__(self, func, interface=None, imlevel=0, name=None):
        self.annotations = func.__annotations__
        self.__name__ = self.name = name = name or func.__name__
        self.defaults = getattr(func, '__defaults__', None) or ()
        code = func.__code__
        # Number of positional arguments
        na = code.co_argcount - imlevel
        names = code.co_varnames[imlevel:]
        opt = {}
        # Number of required arguments
        nr = na - len(self.defaults)
        if nr < 0:
            self.defaults = self.defaults[-nr:]
            nr = 0

        # Determine the optional arguments.
        opt.update(dict(zip(names[nr:], self.defaults)))

        self.positional = names[:na]
        self.required = names[:nr]
        self.optional = opt

        argno = na

        # Determine the function's variable argument's name (i.e. *args)
        if code.co_flags & 0x04:
            self.varargs = names[argno]
            argno = argno + 1
        else:
            self.varargs = None

        # Determine the function's keyword argument's name (i.e. **kw)
        if code.co_flags & 0x08:
            self.kwargs = names[argno]
        else:
            self.kwargs = None

        self.interface = interface

        for key, value in func.__dict__.items():
            self.setTaggedValue(key, value)


    def __call__(self, *args, **kw):
        raise BrokenImplementation(self.interface, self.__name__)

    def getSignatureInfo(self):
        return {'positional': self.positional,
                'required': self.required,
                'optional': self.optional,
                'varargs': self.varargs,
                'kwargs': self.kwargs,
                'annotations': self.annotations
                }

    def getSignatureString(self):
        sig = []
        for v in self.positional:
            sig.append(v)
            if v in self.optional.keys():
                sig[-1] += "=" + repr(self.optional[v])
        if self.varargs:
            sig.append("*" + self.varargs)
        if self.kwargs:
            sig.append("**" + self.kwargs)

        return "(%s)" % ", ".join(sig)


class OverloadedMethod(Method):
    def __init__(self, overloader, interface=None, imlevel=0, name=None):
        self.annotations = [func.__annotations__ for func in overloader.functions]
        self.__name__ = self.name = name = name or overloader.__name__
        self.defaults = [getattr(func, '__defaults__', None) or () for func in overloader.functions]
        self.positional = []
        self.required = []
        self.optional = []
        self.varargs = []
        self.kwargs = []
        for idx, func in enumerate(overloader.functions):
            code = func.__code__
            # Number of positional arguments
            na = code.co_argcount - imlevel
            names = code.co_varnames[imlevel:]
            opt = {}
            # Number of required arguments
            nr = na - len(self.defaults)
            if nr < 0:
                self.defaults[idx] = self.defaults[idx][-nr:]
                nr = 0

            # Determine the optional arguments.
            opt.update(dict(zip(names[nr:], self.defaults)))

            self.positional.append(names[:na])
            self.required.append(names[:nr])
            self.optional.append(opt)

            argno = na

            # Determine the function's variable argument's name (i.e. *args)
            if code.co_flags & 0x04:
                self.varargs.append(names[argno])
                argno = argno + 1
            else:
                self.varargs.append(None)

        # Determine the function's keyword argument's name (i.e. **kw)
            if code.co_flags & 0x08:
                self.kwargs.append(names[argno])
            else:
                self.kwargs.append(None)

        self.interface = interface

        for key, value in func.__dict__.items():
            self.setTaggedValue(key, value)


    def __call__(self, *args, **kw):
        raise BrokenImplementation(self.interface, self.__name__)

    def getSignatureInfo(self):
        return {'positional': self.positional,
                'required': self.required,
                'optional': self.optional,
                'varargs': self.varargs,
                'kwargs': self.kwargs,
                'annotations': self.annotations,
                'overloaded': True
                }

    def getSignatureString(self):
        out = []
        for idx, each in enumerate(self.positional):
            sig = []
            for v in each:
                sig.append(v)
                if v in self.optional[idx].keys():
                    sig[-1] += "=" + repr(self.optional[idx][v])
            if self.varargs[idx]:
                sig.append("*" + self.varargs[idx])
            if self.kwargs[idx]:
                sig.append("**" + self.kwargs[idx])

            out.append("(%s)" % ", ".join(sig))
        return '\n'.join(out)



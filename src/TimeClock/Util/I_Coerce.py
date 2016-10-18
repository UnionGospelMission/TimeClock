from collections import OrderedDict

from zope.interface import Interface
from zope.interface.verify import verifyObject

from TimeClock.Util.BoundFunction import BoundFunction
from TimeClock.Util.Default import Defalt
from TimeClock.Util.needs_coercing import needs_coercing
from .subclass import issubclass


class I_Coercer(object):
    def __init__(self, func):
        self.func = func
        self.varargs = bool(self.func.__code__.co_flags & 0x04)
        self.kwargs = bool(self.func.__code__.co_flags & 0x08)
        self.__annotations__ = func.__annotations__

    def __get__(self, instance, _):
        return BoundFunction(instance, self)

    def __call__(self, *a, **kw):
        null = object()
        varargs = []
        if self.kwargs:
            varkwarg = self.func.__code__.co_varnames[self.func.__code__.co_argcount +
                                                      self.varargs + self.func.__code__.co_kwonlyargcount]
        else:
            varkwarg = None
        varkwargs = {}
        params = self.func.__code__.co_varnames[:self.func.__code__.co_argcount]
        dft = self.func.__defaults__ or ()
        num_defaults = len(dft)
        defaults = {params[self.func.__code__.co_argcount - num_defaults + idx]: Defalt(i) for idx, i in enumerate(dft)}
        args = OrderedDict()
        for i in range(self.func.__code__.co_argcount):
            args[params[i]] = defaults.get(params[i], null)

        kwonly = self.func.__code__.co_varnames[self.func.__code__.co_argcount:
                                                self.func.__code__.co_argcount + self.func.__code__.co_kwonlyargcount]
        kwargs = {k:Defalt(v) for k,v in (self.func.__kwdefaults__ or {}).items()}

        for idx, i in enumerate(a):
            if idx < len(params):
                args[params[idx]] = i
            elif self.varargs:
                varargs.append(i)
            else:
                raise TypeError("%r takes %i positional argument%s but %i %s given" %
                                (self, len(args), "s" if len(args) != 1 else "", len(a), "was" if len(a)==1 else "were"))
        for key, value in kw.items():
            if key in args:
                if args[key] == null or isinstance(args[key], Defalt):
                    args[key] = value
                else:
                    raise TypeError("%r got multiple values for argument %s" % (self, key))
            elif key in kwonly:
                if key in kwargs:
                    if not isinstance(kwargs[key], Defalt):
                        raise TypeError("%r got multiple values for argument %s" % (self, key))
                kwargs[key] = value
            elif self.kwargs:
                if key in kwargs or key in varkwargs:
                    raise TypeError("%r got multiple values for argument %s" % (self, key))
                varkwargs[key] = value
            else:
                raise TypeError("%r got an unexpected keyword argument %s" % (self, key))
        kwargs = {k:(v.obj if isinstance(v, Defalt) else v) for k,v in kwargs.items()}
        annotations = self.func.__annotations__
        for label in self.func.__annotations__:
            if label == 'return':
                continue
            if label in args:
                if isinstance(args[label], Defalt):
                    args[label] = args[label].obj
                if args[label] is None:
                    continue
                if isinstance(annotations[label], (list,tuple)):
                    typ = type(annotations[label])
                    newarg = []
                    for a in args[label]:
                        if needs_coercing(a, annotations[label][0]):
                            o = annotations[label][0](a)
                        else:
                            o = a
                        if issubclass(annotations[label], Interface):
                            verifyObject(annotations[label], o)
                        newarg.append(o)
                    args[label] = typ(newarg)
                else:
                    if needs_coercing(args[label], annotations[label]):
                        args[label] = annotations[label](args[label])
                    if issubclass(annotations[label], Interface):
                        verifyObject(annotations[label], args[label])
            elif label in kwargs:
                if isinstance(kwargs[label], Defalt):
                    kwargs[label] = kwargs[label].obj
                if kwargs[label] is None:
                    continue
                if needs_coercing(kwargs[label], annotations[label]):
                    kwargs[label] = annotations[label](kwargs[label])
                if issubclass(annotations[label], Interface):
                    verifyObject(annotations[label], kwargs[label])
            elif label == varkwarg:
                for k, v in varkwargs.items():
                    if needs_coercing(v, annotations[label]):
                        varkwargs[k] = annotations[label](v)
            elif self.varargs and label == self.func.__code__.co_varnames[
                    self.func.__code__.co_argcount + self.func.__code__.co_kwonlyargcount]:
                new_varargs = []
                for va in varargs:
                    if needs_coercing(va, annotations[label]):
                        new_varargs.append(annotations[label](va))
                    else:
                        new_varargs.append(va)
                    if issubclass(annotations[label], Interface):
                        verifyObject(annotations[label], va)
                varargs = new_varargs
            else:
                raise TypeError("%r could not coerce %s to %r" % (self, label, annotations[label]))
        retval = self.func(*[(i if not isinstance(i, Defalt) else i.obj)
                             for i in args.values() if i is not null], *varargs, **kwargs, **varkwargs)
        if retval is None:
            yield retval
        else:
            if 'return' in annotations:
                rvt = annotations['return']
                for rv in retval:
                    if needs_coercing(rv, rvt):
                        rv = rvt(rv)
                    if issubclass(rvt, Interface):
                        verifyObject(rvt, rv)
                    yield rv

    def __repr__(self):
        return repr(self.func)

from collections import defaultdict, OrderedDict

from zope.interface import Interface
from zope.interface.exceptions import BrokenImplementation, BrokenMethodImplementation, DoesNotImplement
from zope.interface.interface import Attribute
from zope.interface.verify import verifyObject

from .BoundFunction import BoundFunction
from .Default import Defalt
from .needs_coercing import needs_coercing


class Overloader(Attribute):
    def __new__(cls):
        import inspect
        frame = inspect.currentframe()
        fback = inspect.getouterframes(frame)[2][0]
        flocals = fback.f_locals
        if '__overloader__' not in flocals:
            flocals['__overloader__'] = object.__new__(cls)
        return flocals['__overloader__']

    def __init__(self):
        self.__name__='overloader'
        if not hasattr(self, 'functions'):
            self.functions = defaultdict(Overloaded)

    def add(self, func):
        return self.functions[func.__name__].add(func)


class Overloaded(object):
    def __init__(self):
        self.__name__ = 'undefined'
        self.functions = []
    def __repr__(self):
        return '<OverloadedFunction %r>' % self.functions[0]
    def add(self, func):
        self.functions.append(func)
        self.__name__ = func.__name__
        return self
    def __get__(self, instance, _):
        return BoundFunction(instance, self)
    def __call__(self, *args, **kwargs):
        for func in self.functions:
            can_call, func, a, kw = self.prepareCall(func, False, *args, **kwargs)
            if can_call:
                return self.doCall(func, *a, **kw)
        for func in self.functions:
            can_call, func, a, kw = self.prepareCall(func, True, *args, **kwargs)
            if can_call:
                return self.doCall(func, *a, **kw)
        raise TypeError("%s() has no implementations matching arguments %r, %r" % (self.__name__, args, kwargs))
    def prepareCall(self, func, should_coerce, *a, **kw):

        is_varargs = bool(func.__code__.co_flags & 0x04)
        is_kwargs = bool(func.__code__.co_flags & 0x08)

        if is_kwargs:
            varkwarg = func.__code__.co_varnames[
                func.__code__.co_argcount + is_varargs + func.__code__.co_kwonlyargcount]
        else:
            varkwarg = None
        varkwargs = {}

        null = object()
        varargs = []
        params = func.__code__.co_varnames[:func.__code__.co_argcount + func.__code__.co_kwonlyargcount]
        dft = func.__defaults__ or ()
        num_defaults = len(dft)
        defaults = {params[func.__code__.co_argcount - num_defaults + idx]: Defalt(i) for idx, i in enumerate(dft)}
        args = OrderedDict()
        for i in range(func.__code__.co_argcount):
            args[params[i]] = defaults.get(params[i], null)

        kwonly = func.__code__.co_varnames[func.__code__.co_argcount:
                                           func.__code__.co_argcount + func.__code__.co_kwonlyargcount]
        kwargs = {k: (v.obj if isinstance(v, Defalt) else v) for k, v in (func.__kwdefaults__ or {}).items()}
        for idx, i in enumerate(a):
            if idx < len(params):
                args[params[idx]] = i
            elif is_varargs:
                varargs.append(i)
            else:
                return False, None, None, None
        for key, value in kw.items():
            if key in args:
                if args[key] == null or isinstance(args[key], Defalt):
                    args[key] = value
                else:
                    return False, None, None, None
            elif key in kwonly:
                if key in kwargs:
                    if not isinstance(kwargs[key], Defalt):
                        return False, None, None, None
                kwargs[key] = value
            elif is_kwargs:
                if key in kwargs:
                    return False, None, None, None
                if key in varkwargs:
                    return False, None, None, None
                varkwargs[key] = value
            else:
                return False, None, None, None
        kwargs = {k: (v.obj if isinstance(v, Defalt) else v) for k, v in kwargs.items()}
        annotations = func.__annotations__
        for label in func.__annotations__:
            if label == 'return':
                continue
            if label in args:
                if isinstance(args[label], Defalt):
                    args[label] = args[label].obj
                if needs_coercing(args[label], annotations[label]):
                    if not should_coerce:
                        return False, None, None, None
                    try:
                        args[label] = annotations[label](args[label])
                    except TypeError:
                        return False, None, None, None
                if isinstance(annotations[label], list):
                    if issubclass(annotations[label][0], Interface):
                        for v in args[label]:
                            try:
                                verifyObject(annotations[label][0], v)
                            except BrokenImplementation:
                                return False, None, None, None
                            except BrokenMethodImplementation:
                                return False, None, None, None
                elif issubclass(annotations[label], Interface):
                    try:
                        verifyObject(annotations[label], args[label])
                    except BrokenImplementation:
                        return False, None, None, None
                    except BrokenMethodImplementation:
                        return False, None, None, None
                    except DoesNotImplement:
                        return False, None, None, None
            elif label in kwargs:
                if isinstance(kwargs[label], Defalt):
                    kwargs[label] = kwargs[label].obj
                if needs_coercing(kwargs[label], annotations[label]):
                    if not should_coerce:
                        return False, None, None, None
                    kwargs[label] = annotations[label](kwargs[label])
                if issubclass(annotations[label], Interface):
                    try:
                        verifyObject(annotations[label], kwargs[label])
                    except BrokenImplementation:
                        return False, None, None, None
                    except BrokenMethodImplementation:
                        return False, None, None, None
                    except DoesNotImplement:
                        return False, None, None, None
            elif label == varkwarg:
                for k, v in varkwargs.items():
                    if needs_coercing(v, annotations[label]):
                        varkwargs[k] = annotations[label](v)

            elif is_varargs and label == func.__code__.co_varnames[func.__code__.co_argcount]:
                new_varargs = []
                for va in varargs:
                    if needs_coercing(va, annotations[label]):
                        if not should_coerce:
                            return False, None, None, None
                        new_varargs.append(annotations[label](va))
                    else:
                        new_varargs.append(va)
                    if issubclass(annotations[label], Interface):
                        try:
                            verifyObject(annotations[label], va)
                        except BrokenImplementation:
                            return False, None, None, None
                        except BrokenMethodImplementation:
                            return False, None, None, None
                        except DoesNotImplement:
                            return False, None, None, None
                varargs = new_varargs
            else:
                return False, None, None, None
        kwargs.update(varkwargs)
        return True, func, [(i if not isinstance(i, Defalt) else i.obj)
                            for i in args.values() if i is not null] + varargs, kwargs
    def doCall(self, func, *args, **kwargs):
        retval = func(*args, **kwargs)
        if 'return' in func.__annotations__:
            rettyp = func.__annotations__['return']
            if isinstance(rettyp, (list, tuple)):
                typ = type(rettyp)
                out = []
                for i in retval:
                    if needs_coercing(i, rettyp[0]):
                        o = (rettyp[0](i))
                    else:
                        o = (i)
                    if issubclass(rettyp[0], Interface):
                        verifyObject(rettyp[0], o)
                    out.append(o)
                return typ(out)

            elif needs_coercing(retval, func.__annotations__['return']):
                retval = func.__annotations__['return'](retval)
            if retval is None:
                return retval
            if issubclass(rettyp, Interface):
                verifyObject(func.__annotations__['return'], retval)
        return retval




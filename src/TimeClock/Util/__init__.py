from types import MethodType

from zope.interface import Interface
from zope.interface.interface import fromFunction as _fromFunction
from zope.interface.verify import _incompat
import zope.interface.interface
import zope.interface.verify

from TimeClock.Axiom.Store import Store
from .BoundFunction import BoundFunction
from .Coerce import Coercer
from .InterfaceMethod import OverloadedMethod, AnnotatedMethod
from .Overload import Overloaded
from .subclass import issubclass


def getSignatureString(positional, optional, varargs, kwargs, annotations = None, **kw):
    if isinstance(positional, tuple):
        positional = [positional]
        optional = [optional]
        varargs = [varargs]
        kwargs = [kwargs]
        annotations = [annotations] if annotations else [{}]
    out = []
    for idx, each in enumerate(positional):
        sig = []
        for v in each:
            sig.append(v)
            if annotations and v in annotations[idx]:
                sig[-1] +=":"+str(annotations[idx][v])
            if v in optional[idx].keys():
                sig[-1] += "=" + repr(optional[idx][v])
        if varargs[idx]:
            sig.append("*" + varargs[idx])
            if annotations and varargs[idx] in annotations[idx]:
                sig[-1] += ":" + str(annotations[idx][varargs[idx]])
        if kwargs[idx]:
            sig.append("**" + kwargs[idx])
        out.append("(%s)" % ", ".join(sig))
        if annotations and 'return' in annotations[idx]:
            out[-1]+=' -> '+str(annotations[idx]['return'])
    return '\n'.join(out)


def fromFunction(func, interface=None, imlevel=0, name=None):
    if isinstance(func, BoundFunction):
        func = func.__func__
        imlevel = 1
    if isinstance(func, Overloaded):
        return OverloadedMethod(func, interface, imlevel, name)
    if isinstance(func,Coercer):
        func = func.func
    if func.__annotations__:
        return AnnotatedMethod(func, interface, imlevel, name)
    return _fromFunction(func, interface, imlevel, name)


def fromMethod(meth, interface=None, name=None):
    if isinstance(meth, (MethodType, BoundFunction)):
        func = meth.__func__
    else:
        func = meth
    return fromFunction(func, interface, 1, name)


def incompat(required, implemented):
    if 'overloaded' in required:
        for idx, annotations in enumerate(required['annotations']):
            positional = required['positional'][idx]
            required_ = required['required'][idx]
            optional = required['optional'][idx]
            varargs = required['varargs'][idx]
            kwargs = required['kwargs'][idx]
            r = incompat(dict(positional=positional, required=required_, optional=optional, varargs=varargs, kwargs=kwargs), implemented)
            if r:
                return r
        return None
    if 'overloaded' in implemented:
        for idx, annotations in enumerate(implemented['annotations']):
            positional = implemented['positional'][idx]
            required_ = implemented['required'][idx]
            optional = implemented['optional'][idx]
            varargs = implemented['varargs'][idx]
            kwargs = implemented['kwargs'][idx]
            r = incompat(
                required,
                dict(positional=positional, required=required_, optional=optional, varargs=varargs, kwargs=kwargs, annotations=annotations)
                )
            if not r:
                return None
        return "overloaded implementation does not provide function matching signature(s) \n%s" %(getSignatureString(**required))
    r = _incompat(required, implemented)
    if r:
        return r
    if 'annotations' in required:
        if not 'annotations' in implemented:
            return 'implementation is not annotated'
        for a in required['annotations']:
            if a not in implemented['annotations']:
                return 'implementation is missing formal parameter named %s' %a
            required_type = required['annotations'][a]
            implemented_type = implemented['annotations'][a]
            if required_type == implemented_type:
                continue
            if issubclass(required_type, implemented_type):
                continue
            if issubclass(implemented_type, Interface):
                if implemented_type.providedBy(required_type):
                    continue
                if implemented_type.implementedBy(required_type):
                    continue
            return 'implementation formal parameter named %s is not the required type' %a


zope.interface.verify._incompat = incompat
zope.interface.verify.FunctionType = (zope.interface.verify.FunctionType, Overloaded, Coercer, OverloadedMethod, BoundFunction)
zope.interface.verify.fromFunction = fromFunction
zope.interface.verify.fromMethod = fromMethod
zope.interface.interface.fromFunction = fromFunction
zope.interface.interface.fromMethod = fromMethod


class Null(object):
    ifaces={

    }
    def __repr__(self):
        return "<NULL>"
    def __conform__(self, iface):
        if iface in self.ifaces:
            return self.ifaces[iface](store=Store)

NULL=Null()

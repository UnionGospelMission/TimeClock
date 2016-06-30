import types
from dis import opmap, HAVE_ARGUMENT


class ByteCodeManager(object):
    def __getattr__(self, attr):
        r = opmap[attr]
        if r >= HAVE_ARGUMENT:
            return lambda y: [r, y % 256, y // 256]
        return lambda: [r]
    def toBytes(self, lst):
        o = []
        for i in lst:
            o.extend(i)
        return bytes(o)

bcm = ByteCodeManager()


def Transaction(func):
    from . import Store
    c = func.__code__
    bytecode = [
        bcm.LOAD_GLOBAL(0),
        bcm.LOAD_ATTR(0),
        bcm.LOAD_ATTR(1),
        bcm.LOAD_GLOBAL(2),
    ]

    for idx in range(c.co_argcount):
        bytecode.append(bcm.LOAD_FAST(idx))
    for idx in range(c.co_kwonlyargcount):
        bytecode.append(bcm.LOAD_CONST(idx + c.co_argcount))
        bytecode.append(bcm.LOAD_FAST(idx + c.co_argcount))
    if c.co_flags & 0x04 and c.co_flags & 0x08:
        bytecode.append(bcm.CALL_FUNCTION_VAR_KW(c.co_argcount + 1 + 256 * c.co_kwonlyargcount))
    elif c.co_flags & 0x04:
        bytecode.append(bcm.CALL_FUNCTION_VAR(c.co_argcount + 1 + 256 * c.co_kwonlyargcount))
    elif c.co_flags & 0x08:
        bytecode.append(bcm.CALL_FUNCTION_KW(c.co_argcount + 1 + 256 * c.co_kwonlyargcount))
    else:
        bytecode.append(bcm.CALL_FUNCTION(c.co_argcount + 1 + 256 * c.co_kwonlyargcount))

    bytecode.append(bcm.RETURN_VALUE())

    varnames = c.co_varnames
    names = ('Store', 'transact', 'func')
    lnotab = bytearray([
        0, 3,
        3, 1,
        3, 1,
        3, 1,
        3, 4,
        3 * c.co_argcount, 2,
        3 * c.co_kwonlyargcount, 1,
        3 * c.co_kwonlyargcount, 2,
        3, 8,
        1, 2
    ])

    return types.FunctionType(
        types.CodeType(
            c.co_argcount,
            c.co_kwonlyargcount,
            c.co_nlocals,
            c.co_stacksize + 2,
            c.co_flags,
            bcm.toBytes(bytecode),
            varnames,
            names,
            varnames,
            c.co_filename + ' -> %s:%i' % (__file__, 21),
            c.co_name,
            21,
            bytes(lnotab),
        ),
        {'Store': Store, 'func': func},
        c.co_name,
        (),
    )

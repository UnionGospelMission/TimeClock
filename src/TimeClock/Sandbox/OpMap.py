from .Function import Function
from .Sandbox import Sandbox
from operator import lt, gt, eq, le, ge, ne, is_, is_not, contains
cmp_map = [lt, le, eq, ne, gt, ge, contains, lambda x, y: not contains(x, y), is_, is_not]


class OpMap(object):
    NORETURN = object()
    @staticmethod
    def getOp(opname):
        return getattr(OpMap, opname)
    @staticmethod
    def POP_TOP(sandbox: Sandbox, args: list):
        sandbox.stack.get()
        return OpMap.NORETURN
    @staticmethod
    def ROT_TWO(sandbox: Sandbox, args: list):
        sandbox.stack[-1], sandbox.stack[-2] = sandbox.stack[-2], sandbox.stack.queue[-1]
        return OpMap.NORETURN
    @staticmethod
    def ROT_THREE(sandbox: Sandbox, args: list):
        a = sandbox.stack[-3:]
        a.insert(-3, a.get(-1))
        sandbox.stack[-3:] = a
        return OpMap.NORETURN
    @staticmethod
    def DUP_TOP(sandbox: Sandbox, args: list):
        sandbox.stack.put(sandbox.stack[-1])
        return OpMap.NORETURN

    @staticmethod
    def UNARY_NEGATIVE(sandbox: Sandbox, args: list):
        sandbox.stack[-1] = - sandbox.stack[-1]
        return OpMap.NORETURN

    @staticmethod
    def UNARY_NOT(sandbox: Sandbox, args: list):
        sandbox.stack[-1] = not sandbox.stack[-1]
        return OpMap.NORETURN

    @staticmethod
    def UNARY_INVERT(sandbox: Sandbox, args: list):
        sandbox.stack[-1] = ~ sandbox.stack[-1]
        return OpMap.NORETURN

    @staticmethod
    def BINARY_POWER(sandbox: Sandbox, args: list):
        a = sandbox.stack.get()
        b = sandbox.stack.get()
        if a > 1000000:
            raise TypeError("Mantissa above 1000000 not allowed")
        sandbox.stack.put(b**a)
        return OpMap.NORETURN

    @staticmethod
    def BINARY_MULTIPLY(sandbox: Sandbox, args: list):
        a = sandbox.stack.get()
        b = sandbox.stack.get()
        sandbox.stack.put(b*a)
        return OpMap.NORETURN

    @staticmethod
    def BINARY_MATRIX_MULTIPLY(sandbox: Sandbox, args: list):
        a = sandbox.stack.get()
        b = sandbox.stack.get()
        sandbox.stack.put(b @ a)
        return OpMap.NORETURN

    @staticmethod
    def BINARY_FLOOR_DIVIDE(sandbox: Sandbox, args: list):
        a = sandbox.stack.get()
        b = sandbox.stack.get()
        sandbox.stack.put(b // a)
        return OpMap.NORETURN

    @staticmethod
    def BINARY_TRUE_DIVIDE(sandbox: Sandbox, args: list):
        a = sandbox.stack.get()
        b = sandbox.stack.get()
        sandbox.stack.put(b / a)
        return OpMap.NORETURN

    @staticmethod
    def BINARY_MODULO(sandbox: Sandbox, args: list):
        a = sandbox.stack.get()
        b = sandbox.stack.get()
        sandbox.stack.put(b % a)
        return OpMap.NORETURN

    @staticmethod
    def BINARY_ADD(sandbox: Sandbox, args: list):
        a = sandbox.stack.get()
        b = sandbox.stack.get()
        sandbox.stack.put(b + a)
        return OpMap.NORETURN

    @staticmethod
    def BINARY_SUBTRACT(sandbox: Sandbox, args: list):
        a = sandbox.stack.get()
        b = sandbox.stack.get()
        sandbox.stack.put(b - a)
        return OpMap.NORETURN

    @staticmethod
    def BINARY_SUBSCR(sandbox: Sandbox, args: list):
        a = sandbox.stack.get()
        b = sandbox.stack.get()
        sandbox.stack.put(b[a])
        return OpMap.NORETURN

    @staticmethod
    def LOAD_NAME(sandbox: Sandbox, args: list):
        name_idx = args[0] + args[1] * 256
        name = sandbox.function.names[name_idx]
        sandbox.stack.put(sandbox.loadName(name))
        return OpMap.NORETURN

    @staticmethod
    def LOAD_FAST(sandbox: Sandbox, args: list):
        name_idx = args[0] + args[1] * 256
        name = sandbox.function.varnames[name_idx]
        sandbox.stack.put(sandbox.loadName(name))
        return OpMap.NORETURN

    @staticmethod
    def STORE_NAME(sandbox: Sandbox, args: list):
        name_idx = args[0] + args[1] * 256
        name = sandbox.function.names[name_idx]
        sandbox.storeName(name, sandbox.stack.get())
        return OpMap.NORETURN

    @staticmethod
    def CALL_FUNCTION(sandbox: Sandbox, args: list):
        argc = args[0]
        argk = args[1]
        kargs = {}
        for idx in range(argk):
            val = sandbox.stack.get()
            key = sandbox.stack.get()
            kargs[key] = val
        args = []
        for idx in range(argc):
            args.insert(0, sandbox.stack.get())
        function = sandbox.stack.get()
        sandbox.stack.put(sandbox.callFunction(function, args, kargs))
        return OpMap.NORETURN

    @staticmethod
    def LOAD_CONST(sandbox: Sandbox, args: list):
        const_idx = args[0] + args[1] * 256
        sandbox.stack.put(sandbox.function.constants[const_idx])
        return OpMap.NORETURN

    @staticmethod
    def MAKE_FUNCTION(sandbox: Sandbox, args: list):
        argc = args[0]+args[1]*256
        if argc!=0:
            raise TypeError("Annotations and default arguments are not supported")
        name = sandbox.stack.get()
        code = sandbox.stack.get()
        args = code.co_varnames[:code.co_argcount]
        function = Function(name, code, args, sandbox)
        sandbox.stack.put(function)
        return OpMap.NORETURN

    @staticmethod
    def RETURN_VALUE(sandbox: Sandbox, args: list):
        return sandbox.stack.get()

    @staticmethod
    def LOAD_ATTR(sandbox: Sandbox, args: list):
        namei = args[0] + args[1] * 256
        name = sandbox.function.names[namei]
        tos = sandbox.stack.get()
        sandbox.stack.put(sandbox.getAttr(tos, name))
        return OpMap.NORETURN

    @staticmethod
    def BUILD_LIST(sandbox: Sandbox, args: list):
        count = args[0] + args[1]*256
        o = sandbox.stack[-count:]
        sandbox.stack[-count:] = [o]
        return OpMap.NORETURN

    @staticmethod
    def BUILD_MAP(sandbox: Sandbox, args: list):
        count = args[0] + args[1] * 256
        o = {}
        for idx in range(count):
            val = sandbox.stack.get()
            o[sandbox.stack.get()] = val
        sandbox.stack.put(o)
        return OpMap.NORETURN

    @staticmethod
    def SETUP_LOOP(sandbox: Sandbox, args: list):
        delta = args[0] + args[1] * 256
        sandbox.blocks.put(sandbox.function[sandbox.index:sandbox.index + delta])
        return OpMap.NORETURN

    @staticmethod
    def GET_ITER(sandbox: Sandbox, args: list):
        sandbox.stack[-1]=iter(sandbox.stack[-1])
        return OpMap.NORETURN

    @staticmethod
    def FOR_ITER(sandbox: Sandbox, args: list):
        delta = args[0] + args[1] * 256
        sigil = object()
        n = next(sandbox.stack[-1], sigil)
        if n is sigil:
            sandbox.stack.get()
            sandbox.index+=delta
        else:
            sandbox.stack.put(n)
        return OpMap.NORETURN

    @staticmethod
    def JUMP_ABSOLUTE(sandbox: Sandbox, args: list):
        idx = args[0] + args[1] * 256
        sandbox.index = idx
        return OpMap.NORETURN

    @staticmethod
    def POP_BLOCK(sandbox: Sandbox, args: list):
        sandbox.blocks.get()
        return OpMap.NORETURN

    @staticmethod
    def COMPARE_OP(sandbox: Sandbox, args: list):
        op = args[0] + args[1] * 256
        operator = cmp_map[op]
        tos = sandbox.stack.get()
        tos1 = sandbox.stack.get()
        v = operator(tos1, tos)
        sandbox.stack.put(v)
        return OpMap.NORETURN

    @staticmethod
    def POP_JUMP_IF_FALSE(sandbox: Sandbox, args: list):
        target = args[0] + args[1] * 256
        tos = sandbox.stack.get()
        if not tos:
            sandbox.index = target
        return OpMap.NORETURN

    @staticmethod
    def POP_JUMP_IF_TRUE(sandbox: Sandbox, args: list):
        target = args[0] + args[1] * 256
        tos = sandbox.stack.get()
        if tos:
            sandbox.index = target
        return OpMap.NORETURN

    @staticmethod
    def JUMP_IF_TRUE_OR_POP(sandbox: Sandbox, args: list):
        target = args[0] + args[1] * 256
        if sandbox.stack[-1]:
            sandbox.index = target
        else:
            sandbox.stack.get()
        return OpMap.NORETURN

    @staticmethod
    def JUMP_IF_FALSE_OR_POP(sandbox: Sandbox, args: list):
        target = args[0] + args[1] * 256
        if not sandbox.stack[-1]:
            sandbox.index = target
        else:
            sandbox.stack.get()
        return OpMap.NORETURN

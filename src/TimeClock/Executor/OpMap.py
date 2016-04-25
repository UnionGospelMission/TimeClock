from .Function import Function
from .Executor import Executor
from operator import lt, gt, eq, le, ge, ne, is_, is_not, contains
cmp_map = [lt, le, eq, ne, gt, ge, contains, lambda x, y: not contains(x, y), is_, is_not]


class OpMap(object):
    NORETURN = object()
    @staticmethod
    def getOp(opname):
        return getattr(OpMap, opname)
    @staticmethod
    def POP_TOP(executor: Executor, args: list):
        executor.stack.get()
        return OpMap.NORETURN
    @staticmethod
    def ROT_TWO(executor: Executor, args: list):
        executor.stack[-1], executor.stack[-2] = executor.stack[-2], executor.stack.queue[-1]
        return OpMap.NORETURN
    @staticmethod
    def ROT_THREE(executor: Executor, args: list):
        a = executor.stack[-3:]
        a.insert(-3, a.get(-1))
        executor.stack[-3:] = a
        return OpMap.NORETURN
    @staticmethod
    def DUP_TOP(executor: Executor, args: list):
        executor.stack.put(executor.stack[-1])
        return OpMap.NORETURN

    @staticmethod
    def UNARY_NEGATIVE(executor: Executor, args: list):
        executor.stack[-1] = - executor.stack[-1]
        return OpMap.NORETURN

    @staticmethod
    def UNARY_NOT(executor: Executor, args: list):
        executor.stack[-1] = not executor.stack[-1]
        return OpMap.NORETURN

    @staticmethod
    def UNARY_INVERT(executor: Executor, args: list):
        executor.stack[-1] = ~ executor.stack[-1]
        return OpMap.NORETURN

    @staticmethod
    def BINARY_POWER(executor: Executor, args: list):
        a = executor.stack.get()
        b = executor.stack.get()
        if a > 1000000:
            raise TypeError("Mantissa above 1000000 not allowed")
        executor.stack.put(b**a)
        return OpMap.NORETURN

    @staticmethod
    def BINARY_MULTIPLY(executor: Executor, args: list):
        a = executor.stack.get()
        b = executor.stack.get()
        executor.stack.put(b*a)
        return OpMap.NORETURN

    @staticmethod
    def BINARY_MATRIX_MULTIPLY(executor: Executor, args: list):
        a = executor.stack.get()
        b = executor.stack.get()
        executor.stack.put(b @ a)
        return OpMap.NORETURN

    @staticmethod
    def BINARY_FLOOR_DIVIDE(executor: Executor, args: list):
        a = executor.stack.get()
        b = executor.stack.get()
        executor.stack.put(b // a)
        return OpMap.NORETURN

    @staticmethod
    def BINARY_TRUE_DIVIDE(executor: Executor, args: list):
        a = executor.stack.get()
        b = executor.stack.get()
        executor.stack.put(b / a)
        return OpMap.NORETURN

    @staticmethod
    def BINARY_MODULO(executor: Executor, args: list):
        a = executor.stack.get()
        b = executor.stack.get()
        executor.stack.put(b % a)
        return OpMap.NORETURN

    @staticmethod
    def BINARY_ADD(executor: Executor, args: list):
        a = executor.stack.get()
        b = executor.stack.get()
        executor.stack.put(b + a)
        return OpMap.NORETURN

    @staticmethod
    def BINARY_SUBTRACT(executor: Executor, args: list):
        a = executor.stack.get()
        b = executor.stack.get()
        executor.stack.put(b - a)
        return OpMap.NORETURN

    @staticmethod
    def BINARY_SUBSCR(executor: Executor, args: list):
        a = executor.stack.get()
        b = executor.stack.get()
        executor.stack.put(b[a])
        return OpMap.NORETURN

    @staticmethod
    def LOAD_NAME(executor: Executor, args: list):
        name_idx = args[0] + args[1] * 256
        name = executor.function.names[name_idx]
        executor.stack.put(executor.loadName(name))
        return OpMap.NORETURN

    def LOAD_FAST(executor: Executor, args: list):
        name_idx = args[0] + args[1] * 256
        name = executor.function.varnames[name_idx]
        executor.stack.put(executor.loadName(name))
        return OpMap.NORETURN

    @staticmethod
    def STORE_NAME(executor: Executor, args: list):
        name_idx = args[0] + args[1] * 256
        name = executor.function.names[name_idx]
        executor.storeName(name, executor.stack.get())
        return OpMap.NORETURN

    @staticmethod
    def CALL_FUNCTION(executor: Executor, args: list):
        argc = args[0]
        if args[1]!=0:
            raise TypeError("Keyword arguments not supported")
        args = []
        for idx in range(argc):
            args.insert(0, executor.stack.get())
        function = executor.stack.get()
        executor.stack.put(executor.callFunction(function, args))
        return OpMap.NORETURN

    @staticmethod
    def LOAD_CONST(executor: Executor, args: list):
        const_idx = args[0] + args[1] * 256
        executor.stack.put(executor.function.constants[const_idx])
        return OpMap.NORETURN

    @staticmethod
    def MAKE_FUNCTION(executor: Executor, args: list):
        argc = args[0]+args[1]*256
        if argc!=0:
            raise TypeError("Annotations and default arguments are not supported")
        name = executor.stack.get()
        code = executor.stack.get()
        args = code.co_varnames[:code.co_argcount]
        function = Function(name, code, args, executor)
        executor.stack.put(function)
        return OpMap.NORETURN

    @staticmethod
    def RETURN_VALUE(executor: Executor, args: list):
        return executor.stack.get()

    @staticmethod
    def LOAD_ATTR(executor: Executor, args: list):
        namei = args[0] + args[1] * 256
        name = executor.function.names[namei]
        tos = executor.stack.get()
        executor.stack.put(executor.getAttr(tos, name))
        return OpMap.NORETURN

    @staticmethod
    def BUILD_LIST(executor: Executor, args: list):
        count = args[0] + args[1]*256
        o = executor.stack[-count:]
        executor.stack[-count:] = [o]
        return OpMap.NORETURN

    @staticmethod
    def BUILD_MAP(executor: Executor, args: list):
        count = args[0] + args[1] * 256
        o = {}
        for idx in range(count):
            val = executor.stack.get()
            o[executor.stack.get()] = val
        executor.stack.put(o)
        return OpMap.NORETURN

    @staticmethod
    def SETUP_LOOP(executor: Executor, args: list):
        delta = args[0] + args[1] * 256
        executor.blocks.put(executor.function[executor.index:executor.index + delta])
        return OpMap.NORETURN

    @staticmethod
    def GET_ITER(executor: Executor, args: list):
        executor.stack[-1]=iter(executor.stack[-1])
        return OpMap.NORETURN

    @staticmethod
    def FOR_ITER(executor: Executor, args: list):
        delta = args[0] + args[1] * 256
        sigil = object()
        n = next(executor.stack[-1], sigil)
        if n is sigil:
            executor.stack.get()
            executor.index+=delta
        else:
            executor.stack.put(n)
        return OpMap.NORETURN

    @staticmethod
    def JUMP_ABSOLUTE(executor: Executor, args: list):
        idx = args[0] + args[1] * 256
        executor.index = idx
        return OpMap.NORETURN

    @staticmethod
    def POP_BLOCK(executor: Executor, args: list):
        executor.blocks.get()
        return OpMap.NORETURN

    @staticmethod
    def COMPARE_OP(executor: Executor, args: list):
        op = args[0] + args[1] * 256
        operator = cmp_map[op]
        tos = executor.stack.get()
        tos1 = executor.stack.get()
        v = operator(tos1, tos)
        executor.stack.put(v)
        return OpMap.NORETURN

    @staticmethod
    def POP_JUMP_IF_FALSE(executor: Executor, args: list):
        target = args[0] + args[1] * 256
        tos = executor.stack.get()
        if not tos:
            executor.index = target
        return OpMap.NORETURN

    @staticmethod
    def POP_JUMP_IF_TRUE(executor: Executor, args: list):
        target = args[0] + args[1] * 256
        tos = executor.stack.get()
        if tos:
            executor.index = target
        return OpMap.NORETURN

    @staticmethod
    def JUMP_IF_TRUE_OR_POP(executor: Executor, args: list):
        target = args[0] + args[1] * 256
        if executor.stack[-1]:
            executor.index = target
        else:
            executor.stack.get()
        return OpMap.NORETURN

    @staticmethod
    def JUMP_IF_FALSE_OR_POP(executor: Executor, args: list):
        target = args[0] + args[1] * 256
        if not executor.stack[-1]:
            executor.index = target
        else:
            executor.stack.get()
        return OpMap.NORETURN

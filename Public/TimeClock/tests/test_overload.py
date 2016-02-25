from twisted.python.components import registerAdapter
from zope.interface import Interface, implementer

from TimeClock.Utils import overload
from unittest import TestCase


class Overload(TestCase):
    def test_overload(self):
        @overload
        def a(x: int) -> str:
            return x

        @overload
        def a(x: float) -> int:
            return int(x)
        self.assertEqual(a(1), "1")
        self.assertEqual(a(1.0), 1)

    def test_coersiveOverload(self):
        @overload
        def a(x: float) -> str:
            return x
        @overload
        def a(x: str) -> str:
            return x

        self.assertEqual(a(1), "1.0")
        self.assertEqual(a('1'), "1")

    def test_overloadClass(self):
        class Foo(object):
            @overload
            def bar(self, x: float) -> str:
                return x

            @overload
            def bar(self, x: int) -> str:
                return x
        foo = Foo()
        self.assertEqual(foo.bar(1.0), '1.0')
        self.assertEqual(foo.bar(2), '2')

    def test_overloadedConstructor(self):
        class Foo(object):
            @overload
            def __init__(self):
                self.x=1

            @overload
            def __init__(self, x:int):
                self.x=x
        self.assertEqual(Foo().x, 1)
        self.assertEqual(Foo(2).x, 2)

    def test_overloadedInterface(self):
        class IFoo(Interface):
            def hello() -> str:
                pass

            def name() -> str:
                pass

        @implementer(IFoo)
        class Foo(object):
            _name = "Foo"

            @overload
            def hello(self) -> str:
                return "hello world"

            @overload
            def hello(self, other:IFoo) -> str:
                return "hello %s, pleased to meet you" %other.name()

            @overload
            def name(self) -> str:
                return self._name

            @overload
            def __init__(self):
                pass

            @overload
            def __init__(self, name:int):
                self._name = 'foo%i'%name

            @overload
            def __init__(self, name:str):
                self._name = name

        foo1 = Foo(1)
        foo2 = Foo('foo2')
        self.assertEqual(foo1.hello(), 'hello world')
        self.assertEqual(foo1.hello(foo2), 'hello foo2, pleased to meet you')
        registerAdapter(Foo, int, IFoo)
        self.assertEqual(foo1.hello(3), 'hello foo3, pleased to meet you')



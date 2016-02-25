from TimeClock.Utils import coerce
from unittest import TestCase
from zope.interface import Interface, implementer
from zope.interface.exceptions import BrokenImplementation
from twisted.python.components import registerAdapter


class IFoo(Interface):
    def hello() -> str:
        """returns greeting"""


class IBar(IFoo):
    pass


class IBaz(Interface):
    pass


@implementer(IFoo)
class Foo(object):
    def __init__(self, _):
        pass

    def hello(self) -> str:
        return "hello world"


@implementer(IBar)
class Bar(Foo):
    pass


@implementer(IFoo)
class Bad(object):
    pass


registerAdapter(Foo, int, IFoo)
registerAdapter(Bar, float, IBar)


class Coercer(TestCase):
    def test_parameterCoersion(self):
        @coerce
        def test(x:int):
            return x
        self.assertIsInstance(test(1.0), int)

    def test_returnCoersion(self):
        @coerce
        def test() -> str:
            return 1
        self.assertEquals(test(), '1')

    def test_varargCoersion(self):
        @coerce
        def test(*x:float) -> list:
            return x
        self.assertEquals(test(1,2,3), [1.0, 2.0, 3.0])

    def test_kwargCoersion(self):
        @coerce
        def test(x:float = 5):
            return x
        self.assertEquals(test(1), 1.0)
        self.assertEquals(test(), 5.0)
        self.assertEquals(test(x=1), 1.0)

    def test_varkwCoersion(self):
        @coerce
        def test(**x:float):
            return x
        self.assertEquals(test(), {})
        self.assertEquals(test(x=1), {'x':1.0})
        self.assertEquals(test(x=1, y=2), {'x': 1.0, 'y': 2.0})

    def test_kwonlyCoersion(self):
        @coerce
        def test(*, x:float=5.0):
            return x
        self.assertEquals(test(), 5.0)
        self.assertEquals(test(x=1), 1.0)
        with self.assertRaises(TypeError):
            test(1)

    def test_interfaceCoersion(self):
        @coerce
        def test(x:IFoo) -> str:
            return x.hello()
        self.assertEquals(test(1), "hello world")

    def test_badInterface(self):
        @coerce
        def test(x: IFoo) -> str:
            return x.hello()
        with self.assertRaises(BrokenImplementation):
            test(Bad())

    def test_notAdaptable(self):
        @coerce
        def test(x: IBaz) -> str:
            return str(x)
        with self.assertRaises(TypeError):
            test(1)

    def test_self(self):
        class testSelf(object):
            @coerce
            def test_self(self, other: int):
                return type(self), type(other)

        t = testSelf()
        s,o = t.test_self(1)
        self.assertEqual(s, testSelf)
        self.assertEqual(o, int)

    def test_array(self):
        @coerce
        def testArray() -> [int]:
            return [5.0,6,7]
        self.assertEqual(testArray(), [5,6,7])

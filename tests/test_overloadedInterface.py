from unittest import TestCase

from zope.interface import Interface, implementer
from zope.interface.exceptions import BrokenMethodImplementation
from zope.interface.verify import verifyObject

from TimeClock.Utils import overload, coerce, fromFunction


class INamed(Interface):
    @fromFunction
    def getName() -> str:
        pass

class IFoo(Interface):
    @fromFunction
    @overload
    def hello()->str:
        pass
    @fromFunction
    @overload
    def hello(other: INamed) -> str:
        pass


@implementer(INamed)
class Named(object):
    def __init__(self, name):
        self.name=name
    @coerce
    def getName(self) -> str:
        return self.name




class OverloadedInterface(TestCase):
    def testOverloadedInerface(self):
        @implementer(IFoo)
        class Foo(object):
            @overload
            def hello(self) -> str:
                return "Hello World"
            @overload
            def hello(self, other: INamed) -> str:
                return "Hello %s" % other.getName()
    def testUsingOverloadedInterface(self):
        @implementer(IFoo)
        class Foo(object):
            @overload
            def hello(self) -> str:
                return "Hello World"
            @overload
            def hello(self, other: INamed) -> str:
                return "Hello %s" % other.getName()
        n = Named("John Doe")
        f = Foo()
        self.assertEqual(f.hello(), 'Hello World')
        self.assertEqual(f.hello(n), 'Hello John Doe')
    def testOverloadedImplementation(self):
        @implementer(INamed)
        class Alias(Named):
            @overload
            def getName(self) -> str:
                return self.name
            @overload
            def getName(self, alias: str) -> str:
                return self.name+', AKA '+alias
        n = Alias("John Doe")
        self.assertEqual(n.getName(), "John Doe")
        self.assertEqual(n.getName('JD'), "John Doe, AKA JD")
    def testPartialImplementation(self):
        @implementer(IFoo)
        class Foo(object):
            @overload
            def hello(self) -> str:
                return "Hello World"

        f = Foo()
        with self.assertRaises(BrokenMethodImplementation):
            verifyObject(IFoo, f)



from unittest import TestCase

from axiom.store import Store

from axiom.attributes import text, reference

from axiom.item import Item
from zope.interface import Interface


class IFoo(Interface):
    pass


class IBar(Interface):
    def hello(self) -> str:
        pass


class Foo(Item):
    name=text()


class Bar(Item):
    foo=reference()

    def hello(self) -> str:
        return "hello from %i" %self.foo.storeID


class EmployeeTester(TestCase):
    def test_powerup(self):
        s = Store()
        foo = Foo(store=s)
        bar = Bar(store=s)
        bar.foo=foo
        foo.powerUp(bar, IBar)
        self.assertEqual(IBar(foo).hello(), 'hello from 1')

    def test_powerdown(self):
        s = Store()
        foo = Foo(store=s)
        bar = Bar(store=s)
        bar.foo = foo
        foo.powerUp(bar, IBar)
        self.assertEqual(IBar(foo).hello(), 'hello from 1')
        foo.powerDown(IBar(foo), IBar)
        with self.assertRaises(TypeError):
            IBar(foo).hello()


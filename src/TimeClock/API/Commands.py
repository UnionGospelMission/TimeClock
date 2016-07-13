from TimeClock.ITimeClock.ICommand import ICommand

from ..Axiom import Store


for c in Store.Store.powerupsFor(ICommand):
    n = c.name.title().replace(' ', '')
    globals()[n] = c


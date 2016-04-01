from TimeClock.Axiom import Store
from TimeClock.ITimeClock.IAPI import IAPI


for i in Store.Store.powerupsFor(IAPI):
    print(6, i)
    n = i.name.title().replace(' ', '')
    globals()[n] = i

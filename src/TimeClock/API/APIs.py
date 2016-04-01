from TimeClock.Axiom import Store
from TimeClock.ITimeClock.IAPI import IAPI


for i in Store.Store.powerupsFor(IAPI):
    n = i.name.replace(' ', '')
    globals()[n] = i

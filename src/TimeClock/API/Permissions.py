from TimeClock.Axiom import Store
from TimeClock.Database.Permissions import Permission


for i in Store.Store.query(Permission):
    globals()[i.name.replace(' ', '')] = i

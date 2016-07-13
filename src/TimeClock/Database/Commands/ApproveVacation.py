from axiom.attributes import text

from axiom.item import Item


class ApproveVacation(Item):
    name = text(default='Approve Vacation')
    def hasPermission(self, *a):
        return False

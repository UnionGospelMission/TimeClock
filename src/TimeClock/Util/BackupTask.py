from zope.interface import implementer

import twisted
from TimeClock.Util.DateTime import DateTime
from axiom.attributes import text, reference
from axiom.item import Item
from twisted.application.service import IServiceCollection
import tarfile
import os


@implementer(twisted.application.service.IService)
class BackupTask(Item):
    schemaVersion = 1
    destination = text()
    timeOfDay = text()
    name = text()
    parent = reference()

    @staticmethod
    def new(options):
        self = BackupTask()
        destination = options['destination']
        timeOfDay = options.get('when', '0:00:00')
        self.timeOfDay = timeOfDay
        self.destination = destination
        return self

    def installOn(self, store):
        self.store = store
        store.powerUp(self, twisted.application.service.IService)

    def setName(self, name):
        if self.parent:
            raise RuntimeError("Cannot set name after parent")
        self.name = name

    def setServiceParent(self, parent):
        IServiceCollection(parent).addService(self)
        if isinstance(parent, Item):
            self.parent = parent

    def disownServiceParent(self, parent):
        return self.parent.removeService(self)

    def startService(self):
        self.scheduleRun()

    def scheduleRun(self):
        from twisted.internet import reactor
        hour, minute, second = [int(i) for i in self.timeOfDay.split(':')]
        now = DateTime.now()
        then = now.replace(hour=hour, minute=minute, second=second)
        if then < now:
            then = then.replace(days=1)
        delay = (then - now).total_seconds()
        reactor.callLater(delay, self.runBackup)

    def runBackup(self):
        import shutil
        path = self.store.filesdir.parent()
        sibling = path.temporarySibling()
        sibling.createDirectory()
        path.copyTo(sibling.child(path.basename()))
        sibling.child(path.basename()).child('run').child('axiomatic.pid').remove()
        now = DateTime.now()
        self.make_tarfile(self.destination % dict(year=now.year,
                                                  month=now.month,
                                                  day=now.day,
                                                  hour=now.hour,
                                                  minute=now.minute),
                          sibling.child(path.basename()).path)
        sibling.remove()
        self.scheduleRun()

    def stopService(self):
        return

    def make_tarfile(self, output_filename, source_dir):
        with tarfile.open(output_filename, "w:gz") as tar:
            tar.add(source_dir, arcname=os.path.basename(source_dir))

    def privilegedStartService(self):
        return


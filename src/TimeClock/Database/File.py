from zope.interface import implementer, Interface

from TimeClock.ITimeClock.IDatabase.IFile import IFile
from axiom.attributes import text
from axiom.item import Item


@implementer(IFile)
class File(Item):
    path = text()

    def open(self, mode: str='r') -> IFile:
        f = list(self.powerupsFor(IFile))
        if not f:
            f = open(self.path, mode)
            self.inMemoryPowerUp(f, IFile)
        return self

    def read(self, size: int = None) -> str:
        f = list(self.powerupsFor(IFile))[0]
        return f.read(size)

    def write(self, txt: str) -> int:
        f = list(self.powerupsFor(IFile))[0]
        return f.write(txt)

    def seek(self, offset: int):
        f = list(self.powerupsFor(IFile))[0]
        f.seek(offset)

    def close(self):
        f = list(self.powerupsFor(IFile))[0]
        f.close()
        del self._inMemoryPowerups[IFile]

    def __enter__(self):
        self.open()

    def __exit__(self, exc_type, exc_value, stacktrace):
        self.close()

    def flush(self):
        f = list(self.powerupsFor(IFile))[0]
        f.flush()

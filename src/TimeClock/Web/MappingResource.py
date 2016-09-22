from gzip import GzipFile

from nevow.athena import MappingResource as MR
from zope.interface import implementer
from nevow import inevow, static, rend
from nevow.compression import parseAcceptEncoding
from nevow.inevow import IRequest
from io import BytesIO
from twisted.python.filepath import FilePath as FP


@implementer(inevow.IResource)
class GZFile(static.File):
    encoding = None
    @staticmethod
    def canCompress(req):
        value = req.getHeader('accept-encoding')
        if value is not None:
            encodings = parseAcceptEncoding(value)
            return encodings.get('gzip', 0.0) > 0.0
        return False

    def __init__(self, path):
        super().__init__(path)
        self._compressed = BytesIO()
        self._gzipFile = GzipFile(fileobj=self._compressed, mode='wb', compresslevel=9)
        if self.fp.exists():
            with self.fp.open('rb') as f:
                txt = f.read()
                self._gzipFile.write(txt)
                self._gzipFile.close()

    def renderHTTP(self, ctx):
        self.fp.restat()

        if self.type is None:
            self.type, self.encoding = static.getTypeAndEncoding(self.fp.basename(),
                                                          self.contentTypes,
                                                          self.contentEncodings,
                                                          self.defaultType)

        if not self.fp.exists():
            return rend.FourOhFour()

        request = inevow.IRequest(ctx)
        compress = self.canCompress(request)

        if self.fp.isdir():
            return self.redirect(request)

        # fsize is the full file size
        # size is the length of the part actually transmitted
        if compress:
            self.encoding = 'gzip'

        request.setHeader(b'accept-ranges', 'none')

        if self.type:
            request.setHeader(b'content-type', self.type)
        if self.encoding:
            request.setHeader(b'content-encoding', self.encoding)

        if b'transfer-encoding' in request.headers:
            request.headers.pop(b'transfer-encoding')
        try:
            f = self.openForReading()
        except IOError as e:
            import errno
            if e[0] == errno.EACCES:
                return static.ForbiddenResource().render(request)
            else:
                raise

        if request.setLastModified(self.fp.getmtime()) is static.http.CACHED:
            return ''


        if request.method == 'HEAD':
            return ''

        if compress:
            return self._compressed.getvalue()
        # return data
        return f.read()


@implementer(inevow.IResource)
class MappingResource(MR):
    __cache__ = {}
    
    def resourceFactory(self, fileName):
        if fileName not in self.__cache__:
            self.__cache__[fileName] = GZFile(fileName)
        return self.__cache__[fileName]

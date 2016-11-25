import os
from collections import namedtuple
from datetime import date, timedelta
from time import mktime
from wsgiref.handlers import format_date_time

from rapui.DeferUtil import deferToThreadWrap
from rapui.site.ResourceUtil import RapuiResource




class FileResource(RapuiResource):
    """
      TODO: Minify combined css file
    """
    isLeaf = True

    def __init__(self, userAccess, staticResources):
        RapuiResource.__init__(self, userAccess)
        self._staticResources = staticResources

    def render_GET(self, request):
        # request.responseHeaders.setRawHeaders('content-type', ['text/css'])

        resourceFilePath = os.path.join(*request.postpath).decode()
        fullFileName = self._staticResources.getFontFileName(resourceFilePath)

        return self.serveStaticFileWithCache(request, fullFileName)

    @classmethod
    def serveStaticFileWithCache(request, fileNamePath,
                                 expireMinutes=30,
                                 chunkSize=128000):
        ''' Resource Create And Serve Static File

        This should probably be a class now.

        '''
        FileData = namedtuple("FileData", ["fobj", "size", "cacheControl", "expires"])
        if isinstance(fileNamePath, bytes):
            fileNamePath = fileNamePath.decode("UTF-8")

        class Closure:
            cancelDownload = False

        if Closure.cancelDownload:
            print((Closure.cancelDownload))

        @deferToThreadWrap
        def loadFileInThread():
            requestPath = request.path
            if not fileNamePath or not os.path.exists(fileNamePath):
                raise Exception("File %s doesn't exist for resource %s"
                                % (fileNamePath, requestPath))

            size = os.stat(fileNamePath).st_size
            fobj = open(fileNamePath, 'rb')

            expiry = (date.today() + timedelta(expireMinutes)).timetuple()
            expiresTime = format_date_time(mktime(expiry))

            cacheControl = "max-age=" + str(expireMinutes * 60)  # In Seconds
            cacheControl += ", private"

            return FileData(fobj=fobj, size=size,
                            cacheControl=cacheControl, expires=expiresTime)

        def setHeaders(fileData):
            # DISABLED
            # Cache control is disabled for gziped resources as they are chunk-encoded
            # request.setHeader("Cache-Control", fileData.cacheControl)
            # request.setHeader("Expires", fileData.expires)
            request.setHeader("Content-Length", fileData.size)
            return fileData

        def writeData(fileData):
            def writer():
                try:
                    data = fileData.fobj.read(chunkSize)
                    while data and not Closure.cancelDownload:
                        request.write(data)
                        yield None  # Yield to the reactor for a bit
                        data = fileData.fobj.read(chunkSize)
                    request.finish()
                    fileData.fobj.close()
                except Exception as e:
                    logger.error("An error occured loading and sending the file"
                                 " data for file %s for resource %s",
                                 fileNamePath, request.path)
                    logger.exception(e)

            return cooperate(writer())

        def fileFailed(failure):
            Closure.cancelDownload = True
            request.setResponseCode(404)
            logger.error(str(failure.value))
            request.finish()

            logger.error("Failed to send file %s for resource %s", fileNamePath,
                         request.path)
            logger.exception(failure.value)

        def closedError(failure):
            logger.error("Got closedError %s" % failure)

        d = loadFileInThread()
        d.addCallback(setHeaders)
        d.addCallback(writeData)
        d.addErrback(fileFailed)

        request.notifyFinish().addErrback(closedError)

        return NOT_DONE_YET

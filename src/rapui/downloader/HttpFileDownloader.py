"""
 * Created by Synerty Pty Ltd
 *
 * This software is open source, the MIT license applies.
 *
 * Website : http://www.synerty.com
 * Support : support@synerty.com
"""

import logging

from pydirectory.Directory import Directory
from twisted.internet import reactor
from twisted.internet.defer import Deferred
from twisted.internet.protocol import Protocol
from twisted.web._newclient import ResponseDone
from twisted.web.client import Agent
from twisted.web.http_headers import Headers

logger = logging.getLogger(__name__)


class HttpFileDownloader:
    def __init__(self, url):
        self._url = url

    def run(self):
        agent = Agent(reactor)

        d = agent.request(
            'GET',
            self._url,
            Headers({'User-Agent': ['Synerty File Downloader']}),
            None)

        def cbResponse(response):
            if response.code == 200:
                bodyDownloader = _RapuiHttpFileDownloaderBody()
            else:
                bodyDownloader = _RapuiHttpBodyError(response.code,
                                                     response.request.absoluteURI)
            response.deliverBody(bodyDownloader)
            return bodyDownloader.deferred

        d.addCallback(cbResponse)

        return d


class _RapuiHttpFileDownloaderBody(Protocol):
    def __init__(self):
        self._finishedDeferred = Deferred()
        self._directory = Directory()
        self._tmpFile = self._directory.createFile(name="downloadedFile")
        self._openedFobj = self._tmpFile.open(append=True)

    @property
    def deferred(self):
        return self._finishedDeferred

    def dataReceived(self, bytes):
        self._openedFobj.write(bytes)

    def connectionLost(self, reason):
        self._openedFobj.close()

        if isinstance(reason.value, ResponseDone):
            logger.debug('File download complete, size=%s', self._tmpFile.size)
            self._finishedDeferred.callback((self._directory, self._tmpFile))
            return

        self._finishedDeferred.errback(reason)


class _RapuiHttpBodyError(Protocol):
    def __init__(self, responseCode, responseUri):
        self._finishedDeferred = Deferred()
        self._responseCode = responseCode
        self._responseUri = responseUri
        self._msg = ""

    @property
    def deferred(self):
        return self._finishedDeferred

    def dataReceived(self, bytes):
        self._msg += bytes

    def connectionLost(self, reason):
        self._finishedDeferred.errback(Exception("Server returned %s for %s\n%s\n%s"
                              % (self._responseCode, self._responseUri,
                                                 reason,
                                                 self._msg)))

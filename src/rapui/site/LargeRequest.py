import logging
import tempfile
from io import BytesIO

from twisted.web import server

from rapui.site.ResourceUtil import LARGE_REQUEST_PATHS

logger = logging.getLogger(name="largerequest")


class LargeRequest(server.Request):

    def gotLength(self, length):
        """
        Called when HTTP channel got length of content in this request.

        This method is not intended for users.

        @param length: The length of the request body, as indicated by the
            request headers.  L{None} if the request headers do not indicate a
            length.
        """
        if length is not None and length < 100000 and not self._useLargeRequest():
            self.content = BytesIO()
        else:
            self.content = tempfile.TemporaryFile()

    def _useLargeRequest(self):
        """
        Process a request.
        """
        assert not hasattr(self, "useLargeRequest"), (
            "useLargeRequest class attribute is depreciated"
            ", use d@addResourceCreator(path, useLargeRequest=True) decorator instead")

        return self.path in LARGE_REQUEST_PATHS

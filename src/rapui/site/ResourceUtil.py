"""
 * Created by Synerty Pty Ltd
 *
 * This software is open source, the MIT license applies.
 *
 * Website : http://www.synerty.com
 * Support : support@synerty.com
"""

import logging

from twisted.web.resource import Resource, EncodingResourceWrapper
from twisted.web.server import GzipEncoderFactory

logger = logging.getLogger(__name__)

RESOURCES = None

if not RESOURCES:
    RESOURCES = {}

LARGE_REQUEST_PATHS = None

if not LARGE_REQUEST_PATHS:
    LARGE_REQUEST_PATHS = set()


class RapuiResource(Resource):
    isGzipped = True

    def __init__(self, userAccess):
        Resource.__init__(self)
        self.userAccess = userAccess

    def getChildWithDefault(self, path, request):
        return self._gzipIfRequired(Resource.getChildWithDefault(self, path, request))

    def getChild(self, path, request):
        return self._gzipIfRequired(Resource.getChild(self, path, request))

    def _gzipIfRequired(self, resource):
        if (not isinstance(resource, EncodingResourceWrapper)
                and hasattr(resource, 'isGzipped')
                and resource.isGzipped):
            return EncodingResourceWrapper(resource, [GzipEncoderFactory()])
        return resource


def addResourceCreator(path: bytes, useLargeRequest=False):
    ''' Add Resource Creator
    param: RapuiElement, an element class
    '''
    assert isinstance(path, bytes)

    if path in RESOURCES:
        raise KeyError("Resource path %s is already registered" % path)

    def decorator(creatorFunction):

        RESOURCES[path] = creatorFunction

        if useLargeRequest:
            LARGE_REQUEST_PATHS.add(path)

        return creatorFunction

    return decorator



def removeResourcePaths(paths: [bytes]):
    ''' Remove Resource Paths

    Unregister the resource paths so that the server will no longer respond to them.

    '''
    for path in paths:
        assert isinstance(path, bytes)
        if path in RESOURCES:
            del RESOURCES[path]

        if path in LARGE_REQUEST_PATHS:
            del LARGE_REQUEST_PATHS[path]


def registeredResourcePaths():
    return list(RESOURCES.keys())

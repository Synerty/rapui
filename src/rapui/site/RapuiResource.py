import logging
import os

from twisted.python.compat import nativeString
from twisted.web.error import UnsupportedMethod
from twisted.web.resource import EncodingResourceWrapper, IResource, NoResource
from twisted.web.server import GzipEncoderFactory
from zope.interface import implementer

logger = logging.getLogger(__name__)

import mimetypes

mimetypes.init()


def get_extensions_for_type(general_type):
    for ext in mimetypes.types_map:
        if mimetypes.types_map[ext].split('/')[0] == general_type:
            yield ext


IMAGE_EXTENSIONS = list(get_extensions_for_type('image'))
FONT_EXTENSIONS = list(get_extensions_for_type('font'))


@implementer(IResource)
class RapuiResource:
    """ RapUI Simple Resource

    This class is a node for the resource tree, It's a slightly simpler version of
    C{twisted.web.resource.Resource}

    """
    isGzipped = False
    entityType = IResource
    server = None
    isLeaf = False

    def __init__(self):
        """
        Initialize.
        """
        self.__children = {}

    def getChild(self, path, request):
        if path in self.__children:
            return self.__children[path]
        return NoResource()

    getChildWithDefault = getChild

    def putChild(self, path: bytes, child):
        if b'/' in path:
            raise Exception("Path %s can not start or end with '/' ", path)

        self.__children[path] = child
        child.server = self.server

    def render(self, request):
        # Optionally, Do some checking with userSession.userDetails.group
        # userSession = IUserSession(request.getSession())
        methodName = 'render_' + nativeString(request.method)

        m = getattr(self, methodName, None)
        if not m:
            raise UnsupportedMethod(methodName)
        return m(request)

    def render_HEAD(self, request):
        return self.render_GET(request)

    def _gzipIfRequired(self, resource):
        if (not isinstance(resource, EncodingResourceWrapper)
            and hasattr(resource, 'isGzipped')
            and resource.isGzipped):
            return EncodingResourceWrapper(resource, [GzipEncoderFactory()])
        return resource


class FileUnderlayResource(RapuiResource):
    """
    This class resolves URLs into either a static file or a C{RapuiRequestDynamicRenderer}

    This is a multi level search :
    1) getChild, looking for resource in the resource tree
    2) The staticFileUnderlay is searched.
    3) Request fails with NoResource()

    """

    acceptedExtensions = ['.js', '.css', '.html', '.xml']
    acceptedExtensions += FONT_EXTENSIONS
    acceptedExtensions += IMAGE_EXTENSIONS

    def __init__(self):
        RapuiResource.__init__(self)

        self._fileSystemRoots = []

    def getChildWithDefault(self, path, request):
        return self.getChild(path, request)

    def getChild(self, path, request):
        # Optionally, Do some checking with userSession.userDetails.group
        # userSession = IUserSession(request.getSession())

        resoureFromTree = RapuiResource.getChild(self, path, request)
        if not isinstance(resoureFromTree, NoResource):
            return resoureFromTree

        # else, look for it in the file system
        filePath = self.getRealFilePath(os.path.join(path, *request.postpath))
        if filePath:
            from rapui.site.StaticFileResource import StaticFileResource
            return self._gzipIfRequired(StaticFileResource(filePath))

        return NoResource()

    def addFileSystemRoot(self, fileSystemRoot:str):
        if not os.path.isdir(fileSystemRoot):
            raise NotADirectoryError("%s is not a directory" % fileSystemRoot)

        self._fileSystemRoots.append(fileSystemRoot)

    def getRealFilePath(self, resourcePath: bytes) -> bytes:

        for rootDir in self._fileSystemRoots[::-1]:
            realFilePath = os.path.join(rootDir, resourcePath.decode())

            if os.path.isdir(realFilePath):
                logger.debug("Resource path %s is a directory %s",
                             resourcePath, realFilePath)

            if os.path.isfile(realFilePath):
                return realFilePath

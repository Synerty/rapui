"""
 * Created by Synerty Pty Ltd
 *
 * This software is open source, the MIT license applies.
 *
 * Website : http://www.synerty.com
 * Support : support@synerty.com
"""

import logging

import os
from os import path as p

logger = logging.getLogger(__name__)

class RapuiStaticResources(object):
    ''' RapUI Web Resources

    Multi level search path for web resources.

    This class serves web resources out of a common structure, EG:
    /view/Thing.html
    /javascript/thing.js
    /style/thing.css
    /image/thing.img

    RapUIWebResources serves these at the root resource by default.

    New RapUIWebResources can be created to serve folders at a different location,
    such as /papp_noop/view/Thing.html

    '''

    def __init__(self, rootPath, groupPermissionsMap):
        self._rootPath = rootPath
        self._groupPermissionsMap = groupPermissionsMap

    def addStaticResourceDir(self, dir):

        if not os.path.isdir(dir):
            logger.debug("addStaticResourceDir, %s doesn't exist",
                         dir)
            return

        self._templatePaths.append(dir)
        self._stylePaths.append(dir)
        self._javascriptPaths.append(dir)
        self._fontPaths.append(dir)
        self._imagePaths.append(dir)

    def createResource(self, userAccess):
        ''' Create Resource

        Create a resource, add the web resources to it and return it

        '''

        from rapui.site.ResourceUtil import RapuiResource
        resource = RapuiResource(userAccess)
        self.addToResource(resource, userAccess)
        return resource

    def addToResource(self, resource, userAccess):
        # type: (RapuiResource, UserAccess) -> None

        """ Add To Resource

        This method adds the web resources as childs to the resource provided

        :param resource: RapuiResource
        :param userAccess: UserAccess
        """
        from rapui.site.FontResource import FontResource
        from old.HtmlResource import HtmlResource
        from old.ImageResource import ImageResource
        from rapui.site.JavascriptResource import JavaScriptResource
        from rapui.site.StyleResource import StyleResource

        resource.putChild(b'style', StyleResource(userAccess, self))
        resource.putChild(b'fonts', FontResource(userAccess, self))
        resource.putChild(b'image', ImageResource(userAccess, self))
        resource.putChild(b'javascript', JavaScriptResource(userAccess, self))
        resource.putChild(b'view', HtmlResource(userAccess, self))

    def getTemplateFileName(self, filename):
        for tempPath in self._templatePaths[::-1]:
            file_ = p.join(tempPath, filename)
            if p.exists(file_):
                return file_

    def getFontFileName(self, filename):
        for tempPath in self._fontPaths[::-1]:
            file_ = p.join(tempPath, filename)
            if p.exists(file_):
                return file_

    def getImageFileName(self, filename):
        for tempPath in self._imagePaths[::-1]:
            file_ = p.join(tempPath, filename)
            if p.exists(file_):
                return file_

    def getJavascriptFileName(self, filename):
        """ Get Javascript Filename
        This function will do a simple two level search for the filename
        Could improve on this by using an array and having a generic function

        @param filename: The filename to search for
        @return the full path or empty string if not found
        """

        for tempPath in self._javascriptPaths[::-1]:
            file_ = p.join(tempPath, filename)
            if p.exists(file_):
                return file_

    def getJavascriptLoadFileNames(self, paths):
        """ Get Javascript File Names

        @return: List of relative javascript file names
        """
        uniqueNames = set()
        fileNames = []
        # Get a combined list of javascript file names
        for tempPath in paths:
            if not p.exists(tempPath):
                continue

            thisPathsNames = []

            # This is hard coded into HtmlTemplate.xml
            uniqueNames.add("require.js")

            for file_ in os.listdir(tempPath):
                if not file_.lower().endswith(".js"):
                    continue

                if file_ in uniqueNames:
                    continue

                if "require.js" in file_:
                    continue

                uniqueNames.add(file_)
                thisPathsNames.append(file_)

            thisPathsNames.sort()

            fileNames.extend(thisPathsNames)

        return fileNames

    def getStyleFileName(self, filename):
        for tempPath in self._stylePaths[::-1]:
            file_ = p.join(tempPath, filename)
            if p.exists(file_):
                return file_

    def getStyleLoadFileNames(self, paths):
        uniqueNames = set()
        fileNames = []

        for tempPath in paths:
            if not p.exists(tempPath):
                continue

            thisPathsNames = []

            for file_ in os.listdir(tempPath):
                if not file_.lower().endswith("css"):
                    continue

                if file_ in uniqueNames:
                    continue

                uniqueNames.add(file_)
                thisPathsNames.append(file_)

            thisPathsNames.sort()
            fileNames.extend(thisPathsNames)

        return fileNames

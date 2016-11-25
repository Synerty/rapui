""" 
 * view.common.uiobj.Javascript.py
 *
 *  Copyright Synerty Pty Ltd 2013
 *
 *  This software is proprietary, you are not free to copy
 *  or redistribute this code in any format.
 *
 *  All rights to this software are reserved by 
 *  Synerty Pty Ltd
 *
"""
import logging
import os

from rapui.site.ResourceUtil import RapuiResource, resourceCacheAndServeStaticFile

logger = logging.getLogger(__name__)


class JavaScriptResource(RapuiResource):
    isLeaf = True

    def __init__(self, userAccess, staticResources):
        RapuiResource.__init__(self, userAccess)
        self._staticResources = staticResources

    def render_GET(self, request):
        request.responseHeaders.setRawHeaders('content-type', ['text/javascript'])

        resourceFilePath = os.path.join(*request.postpath).decode("UTF-8")
        fullFileName = self._staticResources.getJavascriptFileName(resourceFilePath)

        return resourceCacheAndServeStaticFile(request, fullFileName)

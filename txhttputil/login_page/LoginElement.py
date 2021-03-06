'''
Created on 17/06/2013

@author: Jarrod Chesney
'''
import os

from twisted.python.filepath import FilePath
from twisted.web._element import renderer, Element
from twisted.web.template import XMLFile

import txhttputil


class LoginElement(Element):
    xmlFileName = 'LoginTemplate.xml'
    loader = XMLFile(FilePath(os.path.join(os.path.dirname(__file__), xmlFileName)))

    siteName = "txHttpWeb"

    def __init__(self, failed):
        self._failed = failed

    @renderer
    def loginTitle(self, request, tag):
        tag("Login to %s" % self.siteName)
        return tag

    @renderer
    def metaDescriptionContent(self, request, tag):
        # tag(content="%s" % globalSetting()[SYSTEM_DESCRIPTION])
        return tag

    @renderer
    def errorPanel(self, request, tag):
        if self._failed:
            return tag("Failed to login")
        return ""

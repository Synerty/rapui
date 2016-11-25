"""   
 * uiobj.__init__.py
    
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
import os.path as p

from twisted.web._stan import Tag

from rapui.RapuiConfig import Debug

logger = logging.getLogger(__name__)

__modPath = p.dirname(__file__)

TITLE = "RapUI - Synertys' Rapid UI Framework"
DESCRIPTION = "RapUI - Synertys' Rapid UI Framework"
KEYWORDS = []
HEAD_CUSTOM_TAGS = []


def addMetaTag(name, content):
    HEAD_CUSTOM_TAGS.append(Tag("meta")(name=name)(content=content))
    HEAD_CUSTOM_TAGS.append('\n\t\t')


_RAPUI_TEMPLATE_PATHS = []
_RAPUI_JAVASCRIPT_PATHS = []
_RAPUI_STYLE_PATHS = []
_RAPUI_FONT_PATHS = []
_RAPUI_IMAGE_PATHS = []

rapuiRootStaticResources = None


def addStaticResourceDir(dir):
    from rapui.site.StaticFileResources import RapuiStaticResources
    global rapuiRootStaticResources

    if not rapuiRootStaticResources:
        rapuiRootStaticResources = RapuiStaticResources()

        rapuiRootStaticResources._templatePaths.extend(_RAPUI_TEMPLATE_PATHS)
        rapuiRootStaticResources._javascriptPaths = _RAPUI_JAVASCRIPT_PATHS[:]
        rapuiRootStaticResources._stylePaths = _RAPUI_STYLE_PATHS[:]
        rapuiRootStaticResources._fontPaths = _RAPUI_FONT_PATHS[:]
        rapuiRootStaticResources._imagePaths = _RAPUI_IMAGE_PATHS[:]

    # if autoloadjs:
    #     _RAPUI_TEMPLATE_PATHS.append(dir)
    #     _RAPUI_JAVASCRIPT_PATHS.append(dir)
    #     _RAPUI_IMAGE_PATHS.append(dir)
    #
    # if autoloadcss:
    #     _RAPUI_FONT_PATHS.append(dir)
    #     _RAPUI_STYLE_PATHS.append(dir)

    rapuiRootStaticResources.addStaticResourceDir(dir)


# Serve the npm packages
nodeModulesPath = os.path.join(__modPath, "node_modules")
if os.path.isdir(nodeModulesPath):
    addStaticResourceDir(nodeModulesPath)

import rapui.angular_custom
import rapui.auth

import rapui.site
# import test

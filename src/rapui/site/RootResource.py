'''
Created on 05/06/2013

@author: darkstar
'''
from twisted.web.resource import NoResource

from rapui import rapuiRootStaticResources
from rapui.site.ResourceUtil import RapuiResource, RESOURCES


class RootResource(RapuiResource):
    pass


def createRootResource(userAccess):
    rootResource = RootResource(userAccess)

    rapuiRootStaticResources.addToResource(rootResource, userAccess)

    callResourceCreators(RESOURCES, rootResource, userAccess)

    return rootResource


def callResourceCreators(resourceCreatorByPath,
                         rootResource,
                         userAccess):

    # Put all the child resources in
    resources = [(key.strip(b'/').split(b'/'), value)
                 for key, value in list(resourceCreatorByPath.items())]
    resources.sort(key=lambda x: len(x[0]))
    for paths, resourceCreator in resources:
        parentResource = rootResource
        paths.reverse()
        name = paths.pop()
        while paths:
            path = paths.pop()
            if path in parentResource.children:
                parentResource.children[path]
            else:
                parentResource.putChild(path, NoResource())
        parentResource.putChild(name, resourceCreator(userAccess))

"""
 * Created by Synerty Pty Ltd
 *
 * This software is open source, the MIT license applies.
 *
 * Website : http://www.synerty.com
 * Support : support@synerty.com
"""

from rapui.site.ResourceUtil import RESOURCES
from rapui.site.StaticFileResource import StaticFileResource
from rapui.site.StaticFileMultiPath import StaticFileMultiPath
from rapui.site.AuthUserDetails import AuthUserDetails


class RootResource(StaticFileResource):
    """ Root Resource

    This resource is the root or subroot of a resource tree.
    It first looks for resources created with "createRoot
    """


def createRootResource(userAccess: AuthUserDetails, staticFileRoot: StaticFileMultiPath):
    rootResource = RootResource(userAccess, staticFileRoot=staticFileRoot)
    callResourceCreators(RESOURCES, rootResource, userAccess)

    return rootResource

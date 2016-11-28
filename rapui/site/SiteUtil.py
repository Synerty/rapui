"""
 * Created by Synerty Pty Ltd
 *
 * This software is open source, the MIT license applies.
 *
 * Website : http://www.synerty.com
 * Support : support@synerty.com
"""

import logging

from twisted.internet import reactor
from twisted.web import server
from twisted.web.http import HTTPChannel

from rapui.login_page.RapuiLoginElement import RapuiLoginElement
from rapui.site.AuthCredentials import AllowAllAuthCredentials, AuthCredentials
from rapui.site.AuthRealm import RapuiAuthSessionWrapper
from rapui.site.FileUploadRequest import FileUploadRequest
from rapui.site.RapuiResource import RapuiResource

logger = logging.getLogger(__name__)


def setupSite(name: str,
              rootResource: RapuiResource,
              portNum: int = 8000,
              credentialChecker: AuthCredentials = AllowAllAuthCredentials()):
    ''' Setup Site
    Sets up the web site to listen for connections and serve the site.
    Supports customisation of resources based on user details

    @return: Port object
    '''

    RapuiLoginElement.siteName = name

    protectedResource = RapuiAuthSessionWrapper(rootResource, credentialChecker)

    site = server.Site(protectedResource)
    site.protocol = HTTPChannel
    site.requestFactory = FileUploadRequest

    sitePort = reactor.listenTCP(portNum, site)

    import subprocess
    ip = subprocess.getoutput("/sbin/ifconfig").split("\n")[1].split()[1][5:]

    logger.info('%s is alive and listening on http://%s:%s', name, ip, sitePort.port)
    return sitePort

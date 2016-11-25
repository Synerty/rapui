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

from rapui.site.LargeRequest import LargeRequest
from rapui.site.RootResource import createRootResource
from rapui.site.UserAccess import UserAccess

logger = logging.getLogger(__name__)


def setupSite(name, portNum=0, protectedResource=None):
    ''' Setup Site
    Sets up the web site to listen for connections and serve the site.
    Supports customisation of resources based on user details

    @return: Port object
    '''

    if not protectedResource:
        userAccess = UserAccess()
        userAccess.loggedIn = True
        userAccess.readOnly = False
        protectedResource = createRootResource(userAccess)

    site = server.Site(protectedResource)
    site.protocol = HTTPChannel
    site.requestFactory = LargeRequest

    port = reactor.listenTCP(portNum, site).port

    import subprocess
    ip = subprocess.getoutput("/sbin/ifconfig").split("\n")[1].split()[1][5:]

    logger.info('%s is alive and listening on http://%s:%s', name, ip, port)
    return port

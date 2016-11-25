'''
Created on 24/08/2013

@author: synerty
'''
import logging

from twisted.internet import reactor
from twisted.web import server
from twisted.web.http import HTTPChannel

from old.ElementUtil import addPageElement
from rapui import RapuiConfig
from rapui.site.LargeRequest import LargeRequest
from rapui.site.RootResource import createRootResource
from rapui.site.UserAccess import UserAccess

logger = logging.getLogger(__name__)


def setupSite(portNum=0, testSuite=False, debug=False, protectedResource=None):
    ''' Setup Site
    Sets up the web site to listen for connections and serve the site.
    Supports customisation of resources based on user details

    @return: Port object
    '''

    if testSuite:
        from rapui.test import loadTestSuite
        loadTestSuite()

        from rapui.test.TestsElement import TestsElement
        addPageElement('')(TestsElement)

    RapuiConfig.Debug = debug

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

    import rapui
    logger.info('%s is alive and listening on http://%s:%s',
                rapui.TITLE, ip, port)
    return port

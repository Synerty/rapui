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
import sys

from twisted.internet import reactor, defer
from twisted.web.resource import ErrorPage

from txhttputil.site.FileUnderlayResource import FileUnderlayResource
from txhttputil.site.SiteUtil import setupSite

testUnicode = '''
double hyphen :-( — “fancy quotes”
'''

def main():
    defer.setDebugging(True)
    setupLogging()

    rootResource = FileUnderlayResource()
    rootResource.addFileSystemRoot(os.path.dirname(__file__)) # Add here as a test

    rootResource.putChild(b"test", ErrorPage(200, "This path worked, /test", ""))

    setupSite("txHttpUtil Test Siteport", rootResource)

    reactor.run()


if __name__ == '__main__':
    main()

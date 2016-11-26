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

from rapui.site.FileUnderlayResource import FileUnderlayResource
from rapui.site.SiteUtil import setupSite

testUnicode = '''
double hyphen :-( — “fancy quotes”
'''

def main():
    defer.setDebugging(True)

    # import pydevd
    # pydevd.settrace(suspend=False)


    # Setup the logger AFTER the alembic migration.
    logging.basicConfig(format='%(asctime)s %(levelname)s:%(name)s:%(message)s'
                        , datefmt='%d-%b-%Y %H:%M:%S'
                        , level=logging.DEBUG
                        , stream=sys.stdout)

    logger = logging.getLogger(name="rapui_server")

    rootResource = FileUnderlayResource()
    rootResource.addFileSystemRoot(os.path.dirname(__file__)) # Add here as a test

    rootResource.putChild(b"test", ErrorPage(200, "This path worked, /test", ""))

    port = 8000
    setupSite("RapUI Test Siteport", rootResource)

    reactor.run()


if __name__ == '__main__':
    main()

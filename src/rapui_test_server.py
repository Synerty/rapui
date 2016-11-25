"""
 * Created by Synerty Pty Ltd
 *
 * This software is open source, the MIT license applies.
 *
 * Website : http://www.synerty.com
 * Support : support@synerty.com
"""

import logging
import sys

from twisted.internet import reactor, defer

from rapui.site.SiteUtil import setupSite


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

    port = 8000
    setupSite("RapUI Test Siteport")

    reactor.run()


if __name__ == '__main__':
    main()

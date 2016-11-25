""" 
 * synlacky_server.py
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
import sys

from twisted.internet import reactor, defer

from rapui.site.Site import setupSite


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
    setupSite(port, testSuite=True, debug=True)

    logger.info('RapUI alive and listening on port %s' % port)
    reactor.run()


if __name__ == '__main__':
    main()

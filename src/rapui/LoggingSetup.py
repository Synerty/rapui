import logging

import sys


def setup():

    logging.basicConfig(format='%(asctime)s %(levelname)s %(name)s:%(message)s'
                        , datefmt='%d-%b-%Y %H:%M:%S'
                        , level=logging.DEBUG)

    # logging.getLogger('rapui.site.JavascriptResource').setLevel(logging.INFO)
    # logging.getLogger('rapui.site.StyleResource').setLevel(logging.INFO)

    logging.getLogger('suds.client').setLevel(logging.INFO)
    logging.getLogger('suds.transport').setLevel(logging.INFO)
    logging.getLogger('suds.resolver').setLevel(logging.INFO)
    logging.getLogger('suds.mx.core').setLevel(logging.INFO)
    logging.getLogger('suds.mx.literal').setLevel(logging.INFO)
    logging.getLogger('suds.metrics').setLevel(logging.INFO)
    logging.getLogger('suds.wsdl').setLevel(logging.INFO)
    logging.getLogger('suds.xsd.schema').setLevel(logging.INFO)
    logging.getLogger('suds.xsd.query').setLevel(logging.INFO)
    logging.getLogger('suds.xsd.sxbasic').setLevel(logging.INFO)
    logging.getLogger('suds.xsd.sxbase').setLevel(logging.INFO)
    logging.getLogger('suds.umx.typed').setLevel(logging.INFO)

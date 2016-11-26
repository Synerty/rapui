"""
 * Created by Synerty Pty Ltd
 *
 * This software is open source, the MIT license applies.
 *
 * Website : http://www.synerty.com
 * Support : support@synerty.com
"""

import logging

logger = logging.getLogger(__name__)


LARGE_REQUEST_PATHS = None

if not LARGE_REQUEST_PATHS:
    LARGE_REQUEST_PATHS = set()




def removeResourcePaths(paths: [bytes]):
    ''' Remove Resource Paths

    Unregister the resource paths so that the server will no longer respond to them.

    '''
    for path in paths:
        assert isinstance(path, bytes)
        if path in RESOURCES:
            del RESOURCES[path]

        if path in LARGE_REQUEST_PATHS:
            del LARGE_REQUEST_PATHS[path]


def registeredResourcePaths():
    return list(RESOURCES.keys())

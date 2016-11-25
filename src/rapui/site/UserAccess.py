"""
 * Created by Synerty Pty Ltd
 *
 * This software is open source, the MIT license applies.
 *
 * Website : http://www.synerty.com
 * Support : support@synerty.com
"""



class UserAccess(object):
    ''' User Access
    This class stores the details about the user that are required by the
    elements and resources to be able to allow access.
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self.loggedIn = False
        self.readOnly = True
        self.groupId = None

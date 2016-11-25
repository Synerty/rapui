'''
 *
 *  Copyright Synerty Pty Ltd 2013
 *
 *  This software is proprietary, you are not free to copy
 *  or redistribute this code in any format.
 *
 *  All rights to this software are reserved by 
 *  Synerty Pty Ltd
 *
 * Website : http://www.synerty.com
 * Support : support@synerty.com
 *
'''


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

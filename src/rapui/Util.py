""" 
 * SynENCONF.view.Root.py
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
from typing import Generator




def filterModules(name_:str, file_: str) -> [str]:
    import os.path

    for module in os.listdir(os.path.dirname(file_)):
        modName, modExt = module.rsplit('.', 1) if '.' in module else [module, '']
        if modExt not in ('py', 'pyc'):
            continue

        if modName == '__init__':
            continue

        if modName.endswith("Test"):
            continue

        yield '%s.%s' % (name_, module.rsplit('.', 1)[0])

# python
"""
Name:         SMO_CLEANUP_DelLight_Cmd.py

Purpose:      This script is designed to:
              Search for all Light in the scene and Delete them

Author:       Franck ELISABETH (with the help of James O'Hare)
Website:      https://www.linkedin.com/in/smoluck/
Created:      17/02/2020
Copyright:    (c) Franck Elisabeth 2017-2022
"""

import lx
import lxu

Cmd_Name = "smo.CLEANUP.DelLight"


class SMO_Cleanup_DelLight_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
    
    def cmd_Flags(self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO
    
    def cmd_Interact (self):
        pass
    
    def cmd_UserName (self):
        return 'SMO CLEANUP - Delete all Lights'
    
    def cmd_Desc (self):
        return 'Search for all Light in the scene and Delete them.'
    
    def cmd_Tooltip (self):
        return 'Search for all Light in the scene and Delete them.'
    
    def cmd_Help (self):
        return 'https://twitter.com/sm0luck'
    
    def basic_ButtonName (self):
        return 'SMO CLEANUP - Delete all Lights'
    
    def basic_Enable (self, msg):
        return True
        
    
    def basic_Execute(self, msg, flags):
        lx.eval('select.drop item')
        # Select all Lights in scene and Delete them
        lx.eval('select.itemType light super:true')
        try:
            lx.eval('!item.delete')
            lx.out('Light Deleted')
        except:
            lx.out('No Light Deleted')

    
lx.bless(SMO_Cleanup_DelLight_Cmd, Cmd_Name)

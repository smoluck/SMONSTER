# python
"""
# Name:         SMO_CLEANUP_DelCam_Cmd.py
# Version:      1.0
#
# Purpose:      This script is designed to:
#               Search for all camera in the scene and Delete them
#
#
# Author:       Franck ELISABETH (with the help of James O'Hare)
# Website:      https://www.smoluck.com
#
# Created:      17/02/2020
# Copyright:    (c) Franck Elisabeth 2017-2022
"""

import lx
import lxu

Cmd_Name = "smo.CLEANUP.DelCam"


class SMO_Cleanup_DelCam_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
    
    def cmd_Flags(self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO
    
    def cmd_Interact (self):
        pass
    
    def cmd_UserName (self):
        return 'SMO CLEANUP - Delete all Cameras'
    
    def cmd_Desc (self):
        return 'Search for all camera in the scene and Delete them.'
    
    def cmd_Tooltip (self):
        return 'Search for all camera in the scene and Delete them.'
    
    def cmd_Help (self):
        return 'https://twitter.com/sm0luck'
    
    def basic_ButtonName (self):
        return 'SMO CLEANUP - Delete all Cameras'
    
    def basic_Enable (self, msg):
        return True
    
    def basic_Execute(self, msg, flags):
        lx.eval('select.drop item')
        # Select all Camera in scene and Delete them
        lx.eval('select.itemType camera')
        try:
            lx.eval('!item.delete')
            lx.out('Camera Deleted')
        except:
            lx.out('No Camera Deleted')
        

lx.bless(SMO_Cleanup_DelCam_Cmd, Cmd_Name)

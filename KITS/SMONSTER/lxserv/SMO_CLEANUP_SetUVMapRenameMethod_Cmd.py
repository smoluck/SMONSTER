# python
"""
# Name:         SMO_CLEANUP_SetUVMapRenameMethod_Cmd.py
# Version:      1.0
#
# Purpose:      This script is designed to:
#               Set the current Renaming Method for UVMap by setting User Defined Preferences.
#
#
# Author:       Franck ELISABETH
# Website:      https://www.smoluck.com
#
# Created:      21/06/2020
# Copyright:    (c) Franck Elisabeth 2017-2022
"""

import lx
import lxu

Cmd_Name = "smo.CLEANUP.SetUVMapRenameMethod"


class SMO_Cleanup_SetUVMapRenameMethod_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
        self.dyna_Add("Rename By User Pref or Default", lx.symbol.sTYPE_BOOLEAN)
        self.basic_SetFlags (0, lx.symbol.fCMDARG_OPTIONAL)             # here the (0) define the argument index.
    
    def cmd_Flags(self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO
    
    def cmd_Interact (self):
        pass
    
    def cmd_UserName (self):
        return 'SMO CLEANUP - Set UVMap Rename Method'
    
    def cmd_Desc (self):
        return 'Set the current Renaming Method for UVMap by setting User Defined Preferences.'
    
    def cmd_Tooltip (self):
        return 'Set the current Renaming Method for UVMap by setting User Defined Preferences.'
    
    def cmd_Help (self):
        return 'https://twitter.com/sm0luck'
    
    def basic_ButtonName (self):
        return 'SMO CLEANUP - Set UVMap Rename Method'
    
    def basic_Enable (self, msg):
        return True
    
    def basic_Execute(self, msg, flags):
        # # ------------- ARGUMENTS ------------- #
        RenameByDefault = self.dyna_Bool (0)
        # # ------------- ARGUMENTS ------------- #
        if RenameByDefault == 1 :
            lx.eval('user.value SMO_UseVal_CLEANUP_FullAuto_RenameUVToDefault true')
            lx.eval('user.value SMO_UseVal_CLEANUP_FullAuto_RenameUVToUserPref false')
        if RenameByDefault == 0 :
            lx.eval('user.value SMO_UseVal_CLEANUP_FullAuto_RenameUVToDefault false')
            lx.eval('user.value SMO_UseVal_CLEANUP_FullAuto_RenameUVToUserPref true')
        
    
lx.bless(SMO_Cleanup_SetUVMapRenameMethod_Cmd, Cmd_Name)

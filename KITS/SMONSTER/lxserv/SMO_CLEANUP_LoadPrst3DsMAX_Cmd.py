# python
"""
# Name:         SMO_CLEANUP_LoadPrst3DsMAX_Cmd.py
# Version:      1.0
#
# Purpose:      This script is designed to:
#               Load the 3DsMAX Default Channel Preset in the
#               Preferences to be used by the Batch Cleaner command.
#
# Author:       Franck ELISABETH
# Website:      https://www.smoluck.com
#
# Created:      19/12/2019
# Copyright:    (c) Franck Elisabeth 2017-2022
"""

import lx
import lxu

Cmd_Name = "smo.CLEANUP.LoadPrst3DsMAX"


class SMO_Cleanup_LoadPrst3DsMAX_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
    def cmd_Flags(self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO
    
    def cmd_Interact (self):
        pass
    
    def cmd_UserName (self):
        return 'SMO CLEANUP - Load 3DsMAX Default Channel Preset'
    
    def cmd_Desc (self):
        return 'Load the 3DsMAX Default Channel Preset in the Preferences to be used by the Batch Cleaner command.'
    
    def cmd_Tooltip (self):
        return 'Load the 3DsMAX Default Channel Preset in the Preferences to be used by the Batch Cleaner command.'
    
    def cmd_Help (self):
        return 'https://twitter.com/sm0luck'
    
    def basic_ButtonName (self):
        return 'SMO CLEANUP - Load 3DsMAX Default Channel Preset'
    
    def basic_Enable (self, msg):
        return True
    
    def basic_Execute(self, msg, flags):
        lx.eval('user.value SMO_UseVal_CLEANUP_FullAuto_FBXChan_String_A FBX_UDP3DSMAX')
        lx.eval('user.value SMO_UseVal_CLEANUP_FullAuto_FBXChan_String_B FBX_MaxHandle')
        lx.eval('user.value SMO_UseVal_CLEANUP_FullAuto_FBXChan_String_C FBX_mrdisplacementmethod')
        lx.eval('user.value SMO_UseVal_CLEANUP_FullAuto_FBXChan_String_D FBX_mrdisplacementedgelength')
        lx.eval('user.value SMO_UseVal_CLEANUP_FullAuto_FBXChan_String_E FBX_mrdisplacementmaxdisplace')
        lx.eval('user.value SMO_UseVal_CLEANUP_FullAuto_FBXChan_String_F FBX_mrdisplacementparametricsubdivisionlevel')
        lx.eval('user.value SMO_UseVal_CLEANUP_FullAuto_FBXChan_String_G ____EMPTY_SLOT____')
        lx.eval('user.value SMO_UseVal_CLEANUP_FullAuto_FBXChan_String_H ____EMPTY_SLOT____')
        lx.eval('user.value SMO_UseVal_CLEANUP_FullAuto_FBXChan_String_I ____EMPTY_SLOT____')
        lx.eval('user.value SMO_UseVal_CLEANUP_FullAuto_FBXChan_String_J ____EMPTY_SLOT____')


lx.bless(SMO_Cleanup_LoadPrst3DsMAX_Cmd, Cmd_Name)

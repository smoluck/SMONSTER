#python
#---------------------------------------
# Name:         SMO_LL_RIZOMUV_SetExePath_Cmd.py
# Version:      1.95
#
# Purpose:      This Command is designed to
#               Set the RizomUV exe path to create the LiveLink.
#               It will prompt a File browser to get the EXE file Location.
#
# Author:       Franck ELISABETH
# Website:      http://www.smoluck.com
#
# Modified:     22/05/2020
# Copyright:    (c) Franck Elisabeth 2017-2022
#---------------------------------------

import lx, lxifc, lxu.command, lxu.select, subprocess, os

CMD_NAME = "smo.LL.RIZOMUV.SetExePath"

class SMO_LL_RIZOMUV_SetExePath_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
    
    def cmd_Flags(self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO
    
    def cmd_Interact (self):
        pass
    
    def cmd_UserName (self):
        return 'SMO RIZOMUV LIVELINK Set EXE Path'
    
    def cmd_Desc (self):
        return 'Set the RizomUV exe path to create the LiveLink. It will prompt a File browser to get the EXE file Location.'
    
    def cmd_Tooltip (self):
        return 'Set the RizomUV exe path to create the LiveLink. It will prompt a File browser to get the EXE file Location.'
    
    def cmd_Help (self):
        return 'https://twitter.com/sm0luck'
    
    def basic_ButtonName (self):
        return 'SMO RIZOMUV LIVELINK Set EXE Path'
    
    def basic_Enable (self, msg):
        return True
    
    
    def basic_Execute(self, msg, flags):
        # MODO version checks. Different versions have different FBX options.
        modo_ver = int(lx.eval ('query platformservice appversion ?'))
        
        lx.eval ('dialog.setup fileOpen')
        lx.eval ('dialog.title "Select RizomUV 2018.X or 2019.X or 2020.X executable file"')
        lx.eval ('dialog.fileTypeCustom format:exe username:{EXE} loadPattern:{*.exe} saveExtension:exe')
        if modo_ver == 801:
            lx.eval ('+dialog.open')
        else:
            lx.eval ('dialog.open')
        rizomuv_exe_path = lx.eval1 ('dialog.result ?')
        lx.eval ('user.value Smo_RizomUVPath {%s}' % rizomuv_exe_path)
        

    def cmd_Query(self, index, vaQuery):
        lx.notimpl()

lx.bless(SMO_LL_RIZOMUV_SetExePath_Cmd, CMD_NAME)

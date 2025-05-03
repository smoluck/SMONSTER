# python
"""
Name:         SMO_LL_RIZOMUV_SetExePath_Cmd.py

Purpose:      This Command is designed to
              Set the RizomUV exe path to create the LiveLink.
              It will prompt a File browser to get the EXE file Location.

Author:       Franck ELISABETH
Website:      https://www.linkedin.com/in/smoluck/
Modified:     22/05/2020
Copyright:    (c) Franck Elisabeth 2017-2022
"""

import lx
import lxu.command
import lxu.select
import sys
import platform
from pathlib import Path

Cmd_Name = "smo.LL.RIZOMUV.SetExePath"


class SMO_LL_RIZOMUV_SetExePath_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
    
    def cmd_Flags(self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO
    
    def cmd_Interact (self):
        pass
    
    def cmd_UserName (self):
        return 'SMO LL RIZOMUV - Set EXE Path'
    
    def cmd_Desc (self):
        return 'Set the RizomUV exe path to create the LiveLink. It will prompt a File browser to get the EXE file Location.'
    
    def cmd_Tooltip (self):
        return 'Set the RizomUV exe path to create the LiveLink. It will prompt a File browser to get the EXE file Location.'
    
    def cmd_Help (self):
        return 'https://twitter.com/sm0luck'
    
    def basic_ButtonName (self):
        return 'SMO LL RIZOMUV - Set EXE Path'
    
    def basic_Enable (self, msg):
        return True

    def basic_Execute(self, msg, flags):
        # MODO version checks. Different versions have different FBX options.
        modo_ver = int(lx.eval ('query platformservice appversion ?'))
        
        lx.eval ('dialog.setup fileOpen')
        lx.eval ('dialog.title "Select RizomUV 2018.X, 2019.X, 2022.X, 2023.X, 2024.X executable file"')

        system = platform.system()
        if system == "Windows":
            lx.eval ('dialog.fileTypeCustom format:exe username:{EXE} loadPattern:{*.exe} saveExtension:exe')
        elif system == "Darwin":  # MacOS
            lx.eval('dialog.fileTypeCustom format:app username:{APP} loadPattern:{*.app} saveExtension:app')

        if modo_ver == 801:
            lx.eval ('+dialog.open')
        else:
            lx.eval ('dialog.open')
        rizomuv_exe_path = lx.eval1 ('dialog.result ?')
        lx.eval ('user.value Smo_RizomUVPath {%s}' % rizomuv_exe_path)
        

    def cmd_Query(self, index, vaQuery):
        lx.notimpl()


lx.bless(SMO_LL_RIZOMUV_SetExePath_Cmd, Cmd_Name)

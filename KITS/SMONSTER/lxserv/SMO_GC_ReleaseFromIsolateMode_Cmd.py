# python
# ---------------------------------------
# Name:         SMO_GC_ReleaseFromIsolateMode_Cmd.py
# Version:      1.0
#
# Purpose:      This script is designed to:
#               Release from Isolate Mode by clearing the Reference System state, and fit the view on current selected mesh.
#               
#
# Author:       Franck ELISABETH
# Website:      http://www.smoluck.com
#
# Created:      23/04/2021
# Copyright:    (c) Franck Elisabeth 2017-2022
# ---------------------------------------

import lx, lxu, modo
from math import degrees

Command_Name = "smo.GC.ReleaseFromIsolateMode"
# smo.GC.ReleaseFromIsolateMode

class SMO_GC_ReleaseFromIsolateMode_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)

    def cmd_Flags(self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO

    def cmd_Interact(self):
        pass

    def cmd_UserName(self):
        return 'SMO GC ReleaseFromIsolateMode'

    def cmd_Desc(self):
        return 'Release from Isolate Mode by clearing the Reference System state, and fit the view on current selected mesh.'

    def cmd_Tooltip(self):
        return 'Release from Isolate Mode by clearing the Reference System state, and fit the view on current selected mesh.'

    def cmd_Help(self):
        return 'https://twitter.com/sm0luck'

    def basic_ButtonName(self):
        return 'SMO GC ReleaseFromIsolateMode'

    def cmd_Flags(self):
        return lx.symbol.fCMD_UNDO

    def basic_Enable(self, msg):
        return True

    def basic_Execute(self, msg, flags):
        lx.eval('item.refSystem {}')
        lx.eval('viewport.fitSelected')
        
lx.bless(SMO_GC_ReleaseFromIsolateMode_Cmd, Command_Name)
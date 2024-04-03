# python
"""
Name:         SMO_CLEANUP_UpdateMat_Cmd.py

Purpose:      This script is designed to:
              Update Materials Smoothing Angle to 179 Degree and
              set ON the Weight by Polygon Area according to SMO Modo Workflow.

Author:       Franck ELISABETH (with the help of James O'Hare)
Website:      https://www.linkedin.com/in/smoluck/
Created:      17/02/2020
Copyright:    (c) Franck Elisabeth 2017-2022
"""

import lx
import lxu

Cmd_Name = "smo.CLEANUP.UpdateMat"


class SMO_Cleanup_UpdateMat_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
        self.Modo_ver = int(lx.eval('query platformservice appversion ?'))
        # lx.out('Modo Version:', self.Modo_ver)

    def cmd_Flags(self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO

    def cmd_Interact(self):
        pass

    def cmd_UserName(self):
        return 'SMO CLEANUP - Update All Materials to SMO MicroBevel Workflow'

    def cmd_Desc(self):
        return 'Update Materials Smoothing Angle to User defined value (via Preferences) and set ON the Weight by Polygon Area according to SMO Modo Workflow.'

    def cmd_Tooltip(self):
        return 'Update Materials Smoothing Angle to User defined value (via Preferences) and set ON the Weight by Polygon Area according to SMO Modo Workflow.'

    def cmd_Help(self):
        return 'https://twitter.com/sm0luck'

    def basic_ButtonName(self):
        return 'SMO CLEANUP - Update All Materials to SMO MicroBevel Workflow'

    def basic_Enable(self, msg):
        return True

    def basic_Execute(self, msg, flags):
        SmoothAngle = lx.eval('user.value SMO_UseVal_CLEANUP_SmoothingAngle ?')
        lx.out('user Smoothing Angle desired value:', SmoothAngle)

        lx.eval('select.drop item')
        lx.eval('select.itemType advancedMaterial')
        if self.Modo_ver <= 1520:
            lx.eval('material.smoothWeight area true')
        else:
            lx.eval('material.smoothAreaWeight area')
        lx.eval('material.smoothWeight angle true')
        lx.eval('item.channel advancedMaterial$smAngle %s' % SmoothAngle)
        lx.eval('select.less')
        # lx.eval('select.drop item')
        # lx.eval('select.item %s' % mesh)
        # lx.eval('hardedge.convert true true')
        # lx.eval('select.drop item')
        lx.eval('select.drop item')


lx.bless(SMO_Cleanup_UpdateMat_Cmd, Cmd_Name)

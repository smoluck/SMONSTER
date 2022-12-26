# python
"""
# Name:         SMO_GC_FreezeHighSubdivPoly_Cmd.py
# Version:      1.0
#
# Purpose:      This script is designed to
#               Freeze the Subdiv or Catmull-Clark polygons in the HighPoly Meshes.
#
# Author:       Franck ELISABETH
# Website:      https://www.smoluck.com
#
# Created:      17/12/2020
# Copyright:    (c) Franck Elisabeth 2017-2022
"""

import lx
import lxu

Cmd_Name = "smo.GC.FreezeHighSubdivPoly"
# smo.GC.FreezeHighSubdivPoly


class SMO_GC_FreezeHighSubdivPoly_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)

    def cmd_Flags(self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO

    def cmd_Interact(self):
        pass

    def cmd_UserName(self):
        return 'SMO GC - Freeze High Subdiv Poly'

    def cmd_Desc(self):
        return 'Freeze the Subdiv or Catmull-Clark polygons in the HighPoly Meshes.'

    def cmd_Tooltip(self):
        return 'Freeze the Subdiv or Catmull-Clark polygons in the HighPoly Meshes.'

    def cmd_Help(self):
        return 'https://twitter.com/sm0luck'

    def basic_ButtonName(self):
        return 'SMO GC - Freeze High Subdiv Poly'

    def basic_Enable(self, msg):
        return True

    def basic_Execute(self, msg, flags):
        lx.eval('select.drop item')
        lx.eval('smo.GC.CreateDeleteSelSetFromMTypTag 1')
        # Selection HighPoly Meshes
        lx.eval('smo.GC.SelectMTypMesh 2')
        ###############
        lx.eval('smo.GC.FreezeSubdivPoly')
        lx.eval('smo.GC.SelectMTypMesh 2')
        ###############
        lx.eval('smo.GC.CreateDeleteSelSetFromMTypTag 1')
        lx.eval('select.drop item')

    def cmd_Query(self, index, vaQuery):
        lx.notimpl()


lx.bless(SMO_GC_FreezeHighSubdivPoly_Cmd, Cmd_Name)

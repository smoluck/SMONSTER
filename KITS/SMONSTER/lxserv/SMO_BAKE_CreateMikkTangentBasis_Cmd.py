# python
"""
# Name:         SMO_BAKE_CreateMikkTangentBasis_Cmd.py
# Version:      1.20
#
# Purpose:      This Command is designed to :
#               Select the LowPoly meshes and Create MikkTangent Basis Map.
#
# Author:       Franck ELISABETH
# Website:      https://www.smoluck.com
#
# Modified:     09/07/2020
# Copyright:    (c) Franck Elisabeth 2017-2022
"""

import lx
import lxu.command
import lxu.select

Cmd_Name = "smo.BAKE.CreateMikkTangentBasis"


class SMO_BAKE_CreateMikkTangentBasis_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)

    def cmd_Interact(self):
        pass

    def cmd_UserName(self):
        return 'SMO BAKE - Set Mikk Tangent Basis'

    def cmd_Desc(self):
        return 'Select the LowPoly meshes and Create MikkTangent Basis Map.'

    def cmd_Tooltip(self):
        return 'Select the LowPoly meshes and Create MikkTangent Basis Map.'

    def cmd_Help(self):
        return 'https://twitter.com/sm0luck'

    def basic_ButtonName(self):
        return 'SMO BAKE - Set Mikk Tangent Basis'

    def cmd_Flags(self):
        return lx.symbol.fCMD_UNDO

    def basic_Enable(self, msg):
        return True

    def basic_Execute(self, msg, flags):
        # Create Selection Set from Tags to temporary select Lowpoly, Cage or HighPoly meshes to export them.
        lx.eval('smo.GC.CreateDeleteSelSetFromMTypTag 1')

        # Select target LowPoly Meshes via MTyp Tags
        lx.eval('smo.GC.SelectMTypMesh 0')

        # Apply and Create Mikk Tangent Basis maps
        lx.eval('mesh.mikktspacegen')

        # CLEANUP scene
        # Delete Temporary Selection Set (from Tags) of Lowpoly, Cage or HighPoly meshes
        lx.eval('smo.GC.CreateDeleteSelSetFromMTypTag 0')
        lx.eval('select.drop item')


lx.bless(SMO_BAKE_CreateMikkTangentBasis_Cmd, Cmd_Name)

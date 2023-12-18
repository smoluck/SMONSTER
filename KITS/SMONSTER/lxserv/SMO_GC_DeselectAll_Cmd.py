# python
"""
Name:         SMO_GC_DeselectAll_Cmd.py

Purpose:      This script is designed to
              Deselect anything in the current scene. Items(Meshes, Lights, etc) / Materials or Schematic Nodes.

Author:       Franck ELISABETH (with the help of Pavel Efimov)
Website:      https://www.linkedin.com/in/smoluck/
Created:      26/03/2021
Copyright:    (c) Franck Elisabeth 2017-2022
"""

import lx
import lxu

Cmd_Name = "smo.GC.DeselectAll"
# smo.GC.DeselectAll


class SMO_GC_DeselectAll_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)

    def cmd_Flags(self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO

    def cmd_Interact(self):
        pass

    def cmd_UserName(self):
        return 'SMO GC - Deselect Anything'

    def cmd_Desc(self):
        return 'Deselect anything in the current scene. Items(Meshes, Lights, etc) / Materials or Schematic Nodes.'

    def cmd_Tooltip(self):
        return 'Deselect anything in the current scene. Items(Meshes, Lights, etc) / Materials or Schematic Nodes.'

    def cmd_Help(self):
        return 'https://twitter.com/sm0luck'

    def basic_ButtonName(self):
        return 'SMO GC - Deselect Anything'

    def basic_Enable(self, msg):
        return True

    def basic_Execute(self, msg, flags):
        lx.eval('select.clear item')
        lx.eval('select.drop schmNode')
        lx.eval('select.drop channel')
        lx.eval('select.drop link')


lx.bless(SMO_GC_DeselectAll_Cmd, Cmd_Name)

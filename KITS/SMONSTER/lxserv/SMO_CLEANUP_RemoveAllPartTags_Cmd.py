# python
# ---------------------------------------
# Name:         SMO_CLEANUP_RemoveAllPartTags_Cmd.py
# Version:      1.0
#
# Purpose:      Check for all Meshes in the current scene remove any part tags in it.
#
# Author:       Franck ELISABETH
# Website:      http://www.smoluck.com
#
# Created:      21/10/2021
# Copyright:    (c) Franck Elisabeth 2017-2022
# ---------------------------------------

import lx, lxu, modo

Command_Name = "smo.CLEANUP.RemoveAllPartTags"
# smo.CLEANUP.RemoveAllPartTags

class SMO_CLEANUP_RemoveAllPartTags_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)

    def cmd_Flags(self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO

    def cmd_Interact(self):
        pass

    def cmd_UserName(self):
        return 'SMO CLEANUP RemoveAllPartTags'

    def cmd_Desc(self):
        return 'Check for all Meshes in the current scene and rename their First UVMap (by Index = 0) to Modo/Preferences/Defaults/Application name.'

    def cmd_Tooltip(self):
        return 'Check for all Meshes in the current scene and rename their First UVMap (by Index = 0) to Modo/Preferences/Defaults/Application name.'

    def cmd_Help(self):
        return 'https://twitter.com/sm0luck'

    def basic_ButtonName(self):
        return 'SMO CLEANUP RemoveAllPartTags'

    def basic_Enable(self, msg):
        return True

    def basic_Execute(self, msg, flags):
        scn = modo.scene.current()
        lx.eval('smo.CLEANUP.DelEmptyMeshItem')

        for mesh in scn.items('mesh'):
            mesh.select(True)
            lx.eval('poly.setPart smo_partTagTemp')
            lx.eval('poly.renameTag smo_partTagTemp {} PART')
        lx.eval('smo.GC.DeselectAll')

lx.bless(SMO_CLEANUP_RemoveAllPartTags_Cmd, Command_Name)
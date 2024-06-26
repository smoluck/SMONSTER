# python
"""
Name:         SMO_CLEANUP_RemoveAllPartTags_Cmd.py

Purpose:      Check for all Meshes in the current scene remove any part tags in it.

Author:       Franck ELISABETH
Website:      https://www.linkedin.com/in/smoluck/
Created:      21/10/2021
Copyright:    (c) Franck Elisabeth 2017-2022
"""

import lx
import lxu
import modo

Cmd_Name = "smo.CLEANUP.RemoveAllPartTags"
# smo.CLEANUP.RemoveAllPartTags


class SMO_CLEANUP_RemoveAllPartTags_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)

    def cmd_Flags(self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO

    def cmd_Interact(self):
        pass

    def cmd_UserName(self):
        return 'SMO CLEANUP - Remove All Part Tags'

    def cmd_Desc(self):
        return 'Check for all Meshes in the current scene remove any part tags in it.'

    def cmd_Tooltip(self):
        return 'Check for all Meshes in the current scene remove any part tags in it.'

    def cmd_Help(self):
        return 'https://twitter.com/sm0luck'

    def basic_ButtonName(self):
        return 'SMO CLEANUP - Remove All Part Tags'

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


lx.bless(SMO_CLEANUP_RemoveAllPartTags_Cmd, Cmd_Name)

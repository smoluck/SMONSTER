# python
"""
Name:         SMO_CLEANUP_UnparentInPlace_Cmd.py

Purpose:      This script is designed to:
              Search if a specific UV Map exist, select it and rename it
              via String Argument.

Author:       Franck ELISABETH (with the help of James O'Hare)
Website:      https://www.linkedin.com/in/smoluck/
Created:      17/02/2020
Copyright:    (c) Franck Elisabeth 2017-2022
"""

import lx
import lxu
import modo

Cmd_Name = "smo.CLEANUP.UnparentInPlace"


class SMO_Cleanup_UnparentInPlace_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
    
    def cmd_Flags(self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO
    
    def cmd_Interact (self):
        pass
    
    def cmd_UserName (self):
        return 'SMO CLEANUP - Unparent in place'
    
    def cmd_Desc (self):
        return 'Unparent all Meshes in current Scene.'
    
    def cmd_Tooltip (self):
        return 'Unparent all Meshes in current Scene.'
    
    def cmd_Help (self):
        return 'https://twitter.com/sm0luck'
    
    def basic_ButtonName (self):
        return 'SMO CLEANUP - Unparent in place'
    
    def basic_Enable (self, msg):
        return True
    
    def basic_Execute(self, msg, flags):
        scene = modo.scene.current()
        lx.eval('select.drop item')
        lx.eval('select.itemType mesh')
        mesh_list = scene.selectedByType(lx.symbol.sTYPE_MESH)
        for mesh in mesh_list:
            mesh.select(True)
            try:
                lx.eval('!item.parent parent:{} inPlace:1')
            except:
                lx.out('Mesh Item is at the Scene Root level')
        lx.eval('select.drop item')
        
    
lx.bless(SMO_Cleanup_UnparentInPlace_Cmd, Cmd_Name)

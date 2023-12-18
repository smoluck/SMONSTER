# python
"""
Name:         SMO_GC_SetVertexNormal_Cmd

Purpose:      This script is designed to:
              Set Vertex Normals on current Selection using user
              preferences VertexNormalMap name string.

Author:       Franck ELISABETH
Website:      https://www.linkedin.com/in/smoluck/
Created:      28/05/2021
Copyright:    (c) Franck Elisabeth 2017-2022
"""

import lx
import lxu

Cmd_Name = "smo.GC.SetVertexNormal"
# smo.GC.SetVertexNormal


class SMO_GC_SetVertexNormal_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)

    def cmd_Flags(self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO

    def cmd_Interact(self):
        pass

    def cmd_UserName(self):
        return 'SMO GC - Set Vertex Normal'

    def cmd_Desc(self):
        return 'Set Vertex Normals on current Selection using user preferences VertexNormalMap name string.'

    def cmd_Tooltip(self):
        return 'Set Vertex Normals on current Selection using user preferences VertexNormalMap name string.'

    def cmd_Help(self):
        return 'https://twitter.com/sm0luck'

    def basic_ButtonName(self):
        return 'SMO GC - Set Vertex Normal'

    def basic_Enable(self, msg):
        return True

    def basic_Execute(self, msg, flags):
        VNMapName = lx.eval('pref.value application.defaultVertexNormals ?')
        # print(VNMapName)
        lx.eval('vertMap.normals {%s} normalize:false' % VNMapName)


lx.bless(SMO_GC_SetVertexNormal_Cmd, Cmd_Name)

# python
"""
Name:         SMO_GC_ResetVertexNormal_Cmd

Purpose:      This script is designed to:
              Clear Vertex Normals on current Selection using user preferences
              VertexNormalMap name string and set it again.

Author:       Franck ELISABETH
Website:      https://www.linkedin.com/in/smoluck/
Created:      06/12/2021
Copyright:    (c) Franck Elisabeth 2017-2022
"""

import lx
import lxu
import modo

Cmd_Name = "smo.GC.ResetVertexNormal"
# smo.GC.ResetVertexNormal


class SMO_GC_ResetVertexNormal_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)

    def cmd_Flags(self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO

    def cmd_Interact(self):
        pass

    def cmd_UserName(self):
        return 'SMO GC - Reset Vertex Normal Map'

    def cmd_Desc(self):
        return 'Clear Vertex Normals on current Selection using user preferences VertexNormalMap name string and set it again.'

    def cmd_Tooltip(self):
        return 'Clear Vertex Normals on current Selection using user preferences VertexNormalMap name string and set it again.'

    def cmd_Help(self):
        return 'https://twitter.com/sm0luck'

    def basic_ButtonName(self):
        return 'SMO GC - Reset Vertex Normal Map'

    def basic_Enable(self, msg):
        return True

    def basic_Execute(self, msg, flags):
        scene = modo.scene.current()
        m = modo.Mesh()
        # print(m)
        # print(m.name)

        VNMapName = lx.eval('pref.value application.defaultVertexNormals ?')
        # print(VNMapName)

        maps = m.geometry.vmaps.getMapsByType([lx.symbol.i_VMAP_NORMAL])
        # print(len(maps))

        if len(maps) == 0:
            lx.eval('smo.GC.SetVertexNormal')
            #print('New VNrm Maps created')
            #print('VNrm map name is: %s' % VNMapName)

        if len(maps) > 0:
            if maps[0].name == VNMapName:
                lx.eval('select.vertexMap {%s} norm replace' % VNMapName)
                lx.eval('vertMap.clear norm')
                lx.eval('vertMap.normals {%s} normalize:false' % VNMapName)


lx.bless(SMO_GC_ResetVertexNormal_Cmd, Cmd_Name)

# python
"""
Name:         SMO_GC_SelectPolyByVertCount_Cmd.py

Purpose:      This script is designed to:
              Select Polygons based on the vertex count they share.
              Select Mesh Layers and run.

Author:       Franck ELISABETH (with the help of Tom Dymond)
Website:      https://www.linkedin.com/in/smoluck/
Created:      08/07/2019
Copyright:    (c) Franck Elisabeth 2017-2022
"""

import lx
import lxu
import modo

Cmd_Name = "smo.GC.SelectPolyByVertCount"


class SMO_GC_SelectPolyByVertCount_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
        self.dyna_Add("vertNumber", lx.symbol.sTYPE_INTEGER)

    def cmd_Flags(self):
        return lx.symbol.fCMD_UNDO | lx.symbol.fCMD_MODEL

    def cmd_UserName(self):
        return 'SMO GC - Select poly by Vertex Count'

    def cmd_Desc(self):
        return 'Select polygons based on Vertex Count.'

    def cmd_Tooltip(self):
        return 'Select polygons based on Vertex Count.'

    def basic_ButtonName(self):
        return 'SMO GC - Select poly by Vertex Count'

    def cmd_Help(self):
        return 'https://twitter.com/sm0luck'

    def basic_Execute(self, msg, flags):
        lx.out('basic execute')
        vertNo = self.dyna_Int(0)
        print(vertNo)
        scene = modo.Scene()
        for mesh in scene.selectedByType(modo.c.MESH_TYPE):
            geo = mesh.geometry
            for poly in geo.polygons:
                if poly.numVertices == vertNo:
                    poly.select()


lx.bless(SMO_GC_SelectPolyByVertCount_Cmd, Cmd_Name)

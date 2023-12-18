# python
"""
Name:         SMO_GC_SelectStillImageItem_Cmd.py

Purpose:      This script is designed to
              get used in Static analysis. It checks if a mesh have a VertexNormal Map.

Author:       Franck ELISABETH (with the help of Tom Dymond)
Website:      https://www.linkedin.com/in/smoluck/
Created:      06/12/2021
Copyright:    (c) Franck Elisabeth 2017-2022
"""

# Is there some code example to add more checking process to the Static Analysis Tree ?
# I'm looking for adding VertexNormals presence on mesh for instance

# You can take a look at the once provided by modo:
# https://learn.foundry.com/modo/content/help/pages/modeling/edit_geometry/static_analysis.html

import modo
import lx, lxifc, lxu
import lxu.command as SAC

Cmd_Name = "smo.SA.VNormalCheck"


class SMO_SA_VNormalCheck(SAC.StaticAnalysisCommand):
    def __init__(self):
        SAC.StaticAnalysisCommand.__init__(self)

    def sa_Name(self):
        return "SMO SA VNormalCheck"

    def sa_Category(self):
        return "SMONSTER"

    def sa_Test(self, item=None):
        VNMapName = lx.eval('pref.value application.defaultVertexNormals ?')
        Result = ""
        m = modo.Mesh(item)
        maps = m.geometry.vmaps.getMapsByType([lx.symbol.i_VMAP_NORMAL])
        if len(maps) > 0:
            if maps[0].name == VNMapName:
                # Result = ("%s - GOOD" % (maps[0].name))
                return ""
        if len(maps) == 0:
            Result = "No VNormMap - BAD"
            return Result
        # return ""

    def sa_Fix(self, item=None):
        # do something
        # m = modo.Mesh(item)
        # maps = m.geometry.vmaps.getMapsByType([lx.symbol.i_VMAP_NORMAL])
        # if len(maps) == 0:
        lx.eval("select.item item:{} replace".format(item.Ident()))
        lx.eval('smo.GC.SetVertexNormal')
        return

    def sa_ToolTip(self):
        return "Does the mesh has Vertex Normal Map ?"

    def sa_ItemType(self):
        return "mesh"


SAC.RegisterStaticAnalysisTest(SMO_SA_VNormalCheck, Cmd_Name)

# python
"""
# Name:         SMO_GC_ConvertToHardEdgeWorkflowUsingGeoBoundaryAsHardEdge_Cmd.py
# Version:      1.0
#
# Purpose:      This script is designed to:
#               On current Mesh item, convert Shading Method to HardEdge Workflow using geometry boundary
#               as "HardEdge" and set all other Edges as "Smooth".
#
#
# Author:       Franck ELISABETH
# Website:      https://www.smoluck.com
#
# Created:      11/05/2022
# Copyright:    (c) Franck Elisabeth 2017-2022
"""

import lx
import lxu
import modo

Cmd_Name = "smo.GC.ConvertToHardEdgeWorkflowUsingGeoBoundaryAsHardEdge"
# smo.GC.ConvertToHardEdgeWorkflowUsingGeoBoundaryAsHardEdge 1


class SMO_GC_ConvertToHardEdgeWorkflowUsingGeoBoundaryAsHardEdge_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
        self.dyna_Add("Keep VertexNormals Data", lx.symbol.sTYPE_BOOLEAN)
        # self.basic_SetFlags(0, lx.symbol.fCMDARG_OPTIONAL)  # here the (0) define the argument index.
        self.dyna_Add("Merge Vertex from GeoEdgeBoundary, to make mesh airtight", lx.symbol.sTYPE_BOOLEAN)
        # self.basic_SetFlags(1, lx.symbol.fCMDARG_OPTIONAL)

    def cmd_Flags(self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO

    def cmd_Interact(self):
        pass

    def cmd_UserName(self):
        return 'SMO GC - Convert to HardEdge Workflow using geometry boundary as HardEdge'

    def cmd_Desc(self):
        return 'On current Mesh item, convert Shading Method to HardEdge Workflow using geometry boundary as "HardEdge" and set all other Edges as "Smooth".'

    def cmd_Tooltip(self):
        return 'On current Mesh item, convert Shading Method to HardEdge Workflow using geometry boundary as "HardEdge" and set all other Edges as "Smooth".'

    def cmd_Help(self):
        return 'https://twitter.com/sm0luck'

    def basic_ButtonName(self):
        return 'SMO GC - Convert to HardEdge Workflow using geometry boundary as HardEdge'

    def basic_Enable(self, msg):
        return True

    def basic_Execute(self, msg, flags):
        scene = modo.scene.current()

        KeepVNrmData = self.dyna_Bool(0)
        MergeVertexBorders = self.dyna_Bool(1)

        meshes_list = scene.selectedByType(lx.symbol.sITYPE_MESH)

        hardedgemode = lx.eval('hardedge.setDefault ?')
        if hardedgemode != "auto":
            lx.eval('hardedge.setDefault auto')

        # Convert all VertexNormal Data to HardEdge Workflow and set HardEdge to all Geometry Boundary
        for mesh in meshes_list:
            mesh.select(True)
            if not KeepVNrmData:
                lx.eval('hardedge.convert true true')
            if KeepVNrmData:
                lx.eval('hardedge.convert true false')
            polys_count = lx.eval1('query layerservice poly.N ? all')
            if polys_count > 0:
                lx.eval('@AddBoundary.py')
                lx.eval('hardedge.set hard clear:true')
                lx.eval('select.drop edge')
                lx.eval('select.type item')
        lx.eval('smo.GC.DeselectAll')
        lx.eval('hardedge.setDefault {%s}' % hardedgemode)

        # Merge all together resulting Meshes
        for item in meshes_list:
            lx.eval("schematic.addItem {%s}" % item.name)
        lx.eval('layer.mergeMeshes true')

        # make the mesh airtight so every Geo Boundary vertex are merged by 1 um
        if MergeVertexBorders:
            lx.eval('@AddBoundary.py')
            lx.eval('select.convert vertex')
            lx.eval('!vert.merge fixed false 0.000001 false false')

        lx.eval('select.type item')
        lx.eval('smo.GC.DeselectAll')


lx.bless(SMO_GC_ConvertToHardEdgeWorkflowUsingGeoBoundaryAsHardEdge_Cmd, Cmd_Name)

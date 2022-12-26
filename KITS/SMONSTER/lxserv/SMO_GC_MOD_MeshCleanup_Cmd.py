# python
"""
# Name:         SMO_GC_MOD_MeshCleanup_Cmd.py
# Version:      1.0
#
# Purpose:      This script is designed to:
#               Do a Mesh Cleanup of the current Mesh (only visible components)
#               using Vertex merge by distance in Arguments. As well it can
#               MergeCoplanar Polygons if one polygon is selected and then remove
#               All Colinear Vertex and finaly Triple the resulting Ngon.
#
# Author:       Franck ELISABETH
# Website:      https://www.smoluck.com
#
# Created:      03/06/2021
# Copyright:    (c) Franck Elisabeth 2017-2022
"""

import lx
import lxu
import modo

Cmd_Name = "smo.GC.MOD.MeshCleanup"
# smo.GC.MOD.MeshCleanup [2um] 1
# Using Square Brackets around values validate the use of units like "km", "m" , "cm", "mm", "um".


class SMO_GC_MOD_MeshCleanup_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
        self.dyna_Add("Merge Distance Value", lx.symbol.sTYPE_DISTANCE)
        self.dyna_Add("Flat Merge Mode", lx.symbol.sTYPE_INTEGER)
        self.basic_SetFlags (1, lx.symbol.fCMDARG_OPTIONAL)             # here the (1) define the argument index.

        self.SelModeVert = bool(lx.eval1("select.typeFrom typelist:vertex;edge;polygon;item ?"))
        self.SelModeEdge = bool(lx.eval1("select.typeFrom typelist:edge;vertex;polygon;item ?"))
        self.SelModePoly = bool(lx.eval1("select.typeFrom typelist:polygon;vertex;edge;item ?"))
        self.SelModeItem = bool(lx.eval1("select.typeFrom typelist:item;vertex;edge;polygon ?"))

    def cmd_Flags(self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO

    def cmd_Interact(self):
        pass

    def cmd_UserName(self):
        return 'SMO GC - Set Move And Rotate Center Using Open Boundary'

    def cmd_Desc(self):
        return 'Select an Opened Mesh Move and Rotate the Center to Open boundary centroid and rotate it (use it in item mode)'

    def cmd_Tooltip(self):
        return 'Select an Opened Mesh Move and Rotate the Center to Open boundary centroid and rotate it (use it in item mode)'

    def cmd_Help(self):
        return 'https://twitter.com/sm0luck'

    def basic_ButtonName(self):
        return 'SMO GC - Set Move And Rotate Center Using Open Boundary'

    def basic_Enable(self, msg):
        return True

    def basic_Execute(self, msg, flags):
        scene = modo.scene.current()
        if self.SelModePoly == True or self.SelModeEdge == True or self.SelModeVert == True :
            lx.eval('smo.MASTER.ForceSelectMeshItemOnly')
        mesh = scene.selectedByType('mesh')[0]

        # ------------------------------ #
        # <----( DEFINE ARGUMENTS )----> #
        # ------------------------------ #
        Dist = self.dyna_Float(0)              # Width size

        MergeModeFlat = self.dyna_Int(1)
        # Expose the Result of the Arguments
        # lx.out(Value)
        # ------------------------------ #
        # <----( DEFINE ARGUMENTS )----> #
        # ------------------------------ #


        # BugFix to preserve the state of the RefSystem (item at origin in viewport)
        # This query only works when an item is selected.
        RefSystemActive = bool()
        CurrentRefSystemItem = lx.eval('item.refSystem ?')
        # print(CurrentRefSystemItem)
        if len(CurrentRefSystemItem) != 0:
            RefSystemActive = True
        else:
            RefSystemActive = False
        # print(RefSystemActive)


        if RefSystemActive:
            lx.eval('item.refSystem {}')



        lx.eval('smo.MASTER.SelectModeDetector')

        VertMode = lx.eval1('user.value SMO_SelectModeDetector_Vert ?')
        EdgeMode = lx.eval1('user.value SMO_SelectModeDetector_Edge ?')
        PolyMode = lx.eval1('user.value SMO_SelectModeDetector_Poly ?')
        ItemMode = lx.eval1('user.value SMO_SelectModeDetector_Item ?')

        NoVert = lx.eval1('user.value SMO_SelectModeDetector_NoVertSelected ?')
        NoEdge = lx.eval1('user.value SMO_SelectModeDetector_NoEdgeSelected ?')
        NoPoly = lx.eval1('user.value SMO_SelectModeDetector_NoPolySelected ?')
        NoItem = lx.eval1('user.value SMO_SelectModeDetector_NoItemSelected ?')

        MultiVert = lx.eval1('user.value SMO_SelectModeDetector_MultiVertSelected ?')
        MultiEdge = lx.eval1('user.value SMO_SelectModeDetector_MultiEdgeSelected ?')
        MultiPoly = lx.eval1('user.value SMO_SelectModeDetector_MultiPolySelected ?')
        MultiItem = lx.eval1('user.value SMO_SelectModeDetector_MultiItemSelected ?')

        CountVert = lx.eval1('user.value SMO_SelectModeDetector_CountVertSelected ?')
        CountEdge = lx.eval1('user.value SMO_SelectModeDetector_CountEdgeSelected ?')
        CountPoly = lx.eval1('user.value SMO_SelectModeDetector_CountPolySelected ?')
        CountItem = lx.eval1('user.value SMO_SelectModeDetector_CountItemSelected ?')

        lx.out('V---------- Selection Mode ----------V')
        lx.out('Vert Mode', VertMode)
        lx.out('Edge Mode', EdgeMode)
        lx.out('Poly Mode', PolyMode)
        lx.out('Item Mode', ItemMode)
        lx.out('V---------- Element Not Selected ----------V')
        lx.out('No Vert Selected', NoVert)
        lx.out('No Edge Selected', NoEdge)
        lx.out('No Poly Selected', NoPoly)
        lx.out('No Item Selected', NoItem)
        lx.out('V---------- At least one Element Selected ----------V')
        lx.out('Multi Vert Selected', MultiVert)
        lx.out('Multi Edge Selected', MultiEdge)
        lx.out('Multi Poly Selected', MultiPoly)
        lx.out('Multi Item Selected', MultiItem)
        lx.out('V---------- At least one Element Selected ----------V')
        lx.out('Vert Count Selected', CountVert)
        lx.out('Multi Count Selected', CountEdge)
        lx.out('Multi Count Selected', CountPoly)
        lx.out('Multi Count Selected', CountItem)


        if CountItem > 0 :
            if self.SelModePoly == True and MergeModeFlat == 1 and CountPoly >= 1 :
                lx.eval('smo.GC.SelectCoPlanarPoly 0 2 0.0')
                lx.eval('select.convert vertex')
                lx.eval('select.type polygon')
                lx.eval('smo.CAD.MergeCoplanarPoly 0 2')

            # -------------------------- #
            # <----( Main Macro )----> #
            # -------------------------- #
            lx.eval('!vert.merge range:fixed keep:false dist:{%f} morph:false disco:false' % Dist)
            lx.eval('select.type item')
            lx.eval('!!mesh.cleanup floatingVertex:true onePointPolygon:true twoPointPolygon:true dupPointPolygon:true colinear:true faceNormal:true mergeVertex:false mergeDisco:true unifyPolygon:true forceUnify:true removeDiscoWeight:true')
            lx.eval('select.type polygon')
            lx.eval('!poly.align')

            if self.SelModePoly == True and MergeModeFlat == 1 and CountPoly >= 1 :
                lx.eval('select.type vertex')
                lx.eval('select.convert polygon')
                lx.eval('poly.triple')

            if self.SelModePoly:
                lx.eval('select.type polygon')
            if self.SelModeEdge:
                lx.eval('select.type edge')
            if self.SelModeVert:
                lx.eval('select.type vertex')


            if not RefSystemActive:
                lx.eval('item.refSystem {}')
            if RefSystemActive:
                lx.eval('item.refSystem %s' % CurrentRefSystemItem)


lx.bless(SMO_GC_MOD_MeshCleanup_Cmd, Cmd_Name)

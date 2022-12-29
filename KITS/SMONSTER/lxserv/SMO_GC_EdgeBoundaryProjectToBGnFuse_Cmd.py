# python
"""
Name:         SMO_GC_EdgeBoundaryProjectToBGnFuse_Cmd.py

Purpose:      This script is designed to:
              Extend the current Opened Boundary Edge Loop to nearest BG Mesh using
              BG Constraint and setting an Edge Bevel + applying a VertexNormalTransfer
              to fuse the border with BG Mesh normals.

Author:       Franck ELISABETH
Website:      https://www.smoluck.com
Created:      04/12/2021
Copyright:    (c) Franck Elisabeth 2017-2022
"""

from math import degrees

import lx
import lxu
import modo
import sys

Cmd_Name = "smo.GC.EdgeBoundaryProjectToBGnFuse"
# smo.GC.EdgeBoundaryProjectToBGnFuse [5mm]


class SMO_GC_EdgeBoundaryProjectToBGnFuse_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
        self.dyna_Add("Witdh Value", lx.symbol.sTYPE_DISTANCE)

        self.SelModeVert = bool(lx.eval1("select.typeFrom typelist:vertex;polygon;edge;item;ptag ?"))
        self.SelModeEdge = bool(lx.eval1("select.typeFrom typelist:edge;vertex;polygon;item ?"))
        self.SelModePoly = bool(lx.eval1("select.typeFrom typelist:polygon;vertex;edge;item ?"))
        self.SelModeItem = bool(lx.eval1("select.typeFrom typelist:item;pivot;center;edge;polygon;vertex;ptag ?"))
        # print(self.SelModeVert)
        # print(self.SelModeEdge)
        # print(self.SelModePoly)
        # print(self.SelModeItem)
        if self.SelModePoly == True or self.SelModeItem == True:
            try:
                self.TargetMeshList = lxu.select.ItemSelection().current()
            except:
                self.TargetMeshList = []

            # If we do have something selected, put it in self.TargetMeshList
            if len(self.TargetMeshList) > 0:
                self.TargetMeshList = self.TargetMeshList
            else:
                self.TargetMeshList = None
            # print(self.TargetMeshList)

    def cmd_Flags(self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO

    def cmd_Interact(self):
        pass

    def cmd_UserName(self):
        return 'SMO GC - EdgeBoundary Project to BG and Fuse'

    def cmd_Desc(self):
        return 'Extend the current Opened Boundary Edge Loop to nearest BG Mesh using BG Constraint and setting an Edge Bevel + applying a VertexNormalTransfer to fuse the border with BG Mesh normals.'

    def cmd_Tooltip(self):
        return 'Extend the current Opened Boundary Edge Loop to nearest BG Mesh using BG Constraint and setting an Edge Bevel + applying a VertexNormalTransfer to fuse the border with BG Mesh normals.'

    def cmd_Help(self):
        return 'https://twitter.com/sm0luck'

    def basic_ButtonName(self):
        return 'SMO GC - EdgeBoundary Project to BG and Fuse'

    def basic_Enable(self, msg):
        return True

    def basic_Execute(self, msg, flags):
        scene = modo.scene.current()
        FGMeshAndBGMeshSame = bool()

        EdgeCount = int(lx.eval('user.value SMO_UseVal_GC_ChamferEdgeCount ?'))
        # lx.out(EdgeCount)
        TransfVNormBG = bool(lx.eval('user.value SMO_UseVal_GC_ProjectNFuseTransfVNorm ?'))
        # lx.out(TransfVNormBG)

        if self.SelModeEdge:
            lx.eval('smo.MASTER.ForceSelectMeshItemOnly')
            lx.eval('select.type edge')
            lx.eval('select.createSet GC_ProjectBGnFuseSource')
            selected_mesh = scene.selectedByType('mesh')[0]
            # print('TargetMesh:', selected_mesh)
            CSourceEdges = len(selected_mesh.geometry.edges.selected)
            # print(CSourceEdges)

        CheckGrpSelItems = lxu.select.ItemSelection().current()
        for item in CheckGrpSelItems:
            itemType = modo.Item(item).type
            item = lx.object.Item(item)
            item_name = item.UniqueName()
            # print(item_name)
            if itemType != "mesh":
                scene.deselect(item_name)

        # Function for Radian to Degree
        def rad(a):
            return [degrees(a)]

        # ------------- ARGUMENTS ------------- #
        # args = lx.args()
        # #lx.out(args)

        ChamferValue = self.dyna_Float(0)  # Width size
        InsetValue = ChamferValue * (-1.5)
        # EdgeSlideValue = ChamferValue * (-2000)
        EdgeSlideValue = -2
        # lx.out('Chamfer Distance value:', ChamferValue)
        # ------------- ARGUMENTS ------------- #

        # ------------------------------ #
        # <----( DEFINE VARIABLES )----> #
        # ------------------------------ #

        # ---------------- Define user value for all the different SafetyCheck --- START
        #####
        lx.eval("user.defNew name:SMO_SafetyCheck_PolygonModeEnabled type:integer life:momentary")

        lx.eval("user.defNew name:SMO_SafetyCheck_ItemModeEnabled type:integer life:momentary")
        lx.eval("user.defNew name:SMO_SafetyCheck_min1PolygonSelected type:integer life:momentary")

        lx.eval("user.defNew name:SMO_SafetyCheck_EdgeModeEnabled type:integer life:momentary")
        lx.eval("user.defNew name:SMO_SafetyCheck_min1EdgeSelected type:integer life:momentary")
        #####
        # ---------------- Define user value for all the different SafetyCheck --- END

        # -------------------------- #
        # <---( SAFETY CHECK 1 )---> #
        # -------------------------- #
        # --------------------  safety check 1: Polygon Selection Mode enabled --- START

        selType = ""
        # Used to query layerservice for the list of polygons, edges or vertices.
        attrType = ""

        if lx.eval1("select.typeFrom typelist:vertex;polygon;edge;item;ptag ?"):
            selType = "vertex"
            attrType = "vert"

            SMO_SafetyCheck_ItemModeEnabled = 0
            SMO_SafetyCheck_PolygonModeEnabled = 0
            SMO_SafetyCheck_EdgeModeEnabled = 0
            lx.eval('dialog.setup info')
            lx.eval('dialog.title {SMO VeNom:}')
            lx.eval('dialog.msg {You must be in Item Mode and have 1 Mesh Layer selected to run that script.}')
            lx.eval('+dialog.open')
            lx.out('script Stopped: You must be in Item Mode and have 1 Mesh Layer selected to run that script.')
            sys.exit
            # sys.exit( "LXe_FAILED:Must be in polygon selection mode." )


        elif lx.eval1("select.typeFrom typelist:edge;vertex;polygon;item ?"):
            selType = "edge"
            attrType = "edge"
            SMO_SafetyCheck_ItemModeEnabled = 0
            SMO_SafetyCheck_PolygonModeEnabled = 0
            SMO_SafetyCheck_EdgeModeEnabled = 1
            # lx.out('script Running: Correct Item Selection Mode')
            # sys.exit( "LXe_FAILED:Must be in polygon selection mode." )

        elif lx.eval1("select.typeFrom typelist:polygon;vertex;edge;item ?"):
            selType = "polygon"
            attrType = "poly"
            SMO_SafetyCheck_ItemModeEnabled = 0
            SMO_SafetyCheck_PolygonModeEnabled = 1
            SMO_SafetyCheck_EdgeModeEnabled = 0
            # lx.out('script Running: Correct Item Selection Mode')
            # sys.exit( "LXe_FAILED:Must be in polygon selection mode." )

        else:
            # This only fails if none of the three supported selection
            # modes have yet been used since the program started, or
            # if "item" or "ptag" (ie: materials) is the current
            # selection mode.
            SMO_SafetyCheck_ItemModeEnabled = 1
            SMO_SafetyCheck_PolygonModeEnabled = 0
            SMO_SafetyCheck_EdgeModeEnabled = 0
            # lx.out('script Running: Correct Item Selection Mode')
        # --------------------  safety check 1: Polygon Selection Mode enabled --- END

        #####-------------------------------------------------------------------------------#####
        ####### Track Mouse Over Selection. Is there a polygon under Mouse and select it. #######
        #####-------------------------------------------------------------------------------#####
        if SMO_SafetyCheck_EdgeModeEnabled == 1:
            # mesh = scene.selectedByType('mesh')[0]
            lx.eval('select.type polygon')
            lx.eval('query view3dservice mouse ?')
            view_under_mouse = lx.eval('query view3dservice mouse.view ?')
            lx.eval('query view3dservice view.index ? %s' % view_under_mouse)
            lx.eval('query view3dservice mouse.pos ?')
            Item_under_mouse = lx.eval('query view3dservice element.over ? ITEM ')
            Poly_under_mouse = lx.eval('query view3dservice element.over ? POLY ')
            # Edge_under_mouse = lx.eval('query view3dservice element.over ? EDGE ')
            hitpos = lx.eval('query view3dservice mouse.hitpos ?')

            # lx.out('View under mouse:', view_under_mouse)
            # lx.out('Hit Position:', hitpos)
            # print('Items under mouse:', Item_under_mouse)
            # print('Polygon under mouse:', Poly_under_mouse)
            # lx.out('Edge under mouse:', Edge_under_mouse)

            # lx.eval('select.drop edge')
            # lx.eval('materials.underMouse')

            success = True

            try:
                scene.select(Item_under_mouse)
                lx.eval('select.3DElementUnderMouse')
                BGmesh = scene.selectedByType('mesh')[0]
                # BGmesh = Item_under_mouse
                # print(BGmesh)
            except:
                success = False
            # print(success)
            if success:
                scene.select(BGmesh)
                lx.eval('select.type polygon')
                lx.eval('select.3DElementUnderMouse')

        # print(selected_mesh.id)
        # print(BGmesh)

        if selected_mesh.id != BGmesh.id:
            FGMeshAndBGMeshSame = False
            # print(FGMeshAndBGMeshSame)
            # print(selected_mesh.id)
            # BGMesh = Item_under_mouse
            # print(BGmesh.id)

        if selected_mesh.id == BGmesh.id:
            FGMeshAndBGMeshSame = True
            lx.eval('select.type item')
            scene.select(selected_mesh)
            lx.eval('select.type polygon')
            lx.eval('select.3DElementUnderMouse')
            lx.eval('select.polygonConnect m3d false')
            lx.eval('smo.CAD.CopyCutAsChildOfCurrentMesh 0 1 4 true')
            BGmesh = scene.selectedByType('mesh')[0]
            del Item_under_mouse
            lx.eval('select.type item')

        # print(selected_mesh.id)
        # print(BGmesh.id)

        if SMO_SafetyCheck_EdgeModeEnabled == 1:
            lx.eval('select.type item')
            lx.eval('smo.GC.DeselectAll')
            scene.select(selected_mesh)
            lx.eval('select.type edge')

        items = scene.selected
        # lx.out('Processed Mesh Item:', items)

        if self.SelModeEdge:
            lx.eval('select.type edge')
            lx.eval('select.useSet GC_ProjectBGnFuseSource replace')
            lx.eval('select.type item')

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

        if not RefSystemActive:
            lx.eval('item.refSystem %s' % items[0].id)

        # target_positions = selected_mesh.transforms.position.get()
        # #lx.out(target_positions)
        # target_rotations = selected_mesh.transforms.rotation.get()
        # #lx.out(target_rotations)

        # -------------------------- #
        # <---( SAFETY CHECK 2 )---> #
        # -------------------------- #
        CsEdges = len(selected_mesh.geometry.edges.selected)
        # at Least 1 Edge is selected --- START
        # lx.out('Count Selected Edge', CsEdges)

        if CsEdges < 1:
            SMO_SafetyCheck_min1EdgeSelected = 0
            lx.eval('dialog.setup info')
            lx.eval('dialog.title {SMO GC EdgeBoundaryProjectToBGnFuse:}')
            lx.eval('dialog.msg {You must mouse over an edge to run that script}')
            lx.eval('+dialog.open')
            lx.out('script Stopped: Mouse over an edge')
            sys.exit

        elif CsEdges >= 1:
            SMO_SafetyCheck_min1EdgeSelected = 1
            # lx.out('script running: right amount of Edges in selection')
        # at Least 1 Edge is selected --- END

        # ---------------- Define current value for the Prerequisite TotalSafetyCheck --- START
        #####
        TotalSafetyCheckTrueValue = 2
        # lx.out('Desired Value', TotalSafetyCheckTrueValue)
        if SMO_SafetyCheck_ItemModeEnabled == 1:
            TotalSafetyCheck = (SMO_SafetyCheck_ItemModeEnabled + SMO_SafetyCheck_min1EdgeSelected)
            # lx.out('Current Value', TotalSafetyCheck)

        if SMO_SafetyCheck_EdgeModeEnabled == 1:
            TotalSafetyCheck = (SMO_SafetyCheck_EdgeModeEnabled + SMO_SafetyCheck_min1EdgeSelected)
            # lx.out('Current Value', TotalSafetyCheck)

        #####
        # ---------------- Define current value for the Prerequisite TotalSafetyCheck --- END

        Modo_ver = int(lx.eval('query platformservice appversion ?'))
        # print('Modo Version:', Modo_ver)

        # ------------------------ #
        # <----( Main Macro )----> #
        # ------------------------ #

        # ---------------- Compare TotalSafetyCheck value and decide or not to continue the process  --- START
        # Isolate the 2 Targeted Meshes (FG and BG)
        lx.eval('select.type item')
        scene.select(selected_mesh)
        BGmesh.select(replace=False)
        lx.eval('hide.unsel')
        lx.eval('smo.GC.DeselectAll')
        scene.select(selected_mesh)

        # Manual Selection Mode via a set of edges
        if SMO_SafetyCheck_EdgeModeEnabled == 1:
            scene.select(selected_mesh)
            lx.eval('select.type edge')

            lx.eval('select.edgeLoop base false m3d middle')
            lx.eval('select.createSet GC_ProjectBGnFuseEdgeLoop')
            lx.eval('select.convert vertex')
            lx.eval('select.createSet GC_ProjectBGnFuseVertexLoop')
            lx.eval('select.type edge')
            lx.eval('select.expand')
            lx.eval('select.convert vertex')
            lx.eval('select.convert polygon')
            lx.eval('select.createSet GC_ProjectBGnFusePolyLoop')
            lx.eval('select.type edge')
            lx.eval('select.edge remove bond equal (none)')
            # lx.eval('workPlane.state true')
            lx.eval('select.useSet GC_ProjectBGnFuseEdgeLoop replace')
            lx.eval('meshConstraint.state true')
            lx.eval('tool.attr const.bg geometry vector')
            lx.eval('tool.attr const.bg dblSided true')

            # Transform solution for Projection
            # lx.eval('select.convert vertex')
            # lx.eval('tool.set TransformMove on')
            # lx.eval('tool.set actr.origin on')
            # lx.eval('tool.attr xfrm.transform TX %s' % EdgeSlideValue)
            # lx.eval('tool.setAttr xfrm.transform TX %s' % EdgeSlideValue)
            # lx.eval('tool.doApply')
            # lx.eval('meshConstraint.state false')
            # lx.eval('workPlane.state false')
            # lx.eval('tool.set actr.origin off')

            # EdgeSlide solution  for Projection
            lx.eval('tool.set edge.Slide on')
            lx.eval('tool.setAttr edge.slide mode radial')
            lx.eval('tool.setAttr edge.slide interpolation distance')

            lx.eval('tool.setAttr edge.slide merge false')
            lx.eval('tool.setAttr edge.slide stop false')
            lx.eval('tool.setAttr edge.slide duplicate false')
            lx.eval('tool.setAttr edge.slide loop true')
            lx.eval('tool.setAttr edge.slide curvature false')

            lx.eval('tool.setAttr edge.slide dist %s' % EdgeSlideValue)
            lx.eval('tool.doApply')
            lx.eval('meshConstraint.state false')

            lx.eval('select.type edge')
            lx.eval('select.useSet GC_ProjectBGnFuseEdgeLoop replace')
            lx.eval('poly.make auto')
            lx.eval('select.convert polygon')
            lx.eval('tool.set *.bevel on')
            lx.eval('tool.noChange')
            lx.eval('tool.attr poly.bevel autoWeld false')
            lx.eval('tool.attr poly.bevel inset %s' % InsetValue)
            lx.eval('tool.doApply')
            lx.eval('tool.set *.bevel off')

            lx.eval('script.run "macro.scriptservice:92663570022:macro"')
            lx.eval('select.convert polygon')
            lx.eval('delete')
            lx.eval('select.type edge')
            lx.eval('select.expand')
            lx.eval('select.convert vertex')
            lx.eval('select.convert polygon')
            lx.eval('select.createSet GC_ProjectBGnFusePolyExtended')
            lx.eval('script.run "macro.scriptservice:92663570022:macro"')
            lx.eval('select.edge remove bond equal (none)')

            lx.eval('smo.GC.ChamferEdgesByUnit %s' % ChamferValue)
            lx.eval('select.type polygon')
            lx.eval('select.useSet GC_ProjectBGnFusePolyExtended replace')
            lx.eval('script.run "macro.scriptservice:92663570022:macro"')
            lx.eval('select.vertex remove edge equal 4')
            lx.eval('select.expand')
            lx.eval('select.convert polygon')
            lx.eval('select.createSet GC_ProjectBGnFusePolyFuse')

            lx.eval('select.convert vertex')
            if TransfVNormBG:
                lx.eval('vertMap.transferNormals false')
            lx.eval('select.convert polygon')
            lx.eval('delete')
            lx.eval('select.deleteSet GC_ProjectBGnFusePolyLoop')
            lx.eval('select.deleteSet GC_ProjectBGnFusePolyExtended')
            lx.eval('select.type vertex')
            lx.eval('select.deleteSet GC_ProjectBGnFuseVertexLoop')
            lx.eval('select.type edge')
            lx.eval('select.deleteSet GC_ProjectBGnFuseEdgeLoop')
            lx.eval('select.deleteSet GC_ProjectBGnFuseSource')
            lx.eval('select.drop edge')

        if not RefSystemActive:
            lx.eval('item.refSystem {}')

        # if VeNomItemAsRotation == True :
        #     # Set back the Rotation of the Target item
        #     scene.select(TargetRotXfrm)
        #     TargetOutputRot = [(TargetRotXAngle[0]), (TargetRotYAngle[0]), (TargetRotZAngle[0])]
        #     # print(TargetOutputRot)
        #     # print(TargetOutputRot[0])
        #     # print(TargetOutputRot[1])
        #     # print(TargetOutputRot[2])
        #
        #     lx.eval('select.channel {%s:rot.X} set' % TargetRotXfrm)
        #     lx.eval('channel.value {%s} channel:{%s:rot.X}' % (TargetOutputRot[0], TargetRotXfrm))
        #     lx.eval('select.channel {%s:rot.Y} set' % TargetRotXfrm)
        #     lx.eval('channel.value {%s} channel:{%s:rot.Y}' % (TargetOutputRot[1], TargetRotXfrm))
        #     lx.eval('select.channel {%s:rot.Z} set' % TargetRotXfrm)
        #     lx.eval('channel.value {%s} channel:{%s:rot.Z}' % (TargetOutputRot[2], TargetRotXfrm))
        #     lx.eval('smo.GC.DeselectAll')

        if SMO_SafetyCheck_EdgeModeEnabled == 1:
            lx.eval('select.type item')
            lx.eval('unhide')
            lx.eval('smo.GC.DeselectAll')
            if FGMeshAndBGMeshSame:
                scene.select(BGmesh)
                lx.eval('select.type item')
                lx.eval('!delete')
            scene.select(selected_mesh)
            lx.eval('select.type edge')


lx.bless(SMO_GC_EdgeBoundaryProjectToBGnFuse_Cmd, Cmd_Name)

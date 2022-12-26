# python
"""
# Name:         SMO_GC_StraightenEdgeBoundary_Cmd.py
# Version:      1.0
#
# Purpose:      This script is designed to:
#               Flatten the selected Edge Boundary to fix squeeze.
#
# Author:       Franck ELISABETH
# Website:      https://www.smoluck.com
#
# Created:      04/12/2021
# Copyright:    (c) Franck Elisabeth 2017-2022
"""

import lx
import lxu
import math
import modo

Cmd_Name = "smo.GC.StraightenEdgeBoundary"
# smo.GC.StraightenEdgeBoundary


class SMO_GC_StraightenEdgeBoundary_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)

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
        return 'SMO GC - Straighten Edge Boundary'

    def cmd_Desc(self):
        return 'Flatten the selected Edge Boundary to fix squeeze.'

    def cmd_Tooltip(self):
        return 'Flatten the selected Edge Boundary to fix squeeze.'

    def cmd_Help(self):
        return 'https://twitter.com/sm0luck'

    def basic_ButtonName(self):
        return 'SMO GC - Straighten Edge Boundary'

    def basic_Enable(self, msg):
        return True

    def basic_Execute(self, msg, flags):
        scene = modo.scene.current()

        if self.SelModeEdge:
            lx.eval('select.type edge')
            lx.eval('select.createSet GC_StraightenEdgeBoundarySource')
            lx.eval('smo.MASTER.ForceSelectMeshItemOnly')
            selected_mesh = scene.selected[0]
            CSourceEdges = len(selected_mesh.geometry.edges.selected)

        # Function for Radian to Degree
        def rad(a):
            return [math.degrees(a)]

        # ------------------------------ #
        # <----( DEFINE VARIABLES )----> #
        # ------------------------------ #

        #####--- Define user value for all the different SafetyCheck --- START ---#####
        #####
        lx.eval("user.defNew name:SMO_SafetyCheck_PolygonModeEnabled type:integer life:momentary")

        lx.eval("user.defNew name:SMO_SafetyCheck_ItemModeEnabled type:integer life:momentary")
        lx.eval("user.defNew name:SMO_SafetyCheck_min1PolygonSelected type:integer life:momentary")

        lx.eval("user.defNew name:SMO_SafetyCheck_EdgeModeEnabled type:integer life:momentary")
        lx.eval("user.defNew name:SMO_SafetyCheck_min1EdgeSelected type:integer life:momentary")
        #####
        #####--- Define user value for all the different SafetyCheck --- END ---#####


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
            lx.eval('dialog.title {SMO GC StraightenEdgeBoundary:}')
            lx.eval('dialog.msg {You must be in Edge Mode and have 1 Mesh Layer selected to run that script.}')
            lx.eval('+dialog.open')
            lx.out('script Stopped: You must be in Edge Mode and have 1 Mesh Layer selected to run that script.')
            sys.exit
            # sys.exit( "LXe_FAILED:Must be in edge selection mode." )


        elif lx.eval1("select.typeFrom typelist:edge;vertex;polygon;item ?"):
            selType = "edge"
            attrType = "edge"
            SMO_SafetyCheck_ItemModeEnabled = 0
            SMO_SafetyCheck_PolygonModeEnabled = 0
            SMO_SafetyCheck_EdgeModeEnabled = 1
            #lx.out('script Running: Correct Item Selection Mode')
            # sys.exit( "LXe_FAILED:Must be in polygon selection mode." )

        elif lx.eval1("select.typeFrom typelist:polygon;vertex;edge;item ?"):
            selType = "polygon"
            attrType = "poly"
            SMO_SafetyCheck_ItemModeEnabled = 0
            SMO_SafetyCheck_PolygonModeEnabled = 1
            SMO_SafetyCheck_EdgeModeEnabled = 0
            lx.eval('dialog.setup info')
            lx.eval('dialog.title {SMO GC StraightenEdgeBoundary:}')
            lx.eval('dialog.msg {You must be in Edge Mode and have 1 Mesh Layer selected to run that script.}')
            lx.eval('+dialog.open')
            lx.out('script Stopped: You must be in Edge Mode and have 1 Mesh Layer selected to run that script.')
            sys.exit
            # sys.exit( "LXe_FAILED:Must be in edge selection mode." )

        else:
            # This only fails if none of the three supported selection
            # modes have yet been used since the program started, or
            # if "item" or "ptag" (ie: materials) is the current
            # selection mode.
            SMO_SafetyCheck_ItemModeEnabled = 1
            SMO_SafetyCheck_PolygonModeEnabled = 0
            SMO_SafetyCheck_EdgeModeEnabled = 0
            lx.eval('dialog.setup info')
            lx.eval('dialog.title {SMO GC StraightenEdgeBoundary:}')
            lx.eval('dialog.msg {You must be in Edge Mode and have 1 Mesh Layer selected to run that script.}')
            lx.eval('+dialog.open')
            lx.out('script Stopped: You must be in Edge Mode and have 1 Mesh Layer selected to run that script.')
            sys.exit
            # sys.exit( "LXe_FAILED:Must be in edge selection mode." )
        # --------------------  safety check 1: Polygon Selection Mode enabled --- END


        ###################################################################################################
        # Bugfix for Mesh items that can have multiple Rotation transform (coming from 3DsMax for instance)
        # if self.SelModeEdge == True :
        if self.SelModeEdge:
            lx.eval('select.type edge')
            lx.eval('select.useSet GC_StraightenEdgeBoundarySource replace')
            lx.eval('select.type item')

        scn = scene.selected[0]

        # scene.select(TargetItem)
        if SMO_SafetyCheck_EdgeModeEnabled == 1:
            scene.select(selected_mesh)

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

        items = scene.selected
        #lx.out('Processed Mesh Item:', items)
        if not RefSystemActive:
            lx.eval('item.refSystem %s' % items[0].id)

        # -------------------------- #
        # <---( SAFETY CHECK 2 )---> #
        # -------------------------- #
        CsEdges = len(selected_mesh.geometry.edges.selected)
        # at Least 1 Edge is selected --- START
        #lx.out('Count Selected Edge', CsEdges)

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
            #lx.out('script running: right amount of Edges in selection')
        # at Least 1 Edge is selected --- END

        #####--- Define current value for the Prerequisite TotalSafetyCheck --- START ---#####
        #####
        TotalSafetyCheckTrueValue = 2
        #lx.out('Desired Value', TotalSafetyCheckTrueValue)
        if SMO_SafetyCheck_ItemModeEnabled == 1:
            TotalSafetyCheck = (SMO_SafetyCheck_ItemModeEnabled + SMO_SafetyCheck_min1EdgeSelected)
            #lx.out('Current Value', TotalSafetyCheck)

        if SMO_SafetyCheck_EdgeModeEnabled == 1:
            TotalSafetyCheck = (SMO_SafetyCheck_EdgeModeEnabled + SMO_SafetyCheck_min1EdgeSelected)
            #lx.out('Current Value', TotalSafetyCheck)

        #####
        #####--- Define current value for the Prerequisite TotalSafetyCheck --- END ---#####

        Modo_ver = int(lx.eval('query platformservice appversion ?'))
        #print('Modo Version:', Modo_ver)

        # ------------------------ #
        # <----( Main Macro )----> #
        # ------------------------ #

        #####--------------------  Compare TotalSafetyCheck value and decide or not to continue the process  --- START
        # if TotalSafetyCheck == TotalSafetyCheckTrueValue:
        if SMO_SafetyCheck_EdgeModeEnabled == 1:
            lx.eval('select.type edge')
            lx.eval('select.useSet GC_StraightenEdgeBoundarySource replace')
            lx.eval('select.edgeLoop base false m3d middle')
            lx.eval('select.createSet GC_StraightenEdgeBoundaryEdgeLoop')
            lx.eval('select.convert vertex')
            lx.eval('select.createSet GC_StraightenEdgeBoundaryVertexLoop')
            lx.eval('select.type edge')
            lx.eval('select.expand')
            lx.eval('select.edge remove bond equal (none)')
            lx.eval('select.createSet GC_StraightenEdgeBoundaryEdgeRingDirection')

            EdgesSelectedList = []
            # Loop through the foreground layers
            count = 0
            for e in modo.Mesh().geometry.edges.selected:
                # print(e)
                EdgesSelectedList.append(e)

            print (EdgesSelectedList)
            lx.eval('select.drop edge')
            modo.meshgeometry.MeshEdge.select((EdgesSelectedList[0]))
            del EdgesSelectedList

            lx.eval('workPlane.fitGeometry')
            lx.eval('workPlane.fitSelect')
            WorldTargetRotX = lx.eval('workplane.edit 0 0 0 ? 0 0')
            WorldTargetRotY = lx.eval('workplane.edit 0 0 0 0 ? 0')
            WorldTargetRotZ = lx.eval('workplane.edit 0 0 0 0 0 ?')
            lx.eval('workPlane.state false')
            # lx.out('Workplane posX:', WorldTargetRotX)
            # lx.out('Workplane posY:', WorldTargetRotY)
            # lx.out('Workplane posZ:', WorldTargetRotZ)
            RotX = math.degrees(WorldTargetRotX)
            RotY = math.degrees(WorldTargetRotY)
            RotZ = math.degrees(WorldTargetRotZ)

            lx.eval('select.type vertex')
            lx.eval('select.useSet GC_StraightenEdgeBoundaryVertexLoop replace')
            lx.eval('workPlane.fitGeometry')
            lx.eval('workPlane.fitSelect')
            RelativeOffsetX = lx.eval('workplane.edit ? 0 0 0 0 0')
            RelativeOffsetY = lx.eval('workplane.edit 0 ? 0 0 0 0')
            RelativeOffsetZ = lx.eval('workplane.edit 0 0 ? 0 0 0')
            lx.eval('workPlane.state false')
            # lx.out('Center Offset posX:', RelativeOffsetX)
            # lx.out('Center Offset posY:', RelativeOffsetY)
            # lx.out('Center Offset posZ:', RelativeOffsetZ)
            lx.eval('workPlane.edit cenX:%f cenY:%f cenZ:%f rotX:%f rotY:%f rotZ:%f' % (
            RelativeOffsetX, RelativeOffsetY, RelativeOffsetZ, RotX, RotY, RotZ))
            lx.eval('tool.set TransformScale on')
            lx.eval('tool.set actr.origin on')
            lx.eval('tool.set center.select on')
            lx.eval('tool.setAttr xfrm.transform SX 0.0')
            lx.eval('tool.doApply')
            lx.eval('tool.set TransformScale off')
            lx.eval('workPlane.state false')
            lx.eval('tool.set actr.origin off')

            lx.eval('select.type vertex')
            lx.eval('!select.deleteSet GC_StraightenEdgeBoundaryVertexLoop')
            lx.eval('select.type edge')
            lx.eval('!select.deleteSet GC_StraightenEdgeBoundaryEdgeLoop')
            lx.eval('!select.deleteSet GC_StraightenEdgeBoundaryEdgeRingDirection')
            lx.eval('!select.deleteSet GC_StraightenEdgeBoundarySource')
            lx.eval('select.drop edge')
            lx.eval('tool.clearTask axis center')


        if not RefSystemActive:
            lx.eval('item.refSystem {}')


lx.bless(SMO_GC_StraightenEdgeBoundary_Cmd, Cmd_Name)

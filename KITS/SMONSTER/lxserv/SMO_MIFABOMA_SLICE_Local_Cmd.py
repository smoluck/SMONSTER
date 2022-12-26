# python
"""
# Name:         SMO_MIFABOMA_SLICE_Local_Cmd.py
# Version:      1.0
#
# Purpose:      This Command is designed to Mirror
#               a Polygon Selection from the current Layer
#               on a defined Axis (controlled by Argument).
#
# Author:       Franck ELISABETH (with the help of Tom Dymond for debug)
# Website:      https://www.smoluck.com
#
# Created:      16/09/2019
# Copyright:    (c) Franck Elisabeth 2017-2022
"""

import lx
import lxu
import modo
import sys

Cmd_Name =  "smo.MIFABOMA.SliceLocal"
# smo.MIFABOMA.SliceLocal 1 0 0


class SMO_MIFABOMA_Slice_Local_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
        self.dyna_Add("Axis", lx.symbol.sTYPE_INTEGER)
        self.dyna_Add("Gap_Mode", lx.symbol.sTYPE_INTEGER)
        self.basic_SetFlags (1, lx.symbol.fCMDARG_OPTIONAL)				# here the (1) define the argument index.
        self.dyna_Add("Split_Mode", lx.symbol.sTYPE_BOOLEAN)
        self.basic_SetFlags (2, lx.symbol.fCMDARG_OPTIONAL)				# here the (2) define the argument index.

        self.SelModePoly = bool(lx.eval1("select.typeFrom typelist:polygon;vertex;edge;item ?"))

    def cmd_Flags(self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO
    
    def cmd_Interact (self):
        pass
    
    def cmd_UserName (self):
        return 'SMO MIFABOMA - Slice Local'
    
    def cmd_Desc (self):
        return 'Slice current Polygon Selection using Item Center.'
    
    def cmd_Tooltip (self):
        return 'Slice current Polygon Selection using Item Center.'
    
    def cmd_Help (self):
        return 'https://twitter.com/sm0luck'
    
    def basic_ButtonName (self):
        return 'SMO MIFABOMA - Slice Local'
    
    def basic_Enable (self, msg):
        return True
    
    def basic_Execute(self, msg, flags):
        scene = modo.scene.current()
        if self.SelModePoly:
            lx.eval('smo.MASTER.ForceSelectMeshItemOnly')

        mesh = scene.selectedByType('mesh')[0]
        CsPolys = len(mesh.geometry.polygons.selected)
        SelItems = (lx.evalN('query sceneservice selection ? locator'))
        lx.out('Selected items is:',SelItems)

        

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
        
        
        
        # ------------------------------ #
        # <----( DEFINE VARIABLES )----> #
        # ------------------------------ #
        #####--- Define user value for all the different SafetyCheck --- START ---#####
        #####
        lx.eval("user.defNew name:SMO_SafetyCheck_PolygonModeEnabled type:integer life:momentary")
        lx.eval("user.defNew name:SMO_SafetyCheck_min1PolygonSelected type:integer life:momentary")
        #####
        #####--- Define user value for all the different SafetyCheck --- END ---#####
        
        
        
        # ------------------------------ #
        # <----( DEFINE ARGUMENTS )----> #
        # ------------------------------ #
        args = lx.args()
        lx.out(args)
        AXES = self.dyna_Int (0)                        # Axes selection:       X = 0 ### Y = 1 ### Z = 2
        GAP_MODE = self.dyna_Int (1)                    # Center = 0 ### Negative = 1 ### Positive = 2
        SPLIT_MODE = self.dyna_Bool (2)                 # Off = 0 ### On = 1
        # Expose the Result of the Arguments 
        #lx.out(SLICE_AXES)
        lx.out(AXES, GAP_MODE, SPLIT_MODE)
        # ------------------------------ #
        # <----( DEFINE ARGUMENTS )----> #
        # ------------------------------ #
        
        
        
        
        # -------------------------- #
        # <---( SAFETY CHECK 1 )---> #
        # -------------------------- #
        # --------------------  safety check 1: Polygon Selection Mode enabled --- START
        
        selType = ""
        # Used to query layerservice for the list of polygons, edges or vertices.
        attrType = ""
        
        if lx.eval1( "select.typeFrom typelist:vertex;polygon;edge;item;ptag ?" ):
            selType = "vertex"
            attrType = "vert"
        
            SMO_SafetyCheck_PolygonModeEnabled = 0
            lx.eval('dialog.setup info')
            lx.eval('dialog.title {SMO_Mirror:}')
            lx.eval('dialog.msg {You must be in Polygon Mode to run that script}')
            lx.eval('+dialog.open')
            lx.out('script Stopped: You must be in Polygon Mode to run that script')
            sys.exit
            #sys.exit( "LXe_FAILED:Must be in polygon selection mode." )
        
        
        elif lx.eval1( "select.typeFrom typelist:edge;vertex;polygon;item ?" ):
            selType = "edge"
            attrType = "edge"
        
            SMO_SafetyCheck_PolygonModeEnabled = 0
            lx.eval('dialog.setup info')
            lx.eval('dialog.title {SMO_Mirror:}')
            lx.eval('dialog.msg {You must be in Polygon Mode to run that script}')
            lx.eval('+dialog.open')
            lx.out('script Stopped: You must be in Polygon Mode to run that script')
            sys.exit
            #sys.exit( "LXe_FAILED:Must be in polygon selection mode." )
        
        elif lx.eval1( "select.typeFrom typelist:polygon;vertex;edge;item ?" ):
            selType = "polygon"
            attrType = "poly"
        
            SMO_SafetyCheck_PolygonModeEnabled = 1
            lx.out('script Running: Correct Component Selection Mode')
        
        
        else:
            # This only fails if none of the three supported selection
            # modes have yet been used since the program started, or
            # if "item" or "ptag" (ie: materials) is the current
            # selection mode.
            SMO_SafetyCheck_PolygonModeEnabled = 0
            lx.eval('dialog.setup info')
            lx.eval('dialog.title {SMO_Mirror:}')
            lx.eval('dialog.msg {You must be in Polygon Mode to run that script}')
            lx.eval('+dialog.open')
            lx.out('script Stopped: You must be in Polygon Mode to run that script')
            sys.exit
            #sys.exit( "LXe_FAILED:Must be in polygon selection mode." )
        # --------------------  safety check 1: Polygon Selection Mode enabled --- END
        
        
        
        # -------------------------- #
        # <---( SAFETY CHECK 2 )---> #
        # -------------------------- #
        # at Least 1 Polygons is selected --- START
        lx.out('Count Selected Poly',CsPolys)
        
        if CsPolys < 1:
            SMO_SafetyCheck_min1PolygonSelected = 0
            lx.eval('dialog.setup info')
            lx.eval('dialog.title {SMO_Slice:}')
            lx.eval('dialog.msg {You must select at least 1 polygon to run that script}')
            lx.eval('+dialog.open')
            lx.out('script Stopped: Add more polygons to your selection')
            sys.exit
        
        elif CsPolys >= 1:
            SMO_SafetyCheck_min1PolygonSelected = 1
            lx.out('script running: right amount of polygons in selection')
        # at Least 1 Polygons is selected --- END
        
        
        
        #####--- Define current value for the Prerequisite TotalSafetyCheck --- START ---#####
        #####
        TotalSafetyCheckTrueValue = 2
        lx.out('Desired Value',TotalSafetyCheckTrueValue)
        TotalSafetyCheck = (SMO_SafetyCheck_PolygonModeEnabled + SMO_SafetyCheck_min1PolygonSelected)
        lx.out('Current Value',TotalSafetyCheck)
        #####
        #####--- Define current value for the Prerequisite TotalSafetyCheck --- END ---#####
        
        
        
        
        
        # ------------------------ #
        # <----( Main Macro )----> #
        # ------------------------ #
        
        #####--------------------  Compare TotalSafetyCheck value and decide or not to continue the process  --- START
        if TotalSafetyCheck == TotalSafetyCheckTrueValue:
            lx.eval('hide.unsel')
            lx.eval('tool.set actr.auto on 0')
            lx.eval('select.type item')
            
            # Set RefSystem and query Workplane Pos & Rot value
            lx.eval('item.refSystem %s' % SelItems)
            ItemCenX = lx.eval('workplane.edit ? 0 0 0 0 0')
            ItemCenY = lx.eval('workplane.edit 0 ? 0 0 0 0')
            ItemCenZ = lx.eval('workplane.edit 0 0 ? 0 0 0')
            ItemRotX = lx.eval('workplane.edit 0 0 0 ? 0 0')
            ItemRotY = lx.eval('workplane.edit 0 0 0 0 ? 0')
            ItemRotZ = lx.eval('workplane.edit 0 0 0 0 0 ?')
            lx.out('Workplane posX:', ItemCenX)
            lx.out('Workplane posY:', ItemCenY)
            lx.out('Workplane posZ:', ItemCenZ)
            lx.out('Workplane rotX:', ItemRotX)
            lx.out('Workplane rotY:', ItemRotY)
            lx.out('Workplane rotZ:', ItemRotZ)
            
            lx.eval('tool.set actr.origin on')
            lx.eval('select.type polygon')
            
            # Set Workplane on Polygon selection and query Workplane Pos & Rot value
            lx.eval('workPlane.state true')
            PolyCenX = lx.eval('workplane.edit ? 0 0 0 0 0')
            PolyCenY = lx.eval('workplane.edit 0 ? 0 0 0 0')
            PolyCenZ = lx.eval('workplane.edit 0 0 ? 0 0 0')
            PolyRotX = lx.eval('workplane.edit 0 0 0 ? 0 0')
            PolyRotY = lx.eval('workplane.edit 0 0 0 0 ? 0')
            PolyRotZ = lx.eval('workplane.edit 0 0 0 0 0 ?')
            # return (PolyCenX, PolyCenY, PolyCenZ, PolyRotX, PolyRotY, PolyRotZ)
            
            lx.out('Workplane posX:', PolyCenX)
            lx.out('Workplane posY:', PolyCenY)
            lx.out('Workplane posZ:', PolyCenZ)
            lx.out('Workplane rotX:', PolyRotX)
            lx.out('Workplane rotY:', PolyRotY)
            lx.out('Workplane rotZ:', PolyRotZ)
            lx.eval('workPlane.reset')
            
            
            lx.eval('tool.set poly.knife on')
            # -------------------------- #
            # <----( Main Command )---->
            # -------------------------- #
            lx.eval('tool.setAttr poly.knife infinite true')
            lx.eval('tool.setAttr poly.knife axis custom')
            
            if SPLIT_MODE == 0 :
                lx.eval('tool.setAttr poly.knife split false')
                lx.eval('tool.setAttr poly.knife gap 0.0')
                
            if SPLIT_MODE == 1 :
                lx.eval('tool.setAttr poly.knife split true')
                
            if GAP_MODE == 0 :
                lx.eval('tool.setAttr poly.knife gapSide center')
                lx.eval('tool.setAttr poly.knife gap 0.0')
                
            if GAP_MODE == 1 :
                lx.eval('tool.setAttr poly.knife gapSide negative')
                lx.eval('tool.setAttr poly.knife gap 200.0')
                
            if GAP_MODE == 2 :
                lx.eval('tool.setAttr poly.knife gapSide positive')
                lx.eval('tool.setAttr poly.knife gap 200.0')
                
            if AXES == 0 :
                lx.eval('tool.attr poly.knife startX 0.0')
                lx.eval('tool.attr poly.knife startY 1.0')
                lx.eval('tool.attr poly.knife startZ 0.0')
                lx.eval('tool.attr poly.knife endX 0.0')
                lx.eval('tool.attr poly.knife endY -1.0')
                lx.eval('tool.attr poly.knife endZ 0.0')
                lx.eval('tool.setAttr poly.knife vectorX 0.0')
                lx.eval('tool.setAttr poly.knife vectorY 0.0')
                lx.eval('tool.setAttr poly.knife vectorZ 1.0')
                
            if AXES == 1 :
                lx.eval('tool.attr poly.knife startX 0.0')
                lx.eval('tool.attr poly.knife startY 0.0')
                lx.eval('tool.attr poly.knife startZ -1.0')
                lx.eval('tool.attr poly.knife endX 0.0')
                lx.eval('tool.attr poly.knife endY 0.0')
                lx.eval('tool.attr poly.knife endZ 1.0')
                lx.eval('tool.setAttr poly.knife vectorX 1.0')
                lx.eval('tool.setAttr poly.knife vectorY 0.0')
                lx.eval('tool.setAttr poly.knife vectorZ 0.0')
                
            if AXES == 2 :
                lx.eval('tool.attr poly.knife startX -1.0')
                lx.eval('tool.attr poly.knife startY 0.0')
                lx.eval('tool.attr poly.knife startZ 0.0')
                lx.eval('tool.attr poly.knife endX 1.0')
                lx.eval('tool.attr poly.knife endY 0.0')
                lx.eval('tool.attr poly.knife endZ 0.0')
                lx.eval('tool.setAttr poly.knife vectorX 0.0')
                lx.eval('tool.setAttr poly.knife vectorY 1.0')
                lx.eval('tool.setAttr poly.knife vectorZ 0.0')
                
                
            # query the current Modified value of Slice Tool.
            DefaultSliceSX = lx.eval('tool.attr poly.knife startX ?')
            DefaultSliceSY = lx.eval('tool.attr poly.knife startY ?')
            DefaultSliceSZ = lx.eval('tool.attr poly.knife startZ ?')
            DefaultSliceEX = lx.eval('tool.attr poly.knife endX ?')
            DefaultSliceEY = lx.eval('tool.attr poly.knife endY ?')
            DefaultSliceEZ = lx.eval('tool.attr poly.knife endZ ?')
            # return (DefaultSliceSX, DefaultSliceSY, DefaultSliceSZ, DefaultSliceEX, DefaultSliceEY, DefaultSliceEZ)
            
            # Addition Op to offset the value of Slice Tool.
            SliceSX = DefaultSliceSX + PolyCenX
            SliceSY = DefaultSliceSY + PolyCenY
            SliceSZ = DefaultSliceSZ + PolyCenZ
            SliceEX = DefaultSliceEX + PolyCenX
            SliceEY = DefaultSliceEY + PolyCenY
            SliceEZ = DefaultSliceEZ + PolyCenZ
            
            lx.out('Slice Offseted Start X:', SliceSX)
            lx.out('Slice Offseted Start Y:', SliceSY)
            lx.out('Slice Offseted Start Z:', SliceSZ)
            lx.out('Slice Offseted End X:', SliceEX)
            lx.out('Slice Offseted End Y:', SliceEY)
            lx.out('Slice Offseted End Z:', SliceEZ)
            # return (SliceSX, SliceSY, SliceSZ, SliceEX, SliceEY, SliceEZ)
            
            # Set offseted value back to the tool properties
            lx.eval('tool.attr poly.knife startX %s' % SliceSX)
            lx.eval('tool.attr poly.knife startY %s' % SliceSY)
            lx.eval('tool.attr poly.knife startZ %s' % SliceSZ)
            lx.eval('tool.attr poly.knife endX %s' % SliceEX)
            lx.eval('tool.attr poly.knife endY %s' % SliceEY)
            lx.eval('tool.attr poly.knife endZ %s' % SliceEZ)
            
            if AXES == 0 :
                lx.eval('tool.setAttr poly.knife vectorX 0.0')
                lx.eval('tool.setAttr poly.knife vectorY 0.0')
                lx.eval('tool.setAttr poly.knife vectorZ 1.0')
                
            if AXES == 1 :
                lx.eval('tool.setAttr poly.knife vectorX 1.0')
                lx.eval('tool.setAttr poly.knife vectorY 0.0')
                lx.eval('tool.setAttr poly.knife vectorZ 0.0')
                
            if AXES == 2 :
                lx.eval('tool.setAttr poly.knife vectorX 0.0')
                lx.eval('tool.setAttr poly.knife vectorY 1.0')
                lx.eval('tool.setAttr poly.knife vectorZ 0.0')
            
            
            # -------------------------- #
            # <----( Main Command )---->
            # -------------------------- #
            lx.eval('tool.doApply')
            lx.eval('select.drop polygon')
            lx.eval('select.nextMode')
            lx.eval('item.refSystem {}')
            lx.eval('tool.set actr.auto on 0')
            lx.eval('unhide')

            if not RefSystemActive:
                lx.eval('item.refSystem {}')
            if RefSystemActive:
                lx.eval('item.refSystem %s' % CurrentRefSystemItem)


        elif TotalSafetyCheck != TotalSafetyCheckTrueValue:
            lx.out('script Stopped: your mesh does not match the requirement for that script.')
            sys.exit
            
        lx.out('End of SMO_MirrorLocal  Command')


    def cmd_Query(self, index, vaQuery):
        lx.notimpl()


lx.bless(SMO_MIFABOMA_Slice_Local_Cmd, Cmd_Name)

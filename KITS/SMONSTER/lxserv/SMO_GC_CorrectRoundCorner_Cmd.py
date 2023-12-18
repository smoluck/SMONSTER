# python
"""
Name:         SMO_GC_CorrectRoundCorner_Cmd.py

Purpose:      This script is designed to
              Select the EdgeLoop Corner of a Tube mesh and rebuild a correct triangle at this one.

Author:       Franck ELISABETH (with the help of Tom Dymond for debug)
Website:      https://www.linkedin.com/in/smoluck/
Created:      27/02/2020
Copyright:    (c) Franck Elisabeth 2017-2022
"""

import lx
import lxu
import math
import modo

Cmd_Name = "smo.GC.CorrectRoundCorner"


class SMO_GC_CorrectRoundCorner_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
        # self.dyna_Add("Mode", lx.symbol.sTYPE_INTEGER)
    
    def cmd_Flags(self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO
    
    def cmd_Interact (self):
        pass
    
    def cmd_UserName (self):
        return 'SMO GC - Correct Round Corner'
    
    def cmd_Desc (self):
        return 'Select the EdgeLoop Corner of a Tube mesh and rebuild a correct triangle at this one.'
    
    def cmd_Tooltip (self):
        return 'Select the EdgeLoop Corner of a Tube mesh and rebuild a correct triangle at this one.'
    
    def cmd_Help (self):
        return 'https://twitter.com/sm0luck'
    
    def basic_ButtonName (self):
        return 'SMO GC - Correct Round Corner'

    def basic_Enable (self, msg):
        return True
    
    def basic_Execute(self, msg, flags):
        # mode = self.dyna_Int (0)
        scene = modo.scene.current()
        # Grab the selected items, limiting it to meshes.
        TargetMesh = lx.eval('query sceneservice selection ? mesh')



        # ---------------- COPY/PASTE Check Procedure ---------------- #
        ## create variables
        lx.eval("user.defNew name:User_Pref_CopyDeselectChangedState type:boolean life:momentary")
        lx.eval("user.defNew name:User_Pref_PasteSelectionChangedState type:boolean life:momentary")
        lx.eval("user.defNew name:User_Pref_PasteDeselectChangedState type:boolean life:momentary")

        lx.eval("user.defNew name:User_Pref_CopyDeselect type:boolean life:momentary")
        lx.eval("user.defNew name:User_Pref_PasteSelection type:boolean life:momentary")
        lx.eval("user.defNew name:User_Pref_PasteDeselect type:boolean life:momentary")
        ###################

        # Look at current Copy / Paste user Preferences:
        User_Pref_CopyDeselect = lx.eval('pref.value application.copyDeSelection ?')
        lx.out('User Pref: Deselect Elements after Copying', User_Pref_CopyDeselect)
        User_Pref_PasteSelection = lx.eval('pref.value application.pasteSelection ?')
        lx.out('User Pref: Select Pasted Elements', User_Pref_PasteSelection)
        User_Pref_PasteDeselect = lx.eval('pref.value application.pasteDeSelection ?')
        lx.out('User Pref: Deselect Elements Before Pasting', User_Pref_PasteDeselect)
        # Is Copy Deselect False ?
        if User_Pref_CopyDeselect == 0:
            lx.eval('pref.value application.copyDeSelection true')
            User_Pref_CopyDeselectChangedState = 1

        # Is Paste Selection False ?
        if User_Pref_PasteSelection == 0:
            lx.eval('pref.value application.pasteSelection true')
            User_Pref_PasteSelectionChangedState = 1

        # Is Paste Deselect False ?
        if User_Pref_PasteDeselect == 0:
            lx.eval('pref.value application.pasteDeSelection true')
            User_Pref_PasteDeselectChangedState = 1

        # Is Copy Deselect True ?
        if User_Pref_CopyDeselect == 1:
            User_Pref_CopyDeselectChangedState = 0

        # Is Paste Selection True ?
        if User_Pref_PasteSelection == 1:
            User_Pref_PasteSelectionChangedState = 0

        # Is Paste Deselect True ?
        if User_Pref_PasteDeselect == 1:
            User_Pref_PasteDeselectChangedState = 0
        # -------------------------------------------- #


        
        # Grab the item id, so that you can count the total number of verts on that layer.
        TargetMeshID = lx.eval('query layerservice layer.index ? {%s}' % TargetMesh)
        lx.out('Selected mesh ID:', TargetMeshID)
        
        lx.eval('select.type vertex')
        lx.eval('unhide')
        lx.eval('select.type item')
        # Count the number of verts on the current mesh layer.
        TargetMeshVertCount = lx.eval('query layerservice vert.N ? %s' % TargetMeshID)
        lx.out('Total Vert on Mesh: %s' % TargetMeshVertCount)
        
        Vert_A_ID = TargetMeshVertCount
        lx.out('Vert A (ID) %s' % Vert_A_ID)
        
        
        
        lx.eval('select.type edge')
        lx.eval('select.editSet TargetCorner add')
        lx.eval('workPlane.fitSelect')
        lx.eval('select.type vertex')
        lx.eval('vert.new 0.0')
        
        
        
        ############
        main = lx.eval('query layerservice layers ? selected')
        lx.out('Selected mesh:', main)
        lx.eval('select.element layer:{%i} type:vertex mode:replace index:{%s}' % (main, Vert_A_ID))
        # lx.eval('select.element layer:{%i} type:line mode:add index:0' % main)
        
        
        # lx.eval('select.element 1 vertex set %i' % Vert_A_ID)
        lx.eval('tool.set actr.origin on')
        lx.eval('tool.set TransformScale on')
        lx.eval('tool.noChange')
        lx.eval('tool.setAttr xfrm.transform SX 0.0')
        lx.eval('tool.setAttr xfrm.transform SY 0.0')
        lx.eval('tool.setAttr xfrm.transform SZ 0.0')
        lx.eval('tool.doApply')
        lx.eval('tool.set TransformScale off 0')
        lx.eval('workPlane.state false')
        lx.eval('select.nextMode')
        #################
        
        
        ############
        # Create extremity Vertex of both directions.
        lx.eval('select.type edge')
        lx.eval('select.expand')
        lx.eval('select.convert polygon')
        lx.eval('script.run "macro.scriptservice:92663570022:macro"')
        MeshSource = scene.selected
        
        lx.eval('pmodel.edgeToCurveCMD polyline true')
        
        lx.eval('select.type edge')
        lx.eval('select.all')
        lx.eval('poly.make auto')
        lx.eval('select.type polygon')
        lx.eval('cut')
        lx.eval('!delete')
        lx.eval('paste')
        lx.eval('select.drop polygon')
        lx.eval('select.type item')
        Ext_Mesh_A = scene.selected
        
        lx.eval('item.duplicate false locator false true')
        Ext_Mesh_B = scene.selected
        
        lx.eval('select.drop item')
        
        
        
        
        #######  Delete Poly Index 0 and 1 on both Ext_Mesh_A and Ext_Mesh_B
        scene.select(Ext_Mesh_A)
        lx.eval('select.type polygon')
        main_A = lx.eval('query layerservice layers ? selected')
        lx.eval('select.element layer:{%i} type:polygon mode:replace index:0' % main_A)
        lx.eval('!delete')
        
        #######  Delete Poly Index 0 and 1 on both Ext_Mesh_A and Ext_Mesh_B
        scene.select(Ext_Mesh_B)
        lx.eval('select.type polygon')
        main_B = lx.eval('query layerservice layers ? selected')
        lx.eval('select.element layer:{%i} type:polygon mode:replace index:1' % main_B)
        lx.eval('!delete')
        
        lx.eval('select.drop item')
        
        lx.eval('select.type item')
        scene.select(TargetMesh)
        lx.eval('select.type edge')
        lx.eval('select.useSet TargetCorner select')
        lx.eval('poly.make auto')
        lx.eval('select.convert polygon')
        lx.eval('cut')
        lx.eval('layer.new')
        lx.eval('select.type item')
        lx.eval('item.parent parent:{} inPlace:1')
        lx.eval('select.type polygon')
        lx.eval('paste')
        lx.eval('select.drop polygon')
        lx.eval('select.type item')
        MeshCorner = scene.selected
        lx.eval('select.drop item')
        
        scene.select(MeshCorner)
        lx.eval('item.name "ORIG_CORNER" xfrmcore')
        lx.eval('select.drop item')
        
        scene.select(Ext_Mesh_B)
        lx.eval('item.name "Etremity_A" xfrmcore')
        lx.eval('select.drop item')
        
        scene.select(Ext_Mesh_A)
        lx.eval('item.name "Etremity_B" xfrmcore')
        lx.eval('select.drop item')
        
        
        
        
        # MoveCenter to Poly Centers
        scene.select(MeshCorner)
        lx.eval('select.type polygon')
        lx.eval('select.all')
        lx.eval('smo.GC.Setup.MoveRotateCenterToSelection 1 0')
        lx.eval('select.drop polygon')
        lx.eval('select.drop item')
        
        scene.select(Ext_Mesh_B)
        lx.eval('select.type polygon')
        lx.eval('select.all')
        lx.eval('smo.GC.Setup.MoveRotateCenterToSelection 1 0')
        lx.eval('select.drop polygon')
        lx.eval('select.drop item')
        
        scene.select(Ext_Mesh_A)
        lx.eval('select.type polygon')
        lx.eval('select.all')
        lx.eval('smo.GC.Setup.MoveRotateCenterToSelection 1 0')
        lx.eval('select.drop polygon')
        lx.eval('select.drop item')
        
        
        
        
        # Create a Backup item with the current 3 PolysNgons
        scene.select(MeshCorner)
        lx.eval('select.type polygon')
        lx.eval('select.all')
        lx.eval('copy')
        lx.eval('select.drop polygon')
        lx.eval('select.type item')
        lx.eval('layer.new')
        lx.eval('item.name "BACKUP_PolyCrossSection" xfrmcore')
        lx.eval('select.type polygon')
        lx.eval('paste')
        lx.eval('select.drop polygon')
        lx.eval('select.type item')
        ItemBackupPolys = scene.selected
        
        scene.select(Ext_Mesh_A)
        lx.eval('select.type polygon')
        lx.eval('select.all')
        lx.eval('copy')
        lx.eval('select.type item')
        scene.select(ItemBackupPolys)
        lx.eval('select.type polygon')
        lx.eval('paste')
        lx.eval('select.drop polygon')
        lx.eval('select.type item')
        
        scene.select(Ext_Mesh_B)
        lx.eval('select.type polygon')
        lx.eval('select.all')
        lx.eval('copy')
        lx.eval('select.type item')
        scene.select(ItemBackupPolys)
        lx.eval('select.type polygon')
        lx.eval('paste')
        lx.eval('select.drop polygon')
        lx.eval('select.type item')
        
        
        
        
        # Create Unique Vertex at polygon Center on the 3 Mesh item Corners
        scene.select(MeshCorner)
        lx.eval('select.type polygon')
        lx.eval('select.all')
        lx.eval('workPlane.fitSelect')
        lx.eval('!delete')
        lx.eval('select.type vertex')
        lx.eval('vert.new 0.0')
        lx.eval('tool.set actr.origin on')
        lx.eval('tool.set TransformScale on')
        lx.eval('tool.noChange')
        lx.eval('tool.setAttr xfrm.transform SX 0.0')
        lx.eval('tool.setAttr xfrm.transform SY 0.0')
        lx.eval('tool.setAttr xfrm.transform SZ 0.0')
        lx.eval('tool.doApply')
        lx.eval('tool.set TransformScale off 0')
        lx.eval('workPlane.state false')
        lx.eval('select.type item')
        
        scene.select(Ext_Mesh_A)
        lx.eval('select.type polygon')
        lx.eval('select.all')
        lx.eval('workPlane.fitSelect')
        lx.eval('!delete')
        lx.eval('select.type vertex')
        lx.eval('vert.new 0.0')
        lx.eval('tool.set actr.origin on')
        lx.eval('tool.set TransformScale on')
        lx.eval('tool.noChange')
        lx.eval('tool.setAttr xfrm.transform SX 0.0')
        lx.eval('tool.setAttr xfrm.transform SY 0.0')
        lx.eval('tool.setAttr xfrm.transform SZ 0.0')
        lx.eval('tool.doApply')
        lx.eval('tool.set TransformScale off 0')
        lx.eval('workPlane.state false')
        lx.eval('select.type item')
        
        scene.select(Ext_Mesh_B)
        lx.eval('select.type polygon')
        lx.eval('select.all')
        lx.eval('workPlane.fitSelect')
        lx.eval('!delete')
        lx.eval('select.type vertex')
        lx.eval('vert.new 0.0')
        lx.eval('tool.set actr.origin on')
        lx.eval('tool.set TransformScale on')
        lx.eval('tool.noChange')
        lx.eval('tool.setAttr xfrm.transform SX 0.0')
        lx.eval('tool.setAttr xfrm.transform SY 0.0')
        lx.eval('tool.setAttr xfrm.transform SZ 0.0')
        lx.eval('tool.doApply')
        lx.eval('tool.set TransformScale off 0')
        lx.eval('workPlane.state false')
        lx.eval('select.type item')
        
        
        
        
        # Cut/paste Vertex to MeshCorner item 0 = Corner /// 1 = Extremity A /// 2 = Extremity B
        scene.select(Ext_Mesh_A)
        lx.eval('select.type vertex')
        lx.eval('select.all')
        lx.eval('cut')
        lx.eval('select.type item')
        scene.select(MeshCorner)
        lx.eval('select.type vertex')
        lx.eval('paste')
        lx.eval('select.type item')
        
        scene.select(Ext_Mesh_B)
        lx.eval('select.type vertex')
        lx.eval('select.all')
        lx.eval('cut')
        lx.eval('select.type item')
        scene.select(MeshCorner)
        lx.eval('select.type vertex')
        lx.eval('paste')
        lx.eval('select.type item')
        
        
        
        
        # Build Polygon from 3 Points
        scene.select(MeshCorner)
        lx.eval('select.type vertex')
        lx.eval('select.all')
        lx.eval('poly.make auto')
        lx.eval('select.type vertex')
        CornerIt = lx.eval('query layerservice layers ? selected')
        lx.out('Selected mesh:', CornerIt)
        
        
        
        
        
        # Normalize Distance from Origin to Point A
        lx.eval('select.element layer:{%i} type:vertex mode:replace index:{%i}' % (CornerIt, 0))
        lx.eval('select.element layer:{%i} type:vertex mode:add index:{%i}' % (CornerIt, 1))
        lx.eval('workPlane.fitSelect')
        lx.eval('select.drop vertex')
        # Orientation Check
        
        # Move Point A to Origin
        lx.eval('select.element layer:{%i} type:vertex mode:replace index:{%i}' % (CornerIt, 1))
        lx.eval('tool.set actr.origin on')
        lx.eval('tool.set TransformScale on')
        lx.eval('tool.noChange')
        lx.eval('tool.setAttr xfrm.transform SX 0.0')
        lx.eval('tool.setAttr xfrm.transform SY 0.0')
        lx.eval('tool.setAttr xfrm.transform SZ 0.0')
        lx.eval('tool.doApply')
        lx.eval('tool.set TransformScale off 0')
        lx.eval('select.drop vertex')
        
        # Move Point A to minimum Distance (0.1 Unit)
        lx.eval('select.element layer:{%i} type:vertex mode:replace index:{%i}' % (CornerIt, 1))
        lx.eval('tool.set TransformMove on')
        lx.eval('tool.noChange')
        lx.eval('tool.setAttr xfrm.transform TX -0.1')
        lx.eval('tool.setAttr xfrm.transform TY 0.0')
        lx.eval('tool.setAttr xfrm.transform TZ 0.0')
        lx.eval('tool.doApply')
        lx.eval('tool.set TransformMove off 0')
        lx.eval('workPlane.state false')
        lx.eval('select.drop vertex')
        
        
        
        # Normalize Distance from Origin to Point B
        lx.eval('select.element layer:{%i} type:vertex mode:replace index:{%i}' % (CornerIt, 0))
        lx.eval('select.element layer:{%i} type:vertex mode:add index:{%i}' % (CornerIt, 2))
        lx.eval('workPlane.fitSelect')
        lx.eval('select.drop vertex')
        # Orientation Check
        
        # Move Point A to Origin
        lx.eval('select.element layer:{%i} type:vertex mode:replace index:{%i}' % (CornerIt, 2))
        lx.eval('tool.set actr.origin on')
        lx.eval('tool.set TransformScale on')
        lx.eval('tool.noChange')
        lx.eval('tool.setAttr xfrm.transform SX 0.0')
        lx.eval('tool.setAttr xfrm.transform SY 0.0')
        lx.eval('tool.setAttr xfrm.transform SZ 0.0')
        lx.eval('tool.doApply')
        lx.eval('tool.set TransformScale off 0')
        lx.eval('select.drop vertex')
        
        # Move Point A to minimum Distance (0.1 Unit)
        lx.eval('select.element layer:{%i} type:vertex mode:replace index:{%i}' % (CornerIt, 2))
        lx.eval('tool.set TransformMove on')
        lx.eval('tool.noChange')
        lx.eval('tool.setAttr xfrm.transform TX -0.1')
        lx.eval('tool.setAttr xfrm.transform TY 0.0')
        lx.eval('tool.setAttr xfrm.transform TZ 0.0')
        lx.eval('tool.doApply')
        lx.eval('tool.set TransformMove off 0')
        lx.eval('workPlane.state false')
        lx.eval('select.drop vertex')
        
        
        
        
        # -------------------------------------------- #
        # ------ Mirror Corner Vertex and opposite Poly ------ #
        # Select hypotenuse to Copy the Corner Vertex to opposite side with Mirror tool
        lx.eval('select.drop vertex')
        lx.eval('select.element layer:{%i} type:vertex mode:replace index:{%i}' % (CornerIt, 1))
        lx.eval('select.element layer:{%i} type:vertex mode:add index:{%i}' % (CornerIt, 2))
        lx.eval('workPlane.fitSelect')
        lx.eval('select.drop vertex')
        lx.eval('select.element layer:{%i} type:vertex mode:replace index:{%i}' % (CornerIt, 0))
        
        lx.eval('tool.set *.mirror on')
        lx.eval('tool.setAttr effector.clone merge false')
        lx.eval('tool.setAttr gen.mirror cenX 0.0')
        lx.eval('tool.setAttr gen.mirror cenY 0.0')
        lx.eval('tool.setAttr gen.mirror cenZ 0.0')
        lx.eval('tool.setAttr gen.mirror axis 2')
        lx.eval('tool.setAttr gen.mirror leftX 1')
        lx.eval('tool.setAttr gen.mirror leftY 0.0')
        lx.eval('tool.setAttr gen.mirror leftZ 0.0')
        lx.eval('tool.setAttr gen.mirror upX 0.0')
        lx.eval('tool.setAttr gen.mirror upY 1')
        lx.eval('tool.setAttr gen.mirror upZ 0.0')
        lx.eval('tool.doApply')
        lx.eval('select.nextMode')
        lx.eval('tool.set *.mirror off')
        lx.eval('select.drop vertex')
        lx.eval('workPlane.state false')
        
        # Create Opposite Poly 
        lx.eval('select.element layer:{%i} type:vertex mode:replace index:{%i}' % (CornerIt, 1))
        lx.eval('select.element layer:{%i} type:vertex mode:add index:{%i}' % (CornerIt, 2))
        lx.eval('select.element layer:{%i} type:vertex mode:add index:{%i}' % (CornerIt, 3))
        lx.eval('poly.make auto')
        
        
        # Get the Workplane Offset to Corner
        lx.eval('select.element layer:{%i} type:vertex mode:replace index:{%i}' % (CornerIt, 0))
        lx.eval('select.type vertex')
        lx.eval('workPlane.fitSelect')
        lx.eval('select.drop vertex')
        ItemCenX = lx.eval('workplane.edit ? 0 0 0 0 0')
        ItemCenY = lx.eval('workplane.edit 0 ? 0 0 0 0')
        ItemCenZ = lx.eval('workplane.edit 0 0 ? 0 0 0')
        lx.eval('workPlane.state false')
        lx.out('Workplane posX:', ItemCenX)
        lx.out('Workplane posY:', ItemCenY)
        lx.out('Workplane posZ:', ItemCenZ)
        
        # Get the Workplane Rotation at Hypotenuse
        lx.eval('select.element layer:{%i} type:vertex mode:replace index:{%i}' % (CornerIt, 1))
        lx.eval('select.element layer:{%i} type:vertex mode:add index:{%i}' % (CornerIt, 2))
        lx.eval('workPlane.fitSelect')
        lx.eval('select.drop vertex')
        ItemRotXrad = lx.eval('workplane.edit 0 0 0 ? 0 0')
        ItemRotYrad = lx.eval('workplane.edit 0 0 0 0 ? 0')
        ItemRotZrad = lx.eval('workplane.edit 0 0 0 0 0 ?')
        lx.out('(Rad) Workplane rot X:', ItemRotXrad)
        lx.out('(Rad) Workplane rot Y:', ItemRotYrad)
        lx.out('(Rad) Workplane rot Z:', ItemRotZrad)
        
        ItemRotX = math.degrees(ItemRotXrad)
        ItemRotY = math.degrees(ItemRotYrad)
        ItemRotZ = math.degrees(ItemRotZrad)
        lx.eval('workPlane.state false')
        lx.out('Workplane rot X:', ItemRotX)
        lx.out('Workplane rot Y:', ItemRotY)
        lx.out('Workplane rot Z:', ItemRotZ)
        
        lx.eval('workPlane.edit cenX:%f cenY:%f cenZ:%f rotX:%f rotY:%f rotZ:%f' % (ItemCenX, ItemCenY, ItemCenZ, ItemRotX, ItemRotY, ItemRotZ))
        lx.eval('workPlane.state false')
        lx.eval('select.type item')
        
        
        
        
        ####################################################################################
        # ------ Flatten Backup Poly according to point Corner -> A and Corner -> B ------ #
        ## Corner -> A ##
        scene.select(MeshCorner)
        lx.eval('select.type vertex')
        lx.eval('select.element layer:{%i} type:vertex mode:replace index:{%i}' % (CornerIt, 0))
        lx.eval('select.element layer:{%i} type:vertex mode:add index:{%i}' % (CornerIt, 1))
        lx.eval('workPlane.fitSelect')
        
        scene.select(ItemBackupPolys)
        lx.eval('select.type polygon')
        ItemBackupIt = lx.eval('query layerservice layers ? selected')
        lx.out('Selected mesh:', ItemBackupIt)
        
        # Move Poly Extremity A to Origin
        lx.eval('select.element layer:{%i} type:polygon mode:replace index:{%i}' % (ItemBackupIt, 1))
        lx.eval('tool.set actr.origin on')
        lx.eval('tool.set TransformScale on')
        lx.eval('tool.noChange')
        lx.eval('tool.setAttr xfrm.transform SX 0.0')
        lx.eval('tool.setAttr xfrm.transform SY 1.0')
        lx.eval('tool.setAttr xfrm.transform SZ 1.0')
        lx.eval('tool.doApply')
        lx.eval('tool.set TransformScale off 0')
        
        # Move Point A to minimum Distance (0.1 Unit)
        lx.eval('tool.set TransformMove on')
        lx.eval('tool.noChange')
        lx.eval('tool.setAttr xfrm.transform TX -0.1')
        lx.eval('tool.setAttr xfrm.transform TY 0.0')
        lx.eval('tool.setAttr xfrm.transform TZ 0.0')
        lx.eval('tool.doApply')
        lx.eval('tool.set TransformMove off 0')
        lx.eval('workPlane.state false')
        lx.eval('select.drop polygon')
        
        
        
        
        ## Corner -> B ##
        scene.select(MeshCorner)
        lx.eval('select.type vertex')
        lx.eval('select.element layer:{%i} type:vertex mode:replace index:{%i}' % (CornerIt, 0))
        lx.eval('select.element layer:{%i} type:vertex mode:add index:{%i}' % (CornerIt, 2))
        lx.eval('workPlane.fitSelect')
        
        scene.select(ItemBackupPolys)
        lx.eval('select.type polygon')
        
        # Move Poly Extremity B to Origin
        lx.eval('select.element layer:{%i} type:polygon mode:replace index:{%i}' % (ItemBackupIt, 2))
        lx.eval('tool.set actr.origin on')
        lx.eval('tool.set TransformScale on')
        lx.eval('tool.noChange')
        lx.eval('tool.setAttr xfrm.transform SX 0.0')
        lx.eval('tool.setAttr xfrm.transform SY 1.0')
        lx.eval('tool.setAttr xfrm.transform SZ 1.0')
        lx.eval('tool.doApply')
        lx.eval('tool.set TransformScale off 0')
        
        # Move Point A to minimum Distance (0.1 Unit)
        lx.eval('tool.set TransformMove on')
        lx.eval('tool.noChange')
        lx.eval('tool.setAttr xfrm.transform TX -0.1')
        lx.eval('tool.setAttr xfrm.transform TY 0.0')
        lx.eval('tool.setAttr xfrm.transform TZ 0.0')
        lx.eval('tool.doApply')
        lx.eval('tool.set TransformMove off 0')
        lx.eval('workPlane.state false')
        lx.eval('select.drop polygon')
        lx.eval('select.type item')
        
        
        
        scene.select(MeshCorner)
        lx.eval('select.type vertex')
        lx.eval('select.element layer:{%i} type:vertex mode:replace index:{%i}' % (CornerIt, 1))
        lx.eval('select.element layer:{%i} type:vertex mode:add index:{%i}' % (CornerIt, 0))
        lx.eval('select.element layer:{%i} type:vertex mode:add index:{%i}' % (CornerIt, 2))
        AngleCorner = lx.eval('smo.GC.GetAngleBetweenThreeVert ?')
        lx.out('Angle at Corner is: ', AngleCorner)



        # -------------- COPY/PASTE END Procedure  -------------- #
        # Restore user Preferences:
        if User_Pref_CopyDeselectChangedState == 1 :
            lx.eval('pref.value application.copyDeSelection false')
            lx.out('"Deselect Elements after Copying" have been Restored')
        if User_Pref_PasteSelectionChangedState == 1 :
            lx.eval('pref.value application.pasteSelection false')
            lx.out('"Select Pasted Elements" have been Restored')
        if User_Pref_PasteDeselectChangedState == 1 :
            lx.eval('pref.value application.pasteDeSelection false')
            lx.out('"Deselect Elements Before Pasting" have been Restored')
        # -------------------------------------------- #


lx.bless(SMO_GC_CorrectRoundCorner_Cmd, Cmd_Name)

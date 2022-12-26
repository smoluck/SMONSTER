# python
"""
# Name:         SMO_VENOM_MainCommand_Cmd.py
# Version:      6.0
# 
# Purpose:      This script is designed to:
#               Hard Set Vertex Normal on current Mesh layer using
#               Facing Ratio to flatten the area and fix jagged Vertex Normals.
#               Mouse over a polygon in item mode and launch
# 
# Author:       Franck ELISABETH
# Website:      https://www.smoluck.com
# 
# Created:      22/09/2020
# Copyright:    (c) Franck Elisabeth 2017-2022
"""

from math import degrees

import lx
import lxu
import modo
import sys

Cmd_Name = "smo.VENOM.MainCommand"
# smo.VENOM.MainCommand


def checkvertexnormalpresence():
    VNMapName = lx.eval('pref.value application.defaultVertexNormals ?')
    # print(VNMapName)

    m = modo.Mesh()
    # print(m)
    # print(m.name)
    maps = m.geometry.vmaps.getMapsByType([lx.symbol.i_VMAP_NORMAL])
    # print(len(maps))

    if len(maps) == 0:
        lx.eval('smo.GC.SetVertexNormal')
        # print('New VNrm Maps created')
        # print('VNrm map name is: %s' % VNMapName)


class SMO_VENOM_MainCommand_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
        self.dyna_Add("Similar Selection Mode", lx.symbol.sTYPE_INTEGER)
        self.basic_SetFlags(0, lx.symbol.fCMDARG_OPTIONAL)  # here the (0) define the argument index.
        self.dyna_Add("Select Loop Automatic", lx.symbol.sTYPE_INTEGER)
        self.basic_SetFlags(1, lx.symbol.fCMDARG_OPTIONAL)  # here the (0) define the argument index.

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
        return 'SMO VENOM - Main Command'

    def cmd_Desc(self):
        return 'Hard Set Vertex Normal on current Mesh layer using Facing Ratio to flatten the area and fix jagged Vertex Normals. Mouse over a polygon in item mode and launch'

    def cmd_Tooltip(self):
        return 'Hard Set Vertex Normal on current Mesh layer using Facing Ratio to flatten the area and fix jagged Vertex Normals. Mouse over a polygon in item mode and launch'

    def cmd_Help(self):
        return 'https://twitter.com/sm0luck'

    def basic_ButtonName(self):
        return 'SMO VENOM - Main Command'

    def basic_Enable(self, msg):
        return True

    def basic_Execute(self, msg, flags):
        IntSimilarMode = self.dyna_Int(0)
        IntSelectLoop = self.dyna_Int(1)
        checkvertexnormalpresence()

        scene = modo.scene.current()

        VeNomItemAsRotation = bool()

        if self.SelModePoly:
            lx.eval('smo.MASTER.ForceSelectMeshItemOnly')

        MakeInactiveSameAsActive = bool(lx.eval('view3d.inactiveInvisible ?'))
        if MakeInactiveSameAsActive:
            lx.eval('view3d.inactiveInvisible false')

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


        # # ------------- ARGUMENTS ------------- #
        args = lx.args()
        #lx.out(args)

        # 0 = Similar Touching
        # 1 = Similar Object
        # 2 = Similar Layer
        # 3 = Current Polygons Only
        SimilarMode = IntSimilarMode
        #lx.out('Similar Selection Mode:', SimilarMode)

        # 0 = Keep current selection
        # 1 = Select Loop
        SelectLoop = IntSelectLoop
        #lx.out('Select Loop Automatic:', SelectLoop)
        # # ------------- ARGUMENTS ------------- #

        # ------------------------------ #
        # <----( DEFINE VARIABLES )----> #
        # ------------------------------ #

        #####--- Define user value for all the different SafetyCheck --- START ---#####
        #####
        lx.eval("user.defNew name:SMO_SafetyCheck_PolygonModeEnabled type:integer life:momentary")

        lx.eval("user.defNew name:SMO_SafetyCheck_ItemModeEnabled type:integer life:momentary")
        lx.eval("user.defNew name:SMO_SafetyCheck_min1PolygonSelected type:integer life:momentary")
        #####
        #####--- Define user value for all the different SafetyCheck --- END ---#####

        ###############COPY/PASTE Check Procedure#################
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
        #lx.out('User Pref: Deselect Elements after Copying', User_Pref_CopyDeselect)
        User_Pref_PasteSelection = lx.eval('pref.value application.pasteSelection ?')
        #lx.out('User Pref: Select Pasted Elements', User_Pref_PasteSelection)
        User_Pref_PasteDeselect = lx.eval('pref.value application.pasteDeSelection ?')
        #lx.out('User Pref: Deselect Elements Before Pasting', User_Pref_PasteDeselect)
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
        ################################################

        ################################################
        VMapsName = lx.eval('pref.value application.defaultVertexNormals ?')
        #lx.out(VMapsName)

        IsolateMode =  lx.eval('user.value SMO_UseVal_VENOM_Isolate ?')
        #lx.out(IsolateMode)

        ShowVNVectors = bool(lx.eval('user.value SMO_UseVal_VENOM_ShowVNVectors ?'))
        #lx.out(ShowVNVectors)
        ################################################

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
            lx.eval('dialog.setup info')
            lx.eval('dialog.title {SMO VeNom:}')
            lx.eval('dialog.msg {You must be in Item Mode and have 1 Mesh Layer selected to run that script.}')
            lx.eval('+dialog.open')
            lx.out('script Stopped: You must be in Item Mode and have 1 Mesh Layer selected to run that script.')
            sys.exit
            # sys.exit( "LXe_FAILED:Must be in polygon selection mode." )

        elif lx.eval1("select.typeFrom typelist:polygon;vertex;edge;item ?"):
            selType = "polygon"
            attrType = "poly"

            SMO_SafetyCheck_ItemModeEnabled = 0
            SMO_SafetyCheck_PolygonModeEnabled = 1
            #lx.out('script Running: Correct Item Selection Mode')
            # sys.exit( "LXe_FAILED:Must be in polygon selection mode." )
        else:
            # This only fails if none of the three supported selection
            # modes have yet been used since the program started, or
            # if "item" or "ptag" (ie: materials) is the current
            # selection mode.
            SMO_SafetyCheck_ItemModeEnabled = 1
            SMO_SafetyCheck_PolygonModeEnabled = 0
            #lx.out('script Running: Correct Item Selection Mode')
        # --------------------  safety check 1: Polygon Selection Mode enabled --- END

        #####-------------------------------------------------------------------------------#####
        ####### Track Mouse Over Selection. Is there a polygon under Mouse and select it. #######
        #####-------------------------------------------------------------------------------#####
        if SMO_SafetyCheck_ItemModeEnabled == 1:
            lx.eval('select.type polygon')

            lx.eval('query view3dservice mouse ?')
            view_under_mouse = lx.eval('query view3dservice mouse.view ?')
            lx.eval('query view3dservice view.index ? %s' % view_under_mouse)
            lx.eval('query view3dservice mouse.pos ?')
            Item_under_mouse = lx.eval('query view3dservice element.over ? ITEM ')
            Poly_under_mouse = lx.eval('query view3dservice element.over ? POLY ')
            # edge_under_mouse = lx.eval('query view3dservice element.over ? EDGE ')
            hitpos = lx.eval('query view3dservice mouse.hitpos ?')

            #lx.out('View under mouse:', view_under_mouse)
            #lx.out('Hit Position:', hitpos)
            #lx.out('Items under mouse:', Item_under_mouse)
            #lx.out('Polygon under mouse:', Poly_under_mouse)

            # lx.eval('select.drop polygon')
            # lx.eval('materials.underMouse')

            success = True
            try:
                lx.eval('select.3DElementUnderMouse')
            except:
                success = False
            scene.select(Item_under_mouse)

        if SMO_SafetyCheck_PolygonModeEnabled == 1:
            lx.eval('select.type item')
            mesh = scene.selectedByType('mesh')[0]
            lx.eval('select.type polygon')

        items = scene.selected
        lx.out('Processed Mesh Item:', items)


        ###################################################################################################
        # Bugfix for Mesh items that can have multiple Rotation transform (coming from 3DsMax for instance)
        if self.SelModePoly:
            lx.eval('select.type item')

        scn = scene.selected[0]
        locsup = modo.LocatorSuperType(scn)
        # print(locsup)
        pos = locsup.position
        # print(pos)
        rot = locsup.rotation
        # print(rot)
        sca = locsup.scale
        # print(sca)
        TrsfList = []
        # print(TrsfList)
        RotList = []
        # print(RotList)

        transformsStackRot = [xfrm for xfrm in locsup.transforms]
        # print(transformsStackRot)
        transformsStackRot.reverse()
        # print(transformsStackRot)
        # print('-----')

        # for n, xfrm in enumerate(transformsStackRot):
        #     print(transformsStackRot[n])
        # print('-----')

        for n, xfrm in enumerate(transformsStackRot):
            TrsfList.append((transformsStackRot[n]))
        # print('-----')
        # print(TrsfList)
        # del (TrsfList)

        for i in TrsfList:
            if i.type == 'rotation':
                # print (i)
                RotList.append(i)
        # print('-----')
        # print(RotList)
        # print('-----')
        # print(len(RotList))
        # del (RotList)

        if len(RotList) > 1:
            for n, xfrm in enumerate(transformsStackRot):
                # print(xfrm.name)
                if xfrm == rot:
                    if len(TrsfList) > 1:
                        if transformsStackRot[n + 1].type == 'rotation':
                            scene.select([transformsStackRot[n + 1], xfrm])
                            lx.eval('transform.merge rem:1')
                            break
        lx.eval('smo.GC.DeselectAll')
        scene.select(scn)
        if self.SelModePoly:
            lx.eval('select.type polygon')
        ####################################################





        # Get the Transform of the current selected Item.
        TargetItem = lx.eval1( "query sceneservice selection ? locator" )
        TargetRotXfrm = lx.eval1( "query sceneservice item.xfrmRot ? " + TargetItem )          # Rotation
        # TargetXfrm = lx.eval1( "query sceneservice item.xfrmPos ? " + TargetItem )        # Position
        # print(TargetRotXfrm)

        if TargetRotXfrm is not None:
            VeNomItemAsRotation = True
            scene.select(TargetRotXfrm)
            lx.eval('select.channel {%s:rot.X} set' % TargetRotXfrm)
            TargetRotX = lx.eval('channel.value ? channel:{%s:rot.X}' % TargetRotXfrm)
            lx.eval('select.channel {%s:rot.Y} set' % TargetRotXfrm)
            TargetRotY = lx.eval('channel.value ? channel:{%s:rot.Y}' % TargetRotXfrm)
            lx.eval('select.channel {%s:rot.Z} set' % TargetRotXfrm)
            TargetRotZ = lx.eval('channel.value ? channel:{%s:rot.Z}' % TargetRotXfrm)
            # print(TargetRotX)
            # print(TargetRotY)
            # print(TargetRotZ)

            TargetRotXAngle = rad(TargetRotX)
            TargetRotYAngle = rad(TargetRotY)
            TargetRotZAngle = rad(TargetRotZ)
            # print(TargetRotXAngle)
            # print(TargetRotYAngle)
            # print(TargetRotZAngle)

            lx.eval('channel.value 0 channel:{%s:rot.X}' % TargetRotXfrm)
            lx.eval('channel.value 0 channel:{%s:rot.Y}' % TargetRotXfrm)
            lx.eval('channel.value 0 channel:{%s:rot.Z}' % TargetRotXfrm)

        if TargetRotXfrm is None:
            VeNomItemAsRotation = False

        # scene.select(TargetItem)
        # Select back the Processed Item
        if SMO_SafetyCheck_ItemModeEnabled == 1:
            scene.select(Item_under_mouse)
        if SMO_SafetyCheck_PolygonModeEnabled == 1:
            scene.select(mesh)



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



        selected_mesh = scene.selected[0]  # gets the current selected object (throws an error if nothing is selected)
        print(selected_mesh)

        target_positions = selected_mesh.transforms.position.get()
        lx.out(target_positions)
        target_rotations = selected_mesh.transforms.rotation.get()
        lx.out(target_rotations)

        # -------------------------- #
        # <---( SAFETY CHECK 2 )---> #
        # -------------------------- #
        CsPolys = len(selected_mesh.geometry.polygons.selected)
        # at Least 1 Polygons is selected --- START
        lx.out('Count Selected Poly', CsPolys)

        if CsPolys < 1:
            SMO_SafetyCheck_min1PolygonSelected = 0
            lx.eval('dialog.setup info')
            lx.eval('dialog.title {SMO VeNom:}')
            lx.eval('dialog.msg {You must mouse over a polygon to run that script}')
            lx.eval('+dialog.open')
            lx.out('script Stopped: Mouse over a polygon')
            sys.exit

        elif CsPolys >= 1:
            SMO_SafetyCheck_min1PolygonSelected = 1
            #lx.out('script running: right amount of polygons in selection')
        # at Least 1 Polygons is selected --- END

        #####--- Define current value for the Prerequisite TotalSafetyCheck --- START ---#####
        #####
        TotalSafetyCheckTrueValue = 2
        lx.out('Desired Value', TotalSafetyCheckTrueValue)
        if SMO_SafetyCheck_ItemModeEnabled == 1:
            TotalSafetyCheck = (SMO_SafetyCheck_ItemModeEnabled + SMO_SafetyCheck_min1PolygonSelected)
            lx.out('Current Value', TotalSafetyCheck)

        if SMO_SafetyCheck_PolygonModeEnabled == 1:
            TotalSafetyCheck = (SMO_SafetyCheck_PolygonModeEnabled + SMO_SafetyCheck_min1PolygonSelected)
            lx.out('Current Value', TotalSafetyCheck)

        #####
        #####--- Define current value for the Prerequisite TotalSafetyCheck --- END ---#####

        Modo_ver = int(lx.eval ('query platformservice appversion ?'))
        print('Modo Version:',Modo_ver)

        # ------------------------ #
        # <----( Main Macro )----> #
        # ------------------------ #
        
        #####--------------------  Compare TotalSafetyCheck value and decide or not to continue the process  --- START
        if TotalSafetyCheck == TotalSafetyCheckTrueValue:
            #############
            # # Make Inactive Items Invisible for editing
            # lx.eval('view3d.inactiveInvisible true')
            # # Hide Locator visibility
            # lx.eval('view3d.showLocators false')

            # Load the AVP VeNom Preset to help work.
            if IsolateMode:
                lx.eval('view3d.presetload AVP_VeNom_AA')
            #############

            # Polygon Undermouse Selection Mode. You must be in Item Mode
            if SMO_SafetyCheck_ItemModeEnabled == 1:
                lx.eval('select.type polygon')

                if SimilarMode == 0:
                    lx.eval('smo.GC.SelectCoPlanarPoly 0 2 0')
                if SimilarMode == 1:
                    lx.eval('smo.GC.SelectCoPlanarPoly 1 2')
                if SimilarMode == 2:
                    lx.eval('smo.GC.SelectCoPlanarPoly 2 2')

                lx.eval('select.editSet SelSet_VeNomTargetPoly add {}')
                lx.eval('select.type item')
                lx.eval('view3d.selItemMode none')

                lx.eval('select.editSet SelSet_VeNomTarget add {}')
                lx.eval('select.type polygon')
                lx.eval('select.connect')
                lx.eval('cut')

                lx.eval('layer.new')
                lx.eval('select.type item')
                lx.eval('item.name VENOM_TEMP xfrmcore')
                temp_mesh = scene.selected[0]  # gets the current selected object
                lx.eval('smo.GC.DeselectAll')
                scene.select(temp_mesh)
                selected_mesh_Name = selected_mesh.name
                lx.eval('select.subItem %s add mesh 0 0' % selected_mesh_Name)
                lx.eval('item.parent')
                scene.select(temp_mesh)
                lx.eval('item.parent parent:{} inPlace:1')
                scene.select(temp_mesh)

                # temp_mesh.position.set(target_positions)
                # temp_mesh.rotation.set(target_rotations)
                lx.eval('select.editSet SelSet_VeNomTempLayer add {}')  # Unparent maybe needed
                lx.eval('select.type polygon')
                lx.eval('paste')
                lx.eval('select.drop polygon')
                lx.eval('select.useSet SelSet_VeNomTargetPoly select')
                lx.eval('workPlane.fitSelect')
                lx.eval('select.convert vertex')
                lx.eval('select.editSet SelSet_VeNomTargetVertex add {}')
                lx.eval('select.type item')

                lx.eval('layer.new')
                lx.eval('item.name VENOM_BG xfrmcore')
                bg_mesh = scene.selected[0]  # gets the current selected object
                lx.eval('select.subItem %s add mesh 0 0' % selected_mesh_Name)
                lx.eval('item.parent')
                scene.select(bg_mesh)
                lx.eval('item.parent parent:{} inPlace:1')
                scene.select(bg_mesh)

                # bg_mesh.position.set(target_positions)
                # bg_mesh.rotation.set(target_rotations)
                lx.eval('select.editSet SelSet_VeNomBG add {}')


                lx.eval('select.useSet SelSet_VeNomTempLayer select')
                lx.eval('hide.unsel')

                lx.eval('select.useSet SelSet_VeNomTempLayer deselect')

                # lx.eval('view3d.projection top')
                lx.eval('tool.set prim.cube on')

                # User Settings for Cube Tool
                VeNom_PrimCubeCenX = lx.eval('tool.attr prim.cube cenX ?')
                VeNom_PrimCubeCenY = lx.eval('tool.attr prim.cube cenY ?')
                VeNom_PrimCubeCenZ = lx.eval('tool.attr prim.cube cenZ ?')
                VeNom_PrimCubeSizeX = lx.eval('tool.attr prim.cube sizeX ?')
                VeNom_PrimCubeSizeY = lx.eval('tool.attr prim.cube sizeY ?')
                VeNom_PrimCubeSizeZ = lx.eval('tool.attr prim.cube sizeZ ?')
                VeNom_PrimCubeSegX = lx.eval('tool.attr prim.cube segmentsX ?')
                VeNom_PrimCubeSegY = lx.eval('tool.attr prim.cube segmentsY ?')
                VeNom_PrimCubeSegZ = lx.eval('tool.attr prim.cube segmentsZ ?')
                VeNom_PrimCubeRadius = lx.eval('tool.attr prim.cube radius ?')
                VeNom_PrimCubeUV = lx.eval('tool.attr prim.cube uvs ?')
                VeNom_PrimCubeHandleMode = lx.eval('tool.attr prim.cube handleMode ?')

                # print(VeNom_PrimCubeCenX)
                # print(VeNom_PrimCubeCenY)
                # print(VeNom_PrimCubeCenZ)
                # print(VeNom_PrimCubeSizeX)
                # print(VeNom_PrimCubeSizeY)
                # print(VeNom_PrimCubeSizeZ)
                # print(VeNom_PrimCubeSegX)
                # print(VeNom_PrimCubeSegY)
                # print(VeNom_PrimCubeSegZ)
                # print(VeNom_PrimCubeRadius)
                # print(VeNom_PrimCubeUV)
                # print(VeNom_PrimCubeHandleMode)

                # Set Cube Tool settings for Venom especially
                # lx.eval('tool.attr prim.cube axis y')
                lx.eval('tool.attr prim.cube cenX 0.0')
                lx.eval('tool.attr prim.cube cenY 0.0')
                lx.eval('tool.attr prim.cube cenZ 0.0')
                lx.eval('tool.attr prim.cube sizeX 1.0')
                lx.eval('tool.attr prim.cube sizeY 0.0')
                lx.eval('tool.attr prim.cube sizeZ 1.0')
                lx.eval('tool.attr prim.cube segmentsX 1')
                lx.eval('tool.attr prim.cube segmentsY 1')
                lx.eval('tool.attr prim.cube segmentsZ 1')
                lx.eval('tool.attr prim.cube handleMode resize')
                lx.eval('tool.attr prim.cube uvs false')
                lx.eval('tool.apply')
                lx.eval('tool.set prim.cube off 0')
                lx.eval('tool.clearTask snap')

                # Set back the settings
                lx.eval('tool.set prim.cube on')
                lx.eval('tool.attr prim.cube cenX %s' % VeNom_PrimCubeCenX)
                lx.eval('tool.attr prim.cube cenY %s' % VeNom_PrimCubeCenY)
                lx.eval('tool.attr prim.cube cenZ %s' % VeNom_PrimCubeCenZ)
                lx.eval('tool.attr prim.cube sizeX %s' % VeNom_PrimCubeSizeX)
                lx.eval('tool.attr prim.cube sizeY %s' % VeNom_PrimCubeSizeY)
                lx.eval('tool.attr prim.cube sizeZ %s' % VeNom_PrimCubeSizeZ)
                lx.eval('tool.attr prim.cube segmentsX %s' % VeNom_PrimCubeSegX)
                lx.eval('tool.attr prim.cube segmentsY %s' % VeNom_PrimCubeSegY)
                lx.eval('tool.attr prim.cube segmentsZ %s' % VeNom_PrimCubeSegZ)
                lx.eval('tool.attr prim.cube radius %s' % VeNom_PrimCubeRadius)
                lx.eval('tool.attr prim.cube uvs %s' % VeNom_PrimCubeUV)
                lx.eval('tool.attr prim.cube handleMode %s' % VeNom_PrimCubeHandleMode)
                lx.eval('tool.set prim.cube off 0')

                # lx.eval('view3d.projection psp')
                lx.eval('workPlane.state false')
                if Modo_ver < 1520:
                    lx.eval('vertMap.normals "{%s}"' % VMapsName)
                if Modo_ver >= 1520:
                    lx.eval('vertMap.normals "{%s}" false 1.0 "" false' % VMapsName)
                lx.eval('select.drop item')
                scene.select(temp_mesh)
                lx.eval('select.type vertex')
                lx.eval('select.useSet SelSet_VeNomTargetVertex select')
                lx.eval('view3d.inactiveInvisible false')
                lx.eval('vertMap.transferNormals true')
                lx.eval('select.drop vertex')
                lx.eval('select.type polygon')
                lx.eval('select.all')
                lx.eval('cut')



            # Manual Selection Mode via a set of Polygons
            if SMO_SafetyCheck_PolygonModeEnabled == 1:
                if SelectLoop == 1:
                    lx.eval('select.loop')

                lx.eval('select.editSet SelSet_VeNomTargetPoly add {}')
                lx.eval('select.type item')
                lx.eval('view3d.selItemMode none')
                lx.eval('select.editSet SelSet_VeNomTarget add {}')
                lx.eval('select.type polygon')
                lx.eval('select.connect')
                lx.eval('cut')

                lx.eval('layer.new')
                lx.eval('select.type item')
                temp_mesh = scene.selected[0]  # gets the current selected object
                temp_mesh.position.set(target_positions)
                temp_mesh.rotation.set(target_rotations)
                lx.eval('select.editSet SelSet_VeNomTempLayer add {}')  # Unparent maybe needed

                lx.eval('select.type polygon')
                lx.eval('paste')
                lx.eval('select.drop polygon')
                lx.eval('select.useSet SelSet_VeNomTargetPoly select')
                lx.eval('copy')

                lx.eval('select.useSet SelSet_VeNomTargetPoly select')

                lx.eval('select.convert vertex')
                lx.eval('select.editSet SelSet_VeNomTargetVertex add {}')

                lx.eval('select.type item')
                lx.eval('layer.new')
                bg_mesh = scene.selected[0]  # gets the current selected object
                bg_mesh.position.set(target_positions)
                bg_mesh.rotation.set(target_rotations)
                lx.eval('select.editSet SelSet_VeNomBG add {}')

                lx.eval('select.useSet SelSet_VeNomTempLayer select')
                lx.eval('hide.unsel')

                lx.eval('select.useSet SelSet_VeNomTempLayer deselect')
                lx.eval('paste')
                lx.eval('tool.clearTask snap')
                lx.eval('select.vertexMap "{%s}" norm replace' % VMapsName)
                lx.eval('!vertMap.delete norm')
                if Modo_ver < 1520:
                    lx.eval('vertMap.normals "{%s}"' % VMapsName)
                if Modo_ver >= 1520:
                    lx.eval('vertMap.normals "{%s}" false 1.0 "" false' % VMapsName)
                lx.eval('select.drop item')
                lx.eval('select.useSet SelSet_VeNomTempLayer select')
                lx.eval('select.type vertex')
                lx.eval('select.useSet SelSet_VeNomTargetVertex select')
                lx.eval('view3d.inactiveInvisible false')
                lx.eval('vertMap.transferNormals true')
                lx.eval('select.drop vertex')
                lx.eval('select.type polygon')
                lx.eval('select.all')
                lx.eval('cut')

            lx.eval('select.type item')
            lx.eval('select.drop item')
            lx.eval('select.useSet SelSet_VeNomTarget select')
            lx.eval('unhide')

            lx.eval('select.type polygon')
            lx.eval('paste')
            lx.eval('select.type vertex')
            try:
                lx.eval('!select.deleteSet SelSet_VeNomTargetVertex false')
            except:
                pass
            lx.eval('select.type polygon')
            try:
                lx.eval('!select.deleteSet SelSet_VeNomTargetPoly false')
            except:
                pass
            lx.eval('select.drop polygon')
            lx.eval('select.type item')
            lx.eval('select.drop item')

            lx.eval('select.useSet SelSet_VeNomBG replace')
            lx.eval('select.useSet SelSet_VeNomTempLayer select')
            lx.eval('!!delete')

            lx.eval('select.useSet SelSet_VeNomTarget select')
            try:
                lx.eval('!select.deleteSet SelSet_VeNomTarget false')
            except:
                pass

            if SMO_SafetyCheck_PolygonModeEnabled == 1:
                lx.eval('select.type polygon')

            if ShowVNVectors:
                lx.eval('tool.set util.normshow on')

            if not ShowVNVectors:
                lx.eval('tool.set util.normshow off')

        if not RefSystemActive:
            lx.eval('item.refSystem {}')

        if VeNomItemAsRotation:
            # Set back the Rotation of the Target item
            scene.select(TargetRotXfrm)
            TargetOutputRot = [(TargetRotXAngle[0]), (TargetRotYAngle[0]), (TargetRotZAngle[0])]
            # print(TargetOutputRot)
            # print(TargetOutputRot[0])
            # print(TargetOutputRot[1])
            # print(TargetOutputRot[2])

            lx.eval('select.channel {%s:rot.X} set' % TargetRotXfrm)
            lx.eval('channel.value {%s} channel:{%s:rot.X}' % (TargetOutputRot[0], TargetRotXfrm))
            lx.eval('select.channel {%s:rot.Y} set' % TargetRotXfrm)
            lx.eval('channel.value {%s} channel:{%s:rot.Y}' % (TargetOutputRot[1], TargetRotXfrm))
            lx.eval('select.channel {%s:rot.Z} set' % TargetRotXfrm)
            lx.eval('channel.value {%s} channel:{%s:rot.Z}' % (TargetOutputRot[2], TargetRotXfrm))
            lx.eval('smo.GC.DeselectAll')

        if SMO_SafetyCheck_PolygonModeEnabled == 1:
            scene.select(selected_mesh)
            lx.eval('select.type polygon')

        if SMO_SafetyCheck_ItemModeEnabled == 1:
            lx.eval('select.type item')
            scene.select(selected_mesh)
            # lx.eval('smo.GC.DeselectAll') Bugfix to keep current selection active in Item Mode


        ###############COPY/PASTE END Procedure#################
        # Restore user Preferences:
        if User_Pref_CopyDeselectChangedState == 1:
            lx.eval('pref.value application.copyDeSelection false')
            lx.out('"Deselect Elements after Copying" have been Restored')
        if User_Pref_PasteSelectionChangedState == 1:
            lx.eval('pref.value application.pasteSelection false')
            lx.out('"Select Pasted Elements" have been Restored')
        if User_Pref_PasteDeselectChangedState == 1:
            lx.eval('pref.value application.pasteDeSelection false')
            lx.out('"Deselect Elements Before Pasting" have been Restored')
        ########################################################

        if IsolateMode:
            lx.eval('view3d.inactiveInvisible true')
        if not IsolateMode:
            lx.eval('view3d.inactiveInvisible false')


lx.bless(SMO_VENOM_MainCommand_Cmd, Cmd_Name)

# python
# ---------------------------------------
# Name:         SMO_CAD_RebuildRadialTubeUnderMouse_Cmd.py
# Version:      1.0
#
# Purpose:      This script is designed to:
#               Select the Item and Polygon under mouse, select similar touching polygons Multiple Times with 40 degree value, then delete and recreate the PolyLoop Patch and update the VertexNormal Map if needed.
#
#
# Author:       Franck ELISABETH
# Website:      http://www.smoluck.com
#
# Created:      22/09/2020
# Copyright:    (c) Franck Elisabeth 2017-2022
# ---------------------------------------

import lx, lxu, modo

Command_Name = "smo.CAD.RebuildRadialTube"
# smo.CAD.RebuildRadialTube

class SMO_CAD_RebuildRadialTubeUnderMouse_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)

    def cmd_Flags(self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO

    def cmd_Interact(self):
        pass

    def cmd_UserName(self):
        return 'SMO CAD Rebuild Radial Tube'

    def cmd_Desc(self):
        return 'Select the Item and Polygon under mouse, select similar touching polygons Multiple Times with 40 degree value, then delete and recreate the PolyLoop Patch and update the VertexNormal Map if needed.'

    def cmd_Tooltip(self):
        return 'Select the Item and Polygon under mouse, select similar touching polygons Multiple Times with 40 degree value, then delete and recreate the PolyLoop Patch and update the VertexNormal Map if needed.'

    def cmd_Help(self):
        return 'https://twitter.com/sm0luck'

    def basic_ButtonName(self):
        return 'SMO CAD Rebuild Radial Tube'

    def cmd_Flags(self):
        return lx.symbol.fCMD_UNDO

    def basic_Enable(self, msg):
        return True

    def basic_Execute(self, msg, flags):
        scene = modo.scene.current()

        ################################
        # <----[ DEFINE VARIABLES ]---->#
        ################################

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
        # lx.out('User Pref: Deselect Elements after Copying', User_Pref_CopyDeselect)
        User_Pref_PasteSelection = lx.eval('pref.value application.pasteSelection ?')
        # lx.out('User Pref: Select Pasted Elements', User_Pref_PasteSelection)
        User_Pref_PasteDeselect = lx.eval('pref.value application.pasteDeSelection ?')
        # lx.out('User Pref: Deselect Elements Before Pasting', User_Pref_PasteDeselect)
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





        ##############################
        ####### SAFETY CHECK 1 #######
        ##############################

        #####--------------------  safety check 1: Polygon Selection Mode enabled --- START --------------------#####

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
            lx.out('script Running: Correct Item Selection Mode')
            # sys.exit( "LXe_FAILED:Must be in polygon selection mode." )
        else:
            # This only fails if none of the three supported selection
            # modes have yet been used since the program started, or
            # if "item" or "ptag" (ie: materials) is the current
            # selection mode.
            SMO_SafetyCheck_ItemModeEnabled = 1
            SMO_SafetyCheck_PolygonModeEnabled = 0
            lx.out('script Running: Correct Item Selection Mode')
        #####--------------------  safety check 1: Polygon Selection Mode enabled --- END --------------------#####

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

            lx.out(view_under_mouse)
            lx.out(Item_under_mouse)
            lx.out(Poly_under_mouse)
            lx.out(hitpos)

            lx.eval('select.drop polygon')
            # lx.eval('materials.underMouse')

            success = True
            try:
                lx.eval('select.3DElementUnderMouse')
            except:
                success = False
        scene = modo.Scene()
        scene.select(Item_under_mouse)
        mesh = scene.selectedByType('mesh')[0]
        items = scene.selected
        # lx.out(items)

        selected_mesh = scene.selected[0]  # gets the current selected object (throws an error if nothing is selected)
        target_positions = selected_mesh.transforms.position.get()
        # lx.out(target_positions)
        target_rotations = selected_mesh.transforms.rotation.get()
        # lx.out(target_positions)



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



        ##############################
        ####### SAFETY CHECK 2 #######
        ##############################
        CsPolys = len(mesh.geometry.polygons.selected)
        #####--------------------  safety check 2: at Least 1 Polygons is selected --- START --------------------#####
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
            lx.out('script running: right amount of polygons in selection')
        #####--------------------  safety check 2: at Least 1 Polygons is selected --- END --------------------#####

        #####--- Define current value for the Prerequisite TotalSafetyCheck --- START ---#####
        #####
        TotalSafetyCheckTrueValue = 2
        lx.out('Desired Value', TotalSafetyCheckTrueValue)
        if SMO_SafetyCheck_ItemModeEnabled == 1:
            TotalSafetyCheck = (SMO_SafetyCheck_ItemModeEnabled + SMO_SafetyCheck_min1PolygonSelected)
            lx.out('Current Value', TotalSafetyCheck)

        #####
        #####--- Define current value for the Prerequisite TotalSafetyCheck --- END ---#####


        ##############################
        ## <----( Main Macro )----> ##
        ##############################
        #####--------------------  Compare TotalSafetyCheck value and decide or not to continue the process  --- START --------------------#####
        if TotalSafetyCheck == TotalSafetyCheckTrueValue:
            # Polygon Undermouse Selection Mode. You must be in Item Mode
            if SMO_SafetyCheck_ItemModeEnabled == 1:
                lx.eval('select.type polygon')
                lx.eval('smo.GC.SelectCoPlanarPoly 0 88')
                lx.eval('smo.GC.SelectCoPlanarPoly 0 88')
                lx.eval('smo.GC.SelectCoPlanarPoly 0 88')
                lx.eval('smo.GC.SelectCoPlanarPoly 0 88')
                lx.eval('smo.GC.SelectCoPlanarPoly 0 88')
                lx.eval('smo.GC.SelectCoPlanarPoly 0 88')
                lx.eval('smo.GC.SelectCoPlanarPoly 0 88')
                lx.eval('smo.GC.SelectCoPlanarPoly 0 88')
                lx.eval('script.run "macro.scriptservice:92663570022:macro"')
                lx.eval('select.type polygon')
                lx.eval('!delete')

                lx.eval('select.type edge')
                lx.eval('tool.set edge.bridge on')
                lx.eval('tool.noChange')
                lx.eval('tool.setAttr edge.bridge segments 0')
                lx.eval('tool.attr edge.bridge twist 0')
                lx.eval('tool.attr edge.bridge mode linear')
                lx.eval('tool.attr edge.bridge remove false')
                lx.eval('tool.attr edge.bridge connect false')
                lx.eval('tool.doApply')
                lx.eval('tool.set edge.bridge off')
                lx.eval('select.nextMode')
                lx.eval('select.type edge')

                # Set VertexNormals on New Polygons. Select first the VNormal Map
                lx.eval('select.convert polygon')
                lx.eval('select.convert vertex')
                lx.eval('select.editSet VertexToMerge add')
                lx.eval('select.drop vertex')
                lx.eval('select.type polygon')

                # Cut/Paste the polygons to Set their correct Vertex Normals values.
                lx.eval('cut')
                lx.eval('paste')
                lx.eval('hide.unsel')
                meshUpdateVNMap = modo.Mesh()
                VMapCount = len(meshUpdateVNMap.geometry.vmaps)
                # print(VMapCount)
                if VMapCount > 0:
                    for map in meshUpdateVNMap.geometry.vmaps:
                        mapObj = lx.object.MeshMap(map)
                        # print(mapObj.Name())
                        # print(mapObj.Type())
                        if mapObj.Type() == 1313821261:  # int id for Vertex Normal map
                            lx.eval("select.vertexMap {%s} norm mode:remove" % mapObj.Name())
                            lx.eval("select.vertexMap {%s} norm mode:add" % mapObj.Name())
                            CurrentVertexNormalMapName = mapObj.Name()
                            # print(CurrentVertexNormalMapName)
                            if CurrentVertexNormalMapName is not None:
                                # Clear current VNormal Data to rebuild them.
                                lx.eval('vertMap.clear norm')
                                # HardSet Smooth Vertex Normals
                                lx.eval('vertMap.normals {%s} true 1.0 "" false' % CurrentVertexNormalMapName)

                # Reconnect the Boundaries Vertex
                lx.eval('unhide')
                lx.eval('select.type vertex')
                lx.eval('select.useSet VertexToMerge select')
                lx.eval('!vert.merge fixed false 0.000001 false false')

                # Clear the component selection amd Vertex Selection Sets
                lx.eval('select.type polygon')
                lx.eval('select.drop polygon')
                lx.eval('select.type edge')
                lx.eval('select.drop edge')
                lx.eval('select.type vertex')
                lx.eval('!select.deleteSet VertexToMerge')
                lx.eval('select.drop vertex')
                lx.eval('select.type polygon')

                # Get back to Item Mode
                lx.eval('select.type item')
                lx.eval('smo.GC.DeselectAll')
                
            if RefSystemActive == False:
                lx.eval('item.refSystem {}')
            if RefSystemActive == True:
                lx.eval('item.refSystem %s' % CurrentRefSystemItem)

        ###############COPY/PASTE END Procedure#################
        # Restore user Preferences:
        if User_Pref_CopyDeselectChangedState == 1:
            lx.eval('pref.value application.copyDeSelection false')
            # lx.out('"Deselect Elements after Copying" have been Restored')
        if User_Pref_PasteSelectionChangedState == 1:
            lx.eval('pref.value application.pasteSelection false')
            # lx.out('"Select Pasted Elements" have been Restored')
        if User_Pref_PasteDeselectChangedState == 1:
            lx.eval('pref.value application.pasteDeSelection false')
            # lx.out('"Deselect Elements Before Pasting" have been Restored')
        ########################################################


lx.bless(SMO_CAD_RebuildRadialTubeUnderMouse_Cmd, Command_Name)
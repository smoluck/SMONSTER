# python
# ---------------------------------------
# Name:         SMO_CAD_RebevelProcedByUser_Cmd.py
# Version:      1.0
#
# Purpose:      This script is designed to test
#               if 1 Item is selected and if more than 2
#               Polygons are selected, then process a
#               rebevel on the selected patch
#
# Author:       Franck ELISABETH
# Website:      http://www.smoluck.com
#
# Created:      06/05/2020
# Copyright:    (c) Franck Elisabeth 2017-2022
# ---------------------------------------
import lx, lxu, modo, sys

Cmd_Name = "smo.CAD.RebevelProcedByUser"
# smo.CAD.RebevelProcedByUser 8

class SMO_CAD_RebevelProcedByUser_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
        self.dyna_Add("Side count", lx.symbol.sTYPE_INTEGER)
        self.basic_SetFlags(0, lx.symbol.fCMDARG_OPTIONAL)  # here the (0) define the argument index.

        self.SelModePoly = bool(lx.eval1("select.typeFrom typelist:polygon;vertex;edge;item ?"))

    def cmd_Flags(self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO

    def cmd_Interact(self):
        pass

    def cmd_UserName(self):
        return 'SMO CAD - Rebevel Proced by User'

    def cmd_Desc(self):
        return 'With 1 Item selected and if more than 2 Polygons selected, Process a rebevel on the selected patch of Quads.'

    def cmd_Tooltip(self):
        return 'With 1 Item selected and if more than 2 Polygons selected, Process a rebevel on the selected patch of Quads.'

    def cmd_Help(self):
        return 'https://twitter.com/sm0luck'

    def basic_ButtonName(self):
        return 'SMO CAD - Rebevel Proced by User'

    def basic_Enable(self, msg):
        return True

    def basic_Execute(self, msg, flags):
        scene = modo.scene.current()
        if self.SelModePoly == True:
            lx.eval('smo.MASTER.ForceSelectMeshItemOnly')

        mesh = scene.selectedByType('mesh')[0]



        ######################################
        # <----[ Check Arguments State ]---->#
        ######################################
        # If not Set, ask value to user via Popup window with textt field
        if self.dyna_IsSet(0):
            RebSideCount = self.dyna_Int(0)
        if not self.dyna_IsSet(0):
            RebSideCount = 4
            try:
                #####--- Define User Value for Count --- START ---#####
                #####
                # Create a user value that define the Count for the Command.
                lx.eval("user.defNew name:Count type:integer life:momentary")
                # Set the title name for the dialog window
                lx.eval('user.def Count dialogname "SMO CAD - Rebevel"')
                # Set the input field name for the value that the users will see
                lx.eval("user.def Count username {Set the side count value}")
                # The '?' before the user.value calls a popup to have the user set the value
                lx.eval("?user.value Count")
                # Now that the user set the value, i can query it
                UserInput_Count = lx.eval("user.value Count ?")
                lx.out('User Count:', UserInput_Count)
                RebSideCount = UserInput_Count
            except:
                pass
        print(RebSideCount)



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


        ################################
        # <----[ DEFINE VARIABLES ]---->#
        ################################

        #####--- Define user value for all the different SafetyCheck --- START ---#####
        #####
        lx.eval("user.defNew name:SMO_SafetyCheck_Only1MeshItemSelected type:integer life:momentary")
        lx.eval("user.defNew name:SMO_SafetyCheck_PolygonModeEnabled type:integer life:momentary")
        lx.eval("user.defNew name:SMO_SafetyCheck_min3PolygonSelected type:integer life:momentary")
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
        ################################################

        ##############################
        ####### SAFETY CHECK 1 #######
        ##############################

        #####-------------------- safety check 1 : Only One Item Selected --- START --------------------#####
        ItemCount = lx.eval('query layerservice layer.N ? fg')
        lx.out('Selected Item count:', ItemCount)

        if ItemCount != 1:
            SMO_SafetyCheck_Only1MeshItemSelected = 0
            lx.eval('dialog.setup info')
            lx.eval('dialog.title {SMO_Rebevel:}')
            lx.eval(
                'dialog.msg {You must only select the Mesh Item layer you are working on, in Item List, to run that script}')
            lx.eval('+dialog.open')
            lx.out('Only One Item Selected result:', SMO_SafetyCheck_Only1MeshItemSelected)
            lx.out('script Stopped: Select only one Mesh Item')
            sys.exit

        else:
            SMO_SafetyCheck_Only1MeshItemSelected = 1
            lx.out('Only One Item Selected:', SMO_SafetyCheck_Only1MeshItemSelected)
            lx.out('script running: right amount of Mesh Item selected')
        #####-------------------- safety check 1 : Only One Item Selected --- END --------------------#####

        ##############################
        ####### SAFETY CHECK 2 #######
        ##############################

        #####--------------------  safety check 2: Polygon Selection Mode enabled --- START --------------------#####
        selType = ""
        # Used to query layerservice for the list of polygons, edges or vertices.
        attrType = ""

        if lx.eval1("select.typeFrom typelist:vertex;polygon;edge;item;ptag ?"):
            selType = "vertex"
            attrType = "vert"

            SMO_SafetyCheck_PolygonModeEnabled = 0
            lx.eval('dialog.setup info')
            lx.eval('dialog.title {SMO_Rebevel:}')
            lx.eval('dialog.msg {You must be in Polygon Mode to run that script}')
            lx.eval('+dialog.open')
            lx.out('script Stopped: You must be in Polygon Mode to run that script')
            sys.exit


        elif lx.eval1("select.typeFrom typelist:edge;vertex;polygon;item ?"):
            selType = "edge"
            attrType = "edge"

            SMO_SafetyCheck_PolygonModeEnabled = 0
            lx.eval('dialog.setup info')
            lx.eval('dialog.title {SMO_Rebevel:}')
            lx.eval('dialog.msg {You must be in Polygon Mode to run that script}')
            lx.eval('+dialog.open')
            lx.out('script Stopped: You must be in Polygon Mode to run that script')
            sys.exit

        elif lx.eval1("select.typeFrom typelist:polygon;vertex;edge;item ?"):
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
            lx.eval('dialog.title {SMO_Rebevel:}')
            lx.eval('dialog.msg {You must be in Polygon Mode to run that script}')
            lx.eval('+dialog.open')
            lx.out('script Stopped: You must be in Polygon Mode to run that script')
            sys.exit
        #####--------------------  safety check 2: Polygon Selection Mode enabled --- END --------------------#####

        ##############################
        ####### SAFETY CHECK 3 #######
        ##############################

        #####--------------------  safety check 3: at Least 3 Polygons are selected --- START --------------------#####
        try:
            #####--- Get current selected polygon count --- START ---#####
            #####
            CsPolys = len(mesh.geometry.polygons.selected)
            lx.out('Count Selected Poly', CsPolys)
            #####
            #####--- Get current selected polygon count --- END ---#####

            if CsPolys <= 2:
                SMO_SafetyCheck_min3PolygonSelected = 0
                lx.eval('dialog.setup info')
                lx.eval('dialog.title {SMO_Rebevel:}')
                lx.eval('dialog.msg {You must select more than 2 polygons selected to run that script}')
                lx.eval('+dialog.open')
                lx.out('script Stopped: Add more polygons to your selection')
                sys.exit

            elif CsPolys >= 3:
                SMO_SafetyCheck_min3PolygonSelected = 1
                lx.out('script running: right amount of polygons in selection')
            #####--------------------  safety check 3: at Least 3 Polygons are selected --- END --------------------#####
        except:
            sys.exit

        #####--- Define user value for the Prerequisite TotalSafetyCheck --- START ---#####
        #####
        TotalSafetyCheckTrueValue = 3
        lx.out('SafetyCheck Desired Value', TotalSafetyCheckTrueValue)
        TotalSafetyCheck = (
                    SMO_SafetyCheck_Only1MeshItemSelected + SMO_SafetyCheck_PolygonModeEnabled + SMO_SafetyCheck_min3PolygonSelected)
        lx.out('SafetyCheck Current Value', TotalSafetyCheck)
        #####
        #####--- Define user value for the Prerequisite TotalSafetyCheck --- END ---#####

        ##############################
        ## <----( Main Macro )----> ##
        ##############################

        #####--------------------  Compare TotalSafetyCheck value and decide or not to continue the process  --- START --------------------#####
        if TotalSafetyCheck == TotalSafetyCheckTrueValue:
            # Main Rebevel Macro

            lx.eval('select.type item')
            # lx.eval('select.editSet name:REBEVEL_ITEM mode:add')
            lx.eval('select.type polygon')
            lx.eval('select.editSet name:SelSet_toRemove mode:add')
            lx.eval('select.expand')
            lx.eval('select.useSet name:SelSet_toRemove mode:deselect')
            lx.eval('select.editSet name:SelSet_Expanded mode:add')
            lx.eval('select.useSet name:SelSet_Expanded mode:deselect')
            lx.eval('select.useSet name:SelSet_toRemove mode:select')
            lx.eval('select.loop')
            lx.eval('select.createSet name:SelSet_PolyLoop')
            lx.eval('select.expand')
            lx.eval('copy')

            ### Part 2 : Load the Predefined Assembly Preset

            try:
                ### Load Rebevel Preset for the processing ###
                # example:
                # mypath = lx.eval("query platformservice alias ? {kit_eterea_swissknife:scripts/geometry}")
                # lx.eval("preset.do {%s/Bowl.lxl}" % mypath)
                #####--- Define the Preset directory of the Custom CAD Presets to load the Rebevel Assembly --- START ---#####
                #####
                SMOCADPath = lx.eval("query platformservice alias ? {kit_SMO_CAD_TOOLS:Presets}")
                lx.out('RebevelPresetPath:', SMOCADPath)
                #####
                #####--- Define the Preset directory of the Custom CAD Presets to load the Rebevel Assembly --- START ---#####
                lx.eval('preset.do {%s/SMO_REBEVEL_ASS_15X.lxp}' % SMOCADPath)
                lx.eval('select.type item')
                lx.eval('select.drop item')

            except:
                sys.exit

            # time.sleep(0.1)

            try:
                lx.out('EdgeCount:', RebSideCount)
                lx.eval('select.drop item')
                lx.eval('select.useSet name:SMO_REBEVEL_Loc_control mode:select')

                # Set and get the value of the focal length channel
                # item.channel('Count').set(user_inputRebevelCount)
                # print(item.channel('Count').get())

                lx.eval('item.channel Count %s' % RebSideCount)
                lx.eval('select.drop item')
                lx.eval('select.useSet SMO_REBEVEL_SOURCEMesh select')
            #####
            #####---  Define User Value for Rebevel Count --- END ---#####

            except:
                sys.exit

            ### Part 3 : Paste the Curve into the Meshop Container to rebuild the Curve, then freeze the mesh and Bridge the 2 Edges Strips
            lx.eval('select.type polygon')
            lx.eval('paste')
            lx.eval('select.polygon action:remove test:vertex mode:curve value:4')
            lx.eval('select.polygon action:remove test:vertex mode:"b-spline" value:4')
            lx.eval('select.polygon remove vertex curve 3')
            lx.eval('select.useSet name:SelSet_toRemove mode:select')
            lx.eval('select.invert')
            lx.eval('!!delete')
            lx.eval('select.type vertex')
            lx.eval('select.vertex action:add test:poly mode:equal value:1')
            lx.eval('select.editSet name:Corner mode:add')
            lx.eval('select.drop vertex')
            lx.eval('select.type item')
            lx.eval('select.drop type:item')
            lx.eval('select.useSet name:SMO_REBEVEL_RESULT_Freezed mode:select')

            lx.eval('deformer.freeze duplicate:false')  ##### ERROR
            lx.eval('select.drop type:item')
            lx.eval('select.useSet name:SMO_REBEVEL_RESULT_Freezed mode:select')
            lx.eval('select.type edge')
            lx.eval('select.all')
            lx.eval('tool.set preset:"edge.bridge" mode:on')
            lx.eval('tool.setAttr edge.bridge segments 0')
            lx.eval('tool.setAttr edge.bridge remove true')
            lx.eval('tool.setAttr edge.bridge connect false')
            lx.eval('tool.setAttr edge.bridge mode curve')
            lx.eval('tool.doApply')
            lx.eval('select.nextMode')

            ### Part 4 : Update the Original Poly Selection with the new Polygon Strips

            lx.eval('select.type polygon')
            lx.eval('select.all')
            lx.eval('select.editSet name:Rebevel_DATA mode:add')
            lx.eval('copy')

            lx.eval('select.type item')
            lx.eval('select.drop item')
            lx.eval('select.useSet name:SMO_REBEVEL_SOURCEMesh mode:select')
            lx.eval('select.type polygon')
            lx.eval('select.all')
            lx.eval('!!delete')
            lx.eval('paste')
            # replay name:"Invert Selection"
            lx.eval('select.invert')
            # replay name:"Set Selection"
            lx.eval('select.type vertex')

            # replay name:"Select Vertices"
            lx.eval('select.vertex add poly equal 1')
            lx.eval('select.convert edge')

            lx.eval('tool.set preset:"edge.bridge" mode:on')
            lx.eval('tool.setAttr edge.bridge segments 0')
            lx.eval('tool.setAttr edge.bridge remove true')
            lx.eval('tool.setAttr edge.bridge connect false')
            lx.eval('tool.setAttr edge.bridge mode curve')
            lx.eval('tool.doApply')
            lx.eval('select.nextMode')
            lx.eval('select.convert type:polygon')
            # replay name:"Edit Selection Set"
            lx.eval('select.editSet name:LongPolyToDelete mode:add')
            # replay name:"Selection All"
            lx.eval('select.all')
            # replay name:"Add Boundary"
            lx.eval('script.run hash:"macro.scriptservice:92663570022:macro"')
            # replay name:"Make Polygons"
            lx.eval('poly.make type:auto')
            lx.eval('select.convert type:polygon')
            # replay name:"Edit Selection Set"
            lx.eval('select.editSet name:Top_Bottom mode:add')
            # replay name:"Select Polygons"
            lx.eval('select.polygon action:remove test:vertex mode:"b-spline" value:4')
            # replay name:"Select Polygons"
            lx.eval('select.polygon action:remove test:vertex mode:curve value:4')
            # replay name:"Select Polygons"
            lx.eval('select.polygon action:remove test:vertex mode:curve value:3')
            # replay name:"Use Selection Set"
            lx.eval('select.useSet name:LongPolyToDelete mode:select')
            # replay name:"Delete Selection"
            lx.eval('!!delete')
            # replay name:"Use Selection Set"
            lx.eval('select.useSet name:Rebevel_DATA mode:select')
            # replay name:"Use Selection Set"
            lx.eval('select.useSet name:Top_Bottom mode:select')
            # replay name:"Copy Selection"
            lx.eval('copy')

            ### Part 5 Go back to the Original scene and select the current item to be updated, then swithch to Polygon Mode

            lx.eval('select.drop type:item')
            lx.eval('select.type item')

            scene.select(mesh)
            # # replay name:"Use Selection Set"
            # lx.eval('select.useSet name:REBEVEL_ITEM mode:select')
            lx.eval('select.type polygon')

            ### Part 6

            # replay name:"Use Selection Set"
            lx.eval('select.useSet name:SelSet_toRemove mode:select')
            lx.eval('select.convert type:vertex')
            # replay name:"Contract Selection"
            lx.eval('select.contract')
            # replay name:"Edit Selection Set"
            lx.eval('select.editSet name:SelSet_VertexToRemove mode:add')
            lx.eval('select.type polygon')
            # replay name:"Delete Selection"
            lx.eval('!!delete')
            lx.eval('select.type vertex')
            # replay name:"Delete Selection"
            lx.eval('!!delete')
            lx.eval('select.type polygon')
            # replay name:"Use Selection Set"
            lx.eval('select.useSet name:SelSet_Expanded mode:select')
            # replay name:"Use Selection Set"
            lx.eval('select.useSet name:SelSet_PolyLoop mode:deselect')
            # replay name:"Create Selection Set"
            lx.eval('select.createSet name:SelSet_Sides')
            # replay name:"Use Selection Set"
            lx.eval('select.useSet name:SelSet_Expanded mode:select')
            # replay name:"Use Selection Set"
            lx.eval('select.useSet name:SelSet_Sides mode:deselect')
            # replay name:"Delete Selection Set"
            lx.eval('!select.deleteSet name:SelSet_Expanded all:false')
            # replay name:"Delete Selection Set"
            lx.eval('!select.deleteSet name:SelSet_PolyLoop all:false')
            # replay name:"Paste Selection"
            lx.eval('paste')
            # replay name:"Selection All"
            lx.eval('select.all')
            # replay name:"Add Boundary"
            lx.eval('script.run hash:"macro.scriptservice:92663570022:macro"')
            lx.eval('select.convert type:vertex')
            # replay name:"Merge Vertices"
            lx.eval('!vert.merge range:fixed dist:"1e-05" disco:false')
            lx.eval('select.type polygon')
            # replay name:"Selection All"
            lx.eval('select.all')
            # replay name:"Select Polygons"
            lx.eval('select.polygon action:remove test:vertex mode:curve value:4')
            # replay name:"Select Polygons"
            lx.eval('select.polygon action:remove test:vertex mode:"b-spline" value:4')
            # replay name:"Select Polygons"
            lx.eval('select.polygon action:remove test:vertex mode:curve value:3')
            # replay name:"Use Selection Set"
            lx.eval('select.useSet name:Top_Bottom mode:select')

            ### Part 7 Reconnect all the polygon parts on both side of the Rebeveled polyStrips

            # replay name:"MergeCoplanarPoly.LXM"
            # lx.eval('user.value sene_LS_facingRatio 1')
            # lx.eval('@lazySelect.pl selectTouching 1')
            lx.eval('smo.GC.SelectCoPlanarPoly 0 1 0')
            lx.eval('poly.merge')
            lx.eval('select.contract')
            lx.eval('select.type item')
            lx.eval('select.drop item')

            ### Part 8 Delete the Rebevel Assembly

            lx.eval('select.item Smo_REBEVEL_ASS set')
            lx.eval('!!delete')

            ### Part 9 Remove all the Temp SelectionSets on Edges / Vertex / Polygons

            # replay name:"Item"
            lx.eval('select.type item')
            lx.eval('select.less')
            lx.eval('select.type item')

            scene.select(mesh)
            # # replay name:"Use Selection Set"
            # lx.eval('select.useSet name:REBEVEL_ITEM mode:select')

            lx.eval('select.type polygon')
            # replay name:"Delete Selection Set"
            lx.eval('!select.deleteSet name:Rebevel_DATA')
            # replay name:"Delete Selection Set"
            lx.eval('!select.deleteSet name:SelSet_Sides all:false')
            lx.eval('select.type edge')
            lx.eval('!select.deleteSet name:Boundary all:false')
            lx.eval('select.type vertex')
            # replay name:"Delete Selection Set"
            lx.eval('!select.deleteSet name:SelSet_VertexToRemove all:false')
            # replay name:"Item"
            lx.eval('select.type item')
            lx.eval('select.type polygon')
            lx.eval('select.type item')

            # # replay name:"Delete Selection Set"
            # lx.eval('!select.deleteSet name:REBEVEL_ITEM')

            lx.eval('select.type polygon')
            # replay name:"Selection All"
            lx.eval('select.all')
            # replay name:"Invert Selection"
            lx.eval('select.invert')
            lx.eval('!poly.align')

        elif TotalSafetyCheck != TotalSafetyCheckTrueValue:
            lx.out('script Stopped: your mesh does not match the requirement for that script.')
            sys.exit

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

        lx.out('End of Rebevel Script')
        #####--------------------  Compare TotalSafetyCheck value and decide or not to continue the process  --- END --------------------#####


lx.bless(SMO_CAD_RebevelProcedByUser_Cmd, Cmd_Name)

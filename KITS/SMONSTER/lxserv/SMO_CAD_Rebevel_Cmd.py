# python
"""
Name:           SMO_CAD_Rebevel_Cmd.py

Purpose:        This script is designed to
                Test if 1 Item is selected and if more than 2
                Polygons are selected, then process a
                rebevel on the selected patch of Quads

Author:         Franck ELISABETH
Website:        https://www.smoluck.com
Created:        05/04/2021
Copyright:      (c) Franck Elisabeth 2017-2022
"""

import lx
import lxu
import modo
import sys

Cmd_Name = "smo.CAD.Rebevel"
# smo.CAD.Rebevel


class SMO_CAD_Rebevel_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
        self.dyna_Add("Side count", lx.symbol.sTYPE_INTEGER)
        self.basic_SetFlags (0, lx.symbol.fCMDARG_OPTIONAL)				# here the (0) define the argument index.

        self.SelModePoly = bool(lx.eval1("select.typeFrom typelist:polygon;vertex;edge;item ?"))

    def cmd_Flags(self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO

    def cmd_Interact(self):
        pass

    def cmd_UserName(self):
        return 'SMO CAD - Rebevel'

    def cmd_Desc(self):
        return 'With 1 Item selected and if more than 2 Polygons selected, Process a rebevel on the selected patch of Quads.'

    def cmd_Tooltip(self):
        return 'With 1 Item selected and if more than 2 Polygons selected, Process a rebevel on the selected patch of Quads.'

    def cmd_Help(self):
        return 'https://twitter.com/sm0luck'

    def basic_ButtonName(self):
        return 'SMO CAD - Rebevel'

    def basic_Enable(self, msg):
        return True

    def basic_Execute(self, msg, flags):
        scene = modo.scene.current()
        if self.SelModePoly:
            lx.eval('smo.MASTER.ForceSelectMeshItemOnly')

        mesh = scene.selectedByType('mesh')[0]



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



        ######################################
        # <----( Check Arguments State )----> #
        ######################################
        # If not Set, ask value to user via Popup window with textt field
        if self.dyna_IsSet(0):
            RebSideCount = self.dyna_Int(0)
        if not self.dyna_IsSet(0):
            RebSideCount = 4
            try:
                #####--- Define User Value for Count --- START ---#####
                #####
                #Create a user value that define the Count for the Command.
                lx.eval("user.defNew name:Count type:integer life:momentary")
                #Set the title name for the dialog window
                lx.eval('user.def Count dialogname "SMO CAD - Rebevel"')
                #Set the input field name for the value that the users will see
                lx.eval("user.def Count username {Set the side count value}")
                #The '?' before the user.value calls a popup to have the user set the value
                lx.eval("?user.value Count")
                #Now that the user set the value, i can query it
                UserInput_Count = lx.eval("user.value Count ?")
                lx.out('User Count:',UserInput_Count)
                RebSideCount = UserInput_Count
            except:
                pass
        print(RebSideCount)

        # ------------- ARGUMENTS Test
        # BuildMode = 0
        # ------------- ARGUMENTS ------------- #
        #
        # ------------- 5 ARGUMENTS ------------- #
        # args = lx.args()
        # lx.out(args)
        #
        # 0 = Simple Ngon
        # 1 = Radial Triple
        # RebSideCount = int(args[0])
        # lx.out('Rebuild Mode:', RebSideCount)
        # ------------- ARGUMENTS ------------- #

        # ------------------------------ #
        # <----( DEFINE VARIABLES )----> #
        # ------------------------------ #

        # ---------------- Define user value for all the different SafetyCheck --- START
        #####
        lx.eval("user.defNew name:SMO_SafetyCheck_Only1MeshItemSelected type:integer life:momentary")
        lx.eval("user.defNew name:SMO_SafetyCheck_PolygonModeEnabled type:integer life:momentary")
        lx.eval("user.defNew name:SMO_SafetyCheck_min3PolygonSelected type:integer life:momentary")
        #####
        # ---------------- Define user value for all the different SafetyCheck --- END

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

        # -------------------------- #
        # <---( SAFETY CHECK 1 )---> #
        # -------------------------- #

        # --------------------  safety check 1 : Only One Item Selected --- START
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
        # --------------------  safety check 1 : Only One Item Selected --- END

        # -------------------------- #
        # <---( SAFETY CHECK 2 )---> #
        # -------------------------- #

        # Polygon Selection Mode enabled --- START
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
        # Polygon Selection Mode enabled --- END

        # -------------------------- #
        # <---( SAFETY CHECK 3 )---> #
        # -------------------------- #

        # at Least 3 Polygons are selected --- START
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
        # at Least 3 Polygons are selected --- END
        except:
            sys.exit

        # ------------- Define user value for the Prerequisite TotalSafetyCheck --- START
        #####
        TotalSafetyCheckTrueValue = 3
        lx.out('SafetyCheck Desired Value', TotalSafetyCheckTrueValue)
        TotalSafetyCheck = (
                    SMO_SafetyCheck_Only1MeshItemSelected + SMO_SafetyCheck_PolygonModeEnabled + SMO_SafetyCheck_min3PolygonSelected)
        lx.out('SafetyCheck Current Value', TotalSafetyCheck)
        #####
        # ------------- Define user value for the Prerequisite TotalSafetyCheck --- END

        # ------------------------ #
        # <----( Main Macro )----> #
        # ------------------------ #

        # ---------------- Compare TotalSafetyCheck value and decide or not to continue the process  --- START
        if TotalSafetyCheck == TotalSafetyCheckTrueValue:
            # Main Rebevel Macro

            lx.eval('select.type item')
            lx.eval('select.editSet name:REBEVEL_ITEM mode:add')
            lx.eval('select.type polygon')
            lx.eval('select.editSet name:SelSet_toRemove mode:add')
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
                # ------------- Define the Preset directory of the Custom CAD Presets to load the Rebevel Assembly --- START
                #####
                SMOCADPath = lx.eval("query platformservice alias ? {kit_SMO_CAD_TOOLS:Presets}")
                lx.out('RebevelPresetPath:', SMOCADPath)
                #####
                # ------------- Define the Preset directory of the Custom CAD Presets to load the Rebevel Assembly --- START
                lx.eval('preset.do {%s/SMO_REBEVEL_ASS_2021.lxp}' % SMOCADPath)
                lx.eval('select.type item')
                lx.eval('select.drop item')
            except:
                sys.exit

            try:
                lx.out('EdgeCount:', RebSideCount)
                lx.eval('select.drop item')
                lx.eval('select.useSet name:SMO_REBPOLYSTRIPNORMALIZEDWIDTH_Loc_CTRL mode:select')

                # Set and get the value of the focal length channel
                # item.channel('Count').set(user_inputRebevelCount)
                # print(item.channel('Count').get())

                lx.eval('item.channel Count %s' % RebSideCount)
                lx.eval('select.drop item')
            except:
                sys.exit

            lx.eval('select.type item')
            lx.eval('smo.GC.DeselectAll')

            # Store Normal Data via polygons from the target mesh
            lx.eval('select.useSet NormalData select')
            lx.eval('select.type polygon')
            lx.eval('paste')
            lx.eval('select.drop polygon')
            lx.eval('select.type item')
            lx.eval('smo.GC.DeselectAll')

            ########/////////////////////////////
            lx.eval('select.useSet Normalized_PolyStrip_Output select')
            lx.eval('deformer.freeze duplicate:false')
            lx.eval('select.type polygon')
            lx.eval('!poly.align')
            lx.eval('select.useSet SelSet_Result select')
            lx.eval('copy')

            lx.eval('select.type item')
            lx.eval('smo.GC.DeselectAll')
            lx.eval('select.useSet name:REBEVEL_ITEM mode:select')
            lx.eval('select.type polygon')
            lx.eval('select.drop polygon')
            lx.eval('select.useSet SelSet_toRemove select')
            lx.eval('select.useSet SelSet_Expanded select')
            lx.eval('!!delete')
            lx.eval('paste')

            # Merge Vertex Borders back
            lx.eval('select.all')
            # replay name:"Add Boundary"
            lx.eval('script.run hash:"macro.scriptservice:92663570022:macro"')
            lx.eval('select.convert type:vertex')
            # replay name:"Merge Vertices"
            lx.eval('!vert.merge range:fixed dist:"1e-05" disco:false')
            lx.eval('select.type polygon')
            # replay name:"Selection All"
            lx.eval('select.all')

            lx.eval('select.drop polygon')
            # lx.eval('select.type item')
            # lx.eval('smo.GC.DeselectAll')

            lx.eval('select.useSet SelSet_Result select')
            lx.eval('hide.unsel')
            # replay name:"Select Polygons"
            lx.eval('select.polygon action:remove test:vertex mode:curve value:4')

            ### Part 7 Reconnect all the polygon parts on both side of the Rebeveled polyStrips

            # replay name:"MergeCoplanarPoly.LXM"
            # lx.eval('user.value sene_LS_facingRatio 1')
            # lx.eval('@lazySelect.pl selectTouching 1')
            lx.eval('smo.GC.SelectCoPlanarPoly 0 1 0')
            lx.eval('poly.merge')
            lx.eval('select.drop polygon')
            lx.eval('unhide')
            lx.eval('select.type item')
            lx.eval('smo.GC.DeselectAll')

            ### Part 8 Delete the RebuildPolyStrip Assembly
            lx.eval('select.item Rebevel_2021_ASS set')
            lx.eval('!!delete')

            ### Part 9 Remove all the Temp SelectionSets on Vertex / Edges / Polygons / Items
            lx.eval('select.useSet REBEVEL_ITEM select')

            lx.eval('select.type polygon')
            try:
                lx.eval('!select.deleteSet name:Rebevel_DATA all:false')
            except:
                pass
            try:
                lx.eval('!select.deleteSet name:SelSet_Expanded all:false')
            except:
                pass
            try:
                lx.eval('!select.deleteSet name:SelSet_PolyLoop all:false')
            except:
                pass
            try:
                lx.eval('!select.deleteSet name:SelSet_Result all:false')
            except:
                pass
            try:
                lx.eval('!select.deleteSet name:SelSet_toRemove all:false')
            except:
                pass
            try:
                lx.eval('!select.deleteSet name:Surrounding all:false')
            except:
                pass
            try:
                lx.eval('!select.deleteSet name:Top_Bottom all:false')
            except:
                pass

            lx.eval('select.type vertex')
            try:
                lx.eval('!select.deleteSet name:PtsBorders all:false')
            except:
                pass

            lx.eval('select.type edge')
            try:
                lx.eval('!select.deleteSet name:Boundary all:false')
            except:
                pass

            lx.eval('select.type item')
            try:
                lx.eval('!select.deleteSet name:REBEVEL_ITEM all:false')
            except:
                pass
            lx.eval('select.type polygon')




        elif TotalSafetyCheck != TotalSafetyCheckTrueValue:
            lx.out('script Stopped: your mesh does not match the requirement for that script.')
            sys.exit

        # -------------- COPY/PASTE END Procedure  -------------- #
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
        # -------------------------------------------- #

        lx.out('End of Rebevel Script')

        if not RefSystemActive:
            lx.eval('item.refSystem {}')
        if RefSystemActive:
            lx.eval('item.refSystem %s' % CurrentRefSystemItem)

        # ---------------- Compare TotalSafetyCheck value and decide or not to continue the process  --- END


lx.bless(SMO_CAD_Rebevel_Cmd, Cmd_Name)

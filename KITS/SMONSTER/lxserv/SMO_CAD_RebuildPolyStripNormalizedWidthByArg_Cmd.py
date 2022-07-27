# python
# ---------------------------------------
# Name:         SMO_CAD_RebuildPolyStripNormalizedWidthByArg_Cmd.py
# Version:      1.0
#
# Purpose:      This script is designed to:
#               Test if 1 Item is selected and if more than 3
#               Edges are selected, then process a
#               rebuild on the selected polystrip band (via 2 set of Edges).
#               The Middle Edge will be used to create an in between Width with a regular size all accross the ring.
#
# Author:       Franck ELISABETH
# Website:      http://www.smoluck.com
#
# Created:      31/03/2021
# Copyright:    (c) Franck Elisabeth 2017-2022
# ---------------------------------------
import lx, lxu, modo, sys

Cmd_Name = "smo.CAD.RebuildPolyStripNormalizedWidthByArg"
# smo.CAD.RebuildPolyStripNormalizedWidthByArg

class SMO_CAD_RebuildPolyStripNormalizedWidthByArg_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
        self.dyna_Add("Side count", lx.symbol.sTYPE_INTEGER)
        self.basic_SetFlags (0, lx.symbol.fCMDARG_OPTIONAL)				# here the (0) define the argument index.

        self.SelModeEdge = bool(lx.eval1("select.typeFrom typelist:edge;vertex;polygon;item ?"))
        self.SelModePoly = bool(lx.eval1("select.typeFrom typelist:polygon;vertex;edge;item ?"))

    def cmd_Flags(self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO

    def cmd_Interact(self):
        pass

    def cmd_UserName(self):
        return 'SMO CAD - Rebuild PolyStrip Normalized Width By Arg'

    def cmd_Desc(self):
        return 'Test if 1 Item is selected and if more than 3 Edges are selected, then process a rebuild on the selected polystrip band (via 2 set of Edges). The Middle Edge will be used to create an in between Width with a regular size all accross the ring.'

    def cmd_Tooltip(self):
        return 'Test if 1 Item is selected and if more than 3 Edges are selected, then process a rebuild on the selected polystrip band (via 2 set of Edges). The Middle Edge will be used to create an in between Width with a regular size all accross the ring.'

    def cmd_Help(self):
        return 'https://twitter.com/sm0luck'

    def basic_ButtonName(self):
        return 'SMO CAD - Rebuild PolyStrip Normalized Width By Arg'

    def basic_Enable(self, msg):
        return True

    def basic_Execute(self, msg, flags):
        scene = modo.scene.current()
        if self.SelModePoly == True or self.SelModeEdge == True:
            lx.eval('smo.MASTER.ForceSelectMeshItemOnly')

        mesh = scene.selectedByType('mesh')[0]

        # ############### 1 ARGUMENTS Test ###############
        RebSideCount= self.dyna_Int(0)
        # RebSideCount = 16
        # ############### ARGUMENTS ###############

        # # ############### 5 ARGUMENTS ###############
        # args = lx.args()
        # lx.out(args)
        #
        # # 0 = Simple Ngon
        # # 1 = Radial Triple
        # RebSideCount = int(args[0])
        # lx.out('Rebuild Mode:', RebSideCount)
        # # ############### ARGUMENTS ###############

        ################################
        # <----[ DEFINE VARIABLES ]---->#
        ################################

        #####--- Define user value for all the different SafetyCheck --- START ---#####
        #####
        lx.eval("user.defNew name:SMO_SafetyCheck_Only1MeshItemSelected type:integer life:momentary")
        lx.eval("user.defNew name:SMO_SafetyCheck_EdgeModeEnabled type:integer life:momentary")
        lx.eval("user.defNew name:SMO_SafetyCheck_min4EdgeSelected type:integer life:momentary")
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
            lx.eval('dialog.title {SMO Rebuild PolyStrip:}')
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

        #####--------------------  safety check 2: Edge Selection Mode enabled --- START --------------------#####
        selType = ""
        # Used to query layerservice for the list of polygons, edges or vertices.
        attrType = ""

        if lx.eval1("select.typeFrom typelist:vertex;polygon;edge;item;ptag ?"):
            selType = "vertex"
            attrType = "vert"

            SMO_SafetyCheck_EdgeModeEnabled = 0
            lx.eval('dialog.setup info')
            lx.eval('dialog.title {SMO Rebuild PolyStrip:}')
            lx.eval('dialog.msg {You must be in Edge Mode to run that script}')
            lx.eval('+dialog.open')
            lx.out('script Stopped: You must be in Edge Mode to run that script')
            sys.exit


        elif lx.eval1("select.typeFrom typelist:edge;vertex;polygon;item ?"):
            selType = "edge"
            attrType = "edge"

            SMO_SafetyCheck_EdgeModeEnabled = 1
            lx.out('script Running: Correct Component Selection Mode')


        elif lx.eval1("select.typeFrom typelist:polygon;vertex;edge;item ?"):
            selType = "polygon"
            attrType = "poly"

            SMO_SafetyCheck_EdgeModeEnabled = 0
            lx.eval('dialog.setup info')
            lx.eval('dialog.title {SMO Rebuild PolyStrip:}')
            lx.eval('dialog.msg {You must be in Edge Mode to run that script}')
            lx.eval('+dialog.open')
            lx.out('script Stopped: You must be in Edge Mode to run that script')
            sys.exit


        else:
            # This only fails if none of the three supported selection
            # modes have yet been used since the program started, or
            # if "item" or "ptag" (ie: materials) is the current
            # selection mode.
            SMO_SafetyCheck_EdgeModeEnabled = 0
            lx.eval('dialog.setup info')
            lx.eval('dialog.title {SMO Rebuild PolyStrip:}')
            lx.eval('dialog.msg {You must be in Edge Mode to run that script}')
            lx.eval('+dialog.open')
            lx.out('script Stopped: You must be in Edge Mode to run that script')
            sys.exit
        #####--------------------  safety check 2: Edge Selection Mode enabled --- END --------------------#####


        ##############################
        ####### SAFETY CHECK 3 #######
        ##############################

        #####--------------------  safety check 3: at Least 4 Edges are selected --- START --------------------#####
        try:
            #####--- Get current selected edge count --- START ---#####
            #####
            CsEdges = len(mesh.geometry.edges.selected)
            lx.out('Count Selected Edges', CsEdges)
            #####
            #####--- Get current selected edge count --- END ---#####
            if CsEdges < 4:
                SMO_SafetyCheck_min4EdgeSelected = 0
                lx.eval('dialog.setup info')
                lx.eval('dialog.title {SMO Rebuild PolyStrip:}')
                lx.eval('dialog.msg {You must select at least 4 edges to run that script}')
                lx.eval('+dialog.open')
                lx.out('script Stopped: Add more Edges to your selection')
                sys.exit

            elif CsEdges >= 4:
                SMO_SafetyCheck_min4EdgeSelected = 1
                lx.out('script running: right amount of edges in selection')
        except:
            sys.exit

        #####--- Define user value for the Prerequisite TotalSafetyCheck --- START ---#####
        #####
        TotalSafetyCheckTrueValue = 3
        lx.out('SafetyCheck Desired Value', TotalSafetyCheckTrueValue)
        TotalSafetyCheck = (
                    SMO_SafetyCheck_Only1MeshItemSelected + SMO_SafetyCheck_EdgeModeEnabled + SMO_SafetyCheck_min4EdgeSelected)
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
            lx.eval('select.editSet name:REBUILDPSTRIP_ITEM mode:add')


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
                lx.eval('preset.do {%s/SMO_REBPOLYSTRIPNORMALIZEDWIDTH_ASS.lxp}' % SMOCADPath)
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


            lx.eval('select.useSet REBUILDPSTRIP_ITEM select')
            lx.eval('select.type edge')
            lx.eval('select.editSet name:SelSetRebPS_Edge mode:add')
            lx.eval('select.convert vertex')
            lx.eval('select.convert polygon')
            lx.eval('select.editSet name:SelSetRebPS_PolytoRemove mode:add')
            lx.eval('copy')
            lx.eval('select.type item')
            lx.eval('select.drop item')

            # Store Normal Data via polygons from the target mesh
            lx.eval('select.useSet NormalData select')
            lx.eval('select.type polygon')
            lx.eval('paste')
            lx.eval('select.drop polygon')


            lx.eval('select.type item')
            lx.eval('select.drop item')
            lx.eval('select.useSet name:REBUILDPSTRIP_ITEM mode:select')
            lx.eval('select.type edge')
            lx.eval('select.useSet name:SelSetRebPS_Edge mode:select')

            # Create a New Mesh with the Edges as Curves
            lx.eval('pmodel.edgeToCurveCMD spline true')
            lx.eval('select.type item')
            lx.eval('select.editSet name:REBUILDPSTRIP_CRV mode:add')
            lx.eval('select.useSet name:REBUILDPSTRIP_ITEM mode:select')
            lx.eval('item.parent inPlace:0')
            lx.eval('select.drop item')

            # Select back the target mesh to remove the polygons that will be recreated.
            lx.eval('select.useSet name:REBUILDPSTRIP_ITEM mode:select')
            lx.eval('select.convert polygon')
            lx.eval('select.useSet name:SelSetRebPS_PolytoRemove mode:select')
            lx.eval('!!delete')

            # Get the Twin Curves
            lx.eval('select.type item')
            lx.eval('select.drop item')
            lx.eval('select.useSet name:REBUILDPSTRIP_CRV mode:select')
            lx.eval('select.type polygon')
            lx.eval('select.all')
            lx.eval('copy')
            lx.eval('select.type item')
            lx.eval('select.drop item')

            try:
                lx.out('EdgeCount:', RebSideCount)
                lx.eval('select.drop item')
                lx.eval('select.useSet name:SMO_REBPOLYSTRIPNORMALIZEDWIDTH_Loc_CTRL mode:select')

                # Set and get the value of the focal length channel
                # item.channel('Count').set(user_inputRebevelCount)
                # print(item.channel('Count').get())

                lx.eval('item.channel Count %s' % RebSideCount)
                lx.eval('select.drop item')
                lx.eval('select.useSet SelSetRebPS_ITEM_DATA select')
                #####
                #####---  Define User Value for Rebevel Count --- END ---#####

            except:
                sys.exit

            ### Part 3 : Paste the Curve into the Meshop Container to rebuild the Curve, then freeze the mesh and Bridge the 2 Edges Strips
            lx.eval('select.type polygon')
            lx.eval('paste')
            lx.eval('select.type item')
            lx.eval('select.drop item')

            lx.eval('select.useSet Normalized_PolyStrip_Output select')
            lx.eval('deformer.freeze duplicate:false')
            lx.eval('select.type polygon')
            lx.eval('select.all')
            lx.eval('cut')


            lx.eval('select.type item')
            lx.eval('select.drop item')
            lx.eval('select.useSet name:REBUILDPSTRIP_ITEM mode:select')
            lx.eval('select.type polygon')
            lx.eval('select.drop polygon')
            lx.eval('paste')

            lx.eval('select.drop polygon')
            lx.eval('!poly.align')
            lx.eval('select.type item')
            lx.eval('select.drop item')

            ### Part 8 Delete the RebuildPolyStrip Assembly
            lx.eval('select.item RebuildPolyStripNormalizedWidth_ASS set')
            lx.eval('!!delete')

            ### Part 9 Remove all the Temp SelectionSets on Vertex / Edges / Polygons / Items
            lx.eval('select.useSet name:REBUILDPSTRIP_CRV mode:select')
            lx.eval('!select.deleteSet name:REBUILDPSTRIP_CRV all:false')
            lx.eval('!!delete')
            lx.eval('select.type item')             # missing Delete Sel Set in Item Mode
            lx.eval('select.useSet name:REBUILDPSTRIP_ITEM mode:select')
            lx.eval('!select.deleteSet name:REBUILDPSTRIP_ITEM all:false')
            lx.eval('select.type edge')
            lx.eval('!select.deleteSet name:SelSetRebPS_Edge all:false')
            lx.eval('select.type item')


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


lx.bless(SMO_CAD_RebuildPolyStripNormalizedWidthByArg_Cmd, Cmd_Name)

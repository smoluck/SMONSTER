# python
# ---------------------------------------
# Name:         SMO_CAD_SmartRebuildWithCylinder_Cmd.py
# Version: 1.0
#
# Purpose:  This script is designed to Rebuild the
#           Selected Volume (Polygon Mode) with just a CYLINDER that
#           got the same Radius and Length as the Source volume it can be:
#
#                   a Closed Cylinder (Air Tight)
#                   an Opened Cylinder on both Side
#                   a Hole
#
# Author:       Franck ELISABETH
# Website:      http://www.smoluck.com
#
# Created:      13/04/2019
# Copyright:    (c) Franck Elisabeth 2017-2022
# ---------------------------------------

import lx, lxu, modo

Command_Name = "smo.CAD.SmartRebuildWithCylinder"
# smo.CAD.SmartRebuildWithCylinder 16 2 0 0

class SMO_CAD_SmartRebuildWithCylinder_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
        self.dyna_Add("Sides Count", lx.symbol.sTYPE_INTEGER)
        self.dyna_Add("Axes", lx.symbol.sTYPE_INTEGER)
        self.dyna_Add("Open Mode", lx.symbol.sTYPE_INTEGER)
        self.dyna_Add("Hole Mode", lx.symbol.sTYPE_INTEGER)

        self.SelModePoly = bool(lx.eval1("select.typeFrom typelist:polygon;vertex;edge;item ?"))

    def cmd_Flags(self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO

    def cmd_Interact(self):
        pass

    def cmd_UserName(self):
        return 'SMO CAD SmartRebuildWithCylinderHole'

    def cmd_Desc(self):
        return 'Selected Volume (Polygon Mode) with just a CYLINDER that got the same Radius and Length as the Source volume it can be.'

    def cmd_Tooltip(self):
        return 'Selected Volume (Polygon Mode) with just a CYLINDER that got the same Radius and Length as the Source volume it can be.'

    def cmd_Help(self):
        return 'https://twitter.com/sm0luck'

    def basic_ButtonName(self):
        return 'SMO CAD SmartRebuildWithCylinderHole'

    def basic_Enable(self, msg):
        return True

    def basic_Execute(self, msg, flags):
        scene = modo.scene.current()
        if self.SelModePoly == True:
            lx.eval('smo.MASTER.ForceSelectMeshItemOnly')



        # ################################
        # #<----[ DEFINE ARGUMENTS ]---->#
        # ################################
        CYLINDER_SIDES_COUNT = self.dyna_Int(0)  # Sides Count for the Cylinder as an integer value
        CYLINDER_AXES = self.dyna_Int(1)  # Axes selection:                               X = 0 ### Y = 1 ### Z = 2
        CYLINDER_OPEN = self.dyna_Int(2)  # Open the Cylinder (Via delete NGon):          1 = Enable ### 0 = Disable
        CYLINDER_TO_HOLE = self.dyna_Int(3)  # Change the Cylinder to an Hole:               1 = Enable ### 0 = Disable
        # Expose the Result of the Arguments
        if CYLINDER_SIDES_COUNT == 0:
            try:
                #####--- Define User Value for Count --- START ---#####
                #####
                # Create a user value that define the Count for the Command.
                lx.eval("user.defNew name:Count type:integer life:momentary")
                # Set the title name for the dialog window
                lx.eval('user.def Count dialogname "SMO CAD - Rebuild With Cylinder"')
                # Set the input field name for the value that the users will see
                lx.eval("user.def Count username {Set the side count value}")
                # The '?' before the user.value calls a popup to have the user set the value
                lx.eval("?user.value Count")
                # Now that the user set the value, i can query it
                UserInput_Count = lx.eval("user.value Count ?")
                lx.out('User Count:', UserInput_Count)
                CYLINDER_SIDES_COUNT = UserInput_Count
            except:
                pass
        # lx.out(CYLINDER_SIDES_COUNT, CYLINDER_AXES, CYLINDER_OPEN, CYLINDER_TO_HOLE)
        # ############### ARGUMENTS ###############

        # ##############################
        # #<----[ TEST ARGUMENTS ]---->#
        # ##############################
        # CYLINDER_SIDES_COUNT = 16
        # CYLINDER_AXES = 0
        # CYLINDER_OPEN = 0
        # CYLINDER_TO_HOLE = 0
        # ##############################



        # BugFix to preserve the state of the RefSystem (item at origin in viewport)
        # This query only works when an item is selected.
        RefSystemActive = bool()
        CurrentRefSystemItem = lx.eval('item.refSystem ?')
        # print(CurrentRefSystemItem)
        if len(CurrentRefSystemItem) != 0:
            RefSystemActive = True
            lx.eval('item.refSystem {}')
        else:
            RefSystemActive = False
        # print(RefSystemActive)


        mesh = scene.selectedByType('mesh')[0]
        CsPolys = len(mesh.geometry.polygons.selected)
        SelItems = (lx.evalN('query sceneservice selection ? locator'))
        lx.out('Selected items is:', SelItems)



        ################################
        # <----[ DEFINE VARIABLES ]---->#
        ################################

        #####--- Define user value for all the different SafetyCheck --- START ---#####
        #####
        lx.eval("user.defNew name:SMO_SafetyCheck_PolygonModeEnabled type:integer life:momentary")
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

        #####--------------------  safety check 1: Polygon Selection Mode enabled --- START --------------------#####

        selType = ""
        # Used to query layerservice for the list of polygons, edges or vertices.
        attrType = ""

        if lx.eval1("select.typeFrom typelist:vertex;polygon;edge;item;ptag ?"):
            selType = "vertex"
            attrType = "vert"

            SMO_SafetyCheck_PolygonModeEnabled = 0
            lx.eval('dialog.setup info')
            lx.eval('dialog.title {SMO REBUILD With CYLINDER CLOSED / CYLINDER OPENED / HOLE:}')
            lx.eval('dialog.msg {You must be in Polygon Mode to run that script}')
            lx.eval('+dialog.open')
            lx.out('script Stopped: You must be in Polygon Mode to run that script')
            sys.exit
            # sys.exit( "LXe_FAILED:Must be in polygon selection mode." )


        elif lx.eval1("select.typeFrom typelist:edge;vertex;polygon;item ?"):
            selType = "edge"
            attrType = "edge"

            SMO_SafetyCheck_PolygonModeEnabled = 0
            lx.eval('dialog.setup info')
            lx.eval('dialog.title {SMO REBUILD With CYLINDER CLOSED / CYLINDER OPENED / HOLE:}')
            lx.eval('dialog.msg {You must be in Polygon Mode to run that script}')
            lx.eval('+dialog.open')
            lx.out('script Stopped: You must be in Polygon Mode to run that script')
            sys.exit
            # sys.exit( "LXe_FAILED:Must be in polygon selection mode." )

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
            lx.eval('dialog.title {SMO REBUILD With CYLINDER CLOSED / CYLINDER OPENED / HOLE:}')
            lx.eval('dialog.msg {You must be in Polygon Mode to run that script}')
            lx.eval('+dialog.open')
            lx.out('script Stopped: You must be in Polygon Mode to run that script')
            sys.exit
            # sys.exit( "LXe_FAILED:Must be in polygon selection mode." )
        #####--------------------  safety check 1: Polygon Selection Mode enabled --- END --------------------#####


        ##############################
        ####### SAFETY CHECK 2 #######
        ##############################

        #####--------------------  safety check 2: at Least 1 Polygons is selected --- START --------------------#####
        lx.out('Count Selected Poly', CsPolys)

        if CsPolys < 1:
            SMO_SafetyCheck_min1PolygonSelected = 0
            lx.eval('dialog.setup info')
            lx.eval('dialog.title {SMO REBUILD With CYLINDER CLOSED / CYLINDER OPENED / HOLE:}')
            lx.eval('dialog.msg {You must select at least 1 polygon to run that script}')
            lx.eval('+dialog.open')
            lx.out('script Stopped: Add more polygons to your selection')
            sys.exit

        elif CsPolys >= 1:
            SMO_SafetyCheck_min1PolygonSelected = 1
            lx.out('script running: right amount of polygons in selection')
        #####--------------------  safety check 2: at Least 1 Polygons is selected --- END --------------------#####


        #####--- Define current value for the Prerequisite TotalSafetyCheck --- START ---#####
        #####
        TotalSafetyCheckTrueValue = 2
        lx.out('Desired Value', TotalSafetyCheckTrueValue)
        TotalSafetyCheck = (SMO_SafetyCheck_PolygonModeEnabled + SMO_SafetyCheck_min1PolygonSelected)
        lx.out('Current Value', TotalSafetyCheck)
        #####
        #####--- Define current value for the Prerequisite TotalSafetyCheck --- END ---#####


        ##############################
        ## <----( Main Macro )----> ##
        ##############################
        lx.out('Start of SMO REBUILD With CYLINDER CLOSED / CYLINDER OPENED / HOLE')
        #####--------------------  Compare TotalSafetyCheck value and decide or not to continue the process  --- START --------------------#####
        if TotalSafetyCheck == TotalSafetyCheckTrueValue:
            # Tag the Polygon to Rebuild From
            lx.eval('select.editSet name:TEMP_DATA_VOLUME mode:add')

            # Tag the Source Mesh
            lx.eval('select.typeFrom item')
            lx.eval('select.editSet name:SOURCE_REBUILD_VOLUME mode:add')

            # lx.eval('item.refSystem %s' % SelItems)
            lx.eval('select.type polygon')
            # Copy the Polygon Data
            lx.eval('copy')
            # Switch to Item Mode
            lx.eval('select.type item')
            # Tag the Source Mesh

            ### Part 2 : Load the Predefined Assembly Preset (it will switch the Selection mode to ITEM)
            try:
                ### Load Rebuild Cylinder Preset for the processing ###
                #####--- Define the Preset directory of the Custom CAD Presets to load the Rebuild Cylinder Assembly --- START ---#####
                #####
                SMOCADPath = lx.eval("query platformservice alias ? {kit_SMO_CAD_TOOLS:Presets}")
                lx.out('SMOCAD Preset Path:', SMOCADPath)
                #####
                #####--- Define the Preset directory of the Custom CAD Presets to load the Rebuild Cylinder Assembly --- START ---#####
                lx.eval('preset.do {%s/SMO_REBUILD_WITH_CYLINDER_Assembly_2021.lxp}' % SMOCADPath)
                lx.eval('select.type item')
                lx.eval('select.drop item')

            except:
                sys.exit

            lx.eval('select.useSet name:REBUILD_CYlinderGRP mode:select')
            lx.eval('select.useSet name:SOURCE_REBUILD_VOLUME mode:select')
            lx.eval('item.parent')
            lx.eval('select.drop item')
            lx.eval('select.useSet name:TEMP_DATA_VOLUME mode:select')
            # Switch to Polygon Mode
            lx.eval('select.type polygon')
            # Paste the Data
            lx.eval('paste')

            # Deselect the Polygons
            lx.eval('select.drop polygon')
            # Deselect the Item
            lx.eval('select.drop item')

            lx.eval('select.useSet SMO_CONTROLS_CYLINDER select')

            # Set the Value for the Cylinder Rebuild for SIDES and AXES
            lx.eval('item.channel SidesCountSelect %s' % CYLINDER_SIDES_COUNT)  # Sides Count
            lx.eval('item.channel AxisSelect %s' % CYLINDER_AXES)  # X = 0 ### Y = 1 ### Z = 2
            lx.eval('select.drop item')

            lx.eval('select.useSet name:TEMP_DATA_VOLUME mode:select')
            lx.eval('select.type polygon')
            lx.eval('select.all')
            lx.eval('workPlane.fitSelect')
            lx.eval('select.type item')
            lx.eval('select.convert type:center')
            lx.eval('matchWorkplanePos')
            lx.eval('workPlane.reset')
            lx.eval('select.type polygon')
            lx.eval('select.drop polygon')
            lx.eval('select.type item')
            lx.eval('select.drop item')
            lx.eval('select.useSet SMO_CYLINDER_SelSet select')
            lx.eval('transform.channel pos.X 0.0')
            lx.eval('transform.channel pos.Y 0.0')
            lx.eval('transform.channel pos.Z 0.0')
            lx.eval('select.drop item')

            # Select the CYLINDER Result
            lx.eval('select.useSet name:SMO_CYLINDER_SelSet mode:select')
            # Freeze the Meshop
            lx.eval('poly.freeze face:twoPoints disp:false tess:false fixed:false')
            # Switch to Polygon Mode
            lx.eval('select.typeFrom polygon')
            # Select All Poly
            lx.eval('select.all')
            # tag the polygons as: "CYLINDER"
            lx.eval('select.editSet CYLINDER add')

            lx.out('------ Arguments Results ------')
            if CYLINDER_OPEN == 1 and CYLINDER_TO_HOLE == 1:  # HOLE MODE
                # Deselect the Polygons
                lx.eval('select.drop polygon')
                lx.eval('select.polygon add vertex b-spline 4')
                lx.eval('!!delete')
                lx.eval('select.all')
                lx.eval('poly.flip')
                lx.eval('select.drop polygon')
                lx.out('MODE: HOLE')

            if CYLINDER_OPEN == 1 and CYLINDER_TO_HOLE == 0:  # CYLINDER OPENED
                # Deselect the Polygons
                lx.eval('select.drop polygon')
                lx.eval('select.polygon add vertex b-spline 4')
                lx.eval('!!delete')
                lx.eval('select.drop polygon')
                lx.out('MODE: CYLINDER OPENED')

            if CYLINDER_OPEN == 0 and CYLINDER_TO_HOLE == 0:  # CYLINDER CLOSED
                # Deselect the Polygons
                lx.out('MODE: CYLINDER CLOSED')
                lx.eval('select.drop polygon')

            # if CYLINDER_OPEN == "1":              # Cylinder OPENED:      1 = ENABLE
            # # Deselect the Polygons
            # lx.eval('select.drop polygon')
            # lx.eval('select.polygon add vertex b-spline 4')
            # lx.eval('!!delete')
            # lx.eval('select.all')
            # lx.out('OPEN CYLINDER Mode')

            # elif CYLINDER_OPEN != "1":
            # lx.out('CLOSED CYLINDER Mode')  # Cylinder OPENED:      0 = DISABLE

            # elif CYLINDER_TO_HOLE >= "1":         # Cylinder to an Hole:  1 = ENABLE
            # lx.eval('select.all')
            # lx.eval('poly.flip')
            # lx.out('HOLE Mode: Enable')

            # if CYLINDER_TO_HOLE < "1":          # Cylinder to an Hole:  0 = DISABLE
            # lx.eval('select.all')
            # lx.out('HOLE Mode: Disable')
            lx.eval('select.all')
            # Copy Selection
            lx.eval('copy')

            ### Select back the Source Mesh and update the geometry ###
            # Switch to Item Mode
            lx.eval('select.typeFrom item')
            # Select the SOURCE Mesh
            lx.eval('select.useSet name:SOURCE_REBUILD_VOLUME mode:replace')
            # Switch to Polygon Mode
            lx.eval('select.typeFrom polygon')
            # Deselect the Polygons
            lx.eval('select.drop polygon')
            # select the Polygon to Rebuild From
            lx.eval('select.useSet name:TEMP_DATA_VOLUME mode:select')
            # Delete the old shape Data
            lx.eval('!!delete')
            # Paste Data Result
            lx.eval('paste')
            # Deselect Polygons and Items
            lx.eval('select.drop polygon')
            lx.eval('select.typeFrom item')
            lx.eval('select.drop item')

            ### Part 8 Delete the "Rebuild With CUBE" Assembly
            lx.eval('select.item SMO_Rebuild_With_CYLINDER set')
            lx.eval('!!delete')

            lx.eval('select.type item')  # missing Delete Sel Set in Item Mode
            ### select back the Source Mesh and delete every TAG (Polygons and Item) ###
            lx.eval('select.useSet name:SOURCE_REBUILD_VOLUME mode:select')
            # Delete Selection Set ITEM
            lx.eval('!select.deleteSet name:SOURCE_REBUILD_VOLUME all:false')
            lx.eval('select.typeFrom polygon')
            # Delete Selection Set POLYGON
            lx.eval('!select.deleteSet name:CYLINDER all:false')

        if TotalSafetyCheck != TotalSafetyCheckTrueValue:
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

        if RefSystemActive == False:
            lx.eval('item.refSystem {}')
        if RefSystemActive == True:
            lx.eval('item.refSystem %s' % CurrentRefSystemItem)

        lx.out('End of SMO REBUILD With CYLINDER CLOSED / CYLINDER OPENED / HOLE')
        #####--------------------  Compare TotalSafetyCheck value and decide or not to continue the process  --- END

    def cmd_Query(self, index, vaQuery):
        lx.notimpl()

lx.bless(SMO_CAD_SmartRebuildWithCylinder_Cmd, Command_Name)


#### NOTE ####

# #python
# import modo, lx

# args = lx.args()
# lx.out(args)
# ARG_1st = args[0]
# ARG_2nd = args[1]
# ARG_3rd = args[2]	# Function A State: true or false
# ARG_4th = args[3]	# Function B State: true or false

# # Expose the Result of the Arguments
# lx.out(ARG_1st,ARG_2nd,ARG_3rd,ARG_4th)


# if ARG_3rd == "1":				# Function A Enable
# lx.out('Function A-- Enable')

# if ARG_3rd != "1":				# Function A Disable
# lx.out('Function A-- Disable')

# if ARG_4th == "1":				# Function B Enable
# lx.out('Function --B Enable')

# if ARG_4th != "1":				# Function B Disable
# lx.out('Function --B Disable')
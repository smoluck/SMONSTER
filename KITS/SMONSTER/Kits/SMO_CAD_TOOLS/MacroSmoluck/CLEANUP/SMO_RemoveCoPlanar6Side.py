#python
#---------------------------------------
# Name:         SMO_RemoveCoPlanar6Side.py
# Version:      1.0
#
# Purpose:      Select the Mesh in Item Mode
#               It only cleanup Polygons that are perfectly perpendicular to X Y Z Axis in both direction
#               (Some of the code is related to the Sceneca  LazySelect script. Thanks to him for let me integrate it here)
#
# Author:       Franck ELISABETH
# Website:      http://www.smoluck.com
#
# Created:      14/04/2019
# Copyright:    (c) Franck Elisabeth 2017-2022
#---------------------------------------

import modo, lx

scene = modo.scene.current()
mesh = scene.selectedByType('mesh')[0]
CsPolys = len(mesh.geometry.polygons.selected)


################################
#<----[ DEFINE VARIABLES ]---->#
################################

#####--- Define user value for all the different SafetyCheck --- START ---#####
#####
lx.eval("user.defNew name:SMO_SafetyCheck_ItemModeEnabled type:integer life:momentary")
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

#####--------------------  safety check 1: ITEM Selection Mode enabled --- START --------------------#####

selType = ""
# Used to query layerservice for the list of polygons, edges or vertices.
attrType = ""

if lx.eval1( "select.typeFrom typelist:vertex;polygon;edge;item;ptag ?" ):
    selType = "vertex"
    attrType = "vert"
    
    SMO_SafetyCheck_ItemModeEnabled = 0
    lx.eval('dialog.setup info')
    lx.eval('dialog.title {SMO REBUILD With CUBE:}')
    lx.eval('dialog.msg {You must be in ITEM Mode to run that script}')
    lx.eval('+dialog.open')
    lx.out('script Stopped: You must be in ITEM Mode to run that script')
    sys.exit
    #sys.exit( "LXe_FAILED:Must be in ITEM selection mode." )
    
    
elif lx.eval1( "select.typeFrom typelist:edge;vertex;polygon;item ?" ):
    selType = "edge"
    attrType = "edge"
    
    SMO_SafetyCheck_ItemModeEnabled = 0
    lx.eval('dialog.setup info')
    lx.eval('dialog.title {SMO REBUILD With CUBE:}')
    lx.eval('dialog.msg {You must be in ITEM Mode to run that script}')
    lx.eval('+dialog.open')
    lx.out('script Stopped: You must be in ITEM Mode to run that script')
    sys.exit
    #sys.exit( "LXe_FAILED:Must be in ITEM selection mode." )
    
elif lx.eval1( "select.typeFrom typelist:polygon;vertex;edge;item ?" ):
    selType = "polygon"
    attrType = "poly"
    
    SMO_SafetyCheck_ItemModeEnabled = 0
    lx.eval('dialog.setup info')
    lx.eval('dialog.title {SMO REBUILD With CUBE:}')
    lx.eval('dialog.msg {You must be in ITEM Mode to run that script}')
    lx.eval('+dialog.open')
    lx.out('script Stopped: You must be in ITEM Mode to run that script')
    sys.exit
    #sys.exit( "LXe_FAILED:Must be in ITEM selection mode." )


else:
    # This only fails if none of the three supported selection
    # modes have yet been used since the program started, or
    # if "item" or "ptag" (ie: materials) is the current
    # selection mode.
    SMO_SafetyCheck_ItemModeEnabled = 1
    lx.out('script Running: Correct Component Selection Mode')

#####--------------------  safety check 1: ITEM Selection Mode enabled --- END --------------------#####



#####--- Define current value for the Prerequisite TotalSafetyCheck --- START ---#####
#####
TotalSafetyCheckTrueValue = 1
lx.out('Desired Value',TotalSafetyCheckTrueValue)
TotalSafetyCheck = (SMO_SafetyCheck_ItemModeEnabled)
lx.out('Current Value',TotalSafetyCheck)
#####
#####--- Define current value for the Prerequisite TotalSafetyCheck --- END ---#####



##############################
## <----( Main Macro )----> ##
##############################
lx.out('Start of SMO Remove CoPlanar 6 Side')
#####--------------------  Compare TotalSafetyCheck value and decide or not to continue the process  --- START --------------------#####
if TotalSafetyCheck == TotalSafetyCheckTrueValue:

    ############################################################
    ### Tag the target Mesh and initialize the script.
    # Tag the Source Mesh
    lx.eval('select.editSet name:TARGET_RemoveCoPlanar6Side mode:add')
    # replay name:"Prepare LazySelect Loading"
    # lx.eval('@{kit_SMONSTER:scripts/lazySelect.pl}')
    # replay name:"Select by Items"
    lx.eval('select.typeFrom item;pivot;center;edge;polygon;vertex;ptag true')
    # replay name:"Hide Unselected MeshItems"
    lx.eval('hide.unsel')
    ############################################################




    ############################################################
    ### Load the Mesh Data for the cleanup ###
    try:
        ### Load RemoveCoPlanar6Side Preset for the processing ###
        #####--- Define the Preset directory of the Custom CAD Presets to load the RemoveCoPlanar6Side Assembly --- START ---#####
        #####
        SMOCADPath = lx.eval("query platformservice alias ? {kit_SMO_CAD_TOOLS:Presets}")
        lx.out('SMOCAD Preset Path:',SMOCADPath)
        #####
        #####--- Define the Preset directory of the Custom CAD Presets to load the RemoveCoPlanar6Side Assembly --- START ---#####
        lx.eval('preset.do {%s/SMO_RemoveCoPlanar6Side_Assembly.lxp}' % SMOCADPath)
        lx.eval('select.type item')
        lx.eval('select.drop item')
        
    except:
        sys.exit
    ############################################################
        
        
        
        
    ############################################################
    ### Copy the Cube DATA
    # Select the DATA Container
    lx.eval('select.useSet name:SMO_CUBE_RemoveCoPlanar mode:select')
    ### Copy Data and go back to the previous scene ###

    # replay name:"Select by Items"
    lx.eval('select.type polygon')
    # replay name:"Selection All"
    lx.eval('select.all')
    # replay name:"Copy Selection"
    lx.eval('copy')
    ############################################################



    ############################################################
    ### Paste the Cube DATA in the TARGET
    # replay name:"Select by Items"
    lx.eval('select.type item')
    # Select the DATA Container
    lx.eval('select.useSet name:TARGET_RemoveCoPlanar6Side mode:replace')
    # replay name:"Select by Items"
    lx.eval('select.type polygon')
    # Paste Data
    lx.eval('paste')
    ############################################################



    ############################################################
    ### Call Coplanar Cleanup Macro Process ###

    # replay name:"Use Selection Set"
    lx.eval('select.useSet name:SetSet_CubeFace_Top mode:replace')
    # replay name:"lazySelect.pl"


    lx.eval('@{kit_SMO_CAD_TOOLS:MacroSmoluck/DeleteEdgeInsidePoly.LXM}')

    # Deselect the Polygons
    lx.eval('select.drop polygon')
    # replay name:"Use Selection Set"
    lx.eval('select.useSet name:SetSet_CubeFace_Bottom mode:select')
    # replay name:"lazySelect.pl"
    # lx.eval('user.value sene_LS_facingRatio 0.1')
    # lx.eval('script.implicit name:"lazySelect.pl" args:selectAll')
    lx.eval('smo.GC.SelectCoPlanarPoly 2 2 1000')

    lx.eval('@{kit_SMO_CAD_TOOLS:MacroSmoluck/DeleteEdgeInsidePoly.LXM}')

    # Deselect the Polygons
    lx.eval('select.drop polygon')
    # replay name:"Use Selection Set"
    lx.eval('select.useSet name:SetSet_CubeFace_Left mode:select')
    # lx.eval('script.implicit name:"lazySelect.pl" args:selectAll')
    lx.eval('smo.GC.SelectCoPlanarPoly 2 2 1000')

    lx.eval('@{kit_SMO_CAD_TOOLS:MacroSmoluck/DeleteEdgeInsidePoly.LXM}')

    # Deselect the Polygons
    lx.eval('select.drop polygon')
    # replay name:"Use Selection Set"
    lx.eval('select.useSet name:SetSet_CubeFace_Right mode:select')
    # replay name:"lazySelect.pl"
    # lx.eval('script.implicit name:"lazySelect.pl" args:selectAll')
    lx.eval('smo.GC.SelectCoPlanarPoly 2 2 1000')

    lx.eval('@{kit_SMO_CAD_TOOLS:MacroSmoluck/DeleteEdgeInsidePoly.LXM}')

    # Deselect the Polygons
    lx.eval('select.drop polygon')
    # replay name:"Use Selection Set"
    lx.eval('select.useSet name:SetSet_CubeFace_Front mode:select')
    # replay name:"lazySelect.pl"
    # lx.eval('script.implicit name:"lazySelect.pl" args:selectAll')
    lx.eval('smo.GC.SelectCoPlanarPoly 2 2 1000')

    lx.eval('@{kit_SMO_CAD_TOOLS:MacroSmoluck/DeleteEdgeInsidePoly.LXM}')

    # Deselect the Polygons
    lx.eval('select.drop polygon')
    # replay name:"Use Selection Set"
    lx.eval('select.useSet name:SetSet_CubeFace_Back mode:select')
    # replay name:"lazySelect.pl"
    # lx.eval('script.implicit name:"lazySelect.pl" args:selectAll')
    lx.eval('smo.GC.SelectCoPlanarPoly 2 2 1000')

    lx.eval('@{kit_SMO_CAD_TOOLS:MacroSmoluck/DeleteEdgeInsidePoly.LXM}')

    # Deselect the Polygons
    lx.eval('select.drop polygon')
    # replay name:"Item"
    lx.eval('select.type item')


    # lx.eval('user.value sene_LS_facingRatio 2')



    lx.eval('select.type polygon')
    # replay name:"Use Selection Set"
    lx.eval('select.useSet name:SetSet_CubeFace_Top mode:select')
    lx.eval('select.type edge')
    lx.eval('select.type polygon')
    # replay name:"Delete Selection"
    lx.eval('!!delete')
    # replay name:"Use Selection Set"
    lx.eval('select.useSet name:SetSet_CubeFace_Back mode:select')
    lx.eval('select.type edge')
    lx.eval('select.type polygon')
    # replay name:"Delete Selection"
    lx.eval('!!delete')
    lx.eval('select.useSet name:SetSet_CubeFace_Bottom mode:select')
    lx.eval('select.type edge')
    lx.eval('select.type polygon')
    # replay name:"Delete Selection"
    lx.eval('!!delete')
    # replay name:"Use Selection Set"
    lx.eval('select.useSet name:SetSet_CubeFace_Front mode:select')
    lx.eval('select.type edge')
    lx.eval('select.type polygon')
    # replay name:"Delete Selection"
    lx.eval('!!delete')
    lx.eval('select.useSet name:SetSet_CubeFace_Left mode:select')
    lx.eval('select.type edge')
    lx.eval('select.type polygon')
    # replay name:"Delete Selection"
    lx.eval('!!delete')
    # replay name:"Use Selection Set"
    lx.eval('select.useSet name:SetSet_CubeFace_Right mode:select')
    lx.eval('select.type edge')
    lx.eval('select.type polygon')
    # replay name:"Delete Selection"
    lx.eval('!!delete')
    ############################################################


    ############################################################
    # DELETE the RemoveCoPlanar6Side Assembly
    lx.eval('select.type item')
    lx.eval('select.drop item')
    lx.eval('select.item SMO_RemoveCoPlanar6Side_ASS set')
    lx.eval('!!delete')
    ############################################################


    ############################################################
    # Select the back the TARGET
    lx.eval('select.useSet name:TARGET_RemoveCoPlanar6Side mode:replace')
    # Delete Selection Set of TARGET
    lx.eval('!select.deleteSet name:TARGET_RemoveCoPlanar6Side all:false')
    ############################################################
    
elif TotalSafetyCheck != TotalSafetyCheckTrueValue:
    lx.out('script Stopped: your mesh does not match the requirement for that script.')
    sys.exit
    
    
###############COPY/PASTE END Procedure#################
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
########################################################

lx.out('End of SMO Remove CoPlanar 6 Side')
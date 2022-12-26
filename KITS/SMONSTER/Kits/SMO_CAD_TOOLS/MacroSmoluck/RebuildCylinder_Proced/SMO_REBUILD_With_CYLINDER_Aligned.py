# python
"""
# Name:         SMO_REBUILD_With_CUBE.py
# Version: 1.0
# 
# Purpose: This script is designed to Rebuild the
# selected Volume with just a Cylinder that 
# got the same size as the Bounding Box of this Volume.
#
# Select at least 2 edges then at least one Polygon and run the script
# (it will get the orientation based on Edges selected and eplace all the connected Polygons from the last polygon selection)
#
# Author:       Franck ELISABETH
# Website:      https://www.smoluck.com
#
# Created:      13/03/2019
# Copyright:    (c) Franck Elisabeth 2017-2022
"""

import modo, lx

scene = modo.scene.current()
mesh = scene.selectedByType('mesh')[0]
CsPolys = len(mesh.geometry.polygons.selected)
CsEdges = len(mesh.geometry.edges.selected)


# ------------------------------ #
# <----( DEFINE VARIABLES )----> #
# ------------------------------ #

#####--- Define user value for all the different SafetyCheck --- START ---#####
#####
## Polygons
lx.eval("user.defNew name:SMO_SafetyCheck_PolygonModeEnabled type:integer life:momentary")
lx.eval("user.defNew name:SMO_SafetyCheck_min1PolygonSelected type:integer life:momentary")

## Edges
lx.eval("user.defNew name:SMO_SafetyCheck_EdgeModeEnabled type:integer life:momentary")
lx.eval("user.defNew name:SMO_SafetyCheck_minEdgeSelected type:integer life:momentary")
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
    lx.eval('dialog.title {SMO REBUILD With CYLINDER:}')
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
    lx.eval('dialog.title {SMO REBUILD With CYLINDER:}')
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
    lx.eval('dialog.title {SMO REBUILD With CYLINDER:}')
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
    lx.eval('dialog.title {SMO REBUILD With CYLINDER:}')
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



# -------------------------- #
# <----( Main Macro )----> #
# -------------------------- #
lx.out('Start of SMO REBUILD With CUBE')
#####--------------------  Compare TotalSafetyCheck value and decide or not to continue the process  --- START
if TotalSafetyCheck == TotalSafetyCheckTrueValue:
    # Switch to Edge Mode
    lx.eval('select.typeFrom edge')
    # Tag the Polygon to Rebuild From
    lx.eval('select.editSet name:TEMP_DATA_WORPLANEROT mode:add')
    # Switch to Polygon Mode
    lx.eval('select.typeFrom polygon')
    # Select Connected Polygons
    lx.eval('select.connect')
    # Tag the Polygon to Rebuild From
    lx.eval('select.editSet name:TEMP_DATA_VOLUME mode:add')
    # Copy the Polygon Data
    lx.eval('copy')
    # Switch to Item Mode
    lx.eval('select.typeFrom item')
    # Tag the Source Mesh
    lx.eval('select.editSet name:SOURCE_REBUILD_VOLUME mode:add')
    # Switch to Polygon Mode
    lx.eval('select.typeFrom polygon')
    
    ### Part 2 : Load the Predefined Assembly Preset (it will switch the Selection mode to ITEM)
    try:
        ### Load Rebevel Preset for the processing ###
        #####--- Define the Preset directory of the Custom CAD Presets to load the Rebevel Assembly --- START ---#####
        #####
        SMOCADPath = lx.eval("query platformservice alias ? {kit_SMO_CAD_TOOLS:Presets}")
        lx.out('SMOCAD Preset Path:',SMOCADPath)
        #####
        #####--- Define the Preset directory of the Custom CAD Presets to load the Rebevel Assembly --- START ---#####
        lx.eval('preset.do {%s/SMO_REBUILD_WITH_CYLINDER_Assembly_ViaWorkplane.lxp}' % SMOCADPath)
        lx.eval('select.type item')
        lx.eval('select.drop item')
        
    except:
        sys.exit
        
    # Select the DATA Container
    lx.eval('select.useSet name:SMO_DATA_SelSet mode:select')
    # Switch to Polygon Mode
    lx.eval('select.typeFrom polygon')
    # Paste the Data
    lx.eval('paste')
    
    
    # Switch to Edge Mode
    lx.eval('select.typeFrom edge')
    # Select the Workplane DATA
    lx.eval('select.useSet name:TEMP_DATA_WORPLANEROT mode:select')
    # replay name:"Set the Workplane to Polygon Selection"
    lx.eval('workPlane.fitSelect')
    # replay name:"Convert selection to Item"
    lx.eval('select.type item')
    # replay name:"Convert selection to Center"
    lx.eval('select.convert type:center')
    # replay name:"Match Center to Workplane Rotation"
    lx.eval('matchWorkplaneRot')
    # replay name:"Reset the Workplane"
    lx.eval('workPlane.reset')
    
    ## BUG FIX for Bug Report 59946
    # Deselect the Edges
    lx.eval('select.drop edge')
    ## BUG FIX for Bug Report 59946
    
    # Switch to Polygon Mode
    lx.eval('select.typeFrom polygon')
    # Select Connected Polygons
    lx.eval('select.connect')
    # replay name:"Set the Workplane to Polygon Selection"
    lx.eval('workPlane.fitSelect')
    # replay name:"Convert selection to Item"
    lx.eval('select.type item')
    # replay name:"Convert selection to Center"
    lx.eval('select.convert type:center')
    # replay name:"Match Center to Workplane Position"
    lx.eval('matchWorkplanePos')
    # replay name:"Reset the Workplane"
    lx.eval('workPlane.reset')
    
    
    # Deselect the Item
    lx.eval('select.drop item')
    # Select the CUBE Result
    lx.eval('select.useSet name:SMO_CYLINDER_SelSet mode:select')
    lx.eval('transform.channel pos.X 0.0')
    lx.eval('transform.channel pos.Y 0.0')
    lx.eval('transform.channel pos.Z 0.0')
    lx.eval('transform.channel rot.X 0.0')
    lx.eval('transform.channel rot.Y 0.0')
    lx.eval('transform.channel rot.Z 0.0')
    
    
    ##### OK
    # Freeze the Meshop
    lx.eval('poly.freeze face:twoPoints disp:false tess:false fixed:false')
    # Switch to Polygon Mode
    lx.eval('select.typeFrom polygon')
    # Select All Poly
    lx.eval('select.all')
    # tag the polygons as: "CYLINDER"
    lx.eval('select.editSet CYLINDER add')
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
    
    ### select back the Source Mesh and delete every TAG (Polygons and Item) ###
    lx.eval('select.useSet name:SOURCE_REBUILD_VOLUME mode:select')
    # Delete Selection Set ITEM
    lx.eval('!select.deleteSet name:SOURCE_REBUILD_VOLUME all:false')
    lx.eval('select.typeFrom polygon')
    # Delete Selection Set POLYGON
    lx.eval('!select.deleteSet name:CYLINDER all:false')
    
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

lx.out('End of SMO REBUILD With CYLINDER')
#####--------------------  Compare TotalSafetyCheck value and decide or not to continue the process  --- END
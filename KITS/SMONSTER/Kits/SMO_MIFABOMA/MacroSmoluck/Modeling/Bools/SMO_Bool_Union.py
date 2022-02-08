#python
#---------------------------------------
# Name:         SMO_Bool_Union.py
# Version: 1.0
#
# Purpose: This script is designed to
# boolean Union the last Polygon Selection
# (Connected Polygons) from the current Layer.
#
# Author:       Franck ELISABETH
# Website:      http://www.smoluck.com
#
# Created:      28/12/2018
# Copyright:    (c) Franck Elisabeth 2017-2022
#---------------------------------------

import modo
scene = modo.scene.current()
mesh = scene.selectedByType('mesh')[0]
CsPolys = len(mesh.geometry.polygons.selected)


################################
#<----[ DEFINE VARIABLES ]---->#
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

if lx.eval1( "select.typeFrom typelist:vertex;polygon;edge;item;ptag ?" ):
    selType = "vertex"
    attrType = "vert"
	
    SMO_SafetyCheck_PolygonModeEnabled = 0
    lx.eval('dialog.setup info')
    lx.eval('dialog.title {SMO_BoolSubtract:}')
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
    lx.eval('dialog.title {SMO_BoolSubtract:}')
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
    lx.eval('dialog.title {SMO_BoolSubtract:}')
    lx.eval('dialog.msg {You must be in Polygon Mode to run that script}')
    lx.eval('+dialog.open')
    lx.out('script Stopped: You must be in Polygon Mode to run that script')
    sys.exit
    #sys.exit( "LXe_FAILED:Must be in polygon selection mode." )
#####--------------------  safety check 1: Polygon Selection Mode enabled --- END --------------------#####



##############################
####### SAFETY CHECK 2 #######
##############################

#####--------------------  safety check 2: at Least 1 Polygons is selected --- START --------------------#####
lx.out('Count Selected Poly',CsPolys)

if CsPolys < 1:
	SMO_SafetyCheck_min1PolygonSelected = 0
	lx.eval('dialog.setup info')
	lx.eval('dialog.title {SMO_BoolSubtract:}')
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
lx.out('Desired Value',TotalSafetyCheckTrueValue)
TotalSafetyCheck = (SMO_SafetyCheck_PolygonModeEnabled + SMO_SafetyCheck_min1PolygonSelected)
lx.out('Current Value',TotalSafetyCheck)
#####
#####--- Define current value for the Prerequisite TotalSafetyCheck --- END ---#####



##############################
## <----( Main Macro )----> ##
##############################

#####--------------------  Compare TotalSafetyCheck value and decide or not to continue the process  --- START --------------------#####
if TotalSafetyCheck == TotalSafetyCheckTrueValue:
	# replay name:"Edit Selection Set"
	lx.eval('select.editSet name:Bool_Selected_Tag mode:add')
	# replay name:"Item"
	lx.eval('select.type item')
	lx.eval('select.editSet name:Bool_SOURCE_Tag mode:add')
	lx.eval('select.type polygon')
	# replay name:"Selection All"
	lx.eval('select.all')
	# replay name:"Cut Selection"
	lx.eval('cut')
	lx.eval('layer.new')
	# replay name:"Paste Selection"
	lx.eval('paste')
	# replay name:"Item"
	lx.eval('select.type item')
	# replay name:"Edit Selection Set"
	lx.eval('select.editSet name:Bool_Parent_Tag mode:add')
	# replay name:"Select Polygons"
	lx.eval('select.polygon action:remove test:0 mode:subdiv value:0')
	# replay name:"Use Selection Set"
	lx.eval('select.useSet name:Bool_Selected_Tag mode:select')
	# replay name:"Select Connected"
	lx.eval('select.connect')
	# replay name:"Cut Selection"
	lx.eval('cut')
	lx.eval('layer.new')
	# replay name:"Paste Selection"
	lx.eval('paste')
	# replay name:"Item"
	lx.eval('select.type item')
	# replay name:"Edit Selection Set"
	lx.eval('select.editSet name:Bool_Driver_Tag mode:add')
	lx.eval('select.less')
	# replay name:"Use Selection Set"
	lx.eval('select.useSet name:Bool_Driver_Tag mode:select')
	# replay name:"Use Selection Set"
	lx.eval('select.useSet name:Bool_Parent_Tag mode:select')
	# replay name:"Hide Unselected"
	lx.eval('hide.unsel')
	lx.eval('select.less')
	lx.eval('select.less')
	# replay name:"Use Selection Set"
	lx.eval('select.useSet name:Bool_Parent_Tag mode:select')
	
	
	
	##############################
	## <----( Main Command )----> 
	##############################
	# replay name:"Boolean Action UNION"
	lx.eval('poly.boolean mode:union')
	##############################
	## <----( Main Command )----> 
	##############################
	
	
	
	lx.eval('select.type polygon')
	# replay name:"Selection All"
	lx.eval('select.all')
	# replay name:"Copy Selection"
	lx.eval('copy')
	# replay name:"Item"
	lx.eval('select.type item')
	# replay name:"Delete"
	lx.eval('!delete')
	# replay name:"Use Selection Set"
	lx.eval('select.useSet name:Bool_Driver_Tag mode:select')
	# replay name:"Delete"
	lx.eval('!delete')
	lx.eval('select.useSet name:Bool_SOURCE_Tag mode:select')
	# replay name:"Unhide"
	lx.eval('unhide')
	lx.eval('select.type polygon')
	# replay name:"Paste Selection"
	lx.eval('paste')
	# replay name:"Item"
	lx.eval('select.type item')
	lx.eval('!select.deleteSet Bool_Driver_Tag false')
	lx.eval('!select.deleteSet Bool_Parent_Tag false')
	lx.eval('!select.deleteSet Bool_SOURCE_Tag false')
	lx.eval('select.type polygon')
	lx.eval('select.polygon remove 0 subdiv 0')
	
	
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

lx.out('End of SMO_Bool_Union Script')
#####--------------------  Compare TotalSafetyCheck value and decide or not to continue the process  --- END --------------------#####

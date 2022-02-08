#python
#---------------------------------------
# Name:         SMO_Transfer_UV_Pos_Tagit.py
# Version: 1.00
#
# Purpose: This script is designed to PreTag a set of 2 polygons on the Source Mesh
#
# Author:       Franck ELISABETH
# Website:      http://www.smoluck.com
#
# Created:      29/03/2019
# Modified:		01/04/2019
# Copyright:    (c) Franck Elisabeth 2017-2022
#---------------------------------------

#import the necessary Python libraries
import lx, lxu, os, modo

# get selected items using TD SDK
scene = modo.Scene()
mesh = scene.selectedByType('mesh')[0]
CsPolys = len(mesh.geometry.polygons.selected)


################################
#<----[ DEFINE VARIABLES ]---->#
################################
#####--- Define the PolygonSelSet Name Prefix --- START ---#####
#####
lx.eval("user.defNew name:SMO_SafetyCheck_PolygonModeEnabled type:integer life:momentary")
lx.eval("user.defNew name:SMO_SafetyCheck_2PolygonSelected type:integer life:momentary")

lx.eval("user.defNew name:PolySelSetPrefixName type:string life:momentary")
PolySelSetPrefixNameTAG = 'TRANSUVPOS_'
#####
#####--- Define the PolygonSelSet Name Prefix --- END ---#####

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
    lx.eval('dialog.title {SMO_Transfer_UV_Pos_Tagit:}')
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
    lx.eval('dialog.title {SMO_Transfer_UV_Pos_Tagit:}')
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
    lx.eval('dialog.title {SMO_Transfer_UV_Pos_Tagit:}')
    lx.eval('dialog.msg {You must be in Polygon Mode to run that script}')
    lx.eval('+dialog.open')
    lx.out('script Stopped: You must be in Polygon Mode to run that script')
    sys.exit
    #sys.exit( "LXe_FAILED:Must be in polygon selection mode." )
#####--------------------  safety check 1: Polygon Selection Mode enabled --- END --------------------#####



##############################
####### SAFETY CHECK 2 #######
##############################

#####--------------------  safety check 2: 2 Polygons are selected --- START --------------------#####
lx.out('Count Selected Poly',CsPolys)

if CsPolys != 2:
	SMO_SafetyCheck_2PolygonSelected = 0
	lx.eval('dialog.setup info')
	lx.eval('dialog.title {SMO_Transfer_UV_Pos_Tagit:}')
	lx.eval('dialog.msg {You must select ONLY 2 Polygons to run that script}')
	lx.eval('+dialog.open')
	lx.out('script Stopped: select ONLY 2 polygons')
	sys.exit

elif CsPolys == 2:
	SMO_SafetyCheck_2PolygonSelected = 1
	lx.out('script running: right amount of polygons in selection')
#####--------------------  safety check 2: 2 Polygons are selected --- END --------------------#####



#####--- Define current value for the Prerequisite TotalSafetyCheck --- START ---#####
#####
TotalSafetyCheckTrueValue = 2
lx.out('Desired Value',TotalSafetyCheckTrueValue)
TotalSafetyCheck = (SMO_SafetyCheck_PolygonModeEnabled + SMO_SafetyCheck_2PolygonSelected)
lx.out('Current Value',TotalSafetyCheck)
#####
#####--- Define current value for the Prerequisite TotalSafetyCheck --- END ---#####



##############################
## <----( Main Macro )----> ##
##############################

#####--------------------  Compare TotalSafetyCheck value and decide or not to continue the process  --- START --------------------#####
if TotalSafetyCheck == TotalSafetyCheckTrueValue:
	
	## Transfer UV Position TAGGER ## LOOP
	lx.out('<--- Transfer UV Position TAGGER --->')
	lx.out('<----------- START ---------->')
	try:
		#####--- Define User Value for Rebevel Count --- START ---#####
		#####
		# Create a user value that define the EdgeCount for the Rebevel.
		lx.eval("user.defNew name:Tag_ID type:string life:momentary")
		# Set the title name for the dialog window
		lx.eval('user.def Tag_ID dialogname "Define the Tag Number"')
		# Set the input field name for the value that the users will see
		lx.eval("user.def Tag_ID username {Enter the ID number here}")
		# The '?' before the user.value calls a popup to have the user set the value
		lx.eval("?user.value Tag_ID")
		# Now that the user set the value, i can query it
		user_inputTag_ID = lx.eval("user.value Tag_ID ?")
		lx.out('Tag_ID:',user_inputTag_ID)
		
		PolysetTag =  (PolySelSetPrefixNameTAG + user_inputTag_ID)
		lx.eval('select.editSet {%s} add' % PolysetTag)
		lx.eval('select.connect')
		lx.eval('select.editSet TRANSPOS_POLYISLAND_DONE add')
		lx.eval('hide.sel')
		#####
		#####---  Define User Value for Rebevel Count --- END ---#####
		
	except:
		sys.exit
	lx.out('<----------- END ----------->')
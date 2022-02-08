#python
#---------------------------------------
# Name: Unwrap_PlanarPosX_512px10cm.py
# Version: 1.0
#
# Purpose: This script is designed to
# Unwrap the current Polygon Selection
# on X Axis.
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

args = lx.args()
lx.out(args)
UVProjAxe = int(args[0])
lx.out('Desired Axe change:',UVProjAxe)


################################
#<----[ DEFINE VARIABLES ]---->#
################################

#####--- Define user value for all the different SafetyCheck --- START ---#####
#####
lx.eval("user.defNew name:SMO_SafetyCheck_PolygonModeEnabled type:integer life:momentary")
lx.eval("user.defNew name:SMO_SafetyCheck_min1PolygonSelected type:integer life:momentary")
#####
#####--- Define user value for all the different SafetyCheck --- END ---#####
	

	
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
    lx.eval('dialog.title {Unwrap_PlanarPosX_512px10cm:}')
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
    lx.eval('dialog.title {Unwrap_PlanarPosX_512px10cm:}')
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
    lx.eval('dialog.title {Unwrap_PlanarPosX_512px10cm:}')
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
	lx.eval('dialog.title {Unwrap_PlanarPosX_512px10cm:}')
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
    lx.eval('hide.unsel')
    lx.eval('tool.set preset:"uv.create" mode:on')
    lx.eval('tool.setAttr tool:"uv.create" attr:mode value:manual')

    ## Do a Projection on specific axis via Arguments
    # Command Block Begin:
    if UVProjAxe == 0 :
        lx.eval('tool.setAttr uv.create axis 0')	
    if UVProjAxe == 1 :
        lx.eval('tool.setAttr uv.create axis 1')
    if UVProjAxe == 2 :
        lx.eval('tool.setAttr uv.create axis 2')
    # Command Block End:

    try:
        # Command Block Begin:  
        lx.eval('tool.setAttr tool:"uv.create" attr:sizX value:"0.1"')
        lx.eval('tool.setAttr tool:"uv.create" attr:sizY value:"0.1"')
        lx.eval('tool.setAttr tool:"uv.create" attr:sizZ value:"0.1"')
        # Command Block End:
    except:
        sys.exit
        
    try:
        # Command Block Begin: 
        lx.eval('tool.setAttr tool:"uv.create" attr:cenX value:"0.0"')
        lx.eval('tool.setAttr tool:"uv.create" attr:cenY value:"0.0"')
        lx.eval('tool.setAttr tool:"uv.create" attr:cenZ value:"0.0"')
        # Command Block End:
    except:
        sys.exit
        
    lx.eval('tool.doapply')

    lx.eval('tool.set preset:"uv.create" mode:off')

    lx.eval('tool.viewType uv')
    # replay name:"Fit UVs"
    lx.eval('uv.fit entire true gapsByPixel:0.0 udim:1001')

    ###########################
    # replay name:"Flip UV Island"
    try:
        # Command Block Begin: 
        lx.eval('uv.flip false u')
        # Command Block End:
    except:
        sys.exit
    ###########################

    # replay name:"Move"
    lx.eval('tool.set preset:TransformMove mode:on')

    try:
        # Command Block Begin: 
        lx.eval('tool.setAttr tool:"xfrm.transform" attr:TX value:"-1.0"')
        lx.eval('tool.setAttr tool:"xfrm.transform" attr:TY value:"0.0"')
        lx.eval('tool.setAttr tool:"xfrm.transform" attr:TZ value:"0.0"')
        lx.eval('tool.setAttr tool:"xfrm.transform" attr:U value:"-1.0"')
        lx.eval('tool.setAttr tool:"xfrm.transform" attr:V value:"0.0"')
        # Command Block End:
    except:
        sys.exit
        
    # Launch the Move
    lx.eval('tool.doapply')
    lx.eval('tool.set preset:TransformMove mode:off')
    lx.eval('select.drop polygon')
    lx.eval('unhide')
    
elif TotalSafetyCheck != TotalSafetyCheckTrueValue:
	lx.out('script Stopped: your mesh does not match the requirement for that script.')
	sys.exit
	
lx.out('End of Unwrap_PlanarPosX_512px10cm Script')
#####--------------------  Compare TotalSafetyCheck value and decide or not to continue the process  --- END --------------------#####
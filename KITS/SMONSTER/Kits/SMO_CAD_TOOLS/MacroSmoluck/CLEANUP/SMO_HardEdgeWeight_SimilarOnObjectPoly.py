#python
#---------------------------------------
# Name:         SMO_HardEdgeWeight_SimilarOnObjectPoly.py
# Version:      1.0
#
# Purpose:      This script is designed to:
#               Select similar facing Polygon on object
#               anfd assign to their EdgeBorders a Subdivision Weight of 100%
#
# Author:       Franck ELISABETH
# Website:      http://www.smoluck.com
#
# Created:      22/01/2020
# Copyright:    (c) Franck Elisabeth 2017-2022
#---------------------------------------
import lx, modo

scene = modo.scene.current()




##############################
####### SAFETY CHECK 1 #######
##############################
lx.eval("user.defNew name:SMO_SafetyCheck_Only1MeshItemSelected type:integer life:momentary")
#####-------------------- safety check 1 : Only One Item Selected --- START --------------------#####
ItemCount = lx.eval('query layerservice layer.N ? fg')
lx.out('Selected Item count:', ItemCount)

if ItemCount != 1:
	SMO_SafetyCheck_Only1MeshItemSelected = 0
	lx.eval('dialog.setup info')
	lx.eval('dialog.title {SMO HardEdge Weight Similar On Object Poly:}')
	lx.eval('dialog.msg {You must only select the Mesh Item layer you are working on, in Item List, to run that script}')
	lx.eval('+dialog.open')
	lx.out('Only One Item Selected result:', SMO_SafetyCheck_Only1MeshItemSelected)
	lx.out('script Stopped: Select only one Mesh Item')
	sys.exit
	
else:
	SMO_SafetyCheck_Only1MeshItemSelected = 1
	lx.out('Only One Item Selected:', SMO_SafetyCheck_Only1MeshItemSelected)
	lx.out('script running: right amount of Mesh Item selected')
#####-------------------- safety check 1 : Only One Item Selected --- END --------------------#####


mesh = scene.selectedByType('mesh')[0]


##############################
####### SAFETY CHECK 2 #######
##############################
lx.eval("user.defNew name:SMO_SafetyCheck_PolygonModeEnabled type:integer life:momentary")
#####--------------------  safety check 2: Polygon Selection Mode enabled --- START --------------------#####
selType = ""
# Used to query layerservice for the list of polygons, edges or vertices.
attrType = ""

if lx.eval1( "select.typeFrom typelist:vertex;polygon;edge;item;ptag ?" ):
    selType = "vertex"
    attrType = "vert"
	
    SMO_SafetyCheck_PolygonModeEnabled = 0
    lx.eval('dialog.setup info')
    lx.eval('dialog.title {SMO HardEdge Weight Similar On Object Poly:}')
    lx.eval('dialog.msg {You must be in Polygon Mode to run that script}')
    lx.eval('+dialog.open')
    lx.out('script Stopped: You must be in Polygon Mode to run that script')
    sys.exit
    
	
elif lx.eval1( "select.typeFrom typelist:edge;vertex;polygon;item ?" ):
    selType = "edge"
    attrType = "edge"
	
    SMO_SafetyCheck_PolygonModeEnabled = 0
    lx.eval('dialog.setup info')
    lx.eval('dialog.title {SMO HardEdge Weight Similar On Object Poly:}')
    lx.eval('dialog.msg {You must be in Polygon Mode to run that script}')
    lx.eval('+dialog.open')
    lx.out('script Stopped: You must be in Polygon Mode to run that script')
    sys.exit
	
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
    lx.eval('dialog.title {SMO HardEdge Weight Similar On Object Poly:}')
    lx.eval('dialog.msg {You must be in Polygon Mode to run that script}')
    lx.eval('+dialog.open')
    lx.out('script Stopped: You must be in Polygon Mode to run that script')
    sys.exit
#####--------------------  safety check 2: Polygon Selection Mode enabled --- END --------------------#####



##############################
####### SAFETY CHECK 3 #######
##############################
lx.eval("user.defNew name:SMO_SafetyCheck_min1PolygonSelected type:integer life:momentary")
#####--------------------  safety check 3: at Least 1 Polygons are selected --- START --------------------#####
try:
	#####--- Get current selected polygon count --- START ---#####
	#####
	CsPolys = len(mesh.geometry.polygons.selected)
	lx.out('Count Selected Poly',CsPolys)
	#####
	#####--- Get current selected polygon count --- END ---#####



	if CsPolys < 1:
		SMO_SafetyCheck_min1PolygonSelected = 0
		lx.eval('dialog.setup info')
		lx.eval('dialog.title {SMO HardEdge Weight Similar On Object Poly:}')
		lx.eval('dialog.msg {You must select at least 1 polygon to run that script}')
		lx.eval('+dialog.open')
		lx.out('script Stopped: Add more polygons to your selection')
		sys.exit

	elif CsPolys >= 1:
		SMO_SafetyCheck_min1PolygonSelected = 1
		lx.out('script running: right amount of polygons in selection')
	#####--------------------  safety check 3: at Least 1 Polygons are selected --- END --------------------#####
except:
		sys.exit
		


if SMO_SafetyCheck_Only1MeshItemSelected == 1 and SMO_SafetyCheck_PolygonModeEnabled == 1 and SMO_SafetyCheck_min1PolygonSelected == 1 :
    # lx.eval('user.value name:sene_LS_facingRatio value:"0.5"')
    # lx.eval('script.implicit name:"lazySelect.pl" args:selectOnObject')
    lx.eval('smo.GC.SelectCoPlanarPoly 1 1 1000')
    # replay name:"Add Boundary"
    lx.eval('script.run hash:"macro.scriptservice:92663570022:macro"')
    # replay name:"Edge Weight Tool"
    lx.eval('script.run hash:"macro.scriptservice:3223571edge:macro"')
    lx.eval('tool.setAttr tool:"vertMap.setWeight" attr:weight value:"1.0"')
    lx.eval('tool.doApply')
    lx.eval('select.nextMode')
    lx.eval('select.drop edge')
    lx.eval('select.type polygon')
    # replay name:"Drop Selection"
    lx.eval('select.drop polygon')
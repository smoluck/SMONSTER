#python
#---------------------------------------
# Name:         SMO_SET_MoveCenterPositionAndRotation.py
# Version:      1.0
#
# Purpose: This script is designed to move Center
# and rotate Center of a Mesh Item based on
# Poly, Edge, and Vertex selection
#
# Author:       Franck ELISABETH
# Website:      http://www.smoluck.com
#
# Created:      10/03/2019
# Copyright:    (c) Franck Elisabeth 2017-2022
#---------------------------------------

import modo, lx

scene = modo.scene.current()
mesh = scene.selectedByType('mesh')[0]




################################
#<----[ DEFINE VARIABLES ]---->#
################################

#####--- Define user value for all the different SafetyCheck --- START ---#####
#####
####### SAFETY CHECK 1 ####### Only One Item Selected
lx.eval("user.defNew name:SMO_SafetyCheck_Only1MeshItemSelected type:integer life:momentary")


####### SAFETY CHECK 2 ####### Component Mode
lx.eval("user.defNew name:SMO_SafetyCheck_PolygonModeEnabled type:integer life:momentary")

lx.eval("user.defNew name:SMO_SafetyCheck_EdgeModeEnabled type:integer life:momentary")

lx.eval("user.defNew name:SMO_SafetyCheck_VertexModeEnabled type:integer life:momentary")


####### SAFETY CHECK 3 ####### Poly, Edge, Vertex Count
lx.eval("user.defNew name:SMO_SafetyCheck_min1PolygonSelected type:integer life:momentary")

lx.eval("user.defNew name:SMO_SafetyCheck_min1EdgeSelected type:integer life:momentary")

lx.eval("user.defNew name:SMO_SafetyCheck_min1VertexSelected type:integer life:momentary")

#####--- Define user value for all the different SafetyCheck --- END ---#####


##############################
####### SAFETY CHECK 1 #######
##############################

#####-------------------- safety check 1 : Only One Item Selected --- START --------------------#####
ItemCount = lx.eval('query layerservice layer.N ? selected')
lx.out('ItemCount', ItemCount)

if ItemCount != 1:
	SMO_SafetyCheck_Only1MeshItemSelected = 0
	lx.eval('dialog.setup info')
	lx.eval('dialog.title {Move Center:}')
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




###############################################
####### SAFETY CHECK 2 - Component Mode #######  --START--
###############################################

selType = ""
# Used to query layerservice for the list of polygons, edges or vertices.
attrType = ""

if lx.eval1( "select.typeFrom typelist:vertex;polygon;edge;item;ptag ?" ):
    selType = "vertex"
    attrType = "vert"
    
    SMO_SafetyCheck_VertexModeEnabled = 1
    lx.out('Vertex Mode:', SMO_SafetyCheck_VertexModeEnabled)
    SMO_SafetyCheck_EdgeModeEnabled = 0
    lx.out('Edge Mode:', SMO_SafetyCheck_EdgeModeEnabled)
    SMO_SafetyCheck_PolygonModeEnabled = 0    
    lx.out('Polygon Mode:', SMO_SafetyCheck_PolygonModeEnabled)
    
    #############################################
    ####### SAFETY CHECK 3 - Vertex Count #######  --START--
    #############################################
    
    #####--- Get current selected vertex count --- START ---#####
    #####
    CsVert = len(mesh.geometry.vertices.selected)
    lx.out('Count Selected Vertex',CsVert)
    #####
    #####--- Get current selected vertex count --- END ---#####
    
    try:

        if CsVert <= 0:
            SMO_SafetyCheck_min1VertexSelected = 0
            lx.out('script running: Vertex not selected')

        elif CsVert >= 1:
            SMO_SafetyCheck_min1VertexSelected = 1
            lx.out('script running: Vertex selected')
    except:
        sys.exit
    
	
elif lx.eval1( "select.typeFrom typelist:edge;vertex;polygon;item ?" ):
    selType = "edge"
    attrType = "edge"
	
    SMO_SafetyCheck_VertexModeEnabled = 0
    lx.out('Vertex Mode:', SMO_SafetyCheck_VertexModeEnabled)
    SMO_SafetyCheck_EdgeModeEnabled = 1
    lx.out('Edge Mode:', SMO_SafetyCheck_EdgeModeEnabled)
    SMO_SafetyCheck_PolygonModeEnabled = 0
    lx.out('Polygon Mode:', SMO_SafetyCheck_PolygonModeEnabled)
    
    #########################################
    ####### SAFETY CHECK - Edge Count #######  --START--
    #########################################

    #####--- Get current selected edge count --- START ---#####
    #####
    CsEdges = len(mesh.geometry.edges.selected)
    lx.out('Count Selected Edge',CsEdges)
    #####
    #####--- Get current selected edge count --- END ---#####
    
    try:
        if CsEdges <= 0:
            SMO_SafetyCheck_min1EdgeSelected = 0
            lx.out('script running: Edge not selected')

        elif CsEdges >= 1:
            SMO_SafetyCheck_min1EdgeSelected = 1
            lx.out('script running: Edge selected')
    except:
            sys.exit

            
elif lx.eval1( "select.typeFrom typelist:polygon;vertex;edge;item ?" ):
    selType = "polygon"
    attrType = "poly"
	
    SMO_SafetyCheck_VertexModeEnabled = 0
    lx.out('Vertex Mode:', SMO_SafetyCheck_VertexModeEnabled)
    SMO_SafetyCheck_EdgeModeEnabled = 0
    lx.out('Edge Mode:', SMO_SafetyCheck_EdgeModeEnabled)
    SMO_SafetyCheck_PolygonModeEnabled = 1
    lx.out('Polygon Mode:', SMO_SafetyCheck_PolygonModeEnabled)
    
    ############################################
    ####### SAFETY CHECK - Polygon Count #######  --START--
    ############################################

    #####--- Get current selected poly count --- START ---#####
    #####
    CsPolys = len(mesh.geometry.polygons.selected)
    lx.out('Count Selected Polygon',CsPolys)
    #####
    #####--- Get current selected poly count --- END ---#####
   
    try:
        if CsPolys <= 0:
            SMO_SafetyCheck_min1PolygonSelected = 0
            lx.out('script running: Polygon not selected')

        elif CsPolys >= 1:
            SMO_SafetyCheck_min1PolygonSelected = 1
            lx.out('script running: Polygon selected')
        #####--------------------  safety check 3: at Least 1 Polygons is selected --- END --------------------#####
    except:
            sys.exit

else:
	# This only fails if none of the three supported selection
    # modes have yet been used since the program started, or
    # if "item" or "ptag" (ie: materials) is the current
    # selection mode.
    sys.exit
    
#####--------------------  safety check 2: Polygon Selection Mode enabled --- END --------------------#####



#####--- Define user value for the Prerequisite TotalSafetyCheck --- START ---#####
#####
TotalSafetyCheckTrueValue = 2
lx.out('SafetyCheck Desired Value',TotalSafetyCheckTrueValue)
TotalSafetyCheck = (SMO_SafetyCheck_Only1MeshItemSelected + SMO_SafetyCheck_PolygonModeEnabled + SMO_SafetyCheck_EdgeModeEnabled + SMO_SafetyCheck_VertexModeEnabled)
lx.out('SafetyCheck Current Value',TotalSafetyCheck)
#####
#####--- Define user value for the Prerequisite TotalSafetyCheck --- END ---#####



#############################
## <----( Main Macro )----> ##
##############################

#####--------------------  Compare TotalSafetyCheck value and decide or not to continue the process  --- START --------------------#####
if TotalSafetyCheck <= TotalSafetyCheckTrueValue:
# Main Move Center Macro

    try:
        ### Part 1 : Create SelectionSet Tag & copy the data
        # replay name:"Set the Workplane to Polygon Selection"
        lx.eval('workPlane.fitSelect')
        # replay name:"Convert selection to Item"
        lx.eval('select.type item')
        # replay name:"Convert selection to Center"
        lx.eval('select.convert type:center')
        # replay name:"Match Center to Workplane Position"
        lx.eval('matchWorkplanePos')
        # replay name:"Match Center to Workplane Rotation"
        lx.eval('matchWorkplaneRot')
        # replay name:"Reset the Workplane"
        lx.eval('workPlane.reset')
        # replay name:"Item"
        lx.eval('select.typeFrom typelist:"polygon;vertex;ptag;item;pivot;center;edge" enable:true')
        
    except:
		sys.exit    
        
elif TotalSafetyCheck != TotalSafetyCheckTrueValue:
	lx.out('script Stopped: your mesh does not match the requirement for that script.')
	sys.exit
	
lx.out('Move Center Script')
#####--------------------  Compare TotalSafetyCheck value and decide or not to continue the process  --- END --------------------#####
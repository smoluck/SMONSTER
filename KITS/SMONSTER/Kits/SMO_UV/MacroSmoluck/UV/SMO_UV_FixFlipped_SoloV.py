#python
#---------------------------------------
# Name:         SMO_UV_FixFlipped_SoloV.py
# Version: 1.0
#
# Purpose: This script is designed to
# Unwrap the current Polygon Selection
# on V Axis.
#
# Author:       Franck ELISABETH
# Website:      http://www.smoluck.com
#
# Created:      01/07/2018
# Copyright:    (c) Franck Elisabeth 2017-2022
#---------------------------------------

import modo
scene = modo.scene.current()
mesh = scene.selectedByType('mesh')[0]

############### 1 ARGUMENT ###############
args = lx.args()
lx.out(args)
# Flip U = 0
# Flip V = 1
FlipAxes = int(args[0])
lx.out('Desired flip axes:',FlipAxes)
############### ARGUMENT ###############

# ############### 1 ARGUMENT Test ###############
# FlipAxes = 0
# ############### ARGUMENT ###############


################################
#<----[ DEFINE VARIABLES ]---->#
################################
#####--- Define user value for all the different SafetyCheck --- START ---#####
#####
lx.eval("user.defNew name:SMO_SafetyCheck_PolygonModeEnabled type:integer life:momentary")
lx.eval("user.defNew name:SMO_SafetyCheck_min1PolygonSelected type:integer life:momentary")
#####
#####--- Define user value for all the different SafetyCheck --- END ---#####



lx.out('Start of SMO_UV_FixFlipped Script')


###############################################
####### SAFETY CHECK 1 - UVMap Selected #######
###############################################

##########################
lx.out('<------------- START -------------->')
lx.out('<--- UV Map Safety Check --->')

# Get info about the selected UVMap.
UVmap_Selected = lx.evalN('query layerservice vmaps ? selected')
UVmap_SelectedN = len(lx.evalN('query layerservice vmaps ? selected'))
lx.out('Selected UV Map Index:', UVmap_SelectedN)


if UVmap_SelectedN <= 0:
    lx.eval('dialog.setup info')
    lx.eval('dialog.title {SMONSTER - Normalize and Pack:}')
    lx.eval('dialog.msg {You must have a UV map selected to run this script.}')
    lx.eval('dialog.open')
    sys.exit()

if UVmap_SelectedN > 1:
    lx.eval('dialog.setup info')
    lx.eval('dialog.title {SMONSTER - Normalize and Pack:}')
    lx.eval('dialog.msg {Please select Only One Vertex Map and run that script again.}')
    lx.eval('dialog.open')
    sys.exit()


UserUVMapName = lx.eval1('query layerservice vmap.name ? %s' %UVmap_Selected)
lx.out('USER UV Map Name:', UserUVMapName)	
    
lx.out('<- UV Map Safety Check ->')
lx.out('<------------- END -------------->')
##########################


################################################
####### SAFETY CHECK 2 -  Selection Mode #######
################################################

#####--------------------  safety check 2: Component Selection Mode type --- START --------------------#####

selType = ""
# Used to query layerservice for the list of polygons, edges or vertices.
attrType = ""

if lx.eval1( "select.typeFrom typelist:vertex;polygon;edge;item;ptag ?" ):
    selType = "vertex"
    attrType = "vert"
    
    SMO_SafetyCheck_VertexModeEnabled = 1
    SMO_SafetyCheck_EdgeModeEnabled = 0
    SMO_SafetyCheck_PolygonModeEnabled = 0
    SMO_SafetyCheck_ItemModeEnabled = 0
    
    lx.out('script Running: Vertex Component Selection Mode')
    
    
elif lx.eval1( "select.typeFrom typelist:edge;vertex;polygon;item ?" ):
    selType = "edge"
    attrType = "edge"
    
    SMO_SafetyCheck_VertexModeEnabled = 0
    SMO_SafetyCheck_EdgeModeEnabled = 1
    SMO_SafetyCheck_PolygonModeEnabled = 0
    SMO_SafetyCheck_ItemModeEnabled = 0
    
    lx.out('script Running: Edge Component Selection Mode')
    
elif lx.eval1( "select.typeFrom typelist:polygon;vertex;edge;item ?" ):
    selType = "polygon"
    attrType = "poly"
    
    SMO_SafetyCheck_VertexModeEnabled = 0
    SMO_SafetyCheck_EdgeModeEnabled = 0
    SMO_SafetyCheck_PolygonModeEnabled = 1
    SMO_SafetyCheck_ItemModeEnabled = 0
    
    lx.out('script Running: Polygon Component Selection Mode')


else:
    # This only fails if none of the three supported selection
    # modes have yet been used since the program started, or
    # if "item" or "ptag" (ie: materials) is the current
    # selection mode.
    
    SMO_SafetyCheck_VertexModeEnabled = 0
    SMO_SafetyCheck_EdgeModeEnabled = 0
    SMO_SafetyCheck_PolygonModeEnabled = 0
    SMO_SafetyCheck_ItemModeEnabled = 1
    
    lx.out('script Running: Item Component Selection Mode')

#####--------------------  safety check 2: Component Selection Mode type --- END --------------------#####



if SMO_SafetyCheck_VertexModeEnabled == 1:
    lx.eval('select.type polygon')
    SMO_SafetyCheck_PolygonModeEnabled = 1
    
if SMO_SafetyCheck_EdgeModeEnabled == 1:
    lx.eval('select.type polygon')
    SMO_SafetyCheck_PolygonModeEnabled = 1
    
if SMO_SafetyCheck_ItemModeEnabled == 1:
    lx.eval('select.type polygon')
    SMO_SafetyCheck_PolygonModeEnabled = 1
    
if SMO_SafetyCheck_PolygonModeEnabled == 1:
    lx.eval('select.type polygon')
    SMO_SafetyCheck_PolygonModeEnabled = 1


lx.eval('select.uvOverlap {%s} false false true false false false' % UserUVMapName)

# Test if the Polygon selection count
CsPolys = len(mesh.geometry.polygons.selected)
lx.out('Count Selected Poly',CsPolys)

if CsPolys < 1 :
    SMO_SafetyCheck_min1PolygonSelected = 0
    lx.out('script running: No Flipped UV Island')

elif CsPolys >= 1 :
    SMO_SafetyCheck_min1PolygonSelected = 1
    lx.out('script running: Flipped UV Island Detected')


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
if TotalSafetyCheckTrueValue == TotalSafetyCheck :
    if CsPolys < 1:
        SMO_SafetyCheck_min1PolygonSelected = 0
        lx.out('No UV Island to Flip')

    if CsPolys >= 1:
        SMO_SafetyCheck_min1PolygonSelected = 1
        lx.out('script running: right amount of polygons in selection')
        lx.eval('uv.flip false v')
        lx.eval('select.drop polygon')

    if SMO_SafetyCheck_VertexModeEnabled == 1:
        lx.eval('select.type vertex')

    if SMO_SafetyCheck_EdgeModeEnabled == 1:
        lx.eval('select.type edge')

    if SMO_SafetyCheck_ItemModeEnabled == 1:
        lx.eval('select.type item')

elif TotalSafetyCheck != TotalSafetyCheckTrueValue:
        lx.out('No UV Island to Flip')
    
lx.out('End of SMO_UV_FixFlipped Script')
#####--------------------  Compare TotalSafetyCheck value and decide or not to continue the process  --- END --------------------#####
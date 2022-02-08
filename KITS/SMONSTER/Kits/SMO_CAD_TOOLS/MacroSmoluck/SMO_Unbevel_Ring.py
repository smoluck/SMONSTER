#python
#---------------------------------------
# Name:         SMO_Unbevel_Ring.py
# Version: 1.0
#
# Purpose:  This script is designed to Rebuild the
#           selected Volume (Polygon Mode) with just a CYLINDER that 
#           got the same Radius and Length as the Source volume it can be:
#
# Author:       Franck ELISABETH
# Website:      http://www.smoluck.com
#
# Created:      16/04/2019
# Copyright:    (c) Franck Elisabeth 2017-2022
#---------------------------------------

import modo, lx

scene = modo.scene.current()
mesh = scene.selectedByType('mesh')[0]
CsEdges = len(mesh.geometry.edges.selected)


################################
#<----[ DEFINE VARIABLES ]---->#
################################

#####--- Define user value for all the different SafetyCheck --- START ---#####
#####
lx.eval("user.defNew name:SMO_SafetyCheck_EdgeModeEnabled type:integer life:momentary")
lx.eval("user.defNew name:SMO_SafetyCheck_min3EdgeSelected type:integer life:momentary")
#####
#####--- Define user value for all the different SafetyCheck --- END ---#####


lx.out('Start of SMO Unbevel Ring')


# ################################
# #<----[ DEFINE ARGUMENTS ]---->#
# ################################
# args = lx.args()
# lx.out(args)
# CYLINDER_SIDES_COUNT = args[0]                  # Sides Count for the Cylinder as an integer value
# CYLINDER_AXES = args[1]                         # Axes selection:                               X = 0 ### Y = 1 ### Z = 2
# CYLINDER_OPEN = args[2]                         # Open the Cylinder (Via delete NGon):          1 = Enable ### 0 = Disable
# CYLINDER_TO_HOLE = args[3]                      # Change the Cylinder to an Hole:               1 = Enable ### 0 = Disable
# # Expose the Result of the Arguments 
# lx.out(CYLINDER_SIDES_COUNT,CYLINDER_AXES,CYLINDER_OPEN,CYLINDER_TO_HOLE)



##############################
####### SAFETY CHECK 1 #######
##############################

#####--------------------  safety check 1: Edge Selection Mode enabled --- START --------------------#####

selType = ""
# Used to query layerservice for the list of polygons, edges or vertices.
attrType = ""

if lx.eval1( "select.typeFrom typelist:vertex;polygon;edge;item;ptag ?" ):
    selType = "vertex"
    attrType = "vert"
	
    SMO_SafetyCheck_EdgeModeEnabled = 0
    lx.eval('dialog.setup info')
    lx.eval('dialog.title {SMO Unbevel Ring:}')
    lx.eval('dialog.msg {You must be in Edge Mode to run that script}')
    lx.eval('+dialog.open')
    lx.out('script Stopped: You must be in Edge Mode to run that script')
    sys.exit
    #sys.exit( "LXe_FAILED:Must be in Edge selection mode." )
    
	
elif lx.eval1( "select.typeFrom typelist:edge;vertex;polygon;item ?" ):
	selType = "edge"
	attrType = "edge"
	SMO_SafetyCheck_EdgeModeEnabled = 1
	lx.out('script Running: Correct Component Selection Mode')

	
elif lx.eval1( "select.typeFrom typelist:polygon;vertex;edge;item ?" ):
    selType = "polygon"
    attrType = "poly"
	
    SMO_SafetyCheck_EdgeModeEnabled = 0
    lx.eval('dialog.setup info')
    lx.eval('dialog.title {SMO Unbevel Ring:}')
    lx.eval('dialog.msg {You must be in Edge Mode to run that script}')
    lx.eval('+dialog.open')
    lx.out('script Stopped: You must be in Edge Mode to run that script')
    sys.exit
    #sys.exit( "LXe_FAILED:Must be in polygon selection mode." )


else:
	# This only fails if none of the three supported selection
    # modes have yet been used since the program started, or
    # if "item" or "ptag" (ie: materials) is the current
    # selection mode.
    SMO_SafetyCheck_EdgeModeEnabled = 0
    lx.eval('dialog.setup info')
    lx.eval('dialog.title {SMO Unbevel Ring:}')
    lx.eval('dialog.msg {You must be in Edge Mode to run that script}')
    lx.eval('+dialog.open')
    lx.out('script Stopped: You must be in Edge Mode to run that script')
    sys.exit
    #sys.exit( "LXe_FAILED:Must be in Edge selection mode." )
#####--------------------  safety check 1: Edge Selection Mode enabled --- END --------------------#####


##############################
####### SAFETY CHECK 2 #######
##############################

#####--------------------  safety check 2: at Least 1 Polygons is selected --- START --------------------#####
lx.out('Count Selected Edges',CsEdges)

if CsEdges < 3:
	SMO_SafetyCheck_min3EdgeSelected = 0
	lx.eval('dialog.setup info')
	lx.eval('dialog.title {SMO Unbevel Ring:}')
	lx.eval('dialog.msg {You must select at least 3 edges to run that script}')
	lx.eval('+dialog.open')
	lx.out('script Stopped: Add more polygons to your selection')
	sys.exit

elif CsEdges >= 3:
	SMO_SafetyCheck_min3EdgeSelected = 1
	lx.out('script running: right amount of edges in selection')
#####--------------------  safety check 2: at Least 3 Edges is selected --- END --------------------#####



#####--- Define current value for the Prerequisite TotalSafetyCheck --- START ---#####
#####
TotalSafetyCheckTrueValue = 2
lx.out('Desired Value',TotalSafetyCheckTrueValue)
TotalSafetyCheck = (SMO_SafetyCheck_EdgeModeEnabled + SMO_SafetyCheck_min3EdgeSelected)
lx.out('Current Value',TotalSafetyCheck)
#####
#####--- Define current value for the Prerequisite TotalSafetyCheck --- END ---#####



##############################
## <----( Main Macro )----> ##
##############################

#####--------------------  Compare TotalSafetyCheck value and decide or not to continue the process  --- START --------------------#####
if TotalSafetyCheck == TotalSafetyCheckTrueValue:
	# lx.eval('@lazySelect.pl selectTouching 2')
    lx.eval('smo.GC.SelectCoPlanarPoly 0 2 0')
	lx.eval('select.ring')
	lx.eval('tool.set edge.relax on')
	lx.eval('tool.attr edge.relax convergence true')
	lx.eval('tool.noChange')
	lx.eval('tool.doApply')
	lx.eval('tool.set edge.relax off')

elif TotalSafetyCheck != TotalSafetyCheckTrueValue:
	lx.out('script Stopped: your mesh does not match the requirement for that script.')
	sys.exit
	
lx.out('End of SMO Unbevel Ring')
#####--------------------  Compare TotalSafetyCheck value and decide or not to continue the process  --- END --------------------#####



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


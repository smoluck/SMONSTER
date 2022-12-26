# python
"""
# Name:         SMO_MOD_Poly_To_BoundaryEdgeWeight.py
# Version:      1.0
#
# Purpose: This script is designed to appl
# a specific edge weight to Subdivision weights map
#
# Author:       Franck ELISABETH
# Website:      https://www.smoluck.com
#
# Created:      10/03/2018
# Copyright:    (c) Franck Elisabeth 2017-2022
"""

import modo

# Argument: the amount of EdgeWeight applied in percentage
UserWeightInput = lx.arg()


# ------------------------------ #
# <----( DEFINE VARIABLES )----> #
# ------------------------------ #


#####--- Define user value for all the different SafetyCheck --- START ---#####
#####
lx.eval("user.defNew name:SMO_SafetyCheck_PolygonModeEnabled type:integer life:momentary")
lx.eval("user.defNew name:UserWeightValue type:float life:momentary")

UserWeightValue = (UserWeightInput / 100)
lx.out('Weight value input',UserWeightInput)
lx.out('Weight value output',UserWeightValue)

#####
#####--- Define user value for all the different SafetyCheck --- END ---#####


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
	lx.eval('dialog.title {Poly_To_BoundaryEdgeWeight:}')
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
	lx.eval('dialog.title {Poly_To_BoundaryEdgeWeight:}')
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
	lx.eval('dialog.title {Poly_To_BoundaryEdgeWeight:}')
	lx.eval('dialog.msg {You must be in Polygon Mode to run that script}')
	lx.eval('+dialog.open')
	lx.out('script Stopped: You must be in Polygon Mode to run that script')
	sys.exit
	#sys.exit( "LXe_FAILED:Must be in polygon selection mode." )
# --------------------  safety check 1: Polygon Selection Mode enabled --- END


#####--- Define current value for the Prerequisite TotalSafetyCheck --- START ---#####
#####
TotalSafetyCheckTrueValue = 1
lx.out('Desired Value',TotalSafetyCheckTrueValue)
TotalSafetyCheck = SMO_SafetyCheck_PolygonModeEnabled
lx.out('Current Value',TotalSafetyCheck)
#####
#####--- Define current value for the Prerequisite TotalSafetyCheck --- END ---#####


# -------------------------- #
# <----( Main Macro )----> #
# -------------------------- #

#####--------------------  Compare TotalSafetyCheck value and decide or not to continue the process  --- START
if TotalSafetyCheck == TotalSafetyCheckTrueValue:
	# Select Edge Boundary
	lx.eval('script.run hash:"macro.scriptservice:3223571edge:macro"')

	lx.eval('tool.set vertMap.setWeight on')
	lx.eval('tool.attr vertMap.setWeight additive false')

	# Set edge weight by arguments
	lx.eval('tool.setAttr vertMap.setWeight weight %s' % UserWeightValue)
	lx.eval('tool.doApply')

elif TotalSafetyCheck != TotalSafetyCheckTrueValue:
	lx.out('script Stopped: please select a Polygon.')
	sys.exit
	
lx.out('End of Poly_To_BoundaryEdgeWeight Script')
#####--------------------  Compare TotalSafetyCheck value and decide or not to continue the process  --- END
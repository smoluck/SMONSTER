# python
"""
Name:           SMO_REBUILD_Plain_circle.py

Purpose:        This script is designed to Rebuild the
                selected Volume (Polygon Mode) with just a CYLINDER that 
                got the same Radius and Length as the Source volume it can be:

Author:         Franck ELISABETH
Website:        https://www.linkedin.com/in/smoluck/
Created:        16/04/2019
Copyright:      (c) Franck Elisabeth 2017-2022
"""

import lx
import modo
import sys

scene = modo.scene.current()
mesh = scene.selectedByType('mesh')[0]
CsPolys = len(mesh.geometry.polygons.selected)

# ------------------------------ #
# <----( DEFINE VARIABLES )----> #
# ------------------------------ #

# ---------------- Define user value for all the different SafetyCheck --- START
#####
lx.eval("user.defNew name:SMO_SafetyCheck_PolygonModeEnabled type:integer life:momentary")
lx.eval("user.defNew name:SMO_SafetyCheck_min1PolygonSelected type:integer life:momentary")
#####
# ---------------- Define user value for all the different SafetyCheck --- END


lx.out('Start of SMO REBUILD Plain Circle')

# -------------------------------- #
# <----( DEFINE ARGUMENTS )----> #
# -------------------------------- #
# args = lx.args()
# lx.out(args)
# CYLINDER_SIDES_COUNT = args[0]                  # Sides Count for the Cylinder as an integer value
# CYLINDER_AXES = args[1]                         # Axes selection:                               X = 0 ### Y = 1 ### Z = 2
# CYLINDER_OPEN = args[2]                         # Open the Cylinder (Via delete NGon):          1 = Enable ### 0 = Disable
# CYLINDER_TO_HOLE = args[3]                      # Change the Cylinder to an Hole:               1 = Enable ### 0 = Disable
# Expose the Result of the Arguments 
# lx.out(CYLINDER_SIDES_COUNT,CYLINDER_AXES,CYLINDER_OPEN,CYLINDER_TO_HOLE)


# -------------------------- #
# <---( SAFETY CHECK 1 )---> #
# -------------------------- #

# --------------------  safety check 1: Polygon Selection Mode enabled --- START

selType = ""
# Used to query layerservice for the list of polygons, edges or vertices.
attrType = ""

if lx.eval1("select.typeFrom typelist:vertex;polygon;edge;item;ptag ?"):
    selType = "vertex"
    attrType = "vert"

    SMO_SafetyCheck_PolygonModeEnabled = 0
    lx.eval('dialog.setup info')
    lx.eval('dialog.title {SMO REBUILD Plain Circle:}')
    lx.eval('dialog.msg {You must be in Polygon Mode to run that script}')
    lx.eval('+dialog.open')
    lx.out('script Stopped: You must be in Polygon Mode to run that script')
    sys.exit
    # sys.exit( "LXe_FAILED:Must be in polygon selection mode." )


elif lx.eval1("select.typeFrom typelist:edge;vertex;polygon;item ?"):
    selType = "edge"
    attrType = "edge"

    SMO_SafetyCheck_PolygonModeEnabled = 0
    lx.eval('dialog.setup info')
    lx.eval('dialog.title {SMO REBUILD Plain Circle:}')
    lx.eval('dialog.msg {You must be in Polygon Mode to run that script}')
    lx.eval('+dialog.open')
    lx.out('script Stopped: You must be in Polygon Mode to run that script')
    sys.exit
    # sys.exit( "LXe_FAILED:Must be in polygon selection mode." )

elif lx.eval1("select.typeFrom typelist:polygon;vertex;edge;item ?"):
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
    lx.eval('dialog.title {SMO REBUILD Plain Circle:}')
    lx.eval('dialog.msg {You must be in Polygon Mode to run that script}')
    lx.eval('+dialog.open')
    lx.out('script Stopped: You must be in Polygon Mode to run that script')
    sys.exit
    # sys.exit( "LXe_FAILED:Must be in polygon selection mode." )
# --------------------  safety check 1: Polygon Selection Mode enabled --- END


# -------------------------- #
# <---( SAFETY CHECK 2 )---> #
# -------------------------- #

# at Least 1 Polygons is selected --- START
lx.out('Count Selected Poly', CsPolys)

if CsPolys < 1:
    SMO_SafetyCheck_min1PolygonSelected = 0
    lx.eval('dialog.setup info')
    lx.eval('dialog.title {SMO REBUILD Plain Circle:}')
    lx.eval('dialog.msg {You must select at least 1 polygon to run that script}')
    lx.eval('+dialog.open')
    lx.out('script Stopped: Add more polygons to your selection')
    sys.exit

elif CsPolys >= 1:
    SMO_SafetyCheck_min1PolygonSelected = 1
    lx.out('script running: right amount of polygons in selection')
# at Least 1 Polygons is selected --- END


# ---------------- Define current value for the Prerequisite TotalSafetyCheck --- START
#####
TotalSafetyCheckTrueValue = 2
lx.out('Desired Value', TotalSafetyCheckTrueValue)
TotalSafetyCheck = (SMO_SafetyCheck_PolygonModeEnabled + SMO_SafetyCheck_min1PolygonSelected)
lx.out('Current Value', TotalSafetyCheck)
#####
# ---------------- Define current value for the Prerequisite TotalSafetyCheck --- END


# ------------------------ #
# <----( Main Macro )----> #
# ------------------------ #

# ---------------- Compare TotalSafetyCheck value and decide or not to continue the process  --- START
if TotalSafetyCheck == TotalSafetyCheckTrueValue:
    # lx.eval('@lazySelect.pl selectTouching 2')
    lx.eval('smo.GC.SelectCoPlanarPoly 0 2 0')
    lx.eval('poly.merge')

    lx.eval('tool.set actr.auto on')
    lx.eval('tool.set poly.bevel on')
    # Command Block Begin: ToolAdjustment
    lx.eval('tool.setAttr poly.bevel shift 0.0')
    lx.eval('tool.setAttr poly.bevel inset 0.001')  # 1 millimeter inset
    # Command Block End: ToolAdjustment
    lx.eval('tool.doApply')
    lx.eval('tool.drop')

    lx.eval('tool.set poly.bevel on')
    # Command Block Begin: ToolAdjustment
    lx.eval('tool.setAttr poly.bevel shift 0.0')
    lx.eval('tool.setAttr poly.bevel inset 0.005')
    # Command Block End: ToolAdjustment
    lx.eval('tool.doApply')
    lx.eval('tool.drop')

    lx.eval('poly.collapse')

elif TotalSafetyCheck != TotalSafetyCheckTrueValue:
    lx.out('script Stopped: your mesh does not match the requirement for that script.')
    sys.exit

lx.out('End of SMO REBUILD Plain Circle')
# ---------------- Compare TotalSafetyCheck value and decide or not to continue the process  --- END


# ------- NOTE ------- #

# python
# import modo, lx

# args = lx.args()
# lx.out(args)
# ARG_1st = args[0]                  
# ARG_2nd = args[1]                  
# ARG_3rd = args[2]	# Function A State: true or false                
# ARG_4th = args[3]	# Function B State: true or false

# Expose the Result of the Arguments 
# lx.out(ARG_1st,ARG_2nd,ARG_3rd,ARG_4th)


# if ARG_3rd == "1":				# Function A Enable
# lx.out('Function A-- Enable')

# if ARG_3rd != "1":				# Function A Disable
# lx.out('Function A-- Disable')

# if ARG_4th == "1":				# Function B Enable
# lx.out('Function --B Enable')

# if ARG_4th != "1":				# Function B Disable
# lx.out('Function --B Disable')

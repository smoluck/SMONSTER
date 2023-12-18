# python
"""
Name:               SMO_MOD_Mirror.py

Purpose:            This Script is designed to:
                    Mirror the last Polygon Selection
                    from the current Layer on a defined Axis.

Author:             Franck ELISABETH
Website:            https://www.linkedin.com/in/smoluck/
Created:            16/09/2019
Copyright:          (c) Franck Elisabeth 2017-2022
"""

import lx
import modo
import sys

scene = modo.scene.current()
mesh = scene.selectedByType('mesh')[0]
CsPolys = len(mesh.geometry.polygons.selected)
SelItems = (lx.evalN('query sceneservice selection ? locator'))
lx.out('In Selected items, List of their Unique Name is:', SelItems)

# ------------------------------ #
# <----( DEFINE VARIABLES )----> #
# ------------------------------ #

# ---------------- Define user value for all the different SafetyCheck --- START
#####
lx.eval("user.defNew name:SMO_SafetyCheck_PolygonModeEnabled type:integer life:momentary")
lx.eval("user.defNew name:SMO_SafetyCheck_min1PolygonSelected type:integer life:momentary")
#####
# ---------------- Define user value for all the different SafetyCheck --- END


# MIRROR_AXES = 0
# ------------------------------ #
# <----( DEFINE ARGUMENTS )----> #
# ------------------------------ #
args = lx.args()
lx.out(args)
MIRROR_AXES = args[0]               # Axes selection:            X = 0 ### Y = 1 ### Z = 2
# Expose the Result of the Arguments 
lx.out(MIRROR_AXES)
# ------------------------------ #
# <----( DEFINE ARGUMENTS )----> #
# ------------------------------ #


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
    lx.eval('dialog.title {SMO_Mirror:}')
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
    lx.eval('dialog.title {SMO_Mirror:}')
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
    lx.eval('dialog.title {SMO_Mirror:}')
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
    lx.eval('dialog.title {SMO_Mirror:}')
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
    if MIRROR_AXES == 0:
        lx.out('Mirror on X')
    if MIRROR_AXES == 1:
        lx.out('Mirror on Y')
    if MIRROR_AXES == 2:
        lx.out('Mirror on Z')
    lx.eval('tool.set actr.auto on')
    lx.eval('select.type item')
    lx.eval('item.refSystem %s' % SelItems)
    lx.eval('tool.set actr.origin on')
    lx.eval('select.type polygon')

    lx.eval('tool.set *.mirror on')
    # Command Block Begin:  ToolAdjustment
    lx.eval('tool.setAttr gen.mirror cenX 0.0')
    lx.eval('tool.setAttr gen.mirror cenY 0.0')
    lx.eval('tool.setAttr gen.mirror cenZ 0.0')
    # -------------------------- #
    # <----( Main Command )----> #
    # -------------------------- #
    if MIRROR_AXES == 0:
        lx.eval('tool.setAttr gen.mirror axis {%s}' % MIRROR_AXES)
        lx.eval('tool.setAttr gen.mirror leftX 0.0')
        lx.eval('tool.setAttr gen.mirror leftY 1')
        lx.eval('tool.setAttr gen.mirror leftZ 0.0')
        lx.eval('tool.setAttr gen.mirror upX 0.0')
        lx.eval('tool.setAttr gen.mirror upY 0.0')
        lx.eval('tool.setAttr gen.mirror upZ 1')
    if MIRROR_AXES == 1:
        lx.eval('tool.setAttr gen.mirror axis {%s}' % MIRROR_AXES)
        lx.eval('tool.setAttr gen.mirror leftX 0.0')
        lx.eval('tool.setAttr gen.mirror leftY 0.0')
        lx.eval('tool.setAttr gen.mirror leftZ 1')
        lx.eval('tool.setAttr gen.mirror upX 1')
        lx.eval('tool.setAttr gen.mirror upY 0.0')
        lx.eval('tool.setAttr gen.mirror upZ 0.0')
    if MIRROR_AXES == 2:
        lx.eval('tool.setAttr gen.mirror axis {%s}' % MIRROR_AXES)
        lx.eval('tool.setAttr gen.mirror leftX 1')
        lx.eval('tool.setAttr gen.mirror leftY 0.0')
        lx.eval('tool.setAttr gen.mirror leftZ 0.0')
        lx.eval('tool.setAttr gen.mirror upX 0.0')
        lx.eval('tool.setAttr gen.mirror upY 1')
        lx.eval('tool.setAttr gen.mirror upZ 0.0')
    # Command Block End:  ToolAdjustment
    lx.eval('tool.doApply')

    # -------------------------- #
    # <----( Main Command )----> #
    # -------------------------- #
    lx.eval('select.nextMode')
    lx.eval('select.drop polygon')
    lx.eval('item.refSystem {}')
    lx.eval('tool.set actr.auto on')


elif TotalSafetyCheck != TotalSafetyCheckTrueValue:
    lx.out('script Stopped: your mesh does not match the requirement for that script.')
    sys.exit

lx.out('End of SMO_Mirror Script')
# ---------------- Compare TotalSafetyCheck value and decide or not to continue the process  --- END

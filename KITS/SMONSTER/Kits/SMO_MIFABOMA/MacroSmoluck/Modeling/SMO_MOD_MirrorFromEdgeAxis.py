# python
"""
Name:               SMO_MOD_MirrorFromEdgeAxis.py

Purpose:            This Script is designed to:
                    Mirror the current Selection using 2 edges

Author:             Franck ELISABETH
Website:            https://www.linkedin.com/in/smoluck/
Created:            28/12/2018
Copyright:          (c) Franck Elisabeth 2017-2022
"""

import lx
import modo
import sys

scene = modo.scene.current()
mesh = scene.selectedByType('mesh')[0]
CsEdges = len(mesh.geometry.edges.selected)

# ------------------------------ #
# <----( DEFINE VARIABLES )----> #
# ------------------------------ #

# ---------------- Define user value for all the different SafetyCheck --- START
#####
lx.eval("user.defNew name:SMO_SafetyCheck_EdgeModeEnabled type:integer life:momentary")
lx.eval("user.defNew name:SMO_SafetyCheck_min1EdgesSelected type:integer life:momentary")
#####
# ---------------- Define user value for all the different SafetyCheck --- END


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

    SMO_SafetyCheck_EdgeModeEnabled = 0
    lx.eval('dialog.setup info')
    lx.eval('dialog.title {SMO_MOD_MirrorFromEdgeAxis:}')
    lx.eval('dialog.msg {You must be in Edge Mode to run that script}')
    lx.eval('+dialog.open')
    lx.out('script Stopped: You must be in Edge Mode to run that script')
    sys.exit
    # sys.exit( "LXe_FAILED:Must be in Edge selection mode." )


elif lx.eval1("select.typeFrom typelist:edge;vertex;polygon;item ?"):
    selType = "edge"
    attrType = "edge"

    SMO_SafetyCheck_EdgeModeEnabled = 1
    lx.out('script Running: Correct Component Selection Mode')


elif lx.eval1("select.typeFrom typelist:polygon;vertex;edge;item ?"):
    selType = "polygon"
    attrType = "poly"

    SMO_SafetyCheck_EdgeModeEnabled = 0
    lx.eval('dialog.setup info')
    lx.eval('dialog.title {SMO_MOD_MirrorFromEdgeAxis:}')
    lx.eval('dialog.msg {You must be in Edge Mode to run that script}')
    lx.eval('+dialog.open')
    lx.out('script Stopped: You must be in Edge Mode to run that script')
    sys.exit
    # sys.exit( "LXe_FAILED:Must be in edge selection mode." )



else:
    # This only fails if none of the three supported selection
    # modes have yet been used since the program started, or
    # if "item" or "ptag" (ie: materials) is the current
    # selection mode.
    SMO_SafetyCheck_EdgeModeEnabled = 0
    lx.eval('dialog.setup info')
    lx.eval('dialog.title {SMO_MOD_MirrorFromEdgeAxis:}')
    lx.eval('dialog.msg {You must be in Edge Mode to run that script}')
    lx.eval('+dialog.open')
    lx.out('script Stopped: You must be in Edge Mode to run that script')
    sys.exit
    # sys.exit( "LXe_FAILED:Must be in edge selection mode." )
# --------------------  safety check 1: Edge Selection Mode enabled --- END


# -------------------------- #
# <---( SAFETY CHECK 2 )---> #
# -------------------------- #

# at Least 1 Edge is selected --- START
lx.out('Selected Edges Count', CsEdges)

if CsEdges < 1:
    SMO_SafetyCheck_min1EdgesSelected = 0
    lx.eval('dialog.setup info')
    lx.eval('dialog.title {SMO_MOD_MirrorFromEdgeAxis:}')
    lx.eval('dialog.msg {You must select at least 1 Edge to run that script}')
    lx.eval('+dialog.open')
    lx.out('script Stopped: Add more Edges to your selection')
    sys.exit

if CsEdges == 1:
    SMO_SafetyCheck_min1EdgesSelected = 1
    MirrorAxe = 2
    lx.out('script running: right amount of Edges in selection')

if CsEdges == 2:
    SMO_SafetyCheck_min1EdgesSelected = 1
    MirrorAxe = 1
    lx.out('script running: right amount of Edges in selection')
# at Least 1 Edge is selected --- END


# ---------------- Define current value for the Prerequisite TotalSafetyCheck --- START
#####
TotalSafetyCheckTrueValue = 2
lx.out('Desired Value', TotalSafetyCheckTrueValue)
TotalSafetyCheck = (SMO_SafetyCheck_EdgeModeEnabled + SMO_SafetyCheck_min1EdgesSelected)
lx.out('Current Value', TotalSafetyCheck)
#####
# ---------------- Define current value for the Prerequisite TotalSafetyCheck --- END


# -------------------------- #
# <----( Main Macro )----> #
# -------------------------- #

# ---------------- Compare TotalSafetyCheck value and decide or not to continue the process  --- START
if TotalSafetyCheck == TotalSafetyCheckTrueValue:
    lx.eval('workPlane.reset')
    lx.eval('workPlane.fitSelect')
    lx.eval('tool.set actr.origin on')

    lx.eval('select.type polygon')
    lx.eval('tool.set *.mirror on')
    lx.eval('tool.attr effector.clone merge false')
    lx.eval('tool.attr gen.mirror axis {%s}' % MirrorAxe)
    lx.eval('tool.apply')
    lx.eval('select.nextMode')
    lx.eval('workPlane.reset')

if TotalSafetyCheck != TotalSafetyCheckTrueValue:
    lx.out('script Stopped: your mesh does not match the requirement for that script.')
    sys.exit

lx.out('End of SMO_HardenPolyIsland')
# ---------------- Compare TotalSafetyCheck value and decide or not to continue the process  --- END

# python
"""
Name:         	SMO_Bool_AxisDrill_Y_Stencil.py

Purpose: 		This script is designed to:
                Axis Drill on Y in Stencil Mode the last
                Polygon Selection from the current Layer.

Author:       	Franck ELISABETH
Website:      	https://www.smoluck.com
Created:      	28/12/2018
Copyright:    	(c) Franck Elisabeth 2017-2022
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
    lx.eval('dialog.title {SMO_BoolSubtract:}')
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
    lx.eval('dialog.title {SMO_BoolSubtract:}')
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
    lx.eval('dialog.title {SMO_BoolSubtract:}')
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
    lx.eval('dialog.title {SMO_BoolSubtract:}')
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
    # replay name:"Edit Selection Set"
    lx.eval('select.editSet name:AxisDrill_SelectedPoly_Tag mode:add')
    # replay name:"Item"
    lx.eval('select.type item')
    # replay name:"Edit Selection Set"
    lx.eval('select.editSet name:ProcessedMesh_Tag mode:add')
    lx.eval('select.less')
    # replay name:"Use Selection Set"
    lx.eval('select.useSet name:ProcessedMesh_Tag mode:select')
    # replay name:"Hide the rest"
    lx.eval('hide.unsel')
    # replay name:"Switch back to Polygon Mode"
    lx.eval('select.type polygon')
    # replay name:"Select the Polygon to drill"
    lx.eval('select.useSet name:AxisDrill_SelectedPoly_Tag mode:select')
    # replay name:"Cut poly data"
    lx.eval('cut')
    # replay name:"Create a new Mesh Layer"
    lx.eval('item.create type:mesh')
    # replay name:"Item mode"
    lx.eval('select.type item')
    # replay name:"Edit Selection Set"
    lx.eval('select.editSet name:AxisDrillPolyData_Tag mode:add')
    # replay name:"Switch back to Polygon Mode"
    lx.eval('select.type polygon')
    # replay name:"Paste poly data"
    lx.eval('paste')
    # replay name:"Item mode"
    lx.eval('select.type item')
    lx.eval('select.less')
    # replay name:"Use Selection Set"
    lx.eval('select.useSet name:ProcessedMesh_Tag mode:select')

    # -------------------------- #
    # <----( Main Command )----> #
    # -------------------------- #
    # replay name:"AxisDrill Action on Y"
    lx.eval('poly.drill mode:Stencil axis:Y material:Default cutmesh:background')
    # -------------------------- #
    # <----( Main Command )----> #
    # -------------------------- #

    lx.eval('select.less')
    # replay name:"Select Temp PolyData Layer"
    lx.eval('select.useSet name:AxisDrillPolyData_Tag mode:select')
    lx.eval('!delete')
    # replay name:"Use Selection Set"
    lx.eval('select.useSet name:ProcessedMesh_Tag mode:select')
    # replay name:"Delete Selection Set = Item"
    lx.eval('!select.deleteSet name:ProcessedMesh_Tag all:false')
    # replay name:"Switch back to Polygon Mode"
    lx.eval('select.type polygon')

    # replay name:"Item mode"
    lx.eval('select.type item')

    # replay name:"Unhide"
    lx.eval('unhide')



elif TotalSafetyCheck != TotalSafetyCheckTrueValue:
    lx.out('script Stopped: your mesh does not match the requirement for that script, please select a Polygon.')
    sys.exit

lx.out('End of SMO_Bool_AxisDrill_Y_Stencil Script')
# ---------------- Compare TotalSafetyCheck value and decide or not to continue the process  --- END

# python
"""
# Name:         SMO_DeleteEdgeInsidePoly_LS.py
# Version: 1.0
#
# Purpose:      This script is designed to:
#               Merge the selected Polygons based
#               on their facing Angle to delete the
#               Edges inside those Polygons.
#
# Author:       Franck ELISABETH
# Website:      https://www.smoluck.com
#
# Created:      22/01/2020
# Copyright:    (c) Franck Elisabeth 2017-2022
"""

import lx
import modo
import sys

scene = modo.scene.current()

# # ------------- ARGUMENTS Test
# Angle = 2
# LS_Mode = 0
# # ------------- ARGUMENTS ------------- #

# ------------- ARGUMENTS ------------- #
args = lx.args()
lx.out(args)

Angle = float(args[0])
lx.out('Lazy Select Facing Ratio Angle:', Angle)

# LS_Mode = 0 (Similar Touching Mode)
# LS_Mode = 1 (Similar on Object Mode)
# LS_Mode = 2 (Similar on Item Mode)
LS_Mode = int(args[1])
lx.out('Lazy Select Mode:', LS_Mode)
# ------------- ARGUMENTS ------------- #


# -------------------------- #
# <---( SAFETY CHECK 1 )---> #
# -------------------------- #
lx.eval("user.defNew name:SMO_SafetyCheck_Only1MeshItemSelected type:integer life:momentary")
# --------------------  safety check 1 : Only One Item Selected --- START
ItemCount = lx.eval('query layerservice layer.N ? fg')
lx.out('Selected Item count:', ItemCount)

if ItemCount != 1:
    SMO_SafetyCheck_Only1MeshItemSelected = 0
    lx.eval('dialog.setup info')
    lx.eval('dialog.title {SMO Delete Edge Inside Poly Advanced:}')
    lx.eval(
        'dialog.msg {You must only select the Mesh Item layer you are working on, in Item List, to run that script}')
    lx.eval('+dialog.open')
    lx.out('Only One Item Selected result:', SMO_SafetyCheck_Only1MeshItemSelected)
    lx.out('script Stopped: Select only one Mesh Item')
    sys.exit

else:
    SMO_SafetyCheck_Only1MeshItemSelected = 1
    lx.out('Only One Item Selected:', SMO_SafetyCheck_Only1MeshItemSelected)
    lx.out('script running: right amount of Mesh Item selected')
# --------------------  safety check 1 : Only One Item Selected --- END


mesh = scene.selectedByType('mesh')[0]

# -------------------------- #
# <---( SAFETY CHECK 2 )---> #
# -------------------------- #
lx.eval("user.defNew name:SMO_SafetyCheck_PolygonModeEnabled type:integer life:momentary")
# Polygon Selection Mode enabled --- START
selType = ""
# Used to query layerservice for the list of polygons, edges or vertices.
attrType = ""

if lx.eval1("select.typeFrom typelist:vertex;polygon;edge;item;ptag ?"):
    selType = "vertex"
    attrType = "vert"

    SMO_SafetyCheck_PolygonModeEnabled = 0
    lx.eval('dialog.setup info')
    lx.eval('dialog.title {SMO Delete Edge Inside Poly Advanced:}')
    lx.eval('dialog.msg {You must be in Polygon Mode to run that script}')
    lx.eval('+dialog.open')
    lx.out('script Stopped: You must be in Polygon Mode to run that script')
    sys.exit

elif lx.eval1("select.typeFrom typelist:edge;vertex;polygon;item ?"):
    selType = "edge"
    attrType = "edge"

    SMO_SafetyCheck_PolygonModeEnabled = 0
    lx.eval('dialog.setup info')
    lx.eval('dialog.title {SMO Delete Edge Inside Poly Advanced:}')
    lx.eval('dialog.msg {You must be in Polygon Mode to run that script}')
    lx.eval('+dialog.open')
    lx.out('script Stopped: You must be in Polygon Mode to run that script')
    sys.exit

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
    lx.eval('dialog.title {SMO Delete Edge Inside Poly Advanced:}')
    lx.eval('dialog.msg {You must be in Polygon Mode to run that script}')
    lx.eval('+dialog.open')
    lx.out('script Stopped: You must be in Polygon Mode to run that script')
    sys.exit
# Polygon Selection Mode enabled --- END


# -------------------------- #
# <---( SAFETY CHECK 3 )---> #
# -------------------------- #
lx.eval("user.defNew name:SMO_SafetyCheck_min1PolygonSelected type:integer life:momentary")
# at Least 3 Polygons are selected --- START
#####--- Get current selected polygon count --- START ---#####
#####
CsPolys = len(mesh.geometry.polygons.selected)
lx.out('Count Selected Poly', CsPolys)
#####
#####--- Get current selected polygon count --- END ---#####


if CsPolys == 0:
    SMO_SafetyCheck_min1PolygonSelected = 0
    lx.eval('dialog.setup info')
    lx.eval('dialog.title {SMO Delete Edge Inside Poly Advanced:}')
    lx.eval('dialog.msg {You must select more than 2 polygons selected to run that script}')
    lx.eval('+dialog.open')
    lx.out('script Stopped: Add more polygons to your selection')
    sys.exit

elif CsPolys >= 1:
    SMO_SafetyCheck_min1PolygonSelected = 1
    lx.out('script running: right amount of polygons in selection')
# at Least 3 Polygons are selected --- END


if SMO_SafetyCheck_Only1MeshItemSelected == 1 and SMO_SafetyCheck_PolygonModeEnabled == 1 and SMO_SafetyCheck_min1PolygonSelected == 1:
    # lx.eval('user.value sene_LS_facingRatio {%i}' % Angle)
    if LS_Mode == 0:
        # lx.eval('@lazySelect.pl selectTouching 2')
        lx.eval('smo.GC.SelectCoPlanarPoly 0 {%i} 0' % Angle)
        lx.eval('poly.merge')
    if LS_Mode == 1:
        # lx.eval('@lazySelect.pl selectOnObject')
        lx.eval('smo.GC.SelectCoPlanarPoly 1 2 1000')
    if LS_Mode == 2:
        # lx.eval('@lazySelect.pl selectAll')
        lx.eval('smo.GC.SelectCoPlanarPoly 2 2 1000')
    if LS_Mode == 1 or LS_Mode == 2:
        lx.eval('select.convert edge')
        lx.eval('select.contract')
        lx.eval('!!delete')
        lx.eval('select.nextMode')
    lx.eval('select.drop polygon')

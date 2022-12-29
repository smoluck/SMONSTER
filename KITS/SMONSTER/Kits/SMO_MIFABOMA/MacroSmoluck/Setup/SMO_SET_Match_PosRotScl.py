# python
"""
Name:         		SMO_SET_Match_PosRotScl.py

Purpose:            This Script is designed to:
                    Align a set of item on their position based on the first selected

Author:       		Franck ELISABETH
Website:      		https://www.smoluck.com
Created:      		28/12/2018
Copyright:    		(c) Franck Elisabeth 2017-2022
"""

import lx
import modo

scene = modo.scene.current()

# ------------- ARGUMENTS ------------- #
args = lx.args()
lx.out(args)
# No Match Position = 0
# Match Position on X = 1
# Match Position on Y = 2
# Match Position on Z = 3
# Match Position on All = 4
MatchPos = int(args[0])
lx.out('Match Position on Axe: ', MatchPos)
# No Match Rotation = 0
# Match Rotation on X = 1
# Match Rotation on Y = 2
# Match Rotation on Z = 3
# Match Rotation on All = 4
MatchRot = int(args[1])
lx.out('Match Rotation on Axe: ', MatchRot)
# No Match Scale = 0
# Match Scale on X = 1
# Match Scale on Y = 2
# Match Scale on Z = 3
# Match Scale on All = 4
MatchScl = int(args[2])
lx.out('Match Scale on Axe: ', MatchScl)
# To Last Selected = 0
# Average Mode = 1
Average = int(args[3])
lx.out('Average State: ', Average)
# ------------- ARGUMENTS ------------- #


# ------------------------------ #
# <----( DEFINE VARIABLES )----> #
# ------------------------------ #
# ---------------- Define user value for all the different SafetyCheck --- START
# Vertex
lx.eval("user.defNew name:SMO_SafetyCheck_VertexModeEnabled type:integer life:momentary")

# Edges
lx.eval("user.defNew name:SMO_SafetyCheck_EdgeModeEnabled type:integer life:momentary")

# Polygon
lx.eval("user.defNew name:SMO_SafetyCheck_PolygonModeEnabled type:integer life:momentary")

# Item
lx.eval("user.defNew name:SMO_SafetyCheck_ItemModeEnabled type:integer life:momentary")
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

    SMO_SafetyCheck_VertexModeEnabled = 1
    SMO_SafetyCheck_EdgeModeEnabled = 0
    SMO_SafetyCheck_PolygonModeEnabled = 0
    SMO_SafetyCheck_ItemModeEnabled = 0

    lx.out('script Running: Vertex Component Selection Mode')


elif lx.eval1("select.typeFrom typelist:edge;vertex;polygon;item ?"):
    selType = "edge"
    attrType = "edge"

    SMO_SafetyCheck_VertexModeEnabled = 0
    SMO_SafetyCheck_EdgeModeEnabled = 1
    SMO_SafetyCheck_PolygonModeEnabled = 0
    SMO_SafetyCheck_ItemModeEnabled = 0

    lx.out('script Running: Edge Component Selection Mode')

elif lx.eval1("select.typeFrom typelist:polygon;vertex;edge;item ?"):
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

# --------------------  safety check 1: Polygon Selection Mode enabled --- END


# ------------------------ #
# <----( Main Macro )----> #
# ------------------------ #

if MatchPos == 0:
    lx.out('Pos no change')
if MatchPos == 1:
    lx.eval('item.match item pos x %s' % Average)
if MatchPos == 2:
    lx.eval('item.match item pos y %s' % Average)
if MatchPos == 3:
    lx.eval('item.match item pos z %s' % Average)
if MatchPos == 4:
    lx.eval('item.match item pos all %s' % Average)

if MatchRot == 0:
    lx.out('Rotation no change')
if MatchRot == 1:
    lx.eval('item.match item rot x %s' % Average)
if MatchRot == 2:
    lx.eval('item.match item rot y %s' % Average)
if MatchRot == 3:
    lx.eval('item.match item rot z %s' % Average)
if MatchRot == 4:
    lx.eval('item.match item rot all %s' % Average)

if MatchScl == 0:
    lx.out('Scale no change')
if MatchScl == 1:
    lx.eval('item.match item scl x %s' % Average)
if MatchScl == 2:
    lx.eval('item.match item scl y %s' % Average)
if MatchScl == 3:
    lx.eval('item.match item scl z %s' % Average)
if MatchScl == 4:
    lx.eval('item.match item scl all %s' % Average)

# ------------- Compare SafetyCheck value and decide or not to continue the process  --- START
# if SMO_SafetyCheck_ItemModeEnabled == 1:

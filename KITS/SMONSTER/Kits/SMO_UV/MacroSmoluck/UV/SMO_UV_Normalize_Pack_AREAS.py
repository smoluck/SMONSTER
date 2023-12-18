# python
"""
Name:           Normalize_Pack_AREAS.py

Purpose:        This script is designed to:
                Normalize all the UV Islands based on their Area
                Tagging and Pack them in place

Author:         Franck ELISABETH
Website:        https://www.linkedin.com/in/smoluck/
Created:        28/12/2018
Copyright:      (c) Franck Elisabeth 2017-2022
"""

import lx
import modo

scene = modo.scene.current()
mesh = scene.selectedByType('mesh')[0]
meshseam = modo.Scene().selected[0]
lx.out('selected items:', mesh)

# ------------- ARGUMENTS ------------- #
# args = lx.args()
# lx.out(args)
# no Flipped = 0
# Flipped U = 1
# Flipped U = 2
# FixFlippedUV = int(args[0])
# lx.out('Fix Flipped error UV Island:',FixFlippedUV)
# ------------- ARGUMENTS ------------- #


# ------------------------------ #
# <----( DEFINE VARIABLES )----> #
# ------------------------------ #
# ---------------- Define user value for all the different SafetyCheck --- START
#####

# Vertex
lx.eval("user.defNew name:SMO_SafetyCheck_VertexModeEnabled type:integer life:momentary")

# Edges
lx.eval("user.defNew name:SMO_SafetyCheck_EdgeModeEnabled type:integer life:momentary")

# Polygon
lx.eval("user.defNew name:SMO_SafetyCheck_PolygonModeEnabled type:integer life:momentary")

# Item
lx.eval("user.defNew name:SMO_SafetyCheck_ItemModeEnabled type:integer life:momentary")

#####
# ---------------- Define user value for all the different SafetyCheck --- END


# -------------------------- #
# <---( SAFETY CHECK 1 )---> #
# -------------------------- #
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

UserUVMapName = lx.eval1('query layerservice vmap.name ? %s' % UVmap_Selected)
lx.out('USER UV Map Name:', UserUVMapName)

lx.out('<- UV Map Safety Check ->')
lx.out('<------------- END -------------->')


# -------------------------- #
# <---( SAFETY CHECK 2 )---> #
# -------------------------- #
# Component Selection Mode type --- START

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

# Component Selection Mode type --- END


# ------------- Compare SafetyCheck value and decide or not to continue the process  --- START
if SMO_SafetyCheck_VertexModeEnabled == 1:
    lx.eval('select.type polygon')

if SMO_SafetyCheck_EdgeModeEnabled == 1:
    lx.eval('select.type polygon')

if SMO_SafetyCheck_ItemModeEnabled == 1:
    lx.eval('select.type polygon')

if SMO_SafetyCheck_PolygonModeEnabled == 1:
    lx.eval('select.type polygon')

# if FixFlippedUV == 1:
# ### Load the Mesh Data for the cleanup ###
# lx.eval('select.uvOverlap {%s} false false true false false false' % UserUVMapName)
# CsPolysFlipped = len(mesh.geometry.polygons.selected)
# if CsPolysFlipped == 0:
# lx.out('No Flipped Poly')
# lx.eval('select.drop polygon')

# if CsPolysFlipped >= 1:
# lx.out('Flipped Poly Detected')
# lx.eval('uv.flip false u')
# lx.eval('select.drop polygon')


# replay name:"Hide Unselected"
# lx.eval('hide.unsel')


# ------------- Unwrap
# Unwrap Conform
lx.eval('tool.set util.udim on')
lx.eval('tool.noChange')
# Command Block Begin:
lx.eval('tool.attr util.udim manual true')
lx.eval('tool.attr util.udim posU 0')
lx.eval('tool.attr util.udim posV -1')
lx.eval('tool.attr util.udim width 1.0')
lx.eval('tool.attr util.udim height 1.0')
# Command Block End:
lx.eval('tool.doApply')
lx.eval('udim.select')
CsPolysUnwrapConform = len(mesh.geometry.polygons.selected)
lx.out('USER UV Map Name:', CsPolysUnwrapConform)
if CsPolysUnwrapConform > 0:
    lx.eval('uv.pack true true true auto 0.2 true 8.0 region:manual regionX:0 regionY:-1 regionW:1.0 regionH:1.0')
    lx.eval('tool.set util.udim off')
    lx.eval('select.drop polygon')
else:
    lx.out('No Unwrap Conform Repack:')

# Unwrap Angle Based
lx.eval('tool.set util.udim on')
lx.eval('tool.noChange')
# Command Block Begin:
lx.eval('tool.attr util.udim manual true')
lx.eval('tool.attr util.udim posU 1')
lx.eval('tool.attr util.udim posV -1')
lx.eval('tool.attr util.udim width 1.0')
lx.eval('tool.attr util.udim height 1.0')
# Command Block End:
lx.eval('tool.doApply')
lx.eval('udim.select')
CsPolysUnwrapAB = len(mesh.geometry.polygons.selected)
lx.out('USER UV Map Name:', CsPolysUnwrapAB)
if CsPolysUnwrapAB > 0:
    lx.eval('uv.pack true true true auto 0.2 true 8.0 region:manual regionX:1 regionY:-1 regionW:1.0 regionH:1.0')
    lx.eval('tool.set util.udim off')
    lx.eval('select.drop polygon')
else:
    lx.out('No Unwrap Angle Based Repack:')

# Unwrap Rectangle
lx.eval('tool.set util.udim on')
lx.eval('tool.noChange')
# Command Block Begin:
lx.eval('tool.attr util.udim manual true')
lx.eval('tool.attr util.udim posU 1')
lx.eval('tool.attr util.udim posV -1')
lx.eval('tool.attr util.udim width 1.0')
lx.eval('tool.attr util.udim height 1.0')
# Command Block End:
lx.eval('tool.doApply')
lx.eval('udim.select')
CsPolysUnwrapRec = len(mesh.geometry.polygons.selected)
lx.out('USER UV Map Name:', CsPolysUnwrapRec)
if CsPolysUnwrapRec > 0:
    lx.eval('uv.pack true true true auto 0.2 true 8.0 region:manual regionX:1 regionY:-1 regionW:1.0 regionH:1.0')
    lx.eval('tool.set util.udim off')
    lx.eval('select.drop polygon')
else:
    lx.out('No Unwrap Rectangle Repack:')

# ------------- PLANAR
# Planar X
lx.eval('tool.set util.udim on')
lx.eval('tool.noChange')
# Command Block Begin:
lx.eval('tool.attr util.udim manual true')
lx.eval('tool.attr util.udim posU -2')
lx.eval('tool.attr util.udim posV 0')
lx.eval('tool.attr util.udim width 1.0')
lx.eval('tool.attr util.udim height 1.0')
# Command Block End:
lx.eval('tool.doApply')
lx.eval('udim.select')
CsPolysPlanarX = len(mesh.geometry.polygons.selected)
lx.out('USER UV Map Name:', CsPolysPlanarX)
if CsPolysPlanarX > 0:
    lx.eval('uv.pack true true true auto 0.2 true 8.0 region:manual regionX:-2 regionY:0 regionW:1.0 regionH:1.0')
    lx.eval('tool.set util.udim off')
    lx.eval('select.drop polygon')
else:
    lx.out('No Planar X Repack:')

# Planar Y
lx.eval('tool.set util.udim on')
lx.eval('tool.noChange')
# Command Block Begin:
lx.eval('tool.attr util.udim manual true')
lx.eval('tool.attr util.udim posU -1')
lx.eval('tool.attr util.udim posV 0')
lx.eval('tool.attr util.udim width 1.0')
lx.eval('tool.attr util.udim height 1.0')
# Command Block End:
lx.eval('tool.doApply')
lx.eval('udim.select')
CsPolysPlanarY = len(mesh.geometry.polygons.selected)
lx.out('USER UV Map Name:', CsPolysPlanarY)
if CsPolysPlanarY > 0:
    lx.eval('uv.pack true true true auto 0.2 true 8.0 region:manual regionX:-1 regionY:0 regionW:1.0 regionH:1.0')
    lx.eval('tool.set util.udim off')
    lx.eval('select.drop polygon')
else:
    lx.out('No Planar Y Repack:')

# Planar Z
lx.eval('tool.set util.udim on')
lx.eval('tool.noChange')
# Command Block Begin:
lx.eval('tool.attr util.udim manual true')
lx.eval('tool.attr util.udim posU -1')
lx.eval('tool.attr util.udim posV 1')
lx.eval('tool.attr util.udim width 1.0')
lx.eval('tool.attr util.udim height 1.0')
# Command Block End:
lx.eval('tool.doApply')
lx.eval('udim.select')
CsPolysPlanarZ = len(mesh.geometry.polygons.selected)
lx.out('USER UV Map Name:', CsPolysPlanarZ)
if CsPolysPlanarZ > 0:
    lx.eval('uv.pack true true true auto 0.2 true 8.0 region:manual regionX:-1 regionY:1 regionW:1.0 regionH:1.0')
    lx.eval('tool.set util.udim off')
    lx.eval('select.drop polygon')
else:
    lx.out('No Planar Z Repack:')

# Planar Free
lx.eval('tool.set util.udim on')
lx.eval('tool.noChange')
# Command Block Begin:
lx.eval('tool.attr util.udim manual true')
lx.eval('tool.attr util.udim posU -2')
lx.eval('tool.attr util.udim posV 1')
lx.eval('tool.attr util.udim width 1.0')
lx.eval('tool.attr util.udim height 1.0')
# Command Block End:
lx.eval('tool.doApply')
lx.eval('udim.select')
CsPolysPlanarFree = len(mesh.geometry.polygons.selected)
lx.out('USER UV Map Name:', CsPolysPlanarFree)
if CsPolysPlanarFree > 0:
    lx.eval('uv.pack true true true auto 0.2 true 8.0 region:manual regionX:-2 regionY:1 regionW:1.0 regionH:1.0')
    lx.eval('tool.set util.udim off')
    lx.eval('select.drop polygon')
else:
    lx.out('No Planar Free Repack:')

# ------------- CYLINDRICAL
# Cylindrical X
lx.eval('tool.set util.udim on')
lx.eval('tool.noChange')
# Command Block Begin:
lx.eval('tool.attr util.udim manual true')
lx.eval('tool.attr util.udim posU 1')
lx.eval('tool.attr util.udim posV -1')
lx.eval('tool.attr util.udim width 1.0')
lx.eval('tool.attr util.udim height 1.0')
# Command Block End:
lx.eval('tool.doApply')
lx.eval('udim.select')
CsPolysCylindricalX = len(mesh.geometry.polygons.selected)
lx.out('USER UV Map Name:', CsPolysCylindricalX)
if CsPolysCylindricalX > 0:
    lx.eval('uv.pack true true true auto 0.2 true 8.0 region:manual regionX:-2 regionY:-2 regionW:1.0 regionH:1.0')
    lx.eval('tool.set util.udim off')
    lx.eval('select.drop polygon')
else:
    lx.out('No Cylindrical X Repack:')

# Cylindrical Y
lx.eval('tool.set util.udim on')
lx.eval('tool.noChange')
# Command Block Begin:
lx.eval('tool.attr util.udim manual true')
lx.eval('tool.attr util.udim posU -1')
lx.eval('tool.attr util.udim posV -2')
lx.eval('tool.attr util.udim width 1.0')
lx.eval('tool.attr util.udim height 1.0')
# Command Block End:
lx.eval('tool.doApply')
lx.eval('udim.select')
CsPolysCylindricalY = len(mesh.geometry.polygons.selected)
lx.out('USER UV Map Name:', CsPolysCylindricalY)
if CsPolysCylindricalY > 0:
    lx.eval('uv.pack true true true auto 0.2 true 8.0 region:manual regionX:-1 regionY:-2 regionW:1.0 regionH:1.0')
    lx.eval('tool.set util.udim off')
    lx.eval('select.drop polygon')
else:
    lx.out('No Cylindrical Y Repack:')

# Cylindrical Z
lx.eval('tool.set util.udim on')
lx.eval('tool.noChange')
# Command Block Begin:
lx.eval('tool.attr util.udim manual true')
lx.eval('tool.attr util.udim posU -1')
lx.eval('tool.attr util.udim posV -1')
lx.eval('tool.attr util.udim width 1.0')
lx.eval('tool.attr util.udim height 1.0')
# Command Block End:
lx.eval('tool.doApply')
lx.eval('udim.select')
CsPolysCylindricalZ = len(mesh.geometry.polygons.selected)
lx.out('USER UV Map Name:', CsPolysCylindricalZ)
if CsPolysCylindricalZ > 0:
    lx.eval('uv.pack true true true auto 0.2 true 8.0 region:manual regionX:-1 regionY:-1 regionW:1.0 regionH:1.0')
    lx.eval('tool.set util.udim off')
    lx.eval('select.drop polygon')
else:
    lx.out('No Cylindrical Z Repack:')

# Cylindrical Free
lx.eval('tool.set util.udim on')
lx.eval('tool.noChange')
# Command Block Begin:
lx.eval('tool.attr util.udim manual true')
lx.eval('tool.attr util.udim posU -2')
lx.eval('tool.attr util.udim posV -1')
lx.eval('tool.attr util.udim width 1.0')
lx.eval('tool.attr util.udim height 1.0')
# Command Block End:
lx.eval('tool.doApply')
lx.eval('udim.select')
CsPolysCylindricalFree = len(mesh.geometry.polygons.selected)
lx.out('USER UV Map Name:', CsPolysCylindricalFree)
if CsPolysCylindricalFree > 0:
    lx.eval('uv.pack true true true auto 0.2 true 8.0 region:manual regionX:-2 regionY:-1 regionW:1.0 regionH:1.0')
    lx.eval('tool.set util.udim off')
    lx.eval('select.drop polygon')
else:
    lx.out('No Cylindrical Free Repack:')

# replay name:"Unhide"
# lx.eval('unhide')

if SMO_SafetyCheck_VertexModeEnabled == 1:
    lx.eval('select.type vertex')

if SMO_SafetyCheck_EdgeModeEnabled == 1:
    lx.eval('select.type edge')

if SMO_SafetyCheck_ItemModeEnabled == 1:
    lx.eval('select.type item')

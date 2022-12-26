# python
"""
# Name:         SMO_UnbevelLoops.py
# Version: 1.0
#
# Purpose:      This script is designed to:
#               Unbevel the Polygon Selection, by using the MouseOver an Edge
#
#
# Author:       Franck ELISABETH
# Website:      https://www.smoluck.com
#
# Created:      05/02/2020
# Copyright:    (c) Franck Elisabeth 2017-2022
"""

import modo
import lx

scene = modo.Scene()
items = scene.selected
lx.out(items)

Modo_ver = int(lx.eval('query platformservice appversion ?'))
lx.out('Modo Version:', Modo_ver)

############### 5 ARGUMENTS ------------- #
args = lx.args()
lx.out(args)

# Conformal= 0
# Angle Based = 1
CornerMethod = int(args[0])
lx.out('Corner solver method:', CornerMethod)
# ------------- ARGUMENTS ------------- #


# # ------------- ARGUMENTS Test
# CornerMethod = 1
# # ------------- ARGUMENTS ------------- #


# ------------------------------ #
# <----( DEFINE VARIABLES )----> #
# ------------------------------ #
#####--- Define user value for all the different SafetyCheck --- START ---#####
#####
lx.eval("user.defNew name:SMO_SC_UnbevelPolyLoop_PolygonModeEnabled type:integer life:momentary")
lx.eval("user.defNew name:SMO_SC_UnbevelPolyLoop_min1PolygonSelected type:integer life:momentary")

lx.eval("user.defNew name:SMO_SC_UnbevelPolyLoop_EdgeModeEnabled type:integer life:momentary")
lx.eval("user.defNew name:SMO_SC_UnbevelPolyLoop_1EdgeSelected type:integer life:momentary")

lx.eval("user.defNew name:TotalSafetyCheckPolygon type:integer life:momentary")
lx.eval("user.defNew name:TotalSafetyCheckEdge type:integer life:momentary")
#####
#####--- Define user value for all the different SafetyCheck --- END ---#####


# -------------------------- #
# <---( SAFETY CHECK 1 )---> #
# -------------------------- #

# --------------------  safety check 1 and 2 : Only One Item Selected and Polygon Mode Enabled --- START
try:
    # test if there is actually an item layer selected
    mesh = scene.selectedByType('mesh')[0]
    # if this command return an error then i will select the corresponding mesh layer on the next step.
except:
    # -------------------------- #
    # <---( SAFETY CHECK 2 )---> #
    # -------------------------- #

    # Polygon Selection Mode enabled --- START

    selType = ""
    # Used to query layerservice for the list of polygons, edges or vertices.
    attrType = ""

    if lx.eval1("select.typeFrom typelist:vertex;polygon;edge;item;ptag ?"):
        selType = "vertex"
        attrType = "vert"

        SMO_SC_UnbevelPolyLoop_PolygonModeEnabled = 0
        SMO_SC_UnbevelPolyLoop_PolygonModeEnabled = 0
        SMO_SC_UnbevelPolyLoop_VertexModeEnabled = 1
        lx.eval('dialog.setup info')
        lx.eval('dialog.title {SMO UnbevelPolyLoops:}')
        lx.eval('dialog.msg {You must be in Polygon Mode to run that script}')
        lx.eval('+dialog.open')
        lx.out('script Stopped: You must be in Polygon Mode to run that script')
        sys.exit
        # sys.exit( "LXe_FAILED:Must be in polygon selection mode." )


    elif lx.eval1("select.typeFrom typelist:edge;vertex;polygon;item ?"):
        selType = "edge"
        attrType = "edge"

        SMO_SC_UnbevelPolyLoop_VertexModeEnabled = 0
        SMO_SC_UnbevelPolyLoop_PolygonModeEnabled = 1
        SMO_SC_UnbevelPolyLoop_PolygonModeEnabled = 0
        lx.eval('dialog.setup info')
        lx.eval('dialog.title {SMO UnbevelPolyLoops:}')
        lx.eval('dialog.msg {You must be in Polygon Mode to run that script}')
        lx.eval('+dialog.open')
        lx.out('script Stopped: You must be in Polygon Mode to run that script')
        sys.exit
        # sys.exit( "LXe_FAILED:Must be in polygon selection mode." )

    elif lx.eval1("select.typeFrom typelist:polygon;vertex;edge;item ?"):
        selType = "polygon"
        attrType = "poly"

        SMO_SC_UnbevelPolyLoop_VertexModeEnabled = 0
        SMO_SC_UnbevelPolyLoop_PolygonModeEnabled = 0
        SMO_SC_UnbevelPolyLoop_PolygonModeEnabled = 1
        lx.out('script Running: Polygon Component Selection Mode')
    else:
        # This only fails if none of the three supported selection
        # modes have yet been used since the program started, or
        # if "item" or "ptag" (ie: materials) is the current
        # selection mode.
        SMO_SC_UnbevelPolyLoop_VertexModeEnabled = 0
        SMO_SC_UnbevelPolyLoop_PolygonModeEnabled = 0
        SMO_SC_UnbevelPolyLoop_PolygonModeEnabled = 0
        lx.eval('dialog.setup info')
        lx.eval('dialog.title {SMO UnbevelPolyLoops:}')
        lx.eval('dialog.msg {You must be in Polygon Mode to run that script}')
        lx.eval('+dialog.open')
        lx.out('script Stopped: You must be in Polygon Mode to run that script')
        sys.exit
        # sys.exit( "LXe_FAILED:Must be in polygon selection mode." )
    # Polygon Selection Mode enabled --- END

    ItemLayerName = lx.eval('query layerservice layer.name ? 1')
    lx.out('Item Layer name is:', ItemLayerName)
    ItemLayerID = lx.eval('query layerservice layer.ID ?')
    lx.out('Item Layer ID is:', ItemLayerID)
    lx.eval('select.type item')
    lx.eval('select.item %s add' % ItemLayerID)
    mesh = scene.selectedByType('mesh')[0]

ItemCount = lx.eval('query layerservice layer.N ? selected')
lx.out('ItemCount', ItemCount)

if ItemCount != 1:
    SMO_SC__Only1MeshItemSelected = 0
    lx.eval('dialog.setup info')
    lx.eval('dialog.title {SMO Smart Unwrap:}')
    lx.eval('dialog.msg {You must select the Mesh Item layer you are working on, in Item List, to run that script}')
    lx.eval('+dialog.open')
    lx.out('Only One Item Selected result:', SMO_SC__Only1MeshItemSelected)
    lx.out('script Stopped: Select only one Mesh Item')
    sys.exit

elif ItemCount == 1:
    SMO_SC__Only1MeshItemSelected = 1
    lx.out('Only One Item Selected:', SMO_SC__Only1MeshItemSelected)
    lx.out('script running: right amount of Mesh Item selected')
# --------------------  safety check 1 and 2 : Only One Item Selected and Polygon Mode Enabled --- END

# -------------------------- #
# <---( SAFETY CHECK 2 )---> #
# -------------------------- #

# Polygon Selection Mode enabled --- START

selType = ""
# Used to query layerservice for the list of polygons, edges or vertices.
attrType = ""

if lx.eval1("select.typeFrom typelist:vertex;polygon;edge;item;ptag ?"):
    selType = "vertex"
    attrType = "vert"

    SMO_SC_UnbevelPolyLoop_PolygonModeEnabled = 0
    SMO_SC_UnbevelPolyLoop_PolygonModeEnabled = 0
    SMO_SC_UnbevelPolyLoop_VertexModeEnabled = 1
    lx.eval('dialog.setup info')
    lx.eval('dialog.title {SMO UnbevelPolyLoops:}')
    lx.eval('dialog.msg {You must be in Polygon Mode to run that script}')
    lx.eval('+dialog.open')
    lx.out('script Stopped: You must be in Polygon Mode to run that script')
    sys.exit
    # sys.exit( "LXe_FAILED:Must be in polygon selection mode." )


elif lx.eval1("select.typeFrom typelist:edge;vertex;polygon;item ?"):
    selType = "edge"
    attrType = "edge"

    SMO_SC_UnbevelPolyLoop_VertexModeEnabled = 0
    SMO_SC_UnbevelPolyLoop_PolygonModeEnabled = 1
    SMO_SC_UnbevelPolyLoop_PolygonModeEnabled = 0
    lx.eval('dialog.setup info')
    lx.eval('dialog.title {SMO UnbevelPolyLoops:}')
    lx.eval('dialog.msg {You must be in Polygon Mode to run that script}')
    lx.eval('+dialog.open')
    lx.out('script Stopped: You must be in Polygon Mode to run that script')
    sys.exit
    # sys.exit( "LXe_FAILED:Must be in polygon selection mode." )

elif lx.eval1("select.typeFrom typelist:polygon;vertex;edge;item ?"):
    selType = "polygon"
    attrType = "poly"

    SMO_SC_UnbevelPolyLoop_VertexModeEnabled = 0
    SMO_SC_UnbevelPolyLoop_PolygonModeEnabled = 0
    SMO_SC_UnbevelPolyLoop_PolygonModeEnabled = 1
    lx.out('script Running: Polygon Component Selection Mode')
else:
    # This only fails if none of the three supported selection
    # modes have yet been used since the program started, or
    # if "item" or "ptag" (ie: materials) is the current
    # selection mode.
    SMO_SC_UnbevelPolyLoop_VertexModeEnabled = 0
    SMO_SC_UnbevelPolyLoop_PolygonModeEnabled = 0
    SMO_SC_UnbevelPolyLoop_PolygonModeEnabled = 0
    lx.eval('dialog.setup info')
    lx.eval('dialog.title {SMO UnbevelPolyLoops:}')
    lx.eval('dialog.msg {You must be in Polygon Mode to run that script}')
    lx.eval('+dialog.open')
    lx.out('script Stopped: You must be in Polygon Mode to run that script')
    sys.exit
    # sys.exit( "LXe_FAILED:Must be in polygon selection mode." )
# Polygon Selection Mode enabled --- END


CsPolys = len(mesh.geometry.polygons.selected)

# -------------------------- #
# <---( SAFETY CHECK 3 )---> #
# -------------------------- #

# at Least 1 Polygon is selected --- START
if SMO_SC_UnbevelPolyLoop_PolygonModeEnabled == 1:
    lx.out('Count Selected Poly', CsPolys)

    if CsPolys == 0:
        SMO_SC_UnbevelPolyLoop_min1PolygonSelected = 0
        lx.eval('dialog.setup info')
        lx.eval('dialog.title {SMO UnbevelPolyLoops:}')
        lx.eval('dialog.msg {You must select at least 1 Polygon and Mouse over an Edge to run that script}')
        lx.eval('+dialog.open')
        lx.out('script Stopped: Add more Edges to your selection')
        sys.exit

    elif CsPolys >= 1:
        SMO_SC_UnbevelPolyLoop_min1PolygonSelected = 1
        lx.out('script running: right amount of Edges in selection')
# at Least 1 Polygon is selected --- END


# Select the Edge via Mouse Over function
lx.eval('select.type edge')

lx.eval('query view3dservice mouse ?')
view_under_mouse = lx.eval('query view3dservice mouse.view ?')
lx.eval('query view3dservice view.index ? %s' % view_under_mouse)
lx.eval('query view3dservice mouse.pos ?')
# poly_under_mouse = lx.eval('query view3dservice element.over ? POLY ')
edge_under_mouse = lx.eval('query view3dservice element.over ? EDGE ')
hitpos = lx.eval('query view3dservice mouse.hitpos ?')

lx.out(view_under_mouse)
# lx.out(poly_under_mouse)
lx.out(edge_under_mouse)
lx.out(hitpos)

lx.eval('select.drop edge')
# lx.eval('materials.underMouse')

success = True
try:
    lx.eval('select.3DElementUnderMouse')
except:
    success = False

# -------------------------- #
####### SAFETY CHECK 4 #######
# -------------------------- #
CsEdges = len(mesh.geometry.edges.selected)
lx.out('Count Selected Edges', CsEdges)
# --------------------  safety check 4: at Least 1 Edge is selected --- START


if CsEdges == 0:
    SMO_SC_UnbevelPolyLoop_1EdgeSelected = 0
    lx.eval('dialog.setup info')
    lx.eval('dialog.title {SMO UnbevelPolyLoops:}')
    lx.eval('dialog.msg {You must select at least 1 Polygon and Mouse over an Edge to run that script}')
    lx.eval('+dialog.open')
    lx.out('script Stopped: Mouse over an Edge to validate the script requirements')
    sys.exit

elif CsEdges >= 1:
    SMO_SC_UnbevelPolyLoop_1EdgeSelected = 1
    lx.out('script running: right amount of Edges in selection')
# --------------------  safety check 4: at Least 1 edge is selected --- END


#####--- Define current value for the Prerequisite TotalSafetyCheck --- START ---#####
#####
TotalSafetyCheckTrueValuePoly = 4
lx.out('Desired Value for Polygon Mode', TotalSafetyCheckTrueValuePoly)

TotalSafetyCheckTrueValueEdge = 7
lx.out('Desired Value for Edge Mode', TotalSafetyCheckTrueValueEdge)

TotalSafetyCheckPolygon = (
            SMO_SC__Only1MeshItemSelected + SMO_SC_UnbevelPolyLoop_PolygonModeEnabled + SMO_SC_UnbevelPolyLoop_min1PolygonSelected + SMO_SC_UnbevelPolyLoop_1EdgeSelected)
lx.out('Current Polygon Check Value', TotalSafetyCheckPolygon)
#####
#####--- Define current value for the Prerequisite TotalSafetyCheck --- END ---#####


if TotalSafetyCheckPolygon == TotalSafetyCheckTrueValuePoly:
    if success:
        if Modo_ver < 1400:
            lx.eval('select.editSet UnbevelEdgeGuide add {}')
            lx.eval('select.type polygon')
            lx.eval('select.convert edge')
            lx.eval('select.invert')
            lx.eval('select.editSet UnbevelNoEdgeRing add {}')
            lx.eval('select.type polygon')

            lx.eval('select.editSet UnbevelPolyZone add {}')
            lx.eval('select.expand')
            lx.eval('select.useSet UnbevelPolyZone deselect')
            lx.eval('select.editSet UnbevelPolyBorder add {}')
            lx.eval('select.useSet UnbevelPolyZone replace')
            lx.eval('select.useSet UnbevelPolyBorder select')
            lx.eval('select.type polygon')
            lx.eval('select.polygon remove vertex curve 4')
            lx.eval('select.editSet UnbevelPolyBorder remove')
            lx.eval('select.drop polygon')
            lx.eval('select.useSet UnbevelPolyZone replace')
            lx.eval('select.useSet UnbevelPolyBorder select')

            lx.eval('hide.unsel')
            lx.eval('select.type edge')
            lx.eval('select.drop edge')
            lx.eval('select.useSet UnbevelEdgeGuide replace')
            lx.eval('select.edgeLoop base false m3d middle')
            lx.eval('select.ring')
            lx.eval('unhide')
            lx.eval('@unbevel.pl')

            lx.eval('select.drop edge')
            lx.eval('select.type polygon')
            lx.eval('select.drop polygon')

            lx.eval('select.type edge')
            lx.eval('!select.deleteSet UnbevelEdgeRing')
            lx.eval('!select.deleteSet UnbevelEdgeGuide')
            lx.eval('!select.deleteSet UnbevelNoEdgeRing')
            lx.eval('select.type polygon')
            lx.eval('!select.deleteSet UnbevelPolyZone')
            lx.eval('!select.deleteSet UnbevelPolyBorder')

    if success:
        if Modo_ver >= 1400:
            lx.eval('select.editSet UnbevelEdgeGuide add {}')
            lx.eval('select.type polygon')
            lx.eval('select.convert edge')
            lx.eval('select.invert')
            lx.eval('select.editSet UnbevelNoEdgeRing add {}')
            lx.eval('select.type polygon')
            lx.eval('hide.unsel')
            lx.eval('select.type edge')
            lx.eval('select.drop edge')
            lx.eval('select.useSet UnbevelEdgeGuide replace')
            lx.eval('select.edgeLoop base false m3d middle')
            lx.eval('select.ring')
            lx.eval('select.editSet UnbevelEdgeRing add {}')
            lx.eval('select.drop edge')
            lx.eval('select.type polygon')
            lx.eval('unhide')
            lx.eval('select.drop polygon')
            lx.eval('select.drop edge')
            lx.eval('select.useSet UnbevelEdgeRing replace')
            lx.eval('edge.unbevel convergence')
            lx.eval('!select.deleteSet UnbevelEdgeRing')
            lx.eval('!select.deleteSet UnbevelEdgeGuide')
            lx.eval('!select.deleteSet UnbevelNoEdgeRing')
            lx.eval('select.type polygon')
            if CornerMethod == 1:
                lx.eval('script.run "macro.scriptservice:92663570022:macro"')
                CsEdges = len(mesh.geometry.edges.selected)
                if CsEdges >= 3:
                    lx.eval('poly.make auto')
                    lx.eval('select.type polygon')
                    lx.eval('poly.triple')
                    lx.eval('select.drop polygon')
                    lx.eval('select.type edge')
                    lx.eval('select.drop edge')
                    lx.eval('select.type polygon')
                if CsEdges < 2:
                    lx.eval('select.drop polygon')
                    lx.eval('select.type edge')
                    lx.eval('select.drop edge')
                    lx.eval('select.type polygon')

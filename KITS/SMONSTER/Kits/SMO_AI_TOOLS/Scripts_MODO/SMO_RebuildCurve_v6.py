# python
"""
# Name:         SMO_RebuildCurve.py
# Version:      1.0
#
# Purpose:      This script is designed to:
#               Rebuild the current selected Mesh layer (curve Data)
#               to Polygon Islands with differnet options like an Unmerge and Recenter.
#
# Author:       Franck ELISABETH
# Website:      https://www.smoluck.com
#
# Created:      19/12/2019
# Copyright:    (c) Franck Elisabeth 2017-2022
"""

import lx
import modo

scene = modo.scene.current()

# # ------------- ARGUMENTS Test ------------- #
# CurveRefineAngle = 10
# UnmergeAllIslands = 1
# Recenter = 1
# Cleanup = 1
# NoUndo = 1
# # ------------- ARGUMENTS ------------- #


# ------------- 5 ARGUMENTS ------------- #
args = lx.args()
lx.out(args)

# Curve Refinement Angle for the Curve Freeze passe from 0 to 90 degree
CurveRefineAngle = int(args[0])
lx.out('Curve Refinement Angle for Freezing:', CurveRefineAngle)

# 1 = Unmerge all Polygons Islands in resulting Meshes
# 0 = Do Nothing
UnmergeAllIslands = bool(args[1])
lx.out('Unmerge All Polygon Islands:', UnmergeAllIslands)

# 1 = Reposition the Center to Polygon BBox
# 0 = Do Nothing
Recenter = bool(args[2])
lx.out('Reposition Center to all Poly Island BBox:', Recenter)

# 1 = Reposition the Center to Polygon BBox
# 0 = Do Nothing
Cleanup = bool(args[3])
lx.out('Cleanup Resulting Meshes:', Cleanup)

NoUndo = bool(args[4])
lx.out('Suspend Undo (more stable computation):', NoUndo)
# ------------- ARGUMENTS ------------- #


if NoUndo == 1:
    lx.eval('!!app.undoSuspend')

# -------------------------------------------#
# Delete Unnecesary items Lights and Camera #
# -------------------------------------------#
lx.out('-------------------------------')
lx.out('Start of SMO_RebuildCurve Script')

lx.eval('select.drop item')
# Select all Lights in scene and Delete them
lx.eval('select.itemType light super:true')
lx.eval('!item.delete')

# Select all Camera in scene and Delete them
lx.eval('select.itemType camera')
lx.eval('!item.delete')

# -----------------------------------------------#
# Delete Empty Mesh Layers (default Mesh Layer) #
# -----------------------------------------------#
# # Variables
DefaultMeshItemList = []
numOfVerts = ''

# # First we must select the scene and then all the mesh layers in our scene.
lx.eval('select.drop item')
lx.eval('select.layerTree all:1')
DefaultMeshItemList = lx.eval('query sceneservice selection ? mesh')  # mesh item layers

# Create the monitor item
m = lx.Monitor()
m.init(len(DefaultMeshItemList))

# For each mesh item layer, we check to see if there are any verts in the layer...
for meshItem in DefaultMeshItemList:
    lx.eval('select.drop item')
    lx.eval('select.item %s' % meshItem)
    lx.eval('query layerservice layer.index ? selected')  # scene
    numOfPoly = lx.eval('query layerservice poly.N ? all')

    # If there are no verts, we delete the mesh item layer.
    if numOfPoly == 0: lx.eval('!item.delete')

    # Increare progress monitor
    m.step(1)
###############################################


# -----------------------------------------------------------------#
# Unparent in Place All Mesh Layers and delete the Group Locators #
# -----------------------------------------------------------------#
# Drop layer selection
lx.eval('select.drop item')
lx.eval('select.itemType groupLocator')

grploc_list = scene.selectedByType(lx.symbol.sITYPE_GROUPLOCATOR)
for a in grploc_list:
    a.select(True)
    GrpLoc_Name = lx.eval('item.name ? xfrmcore')
    CurveName = GrpLoc_Name + '_' + 'Curve'
    # lx.out('Group Locator Name:', GrpLoc_Name)
    lx.eval('select.createSet GrpLoc_temp')
    try:
        lx.eval('pickWalk down')
    except:
        lx.out('No Children Item in', GrpLoc_Name)
    ChildCount = len(lx.evalN('query sceneservice selection ? mesh'))
    lx.out('Children Count:', ChildCount)
    if ChildCount >= 1:
        lx.eval('item.name {%s} xfrmcore' % CurveName)
        lx.eval('item.parent parent:{} inPlace:1')
    lx.eval('select.drop item')
    lx.eval('select.useSet GrpLoc_temp select')
    lx.eval('!item.delete')
lx.eval('select.drop item')
#################################################################


# -----------------------------------------------#
#		Delete Empty Mesh Layers	NO Vertex	#
# (Curve Mesh that have been cleanup)			#
# -----------------------------------------------#
# Variables
CleanupCurveList = []
numOfVerts = ''

# First we must select the scene and then all the mesh layers in our scene.
lx.eval('select.drop item')
lx.eval('select.layerTree all:1')
CleanupCurveList = lx.eval('query sceneservice selection ? mesh')  # mesh item layers

# Create the monitor item
m = lx.Monitor()
m.init(len(CleanupCurveList))

# For each mesh item layer, we check to see if there are any verts in the layer...
for meshItem in CleanupCurveList:
    lx.eval('select.drop item')
    lx.eval('select.item %s' % meshItem)
    lx.eval('query layerservice layer.index ? selected')  # scene
    numOfVerts = lx.eval('query layerservice vert.N ? all')

    # If there are no verts, we delete the mesh item layer.
    if numOfVerts == 0: lx.eval('!item.delete')
    # Increare progress monitor
    m.step(1)
# ------------------------------------- #


# ----------------------------------#
# Create a Z positive Face Polygon #
# ----------------------------------#
lx.eval('item.create mesh')
lx.eval('item.name PlaneZ xfrmcore')
lx.eval('select.type polygon')
lx.eval('script.run "macro.scriptservice:32235710027:macro"')
# Get the selected layer.
CubeNormalSelect = lx.eval('query layerservice layers ? selected')
# Select the first vertex.
lx.eval('select.element layer:%d type:polygon mode:add index:1' % CubeNormalSelect)
lx.eval('select.invert')
lx.eval('!delete')
lx.eval('select.invert')
lx.eval('select.createSet Polyflip')
lx.eval('copy')
lx.eval('select.type item')
lx.eval('select.createSet PlaneZ')
lx.eval('select.drop item')
####################################


###################################################################################
# import modo
# scene = modo.Scene()
# mesh_list = scene.selectedByType(lx.symbol.sTYPE_MESH)
# for mesh in mesh_list:
# mesh.select(True)
# lx.eval("select.all")
# lx.eval("poly.flip")
###################################################################################

###################################################################################
# Rename Children of Group Locators by the group Loactors name + Suffix tag (Curve)
# import modo
# scene = modo.Scene()

# # Drop layer selection
# lx.eval('select.drop item')
# lx.eval('select.itemType groupLocator')

# grploc_list = scene.selectedByType(lx.symbol.sITYPE_GROUPLOCATOR)
# for a in grploc_list:
# a.select(True)
# GrpLoc_Name = lx.eval('item.name ? xfrmcore')
# lx.out('Group Locator Name:', GrpLoc_Name)
# lx.eval('pickWalk down')
# CurveName = GrpLoc_Name + '_' + 'Curve'
# lx.eval('item.name {%s} xfrmcore' % CurveName)
# lx.eval('select.drop item groupLocator')
###################################################################################


# ------------------------------------------------------#
# Select only curves Mesh and run the main Script part #
# ------------------------------------------------------#
lx.eval('select.itemType mesh')
lx.eval('select.useSet PlaneZ deselect')

meshes_list = scene.selectedByType(lx.symbol.sITYPE_MESH)

# Modollama Triangulation
# lx.eval('user.value llama_keepuvbounds false')
# lx.eval('user.value llama_keepmatbounds false')


for mesh in meshes_list:
    mesh.select(True)
    # Freeze the curve to Polygons
    lx.eval('poly.freeze face false 2 true true true false %i false Morph' % CurveRefineAngle)

    # #################################################
    # # Delete Colinear Vertex
    # lx.eval('select.type vertex')
    # lx.eval('select.vertex add 4 0 (none)')

    # CsVertex = len(mesh.geometry.vertex.selected)
    # lx.out('Count Selected Poly',CsVertex)

    # if CsVertex < 1:
    # lx.out('No Colinear Vertex')
    # elif CsVertex >= 1:
    # SMO_SafetyCheck_min1PolygonSelected = 1
    # lx.out('Colinear Vertex detected')
    # lx.eval('!delete')
    # #################################################

    lx.eval('select.type item')

    lx.eval('!!mesh.cleanup true true true true true true false true true true true')
    lx.eval('select.type polygon')
    lx.eval('paste')
    lx.eval('select.drop polygon')
    lx.eval('select.all')
    lx.eval('select.polygon remove vertex curve 3')
    lx.eval('select.useSet Polyflip deselect')

    polygons = lx.eval('query layerservice poly.N ? selected')
    if polygons >= 1:
        lx.eval('poly.triple')

    # Modollama Triangulation
    # lx.eval('@SmartTriangulation.pl')

    lx.eval('select.drop polygon')
    lx.eval('select.useSet Polyflip select')

    # lx.eval('select.pickWorkingSet Polyflip true')
    # lx.eval('@lazySelect.pl selectAll')
    lx.eval('smo.GC.SelectCoPlanarPoly 2 2 1000')
    lx.eval('poly.flip')
    lx.eval('select.drop polygon')
    lx.eval('select.useSet Polyflip select')
    # lx.eval('select.pickWorkingSet Polyflip true')
    lx.eval('!delete')

    polygons = 0
    lx.eval('select.type item')
# lx.eval('%s' % item.id)

lx.eval('select.drop item locator')

# -------------------------#
# Delete The Z Plane mesh #
# -------------------------#
lx.eval('select.type item')
lx.eval('select.useSet PlaneZ select')
lx.eval('!delete')

# -----------------------------------#
# Unmerge the resulting Mesh Layers #
# -----------------------------------#
if UnmergeAllIslands == 1:
    lx.eval('select.itemType mesh')
    UnmergeMesh_list = scene.selectedByType(lx.symbol.sITYPE_MESH)
    for mesh in UnmergeMesh_list:
        mesh.select(True)
        lx.eval('!layer.unmergeMeshes')
        lx.eval('select.drop item')

# -------------------------------------------------------------------------#
# Reposition the Center to those MeshLayers using their Vertex as a guide #
# -------------------------------------------------------------------------#
if Recenter == 1:
    lx.eval('select.itemType mesh')
    RecenterMesh_list = scene.selectedByType(lx.symbol.sITYPE_MESH)
    for mesh in RecenterMesh_list:
        mesh.select(True)

        lx.eval('select.type vertex')
        lx.eval('select.all')
        lx.eval('workPlane.fitSelect')
        lx.eval('select.drop vertex')
        lx.eval('select.type item')
        lx.eval('select.convert type:center')
        lx.eval('matchWorkplanePos')
        lx.eval('workPlane.reset')
        lx.eval('select.type item')

# -------------------------#
# Cleanup All Mesh Layers #
# -------------------------#
if Cleanup == 1:
    lx.eval('select.itemType mesh')
    CleanupMesh_list = scene.selectedByType(lx.symbol.sITYPE_MESH)
    for mesh in CleanupMesh_list:
        mesh.select(True)
        lx.eval('!!mesh.cleanup true true true true true true true true true true true')

lx.eval('select.drop item')
lx.eval('select.itemType mesh')
lx.eval('viewport.fitSelected')
lx.eval('select.drop item')

lx.out('End of SMO_RebuildCurve Script')
lx.out('-------------------------------')

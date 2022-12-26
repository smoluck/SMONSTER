# python
"""
# Name:         SMO_MOD_MeshCleanUp.py
# Version: 1.0
#
# Purpose: This script is designed to
# Update the UVseam Cut Map based on the current UVMap
#
# Author:       Franck ELISABETH
# Website:      https://www.smoluck.com
#
# Created:      28/06/2019
# Copyright:    (c) Franck Elisabeth 2017-2022
"""

import modo
scene = modo.scene.current()
mesh = scene.selectedByType('mesh')[0]

# ------------- ARGUMENTS ------------- #
args = lx.args()
lx.out(args)

# Triangulate new Polygons Off = 0
# Triangulate new Polygons On = 1
Dist = (args[0])
lx.out('Vertex Merge distance:',Dist)
# ------------- ARGUMENTS ------------- #


# # ------------- ARGUMENTS Test
# Dist = 0.1  # 10 cm
# Dist = 0.01  # 1 cm
# Dist = 0.001 # 1 mm
# Dist = 0.0001  # 100 um
# Dist = 0.00001  # 10 um
# Dist = 0.000001  # 1 um
# # ------------- ARGUMENTS ------------- #

# ------------------------------ #
# <----( DEFINE VARIABLES )----> #
# ------------------------------ #

#####--- Define user value for all the different SafetyCheck --- START ---#####
#####

## Vertex
lx.eval("user.defNew name:SMO_SafetyCheck_VertexModeEnabled type:integer life:momentary")

## Edges
lx.eval("user.defNew name:SMO_SafetyCheck_EdgeModeEnabled type:integer life:momentary")

## Polygon
lx.eval("user.defNew name:SMO_SafetyCheck_PolygonModeEnabled type:integer life:momentary")

## Item
lx.eval("user.defNew name:SMO_SafetyCheck_ItemModeEnabled type:integer life:momentary")

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
	
	SMO_SafetyCheck_VertexModeEnabled = 1
	SMO_SafetyCheck_EdgeModeEnabled = 0
	SMO_SafetyCheck_PolygonModeEnabled = 0
	SMO_SafetyCheck_ItemModeEnabled = 0
	
	lx.out('script Running: Vertex Component Selection Mode')

	
elif lx.eval1( "select.typeFrom typelist:edge;vertex;polygon;item ?" ):
	selType = "edge"
	attrType = "edge"

	SMO_SafetyCheck_VertexModeEnabled = 0
	SMO_SafetyCheck_EdgeModeEnabled = 1
	SMO_SafetyCheck_PolygonModeEnabled = 0
	SMO_SafetyCheck_ItemModeEnabled = 0

	lx.out('script Running: Edge Component Selection Mode')
	
elif lx.eval1( "select.typeFrom typelist:polygon;vertex;edge;item ?" ):
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


# -------------------------- #
# <----( Main Macro )----> #
# -------------------------- #
lx.out('Start of SMO_MOD_MeshCleanUp Script')

#####--------------------  Compare SafetyCheck value and decide or not to continue the process  --- START
if SMO_SafetyCheck_VertexModeEnabled == 1:
	lx.eval('select.drop vertex')

if SMO_SafetyCheck_EdgeModeEnabled == 1:
	lx.eval('select.type vertex')
	lx.eval('select.drop vertex')

if SMO_SafetyCheck_PolygonModeEnabled == 1:
	lx.eval('select.type vertex')
	lx.eval('select.drop vertex')

if SMO_SafetyCheck_ItemModeEnabled == 1:
	lx.eval('select.type vertex')
	lx.eval('select.drop vertex')

lx.eval('!vert.merge range:fixed keep:false dist:{%s} morph:false disco:false' % Dist)
lx.eval('select.type item')
lx.eval('!!mesh.cleanup floatingVertex:true onePointPolygon:true twoPointPolygon:true dupPointPolygon:true colinear:true faceNormal:true mergeVertex:false mergeDisco:true unifyPolygon:true forceUnify:true removeDiscoWeight:true')
lx.eval('select.type polygon')
lx.eval('!poly.align')

if SMO_SafetyCheck_VertexModeEnabled == 1:
	lx.eval('select.type vertex')

if SMO_SafetyCheck_EdgeModeEnabled == 1:
	lx.eval('select.type edge')

if SMO_SafetyCheck_PolygonModeEnabled == 1:
	lx.eval('select.type polygon')

if SMO_SafetyCheck_ItemModeEnabled == 1:
	lx.eval('select.type item')

lx.out('End of SMO_MOD_MeshCleanUp Script')
# python
"""
Name:           SMO_UV_Update_UVSeamCutMap.py

Purpose:		This script is designed to:
                Update the UVSeam Cut Map based on the current UVMap

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
CsPolys = len(mesh.geometry.polygons.selected)
CsEdges = len(mesh.geometry.edges.selected)
CsVertex = len(mesh.geometry.vertices.selected)


# ------------------------------ #
# <----( DEFINE VARIABLES )----> #
# ------------------------------ #

# ---------------- Define user value for all the different SafetyCheck --- START
#####

# Vertex
lx.eval("user.defNew name:SMO_SafetyCheck_VertexModeEnabled type:integer life:momentary")

lx.eval("user.defNew name:SMO_SafetyCheck_minVertexSelected type:integer life:momentary")

# Edges
lx.eval("user.defNew name:SMO_SafetyCheck_EdgeModeEnabled type:integer life:momentary")

lx.eval("user.defNew name:SMO_SafetyCheck_minEdgeSelected type:integer life:momentary")

# Polygon
lx.eval("user.defNew name:SMO_SafetyCheck_PolygonModeEnabled type:integer life:momentary")

lx.eval("user.defNew name:SMO_SafetyCheck_minPolygonSelected type:integer life:momentary")

# Item
lx.eval("user.defNew name:SMO_SafetyCheck_ItemModeEnabled type:integer life:momentary")

#####
# ---------------- Define user value for all the different SafetyCheck --- END


# ------------- UV SEAM Map Detection
# MODO version checks.
# Modo 13.0 and up have UV Seam map.
# Version below 13.0 haven't
Modo_ver = int(lx.eval ('query platformservice appversion ?'))
lx.out('Modo Version:',Modo_ver)

#Define the UV Seam vmap name Search case.
lx.eval("user.defNew name:DesiredUVSEAMmapName type:string life:momentary")
DesiredUVSEAMmapName = 'UV Seam'

#Define the UV Seam vmap name Search case.
lx.eval("user.defNew name:NoUVSeamMap type:string life:momentary")
NoUVSeamMap = '_____n_o_n_e_____'


# Get the number of UV Seam map available on mesh
DetectedUVSEAMmapCount = len(lx.evalN('vertMap.list seam ?'))
lx.out('UV SEAM Map Count:', DetectedUVSEAMmapCount)

# Get the name of UV Seam map available on mesh
DetectedUVSEAMmapName = lx.eval('vertMap.list seam ?')
lx.out('UV SEAM Map Name:', DetectedUVSEAMmapName)
# ------------- UV SEAM Map Detection


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


if Modo_ver >= 1300:
    # UVSEAM Map Selection Check ##
    lx.out('<--- UVSEAM Map Safety Check --->')
    lx.out('<---------- START ---------->')
    if DetectedUVSEAMmapName == NoUVSeamMap:
        # lx.eval('vertMap.list seam ?')
        # lx.eval('vertMap.list seam _____n_e_w_____')
        lx.eval('vertMap.new "UV Seam" seam true {0.78 0.78 0.78} 2.0')
        lx.eval('vertMap.list seam "UV Seam"')
    
    elif DetectedUVSEAMmapName == DesiredUVSEAMmapName:
        lx.out('UV Map and UVSEAM Map Selected')
        lx.eval('vertMap.list seam "UV Seam"')
    # UserUVSEAMmapName = lx.eval1('query layerservice vmap.name ? %s' %UVSEAM_Selected)
    # lx.out('USER UVSEAM Map Name:', UserUVSEAMmapName)
    
    lx.out('<----------- END ----------->')
# ------------------------------ #

# -------------------------- #
# <----( Main Macro )----> #
# -------------------------- #

# ------------- Compare SafetyCheck value and decide or not to continue the process  --- START
if SMO_SafetyCheck_VertexModeEnabled == 1:
    lx.eval('select.type polygon')
    lx.eval('uv.selectBorder')
    lx.eval('seam.add')
    lx.eval('uv.selectBorder')
    lx.eval('select.invert')
    lx.eval('seam.clear')
    lx.eval('select.type vertex')

if SMO_SafetyCheck_EdgeModeEnabled == 1:
    lx.eval('select.type polygon')
    lx.eval('uv.selectBorder')
    lx.eval('seam.add')
    lx.eval('uv.selectBorder')
    lx.eval('select.invert')
    lx.eval('seam.clear')
    lx.eval('select.type edge')

if SMO_SafetyCheck_PolygonModeEnabled == 1:
    lx.eval('uv.selectBorder')
    lx.eval('seam.add')
    lx.eval('uv.selectBorder')
    lx.eval('select.invert')
    lx.eval('seam.clear')
    lx.eval('select.type polygon')

if SMO_SafetyCheck_ItemModeEnabled == 1:
    lx.eval('select.type polygon')
    lx.eval('uv.selectBorder')
    lx.eval('seam.add')
    lx.eval('uv.selectBorder')
    lx.eval('select.invert')
    lx.eval('seam.clear')
    lx.eval('select.type item')

lx.out('End of Update UVSeam Cut Map Script')
#####--------------------  Compare SafetyCheck value and decide or not to continue the process  --- END
# python
"""
# Name: Normalize_Pack.py
# Version: 1.0
#
# Purpose: This script is designed to
# Normalize all the UV Islands and Pack
# them in 0-1 UVSpace.
#
# Author:       Franck ELISABETH
# Website:      https://www.smoluck.com
#
# Created:      28/12/2018
# Copyright:    (c) Franck Elisabeth 2017-2022
"""

import modo
import lx

scene = modo.scene.current()
mesh = scene.selectedByType('mesh')[0]
#lx.out('selitems',selitems)

# ------------- ARGUMENTS ------------- #
args = lx.args()
lx.out(args)
# no Flipped = 0
# Flipped U = 1
# Flipped U = 2
FixFlippedUV = int(args[0])
lx.out('Fix Flipped error UV Island:',FixFlippedUV)
# Orient preprocess OFF = 0
# Orient preprocess ON = 1
Orient_Pass = int(args[1])
lx.out('Orient preprocess state:',Orient_Pass)
# ------------- ARGUMENTS ------------- #

# ------------------------------ #
# <----( DEFINE VARIABLES )----> #
# ------------------------------ #

#####--- Define user value for all the different SafetyCheck --- START ---#####
#####

## Vertex
lx.eval("user.defNew name:SMO_SafetyCheckNP_VertexModeEnabled type:integer life:momentary")

## Edges
lx.eval("user.defNew name:SMO_SafetyCheckNP_EdgeModeEnabled type:integer life:momentary")

## Polygon
lx.eval("user.defNew name:SMO_SafetyCheckNP_PolygonModeEnabled type:integer life:momentary")
## Polygon Count
lx.eval("user.defNew name:SMO_SafetyCheckNP_minPolygonSelected type:integer life:momentary")

## Item
lx.eval("user.defNew name:SMO_SafetyCheckNP_ItemModeEnabled type:integer life:momentary")

#####
#####--- Define user value for all the different SafetyCheck --- END ---#####


# ----------------------------------------- #
# <---( SAFETY CHECK 1 )---> UVMap Selected #
# ----------------------------------------- #

##########################
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


UserUVMapName = lx.eval1('query layerservice vmap.name ? %s' %UVmap_Selected)
lx.out('USER UV Map Name:', UserUVMapName)	
    
lx.out('<- UV Map Safety Check ->')
lx.out('<------------- END -------------->')
##########################




################################################
####### SAFETY CHECK 2 -  Selection Mode #######
################################################

# Component Selection Mode type --- START

selType = ""
# Used to query layerservice for the list of polygons, edges or vertices.
attrType = ""

if lx.eval1( "select.typeFrom typelist:vertex;polygon;edge;item;ptag ?" ):
    selType = "vertex"
    attrType = "vert"
    
    SMO_SafetyCheckNP_VertexModeEnabled = 1
    SMO_SafetyCheckNP_EdgeModeEnabled = 0
    SMO_SafetyCheckNP_PolygonModeEnabled = 0
    SMO_SafetyCheckNP_ItemModeEnabled = 0
    
    lx.out('script Running: Vertex Component Selection Mode')
    
    
elif lx.eval1( "select.typeFrom typelist:edge;vertex;polygon;item ?" ):
    selType = "edge"
    attrType = "edge"
    
    SMO_SafetyCheckNP_VertexModeEnabled = 0
    SMO_SafetyCheckNP_EdgeModeEnabled = 1
    SMO_SafetyCheckNP_PolygonModeEnabled = 0
    SMO_SafetyCheckNP_ItemModeEnabled = 0
    
    lx.out('script Running: Edge Component Selection Mode')
    
elif lx.eval1( "select.typeFrom typelist:polygon;vertex;edge;item ?" ):
    selType = "polygon"
    attrType = "poly"
    
    SMO_SafetyCheckNP_VertexModeEnabled = 0
    SMO_SafetyCheckNP_EdgeModeEnabled = 0
    SMO_SafetyCheckNP_PolygonModeEnabled = 1
    SMO_SafetyCheckNP_ItemModeEnabled = 0
    
    lx.out('script Running: Polygon Component Selection Mode')


else:
    # This only fails if none of the three supported selection
    # modes have yet been used since the program started, or
    # if "item" or "ptag" (ie: materials) is the current
    # selection mode.
    
    SMO_SafetyCheckNP_VertexModeEnabled = 0
    SMO_SafetyCheckNP_EdgeModeEnabled = 0
    SMO_SafetyCheckNP_PolygonModeEnabled = 0
    SMO_SafetyCheckNP_ItemModeEnabled = 1
    
    lx.out('script Running: Item Component Selection Mode')

# Component Selection Mode type --- END


##########################################
# <----( Main Macro : FixFlipped pass )----> #
##########################################

if SMO_SafetyCheckNP_VertexModeEnabled == 1:
    lx.eval('select.type polygon')
    
if SMO_SafetyCheckNP_EdgeModeEnabled == 1:
    lx.eval('select.type polygon')
    
if SMO_SafetyCheckNP_ItemModeEnabled == 1:
    lx.eval('select.type polygon')
    
if SMO_SafetyCheckNP_PolygonModeEnabled == 1:
    lx.eval('select.type polygon')

CsPolysNP = len(mesh.geometry.polygons.selected)
lx.out('Count Selected Poly',CsPolysNP)
if CsPolysNP >= 1:
    lx.eval('select.editSet name:UV_NormPacked mode:add')
    lx.eval('hide.unsel')
    lx.eval('select.drop polygon')
    if FixFlippedUV == 1 and SMO_SafetyCheckNP_PolygonModeEnabled == 1 :
        lx.eval('@kit_SMO_UV:MacroSmoluck/UV/SMO_UV_FixFlipped.py 0')
        lx.out('Fix Flipped error UV Island: YES')
        lx.eval('select.drop polygon')
        
    if FixFlippedUV == 0 and SMO_SafetyCheckNP_PolygonModeEnabled == 1 :
        lx.out('Fix Flipped error UV Island: NO')
           
    lx.eval('unhide')
    lx.eval('select.useSet UV_NormPacked select')
    lx.eval('!select.deleteSet UV_NormPacked false')

if CsPolysNP == 0 or SMO_SafetyCheckNP_ItemModeEnabled == 1 or SMO_SafetyCheckNP_EdgeModeEnabled == 1 or SMO_SafetyCheckNP_VertexModeEnabled == 1 :
    if FixFlippedUV == 1 :
        lx.eval('@kit_SMO_UV:MacroSmoluck/UV/SMO_UV_FixFlipped.py 0')
        lx.out('Fix Flipped error UV Island: YES')
        lx.eval('select.drop polygon')
    if FixFlippedUV == 0 :
        lx.out('Fix Flipped error UV Island: NO')

# -------------------------- #
# <---( SAFETY CHECK 3 )---> #
# -------------------------- #

# at Least 1 Polygons is selected --- START


if CsPolysNP < 1:
    SMO_SafetyCheckNP_min1PolygonSelected = 0
    lx.out('Normalize and Pack applied on All Polygons in Layer')

elif CsPolysNP >= 1:
    SMO_SafetyCheckNP_min1PolygonSelected = 1
    lx.out('Normalize and Pack applied on Poly Selection Only')
# at Least 1 Polygons is selected --- END



##########################################
# <----( Main Macro : Normalize )----> #
##########################################

if SMO_SafetyCheckNP_min1PolygonSelected >= 1 :
    lx.out('Normalize and Pack applied on Poly Selection Only')
    
if SMO_SafetyCheckNP_min1PolygonSelected < 1 :
    lx.out('Normalize and Pack applied on All Polygons in Layer')
    lx.eval('select.drop polygon')

# replay name:"Hide Unselected"
lx.eval('hide.unsel')
# replay name:"Normalize Texel Density"
lx.eval('texeldensity.normalize')

if Orient_Pass == 0:
    # replay name:"Pack UVs"
    lx.eval('uv.pack true false false gaps:0.2 byPixel:true gapsByPixel:8.0 region:normalized udim:1001 regionX:0.0 regionY:0.0 regionW:1.0 regionH:1.0')


if Orient_Pass == 1:
    # replay name:"Pack UVs"
    lx.eval('uv.pack true false {%i} gaps:0.2 byPixel:true gapsByPixel:8.0 region:normalized udim:1001 regionX:0.0 regionY:0.0 regionW:1.0 regionH:1.0' % Orient_Pass)


if Orient_Pass == 2:
    lx.eval('uv.orient auto')
    # replay name:"Pack UVs"
    lx.eval('uv.pack true false true gaps:0.2 byPixel:true gapsByPixel:8.0 region:normalized udim:1001 regionX:0.0 regionY:0.0 regionW:1.0 regionH:1.0')


# replay name:"Unhide"
lx.eval('unhide')

if SMO_SafetyCheckNP_VertexModeEnabled == 1:
    lx.eval('select.type vertex')

if SMO_SafetyCheckNP_EdgeModeEnabled == 1:
    lx.eval('select.type edge')

if SMO_SafetyCheckNP_ItemModeEnabled == 1:
    lx.eval('select.type item')
# python
"""
Name:         		SMO_QT_Setup.py

Purpose:            This Script is designed to:
					Apply a Selection Set to the current selection of polygons
					OR
					Creating the related Command Region to this Tag

Author:       		Franck ELISABETH
Website:      		https://www.smoluck.com
Created:      		10/01/2020
Copyright:    		(c) Franck Elisabeth 2017-2022
"""

import lx
import modo
import sys

scene = modo.Scene()
selectedItems = scene.selected

# ------------- ARGUMENTS Test
# QT_Op = 2 --------------> Create the SelSet and Command Region
# QT_ID = 8 --------------> (green)
# ------------- ARGUMENTS ------------- #

# ------------- ARGUMENTS ------------- #
# Argument: Create the Tag or select it
args = lx.args()
lx.out(args)
# 0 = Add to current Polyons to selection set Tag
# 1 = Add Command Region Link
# 2 = Create Selection Set and Add Command Region
# 3 = Remove Polygons from the current Tag they have.
# 4 = Delete Specific QTag based on QT_ID
# 5 = Delete All QTag
QT_Op = int(args[0])
lx.out('Quick Tag Operation:', QT_Op)

# QT_ID_Red = 2
# QT_ID_Magenta = 3
# QT_ID_Pink =  4
# QT_ID_Brown =  5
# QT_ID_Orange =  6
# QT_ID_Yellow =  7
# QT_ID_Green =  8
# QT_ID_LightGreen =  9
# QT_ID_Cyan =  10
# QT_ID_Blue =  11
# QT_ID_LightBlue =  12
# QT_ID_Ultramarine =  13
# QT_ID_Purple =  14
# QT_ID_LightPurple =  15
# QT_ID_DarkGrey =  16
# QT_ID_Grey =  17
# QT_ID_White =  18
QT_ID = int(args[1])
lx.out('Quick Tag set:', QT_ID)

# 0 = use only selected Polys
# 1 = expand selection to connected Polys
QT_Connected = int(args[2])
lx.out('Quick Tag to Connected:', QT_Connected)
# ------------- ARGUMENTS ------------- #


QTColorRed = 2
QTColorMagenta = 3
QTColorPink = 4
QTColorBrown = 5
QTColorOrange = 6
QTColorYellow = 7
QTColorGreen = 8
QTColorLightGreen = 9
QTColorCyan = 10
QTColorBlue = 11
QTColorLightBlue = 12
QTColorUltramarine = 13
QTColorPurple = 14
QTColorLightPurple = 15
QTColorDarkGrey = 16
QTColorGrey = 17
QTColorWhite = 18

# ------------------------------ #
# <----( DEFINE VARIABLES )----> #
# ------------------------------ #

# ---------------- Define user value for all the different SafetyCheck --- START
# Only one Item Selected
lx.eval("user.defNew name:SMO_SC_Only1MeshItemSelected type:integer life:momentary")

# Vertex
lx.eval("user.defNew name:SMO_SC_VertexModeEnabled type:integer life:momentary")
# Edges
lx.eval("user.defNew name:SMO_SC_EdgeModeEnabled type:integer life:momentary")
# Polygon
lx.eval("user.defNew name:SMO_SC_PolygonModeEnabled type:integer life:momentary")
# Item
lx.eval("user.defNew name:SMO_SC_ItemModeEnabled type:integer life:momentary")

# Min Polygon count selected
lx.eval("user.defNew name:SMO_SC_min1PolygonSelected type:integer life:momentary")

# PolySelSet Prefix name that will be ping
lx.eval("user.defNew name:PolySelSetPrefixNameRed type:string life:momentary")
PolySelSetPrefixNameRed = 'SMO_QT_Red'
lx.eval("user.defNew name:PolySelSetPrefixNameMagenta type:string life:momentary")
PolySelSetPrefixNameMagenta = 'SMO_QT_Magenta'
lx.eval("user.defNew name:PolySelSetPrefixNamePink type:string life:momentary")
PolySelSetPrefixNamePink = 'SMO_QT_Pink'
lx.eval("user.defNew name:PolySelSetPrefixNameBrown type:string life:momentary")
PolySelSetPrefixNameBrown = 'SMO_QT_Brown'
lx.eval("user.defNew name:PolySelSetPrefixNameOrange type:string life:momentary")
PolySelSetPrefixNameOrange = 'SMO_QT_Orange'
lx.eval("user.defNew name:PolySelSetPrefixNameYellow type:string life:momentary")
PolySelSetPrefixNameYellow = 'SMO_QT_Yellow'
lx.eval("user.defNew name:PolySelSetPrefixNameGreen type:string life:momentary")
PolySelSetPrefixNameGreen = 'SMO_QT_Green'
lx.eval("user.defNew name:PolySelSetPrefixNameLightGreen type:string life:momentary")
PolySelSetPrefixNameLightGreen = 'SMO_QT_LightGreen'
lx.eval("user.defNew name:PolySelSetPrefixNameCyan type:string life:momentary")
PolySelSetPrefixNameCyan = 'SMO_QT_Cyan'
lx.eval("user.defNew name:PolySelSetPrefixNameBlue type:string life:momentary")
PolySelSetPrefixNameBlue = 'SMO_QT_Blue'
lx.eval("user.defNew name:PolySelSetPrefixNameLightBlue type:string life:momentary")
PolySelSetPrefixNameLightBlue = 'SMO_QT_LightBlue'
lx.eval("user.defNew name:PolySelSetPrefixNameUltramarine type:string life:momentary")
PolySelSetPrefixNameUltramarine = 'SMO_QT_Ultramarine'
lx.eval("user.defNew name:PolySelSetPrefixNamePurple type:string life:momentary")
PolySelSetPrefixNamePurple = 'SMO_QT_Purple'
lx.eval("user.defNew name:PolySelSetPrefixNameLightPurple type:string life:momentary")
PolySelSetPrefixNameLightPurple = 'SMO_QT_LightPurple'
lx.eval("user.defNew name:PolySelSetPrefixNameDarkGrey type:string life:momentary")
PolySelSetPrefixNameDarkGrey = 'SMO_QT_DarkGrey'
lx.eval("user.defNew name:PolySelSetPrefixNameGrey type:string life:momentary")
PolySelSetPrefixNameGrey = 'SMO_QT_Grey'
lx.eval("user.defNew name:PolySelSetPrefixNameWhite type:string life:momentary")
PolySelSetPrefixNameWhite = 'SMO_QT_White'
# ---------------- Define user value for all the different SafetyCheck --- END


# -------------------------- #
# <---( SAFETY CHECK 1 )---> #
# -------------------------- #

# --------------------  safety check 1 : Only One Item Selected --- START
ItemCount = lx.eval('query layerservice layer.N ? selected')
lx.out('ItemCount', ItemCount)

if ItemCount != 1:
    SMO_SC_Only1MeshItemSelected = 0
    lx.eval('dialog.setup info')
    lx.eval('dialog.title {SMO Quick Tag:}')
    lx.eval(
        'dialog.msg {You must only select the Mesh Item layer you are working on, in Item List, to run that script}')
    lx.eval('+dialog.open')
    lx.out('Only One Item Selected result:', SMO_SC_Only1MeshItemSelected)
    lx.out('script Stopped: Select only one Mesh Item')
    sys.exit

else:
    SMO_SC_Only1MeshItemSelected = 1
    lx.out('Only One Item Selected:', SMO_SC_Only1MeshItemSelected)
    lx.out('script running: right amount of Mesh Item selected')
# --------------------  safety check 1 : Only One Item Selected --- END


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

    SMO_SC_VertexModeEnabled = 1
    SMO_SC_EdgeModeEnabled = 0
    SMO_SC_PolygonModeEnabled = 0
    SMO_SC_ItemModeEnabled = 0

    lx.out('script Running: Vertex Component Selection Mode')


elif lx.eval1("select.typeFrom typelist:edge;vertex;polygon;item ?"):
    selType = "edge"
    attrType = "edge"

    SMO_SC_VertexModeEnabled = 0
    SMO_SC_EdgeModeEnabled = 1
    SMO_SC_PolygonModeEnabled = 0
    SMO_SC_ItemModeEnabled = 0

    lx.out('script Running: Edge Component Selection Mode')

elif lx.eval1("select.typeFrom typelist:polygon;vertex;edge;item ?"):
    selType = "polygon"
    attrType = "poly"

    SMO_SC_VertexModeEnabled = 0
    SMO_SC_EdgeModeEnabled = 0
    SMO_SC_PolygonModeEnabled = 1
    SMO_SC_ItemModeEnabled = 0

    lx.out('script Running: Polygon Component Selection Mode')


else:
    # This only fails if none of the three supported selection
    # modes have yet been used since the program started, or
    # if "item" or "ptag" (ie: materials) is the current
    # selection mode.

    SMO_SC_VertexModeEnabled = 0
    SMO_SC_EdgeModeEnabled = 0
    SMO_SC_PolygonModeEnabled = 0
    SMO_SC_ItemModeEnabled = 1

    lx.out('script Running: Item Component Selection Mode')

# Component Selection Mode type --- END

# -------------------------- #
# <---( SAFETY CHECK 3 )---> #
# -------------------------- #

# at Least 1 Polygons are selected --- START
try:
    #####--- Get current selected polygon count --- START ---#####
    #####
    CsPolys = len(mesh.geometry.polygons.selected)
    lx.out('Count Selected Poly', CsPolys)
    #####
    #####--- Get current selected polygon count --- END ---#####

    if CsPolys < 1:
        SMO_SC_min1PolygonSelected = 0
        lx.eval('dialog.setup info')
        lx.eval('dialog.title {SMO Quick Tag:}')
        lx.eval('dialog.msg {You must select at least 1 polygon to run that script}')
        lx.eval('+dialog.open')
        lx.out('script Stopped: Add more polygons to your selection')
        sys.exit

    elif CsPolys >= 1:
        SMO_SC_min1PolygonSelected = 1
        lx.out('script running: right amount of polygons in selection')
# at Least 3 Polygons are selected --- END
except:
    sys.exit

# ------------- Define user value for the Prerequisite TotalSafetyCheck --- START


# ---------------- Define current value for the Prerequisite TotalSafetyCheck --- START
#####
if SMO_SC_VertexModeEnabled == 1:
    lx.eval('select.type polygon')
if SMO_SC_EdgeModeEnabled == 1:
    lx.eval('select.type polygon')
if SMO_SC_ItemModeEnabled == 1:
    lx.out('script Running: Item Component Selection Mode')
    lx.eval('select.type polygon')
#####
# ---------------- Define current value for the Prerequisite TotalSafetyCheck --- END


# -------------------------- #
# <----( Main Macro )----> #
# -------------------------- #
lx.out('Start of SMO_QT_Setup Script')
lx.out('--------------------------')
# ---------------- Compare TotalSafetyCheck value and decide or not to continue the process  --- START


# ---------------------------#
# 0 = Add to current Polyons to selection set Tag
# ---------------------------#
if QT_Op == 0:
    if QT_Connected == 1:  # expand selection to connected Polys
        lx.eval('select.connect')

    if QT_ID == QTColorRed:
        lx.eval('select.editSet SMO_QT_Red add')
    elif QT_ID == QTColorMagenta:
        lx.eval('select.editSet SMO_QT_Magenta add')
    elif QT_ID == QTColorPink:
        lx.eval('select.editSet SMO_QT_Pink add')
    elif QT_ID == QTColorBrown:
        lx.eval('select.editSet SMO_QT_Brown add')
    elif QT_ID == QTColorOrange:
        lx.eval('select.editSet SMO_QT_Orange add')
    elif QT_ID == QTColorYellow:
        lx.eval('select.editSet SMO_QT_Yellow add')
    elif QT_ID == QTColorGreen:
        lx.eval('select.editSet SMO_QT_Green add')
    elif QT_ID == QTColorLightGreen:
        lx.eval('select.editSet SMO_QT_LightGreen add')
    elif QT_ID == QTColorCyan:
        lx.eval('select.editSet SMO_QT_Cyan add')
    elif QT_ID == QTColorBlue:
        lx.eval('select.editSet SMO_QT_Blue add')
    elif QT_ID == QTColorLightBlue:
        lx.eval('select.editSet SMO_QT_LightBlue add')
    elif QT_ID == QTColorUltramarine:
        lx.eval('select.editSet SMO_QT_Ultramarine add')
    elif QT_ID == QTColorPurple:
        lx.eval('select.editSet SMO_QT_Purple add')
    elif QT_ID == QTColorLightPurple:
        lx.eval('select.editSet SMO_QT_LightPurple add')
    elif QT_ID == QTColorDarkGrey:
        lx.eval('select.editSet SMO_QT_DarkGrey add')
        lx.eval(
            '!poly.pcrAssign SMO_QT_DarkGrey cmd:"@kit_SMO_QUICK_TAG:MacroSmoluck/TAG_Preset/Select_QT_DarkGrey.py" color:{0,2423 0,2423 0,2423}')
    elif QT_ID == QTColorGrey:
        lx.eval('select.editSet SMO_QT_Grey add')
        lx.eval(
            '!poly.pcrAssign SMO_QT_Grey cmd:"@kit_SMO_QUICK_TAG:MacroSmoluck/TAG_Preset/Select_QT_Grey.py" color:{0.4852 0.4852 0.4852}')
    elif QT_ID == QTColorWhite:
        lx.eval('select.editSet SMO_QT_White add')
        lx.eval(
            '!poly.pcrAssign SMO_QT_White cmd:"@kit_SMO_QUICK_TAG:MacroSmoluck/TAG_Preset/Select_QT_White.py" color:{0.855 0.855 0.855}')

# ---------------------------#
# 1 = Add Command Region Link
# ---------------------------#
if QT_Op == 1:
    # Switch to polygon Mode and dop selection if present
    lx.eval('select.type polygon')
    lx.eval('select.drop polygon')

    if QT_ID == QTColorRed:
        lx.eval('select.editSet SMO_QT_Red add')
        lx.eval(
            '!poly.pcrAssign SMO_QT_Red cmd:"@kit_SMO_QUICK_TAG:MacroSmoluck/TAG_Preset/Select_QT_Red.py" color:{1.0 0.0844 0.0382}')
    elif QT_ID == QTColorMagenta:
        lx.eval('select.editSet SMO_QT_Magenta add')
        lx.eval(
            '!poly.pcrAssign SMO_QT_Magenta cmd:"@kit_SMO_QUICK_TAG:MacroSmoluck/TAG_Preset/Select_QT_Magenta.py" color:{0,8632 0,0802 0,3968}')
    elif QT_ID == QTColorPink:
        lx.eval('select.editSet SMO_QT_Pink add')
        lx.eval(
            '!poly.pcrAssign SMO_QT_Pink cmd:"@kit_SMO_QUICK_TAG:MacroSmoluck/TAG_Preset/Select_QT_Pink.py" color:{0.807 0.1946 0.1946}')
    elif QT_ID == QTColorBrown:
        lx.eval('select.editSet SMO_QT_Brown add')
        lx.eval(
            '!poly.pcrAssign SMO_QT_Brown cmd:"@kit_SMO_QUICK_TAG:MacroSmoluck/TAG_Preset/Select_QT_Brown.py" color:{0.402 0.2232 0.0704}')
    elif QT_ID == QTColorOrange:
        lx.eval('select.editSet SMO_QT_Orange add')
        lx.eval(
            '!poly.pcrAssign SMO_QT_Orange cmd:"@kit_SMO_QUICK_TAG:MacroSmoluck/TAG_Preset/Select_QT_Orange.py" color:{1.0 0.4793 0.0497}')
    elif QT_ID == QTColorYellow:
        lx.eval('select.editSet SMO_QT_Yellow add')
        lx.eval(
            '!poly.pcrAssign SMO_QT_Yellow cmd:"@kit_SMO_QUICK_TAG:MacroSmoluck/TAG_Preset/Select_QT_Yellow.py" color:{1.0 0,8149 0,0452}')
    elif QT_ID == QTColorGreen:
        lx.eval('select.editSet SMO_QT_Green add')
        lx.eval(
            '!poly.pcrAssign SMO_QT_Green cmd:"@kit_SMO_QUICK_TAG:MacroSmoluck/TAG_Preset/Select_QT_Green.py" color:{0,0423 0,7682 0,0423}')
    elif QT_ID == QTColorLightGreen:
        lx.eval('select.editSet SMO_QT_LightGreen add')
        lx.eval(
            '!poly.pcrAssign SMO_QT_LightGreen cmd:"@kit_SMO_QUICK_TAG:MacroSmoluck/TAG_Preset/Select_QT_LightGreen.py" color:{0.2832 0.9131 0.2832}')
    elif QT_ID == QTColorCyan:
        lx.eval('select.editSet SMO_QT_Cyan add')
        lx.eval(
            '!poly.pcrAssign SMO_QT_Cyan cmd:"@kit_SMO_QUICK_TAG:MacroSmoluck/TAG_Preset/Select_QT_Cyan.py" color:{0,0382 0,9911 0,7454}')
    elif QT_ID == QTColorBlue:
        lx.eval('select.editSet SMO_QT_Blue add')
        lx.eval(
            '!poly.pcrAssign SMO_QT_Blue cmd:"@kit_SMO_QUICK_TAG:MacroSmoluck/TAG_Preset/Select_QT_Blue.py" color:{0,0529 0,5029 1.0}')
    elif QT_ID == QTColorLightBlue:
        lx.eval('select.editSet SMO_QT_LightBlue add')
        lx.eval(
            '!poly.pcrAssign SMO_QT_LightBlue cmd:"@kit_SMO_QUICK_TAG:MacroSmoluck/TAG_Preset/Select_QT_LightBlue.py" color:{0,2232 0,624 1.0}')
    elif QT_ID == QTColorUltramarine:
        lx.eval('select.editSet SMO_QT_Ultramarine add')
        lx.eval(
            '!poly.pcrAssign SMO_QT_Ultramarine cmd:"@kit_SMO_QUICK_TAG:MacroSmoluck/TAG_Preset/Select_QT_Ultramarine.py" color:{0.1274 0.2502 1.0}')
    elif QT_ID == QTColorPurple:
        lx.eval('select.editSet SMO_QT_Purple add')
        lx.eval(
            '!poly.pcrAssign SMO_QT_Purple cmd:"@kit_SMO_QUICK_TAG:MacroSmoluck/TAG_Preset/Select_QT_Purple.py" color:{0,3763 0,2423 0,8308}')
    elif QT_ID == QTColorLightPurple:
        lx.eval('select.editSet SMO_QT_LightPurple add')
        lx.eval(
            '!poly.pcrAssign SMO_QT_LightPurple cmd:"@kit_SMO_QUICK_TAG:MacroSmoluck/TAG_Preset/Select_QT_LightPurple.py" color:{0.624 0.4179 1.0}')
    elif QT_ID == QTColorDarkGrey:
        lx.eval('select.editSet SMO_QT_DarkGrey add')
        lx.eval(
            '!poly.pcrAssign SMO_QT_DarkGrey cmd:"@kit_SMO_QUICK_TAG:MacroSmoluck/TAG_Preset/Select_QT_DarkGrey.py" color:{0,2423 0,2423 0,2423}')
    elif QT_ID == QTColorGrey:
        lx.eval('select.editSet SMO_QT_Grey add')
        lx.eval(
            '!poly.pcrAssign SMO_QT_Grey cmd:"@kit_SMO_QUICK_TAG:MacroSmoluck/TAG_Preset/Select_QT_Grey.py" color:{0.4852 0.4852 0.4852}')
    elif QT_ID == QTColorWhite:
        lx.eval('select.editSet SMO_QT_White add')
        lx.eval(
            '!poly.pcrAssign SMO_QT_White cmd:"@kit_SMO_QUICK_TAG:MacroSmoluck/TAG_Preset/Select_QT_White.py" color:{0.855 0.855 0.855}')

    lx.eval('select.drop polygon')
    lx.eval('select.type item')

# -----------------------------------------------#
# 2 = Create Selection Set and Add Command Region
# -----------------------------------------------#
if QT_Op == 2:
    if QT_Connected == 1:  # expand selection to connected Polys
        lx.eval('select.connect')

    if QT_ID == QTColorRed:
        lx.eval('select.editSet SMO_QT_Red add')
        lx.eval(
            '!poly.pcrAssign SMO_QT_Red cmd:"@kit_SMO_QUICK_TAG:MacroSmoluck/TAG_Preset/Select_QT_Red.py" color:{1.0 0.0844 0.0382}')
    elif QT_ID == QTColorMagenta:
        lx.eval('select.editSet SMO_QT_Magenta add')
        lx.eval(
            '!poly.pcrAssign SMO_QT_Magenta cmd:"@kit_SMO_QUICK_TAG:MacroSmoluck/TAG_Preset/Select_QT_Magenta.py" color:{0,8632 0,0802 0,3968}')
    elif QT_ID == QTColorPink:
        lx.eval('select.editSet SMO_QT_Pink add')
        lx.eval(
            '!poly.pcrAssign SMO_QT_Pink cmd:"@kit_SMO_QUICK_TAG:MacroSmoluck/TAG_Preset/Select_QT_Pink.py" color:{0.807 0.1946 0.1946}')
    elif QT_ID == QTColorBrown:
        lx.eval('select.editSet SMO_QT_Brown add')
        lx.eval(
            '!poly.pcrAssign SMO_QT_Brown cmd:"@kit_SMO_QUICK_TAG:MacroSmoluck/TAG_Preset/Select_QT_Brown.py" color:{0.402 0.2232 0.0704}')
    elif QT_ID == QTColorOrange:
        lx.eval('select.editSet SMO_QT_Orange add')
        lx.eval(
            '!poly.pcrAssign SMO_QT_Orange cmd:"@kit_SMO_QUICK_TAG:MacroSmoluck/TAG_Preset/Select_QT_Orange.py" color:{1.0 0.4793 0.0497}')
    elif QT_ID == QTColorYellow:
        lx.eval('select.editSet SMO_QT_Yellow add')
        lx.eval(
            '!poly.pcrAssign SMO_QT_Yellow cmd:"@kit_SMO_QUICK_TAG:MacroSmoluck/TAG_Preset/Select_QT_Yellow.py" color:{1.0 0,8149 0,0452}')
    elif QT_ID == QTColorGreen:
        lx.eval('select.editSet SMO_QT_Green add')
        lx.eval(
            '!poly.pcrAssign SMO_QT_Green cmd:"@kit_SMO_QUICK_TAG:MacroSmoluck/TAG_Preset/Select_QT_Green.py" color:{0,0423 0,7682 0,0423}')
    elif QT_ID == QTColorLightGreen:
        lx.eval('select.editSet SMO_QT_LightGreen add')
        lx.eval(
            '!poly.pcrAssign SMO_QT_LightGreen cmd:"@kit_SMO_QUICK_TAG:MacroSmoluck/TAG_Preset/Select_QT_LightGreen.py" color:{0.2832 0.9131 0.2832}')
    elif QT_ID == QTColorCyan:
        lx.eval('select.editSet SMO_QT_Cyan add')
        lx.eval(
            '!poly.pcrAssign SMO_QT_Cyan cmd:"@kit_SMO_QUICK_TAG:MacroSmoluck/TAG_Preset/Select_QT_Cyan.py" color:{0,0382 0,9911 0,7454}')
    elif QT_ID == QTColorBlue:
        lx.eval('select.editSet SMO_QT_Blue add')
        lx.eval(
            '!poly.pcrAssign SMO_QT_Blue cmd:"@kit_SMO_QUICK_TAG:MacroSmoluck/TAG_Preset/Select_QT_Blue.py" color:{0,0529 0,5029 1.0}')
    elif QT_ID == QTColorLightBlue:
        lx.eval('select.editSet SMO_QT_LightBlue add')
        lx.eval(
            '!poly.pcrAssign SMO_QT_LightBlue cmd:"@kit_SMO_QUICK_TAG:MacroSmoluck/TAG_Preset/Select_QT_LightBlue.py" color:{0,2232 0,624 1.0}')
    elif QT_ID == QTColorUltramarine:
        lx.eval('select.editSet SMO_QT_Ultramarine add')
        lx.eval(
            '!poly.pcrAssign SMO_QT_Ultramarine cmd:"@kit_SMO_QUICK_TAG:MacroSmoluck/TAG_Preset/Select_QT_Ultramarine.py" color:{0.1274 0.2502 1.0}')
    elif QT_ID == QTColorPurple:
        lx.eval('select.editSet SMO_QT_Purple add')
        lx.eval(
            '!poly.pcrAssign SMO_QT_Purple cmd:"@kit_SMO_QUICK_TAG:MacroSmoluck/TAG_Preset/Select_QT_Purple.py" color:{0,3763 0,2423 0,8308}')
    elif QT_ID == QTColorLightPurple:
        lx.eval('select.editSet SMO_QT_LightPurple add')
        lx.eval(
            '!poly.pcrAssign SMO_QT_LightPurple cmd:"@kit_SMO_QUICK_TAG:MacroSmoluck/TAG_Preset/Select_QT_LightPurple.py" color:{0.624 0.4179 1.0}')
    elif QT_ID == QTColorDarkGrey:
        lx.eval('select.editSet SMO_QT_DarkGrey add')
        lx.eval(
            '!poly.pcrAssign SMO_QT_DarkGrey cmd:"@kit_SMO_QUICK_TAG:MacroSmoluck/TAG_Preset/Select_QT_DarkGrey.py" color:{0,2423 0,2423 0,2423}')
    elif QT_ID == QTColorGrey:
        lx.eval('select.editSet SMO_QT_Grey add')
        lx.eval(
            '!poly.pcrAssign SMO_QT_Grey cmd:"@kit_SMO_QUICK_TAG:MacroSmoluck/TAG_Preset/Select_QT_Grey.py" color:{0.4852 0.4852 0.4852}')
    elif QT_ID == QTColorWhite:
        lx.eval('select.editSet SMO_QT_White add')
        lx.eval(
            '!poly.pcrAssign SMO_QT_White cmd:"@kit_SMO_QUICK_TAG:MacroSmoluck/TAG_Preset/Select_QT_White.py" color:{0.855 0.855 0.855}')

    lx.eval('select.drop polygon')

# ---------------------------------------------------#
# 3 = Remove Polygons from the current Tag they have.
# ---------------------------------------------------#
if QT_Op == 3:
    # Polygon selected on Remove SelSetTag
    lx.eval("user.defNew name:SMO_SC_RemoveSSTag type:integer life:momentary")
    try:

        #####--- Get current selected polygon count --- START ---#####
        #####
        removeCsPolys = len(mesh.geometry.polygons.selected)
        lx.out('Count Selected Poly', removeCsPolys)
        #####
        #####--- Get current selected polygon count --- END ---#####

        if removeCsPolys < 1:
            SMO_SC_RemoveSSTag = 0
            lx.out('script running: no Polygon selected --> Remove from All Polygons')

        elif removeCsPolys >= 1:
            SMO_SC_RemoveSSTag = 1
            lx.out('script running: some Polygons selected --> Remove only those Polygons')
    except:
        sys.exit

    if SMO_SC_RemoveSSTag == 0:
        lx.eval('select.all')
    if SMO_SC_RemoveSSTag == 1:
        if QT_ID == QTColorRed:
            lx.eval('select.editSet SMO_QT_Red remove')
        elif QT_ID == QTColorMagenta:
            lx.eval('select.editSet SMO_QT_Magenta remove')
        elif QT_ID == QTColorPink:
            lx.eval('select.editSet SMO_QT_Pink remove')
        elif QT_ID == QTColorBrown:
            lx.eval('select.editSet SMO_QT_Brown remove')
        elif QT_ID == QTColorOrange:
            lx.eval('select.editSet SMO_QT_Orange remove')
        elif QT_ID == QTColorYellow:
            lx.eval('select.editSet SMO_QT_Yellow remove')
        elif QT_ID == QTColorGreen:
            lx.eval('select.editSet SMO_QT_Green remove')
        elif QT_ID == QTColorLightGreen:
            lx.eval('select.editSet SMO_QT_LightGreen remove')
        elif QT_ID == QTColorCyan:
            lx.eval('select.editSet SMO_QT_Cyan remove')
        elif QT_ID == QTColorBlue:
            lx.eval('select.editSet SMO_QT_Blue remove')
        elif QT_ID == QTColorLightBlue:
            lx.eval('select.editSet SMO_QT_LightBlue remove')
        elif QT_ID == QTColorUltramarine:
            lx.eval('select.editSet SMO_QT_Ultramarine remove')
        elif QT_ID == QTColorPurple:
            lx.eval('select.editSet SMO_QT_Purple remove')
        elif QT_ID == QTColorLightPurple:
            lx.eval('select.editSet SMO_QT_LightPurple remove')
        elif QT_ID == QTColorDarkGrey:
            lx.eval('select.editSet SMO_QT_DarkGrey remove')
        elif QT_ID == QTColorGrey:
            lx.eval('select.editSet SMO_QT_Grey remove')
        elif QT_ID == QTColorWhite:
            lx.eval('select.editSet SMO_QT_White remove')

        lx.eval('select.drop polygon')

# --------------------------------#
# 4 = Delete Specificaly this QTag
#       via QT_ID
# --------------------------------#
if QT_Op == 4:
    # Polygon Sel Set Counter / Enumerator ##
    try:
        # Select the main layer
        lx.eval('query layerservice layer.id ? main')
        # Number of Poly Sel Set
        PolySelSet_COUNT = lx.eval('query layerservice polset.N ? all')
        lx.out('<---Polygon Selection Set Total Count:--->')
        lx.out('Total Count:', PolySelSet_COUNT)
        lx.out('<------------------------->')
        PolySelSetsList = []
        lx.out('<--- Polygon Sel Set Name --->')
        for i in range(PolySelSet_COUNT):
            # Name of detected Poly Sel Set
            PolySelSetsList.append(lx.eval('query layerservice polset.name ? %s' % i))
            lx.out('<---Polygon Selection Set Name:--->')
            lx.out('Polygon Selection Set:', PolySelSetsList)
            lx.eval('select.drop polygon')
    except RuntimeError:
        sys.exit()

    if PolySelSetPrefixNameRed in PolySelSetsList and QT_ID == QTColorRed:
        lx.eval('select.useSet SMO_QT_Red replace')
        lx.eval('poly.pcrClear')
        lx.eval('!select.deleteSet SMO_QT_Red')
        lx.eval('select.drop polygon')

    if PolySelSetPrefixNameMagenta in PolySelSetsList and QT_ID == QTColorMagenta:
        lx.eval('select.useSet SMO_QT_Magenta replace')
        lx.eval('poly.pcrClear')
        lx.eval('!select.deleteSet SMO_QT_Magenta')
        lx.eval('select.drop polygon')

    if PolySelSetPrefixNamePink in PolySelSetsList and QT_ID == QTColorPink:
        lx.eval('select.useSet SMO_QT_Pink replace')
        lx.eval('poly.pcrClear')
        lx.eval('!select.deleteSet SMO_QT_Pink')
        lx.eval('select.drop polygon')

    if PolySelSetPrefixNameBrown in PolySelSetsList and QT_ID == QTColorBrown:
        lx.eval('select.useSet SMO_QT_Brown replace')
        lx.eval('poly.pcrClear')
        lx.eval('!select.deleteSet SMO_QT_Brown')
        lx.eval('select.drop polygon')

    if PolySelSetPrefixNameOrange in PolySelSetsList and QT_ID == QTColorOrange:
        lx.eval('select.useSet SMO_QT_Orange replace')
        lx.eval('poly.pcrClear')
        lx.eval('!select.deleteSet SMO_QT_Orange')
        lx.eval('select.drop polygon')

    if PolySelSetPrefixNameYellow in PolySelSetsList and QT_ID == QTColorYellow:
        lx.eval('select.useSet SMO_QT_Yellow replace')
        lx.eval('poly.pcrClear')
        lx.eval('!select.deleteSet SMO_QT_Yellow')
        lx.eval('select.drop polygon')

    if PolySelSetPrefixNameGreen in PolySelSetsList and QT_ID == QTColorGreen:
        lx.eval('select.useSet SMO_QT_Green replace')
        lx.eval('poly.pcrClear')
        lx.eval('!select.deleteSet SMO_QT_Green')
        lx.eval('select.drop polygon')

    if PolySelSetPrefixNameLightGreen in PolySelSetsList and QT_ID == QTColorLightGreen:
        lx.eval('select.useSet SMO_QT_LightGreen replace')
        lx.eval('poly.pcrClear')
        lx.eval('!select.deleteSet SMO_QT_LightGreen')
        lx.eval('select.drop polygon')

    if PolySelSetPrefixNameCyan in PolySelSetsList and QT_ID == QTColorCyan:
        lx.eval('select.useSet SMO_QT_Cyan replace')
        lx.eval('poly.pcrClear')
        lx.eval('!select.deleteSet SMO_QT_Cyan')
        lx.eval('select.drop polygon')

    if PolySelSetPrefixNameBlue in PolySelSetsList and QT_ID == QTColorBlue:
        lx.eval('select.useSet SMO_QT_Blue replace')
        lx.eval('poly.pcrClear')
        lx.eval('!select.deleteSet SMO_QT_Blue')
        lx.eval('select.drop polygon')

    if PolySelSetPrefixNameLightBlue in PolySelSetsList and QT_ID == QTColorLightBlue:
        lx.eval('select.useSet SMO_QT_LightBlue replace')
        lx.eval('poly.pcrClear')
        lx.eval('!select.deleteSet SMO_QT_LightBlue')
        lx.eval('select.drop polygon')

    if PolySelSetPrefixNameUltramarine in PolySelSetsList and QT_ID == QTColorUltramarine:
        lx.eval('select.useSet SMO_QT_Ultramarine replace')
        lx.eval('poly.pcrClear')
        lx.eval('!select.deleteSet SMO_QT_Ultramarine')
        lx.eval('select.drop polygon')

    if PolySelSetPrefixNamePurple in PolySelSetsList and QT_ID == QTColorPurple:
        lx.eval('select.useSet SMO_QT_Purple replace')
        lx.eval('poly.pcrClear')
        lx.eval('!select.deleteSet SMO_QT_Purple')
        lx.eval('select.drop polygon')

    if PolySelSetPrefixNameLightPurple in PolySelSetsList and QT_ID == QTColorLightPurple:
        lx.eval('select.useSet SMO_QT_LightPurple replace')
        lx.eval('poly.pcrClear')
        lx.eval('!select.deleteSet SMO_QT_LightPurple')
        lx.eval('select.drop polygon')

    if PolySelSetPrefixNameDarkGrey in PolySelSetsList and QT_ID == QTColorDarkGrey:
        lx.eval('select.useSet SMO_QT_DarkGrey replace')
        lx.eval('poly.pcrClear')
        lx.eval('!select.deleteSet SMO_QT_DarkGrey')
        lx.eval('select.drop polygon')

    if PolySelSetPrefixNameGrey in PolySelSetsList and QT_ID == QTColorGrey:
        lx.eval('select.useSet SMO_QT_Grey replace')
        lx.eval('poly.pcrClear')
        lx.eval('!select.deleteSet SMO_QT_Grey')
        lx.eval('select.drop polygon')

    if PolySelSetPrefixNameWhite in PolySelSetsList and QT_ID == QTColorWhite:
        lx.eval('select.useSet SMO_QT_White replace')
        lx.eval('poly.pcrClear')
        lx.eval('!select.deleteSet SMO_QT_White')
        lx.eval('select.drop polygon')

    lx.eval('select.drop polygon')

# -------------------#
# 5 = Delete all QTag
# -------------------#
if QT_Op == 5:
    # Polygon Sel Set Counter / Enumerator ##
    try:
        # Select the main layer
        lx.eval('query layerservice layer.id ? main')
        # Number of Poly Sel Set
        PolySelSet_COUNT = lx.eval('query layerservice polset.N ? all')
        lx.out('<---Polygon Selection Set Total Count:--->')
        lx.out('Total Count:', PolySelSet_COUNT)
        lx.out('<------------------------->')
        PolySelSetsList = []
        lx.out('<--- Polygon Sel Set Name --->')
        for i in range(PolySelSet_COUNT):
            # Name of detected Poly Sel Set
            PolySelSetsList.append(lx.eval('query layerservice polset.name ? %s' % i))
            lx.out('<---Polygon Selection Set Name:--->')
            lx.out('Polygon Selection Set:', PolySelSetsList)
            lx.eval('select.drop polygon')
    except RuntimeError:
        sys.exit()

    if PolySelSetPrefixNameRed in PolySelSetsList:
        lx.eval('select.useSet SMO_QT_Red replace')
        lx.eval('poly.pcrClear')
        lx.eval('!select.deleteSet SMO_QT_Red')
        lx.eval('select.drop polygon')

    if PolySelSetPrefixNameMagenta in PolySelSetsList:
        lx.eval('select.useSet SMO_QT_Magenta replace')
        lx.eval('poly.pcrClear')
        lx.eval('!select.deleteSet SMO_QT_Magenta')
        lx.eval('select.drop polygon')

    if PolySelSetPrefixNamePink in PolySelSetsList:
        lx.eval('select.useSet SMO_QT_Pink replace')
        lx.eval('poly.pcrClear')
        lx.eval('!select.deleteSet SMO_QT_Pink')
        lx.eval('select.drop polygon')

    if PolySelSetPrefixNameBrown in PolySelSetsList:
        lx.eval('select.useSet SMO_QT_Brown replace')
        lx.eval('poly.pcrClear')
        lx.eval('!select.deleteSet SMO_QT_Brown')
        lx.eval('select.drop polygon')

    if PolySelSetPrefixNameOrange in PolySelSetsList:
        lx.eval('select.useSet SMO_QT_Orange replace')
        lx.eval('poly.pcrClear')
        lx.eval('!select.deleteSet SMO_QT_Orange')
        lx.eval('select.drop polygon')

    if PolySelSetPrefixNameYellow in PolySelSetsList:
        lx.eval('select.useSet SMO_QT_Yellow replace')
        lx.eval('poly.pcrClear')
        lx.eval('!select.deleteSet SMO_QT_Yellow')
        lx.eval('select.drop polygon')

    if PolySelSetPrefixNameGreen in PolySelSetsList:
        lx.eval('select.useSet SMO_QT_Green replace')
        lx.eval('poly.pcrClear')
        lx.eval('!select.deleteSet SMO_QT_Green')
        lx.eval('select.drop polygon')

    if PolySelSetPrefixNameLightGreen in PolySelSetsList:
        lx.eval('select.useSet SMO_QT_LightGreen replace')
        lx.eval('poly.pcrClear')
        lx.eval('!select.deleteSet SMO_QT_LightGreen')
        lx.eval('select.drop polygon')

    if PolySelSetPrefixNameCyan in PolySelSetsList:
        lx.eval('select.useSet SMO_QT_Cyan replace')
        lx.eval('poly.pcrClear')
        lx.eval('!select.deleteSet SMO_QT_Cyan')
        lx.eval('select.drop polygon')

    if PolySelSetPrefixNameBlue in PolySelSetsList:
        lx.eval('select.useSet SMO_QT_Blue replace')
        lx.eval('poly.pcrClear')
        lx.eval('!select.deleteSet SMO_QT_Blue')
        lx.eval('select.drop polygon')

    if PolySelSetPrefixNameLightBlue in PolySelSetsList:
        lx.eval('select.useSet SMO_QT_LightBlue replace')
        lx.eval('poly.pcrClear')
        lx.eval('!select.deleteSet SMO_QT_LightBlue')
        lx.eval('select.drop polygon')

    if PolySelSetPrefixNameUltramarine in PolySelSetsList:
        lx.eval('select.useSet SMO_QT_Ultramarine replace')
        lx.eval('poly.pcrClear')
        lx.eval('!select.deleteSet SMO_QT_Ultramarine')
        lx.eval('select.drop polygon')

    if PolySelSetPrefixNamePurple in PolySelSetsList:
        lx.eval('select.useSet SMO_QT_Purple replace')
        lx.eval('poly.pcrClear')
        lx.eval('!select.deleteSet SMO_QT_Purple')
        lx.eval('select.drop polygon')

    if PolySelSetPrefixNameLightPurple in PolySelSetsList:
        lx.eval('select.useSet SMO_QT_LightPurple replace')
        lx.eval('poly.pcrClear')
        lx.eval('!select.deleteSet SMO_QT_LightPurple')
        lx.eval('select.drop polygon')

    if PolySelSetPrefixNameDarkGrey in PolySelSetsList:
        lx.eval('select.useSet SMO_QT_DarkGrey replace')
        lx.eval('poly.pcrClear')
        lx.eval('!select.deleteSet SMO_QT_DarkGrey')
        lx.eval('select.drop polygon')

    if PolySelSetPrefixNameGrey in PolySelSetsList:
        lx.eval('select.useSet SMO_QT_Grey replace')
        lx.eval('poly.pcrClear')
        lx.eval('!select.deleteSet SMO_QT_Grey')
        lx.eval('select.drop polygon')

    if PolySelSetPrefixNameWhite in PolySelSetsList:
        lx.eval('select.useSet SMO_QT_White replace')
        lx.eval('poly.pcrClear')
        lx.eval('!select.deleteSet SMO_QT_White')
        lx.eval('select.drop polygon')

    lx.eval('select.drop polygon')

lx.out('--------------------------')
lx.out('End of SMO_QT_Setup Script')
# ---------------- Compare TotalSafetyCheck value and decide or not to continue the process  --- END

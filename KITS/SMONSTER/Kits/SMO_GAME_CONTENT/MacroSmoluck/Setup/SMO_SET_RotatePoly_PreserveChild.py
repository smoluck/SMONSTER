# python
"""
Name:         SMO_RotatePoly_PreserveChild.py

Purpose:		This script is designed to:
                Select the mesh to rotate, in item mode. It will rotate by 180 degree the polygons,
                while rotating the center as opposed, and preserve the child orientation and parenting of this item.

Author:       	Franck ELISABETH
Website:      	https://www.smoluck.com
Created:      	10/06/2019
Copyright:    	(c) Franck Elisabeth 2017-2022
"""

import lx
import modo
import sys

scene = modo.scene.current()
mesh = scene.selectedByType('mesh')[0]
CsPolys = len(mesh.geometry.polygons.selected)
item = modo.Scene().selected[0]

args = lx.args()
lx.out(args)
RotAxe = int(args[0])
lx.out('Desired Axe change:', RotAxe)

# --------------------  safety check 1: ITEM Selection Mode enabled --- START

selType = ""
# Used to query layerservice for the list of polygons, edges or vertices.
attrType = ""

if lx.eval1("select.typeFrom typelist:vertex;polygon;edge;item;ptag ?"):
    selType = "vertex"
    attrType = "vert"

    SMO_SafetyCheck_ItemModeEnabled = 0
    lx.eval('dialog.setup info')
    lx.eval('dialog.title {SMO_RotatePoly_PreserveChild:}')
    lx.eval('dialog.msg {You must be in ITEM Mode to run that script}')
    lx.eval('+dialog.open')
    lx.out('script Stopped: You must be in ITEM Mode to run that script')
    sys.exit
# sys.exit( "LXe_FAILED:Must be in ITEM selection mode." )


elif lx.eval1("select.typeFrom typelist:edge;vertex;polygon;item ?"):
    selType = "edge"
    attrType = "edge"

    SMO_SafetyCheck_ItemModeEnabled = 0
    lx.eval('dialog.setup info')
    lx.eval('dialog.title {SMO_RotatePoly_PreserveChild:}')
    lx.eval('dialog.msg {You must be in ITEM Mode to run that script}')
    lx.eval('+dialog.open')
    lx.out('script Stopped: You must be in ITEM Mode to run that script')
    sys.exit
# sys.exit( "LXe_FAILED:Must be in ITEM selection mode." )

elif lx.eval1("select.typeFrom typelist:polygon;vertex;edge;item ?"):
    selType = "polygon"
    attrType = "poly"

    SMO_SafetyCheck_ItemModeEnabled = 0
    lx.eval('dialog.setup info')
    lx.eval('dialog.title {SMO_RotatePoly_PreserveChild:}')
    lx.eval('dialog.msg {You must be in ITEM Mode to run that script}')
    lx.eval('+dialog.open')
    lx.out('script Stopped: You must be in ITEM Mode to run that script')
    sys.exit
# sys.exit( "LXe_FAILED:Must be in ITEM selection mode." )


else:
    # This only fails if none of the three supported selection
    # modes have yet been used since the program started, or
    # if "item" or "ptag" (ie: materials) is the current
    # selection mode.
    SMO_SafetyCheck_ItemModeEnabled = 1
    lx.out('script Running: Correct Component Selection Mode')

# --------------------  safety check 1: ITEM Selection Mode enabled --- END


# ---------------- Define current value for the Prerequisite TotalSafetyCheck --- START
#####
TotalSafetyCheckTrueValue = 1
lx.out('Desired Value', TotalSafetyCheckTrueValue)
TotalSafetyCheck = SMO_SafetyCheck_ItemModeEnabled
lx.out('Current Value', TotalSafetyCheck)
#####
# ---------------- Define current value for the Prerequisite TotalSafetyCheck --- END


# ------------------------ #
# <----( Main Macro )----> #
# ------------------------ #
lx.out('Start of SMO_RotatePoly_PreserveChild')
# ---------------- Compare TotalSafetyCheck value and decide or not to continue the process  --- START
if TotalSafetyCheck == TotalSafetyCheckTrueValue:

    lx.eval('workPlane.fitSelect')

    # Tag TARGET
    lx.eval('select.editSet RotPoly_ITEM_TARGET add')

    # Tag CHILD of TARGET
    lx.eval('select.itemHierarchy')
    ChildItems = len(lx.evalN('query sceneservice selection ? mesh'))
    lx.out('ChildItems', ChildItems)
    if ChildItems >= 2:
        ChildPresent = 1
        lx.out('This Target as Child elements')
        lx.eval('select.useSet RotPoly_ITEM_TARGET deselect')
        lx.eval('select.editSet RotPoly_ITEM_CHILD add {}')
        lx.eval('select.useSet RotPoly_ITEM_TARGET select')
        lx.eval('select.useSet RotPoly_ITEM_CHILD deselect')
    elif ChildItems <= 1:
        ChildPresent = 0
        lx.out('This Target doesn`t have Child elements')
        lx.eval('select.useSet RotPoly_ITEM_TARGET deselect')
        lx.eval('select.useSet RotPoly_ITEM_TARGET replace')

    # Tag PARENT of TARGET
    item.parent.select()
    lx.eval('select.useSet RotPoly_ITEM_TARGET deselect')
    ParentItem = len(lx.evalN('query sceneservice selection ? mesh'))
    lx.out('ParentItem', ParentItem)
    if ParentItem >= 1:
        ParentPresent = 1
        lx.out('This Target as Parent')
        lx.eval('select.editSet RotPoly_ITEM_PARENT add')
        lx.eval('select.useSet RotPoly_ITEM_TARGET replace')
    elif ParentItem == 0:
        ParentPresent = 0
        lx.out('This Target doesn`t have Parent')
        lx.eval('select.useSet RotPoly_ITEM_TARGET deselect')
        lx.eval('select.useSet RotPoly_ITEM_TARGET replace')

    if ParentPresent == 1:
        # unparent Target in Place
        lx.eval('item.parent parent:{} inPlace:1')

    if ChildPresent == 1:
        # unparent Childs in Place
        lx.eval('select.useSet RotPoly_ITEM_CHILD replace')
        lx.eval('item.parent parent:{} inPlace:1')

    # Align workspace to Target item
    lx.eval('select.useSet RotPoly_ITEM_TARGET replace')
    lx.eval('tool.set actr.origin on')

    # Switch to Polygon Mode and select All
    lx.eval('select.type polygon')
    lx.eval('select.all')
    lx.eval('cut')

    # if RotAxe == 0 :
    # Rotate by 180 Degree All the Polygons
    # lx.eval('@{kit_SMO_GAME_CONTENT:MacroSmoluck/Setup/SMO_SET_RotateXYZ_Component.LXM} 180 0 0')

    # if RotAxe == 1 :
    # Rotate by 180 Degree All the Polygons
    # lx.eval('@{kit_SMO_GAME_CONTENT:MacroSmoluck/Setup/SMO_SET_RotateXYZ_Component.LXM} 0 180 0')

    # if RotAxe == 2 :
    # Rotate by 180 Degree All the Polygons
    # lx.eval('@{kit_SMO_GAME_CONTENT:MacroSmoluck/Setup/SMO_SET_RotateXYZ_Component.LXM} 0 0 180')

    # Drop Polygon selection and switch to Item Mode
    lx.eval('select.drop polygon')
    lx.eval('select.type item')
    lx.eval('tool.set actr.local on')
    lx.eval('workPlane.reset')

    lx.eval('workPlane.fitSelect')
    lx.eval('tool.set actr.origin on')

    # if RotAxe == 0 :
    # lx.eval('@{kit_SMO_GAME_CONTENT:MacroSmoluck/Setup/SMO_SET_RotateXYZ_Item.LXM} 180 0 0')
    # if RotAxe == 1 :
    # lx.eval('@{kit_SMO_GAME_CONTENT:MacroSmoluck/Setup/SMO_SET_RotateXYZ_Item.LXM} 0 180 0')
    # if RotAxe == 2 :
    # lx.eval('@{kit_SMO_GAME_CONTENT:MacroSmoluck/Setup/SMO_SET_RotateXYZ_Item.LXM} 0 0 180')

    if RotAxe == 0:
        # Rotate by 180 Degree the Mesh item back in original place
        lx.eval('@{kit_SMO_GAME_CONTENT:MacroSmoluck/Setup/SMO_SET_ShiftRotateXYZ_Item.py} 1 180')
        lx.eval('@{kit_SMO_GAME_CONTENT:MacroSmoluck/Setup/SMO_SET_ShiftRotateXYZ_Item.py} 2 180')

    if RotAxe == 1:
        # Rotate by 180 Degree the Mesh item back in original place
        lx.eval('@{kit_SMO_GAME_CONTENT:MacroSmoluck/Setup/SMO_SET_ShiftRotateXYZ_Item.py} 0 180')
        lx.eval('@{kit_SMO_GAME_CONTENT:MacroSmoluck/Setup/SMO_SET_ShiftRotateXYZ_Item.py} 2 180')

    if RotAxe == 2:
        # Rotate by 180 Degree the Mesh item back in original place
        lx.eval('@{kit_SMO_GAME_CONTENT:MacroSmoluck/Setup/SMO_SET_ShiftRotateXYZ_Item.py} 0 180')
        lx.eval('@{kit_SMO_GAME_CONTENT:MacroSmoluck/Setup/SMO_SET_ShiftRotateXYZ_Item.py} 1 180')

    lx.eval('select.type polygon')
    lx.eval('paste')
    lx.eval('select.drop polygon')
    lx.eval('select.type item')

    if ChildPresent == 1:
        # Reconnect Child to Target
        lx.eval('select.useSet RotPoly_ITEM_CHILD replace')
        lx.eval('select.useSet RotPoly_ITEM_TARGET select')
        lx.eval('item.parent inPlace:1')

    if ParentPresent == 1:
        # Reconnect Target to Parent
        lx.eval('select.useSet RotPoly_ITEM_TARGET replace')
        lx.eval('select.useSet RotPoly_ITEM_PARENT select')
        lx.eval('item.parent inPlace:1')

    lx.eval('select.useSet RotPoly_ITEM_TARGET replace')

    # Cleanup scene from Temp Item Selection Set Tag

    lx.eval('!select.deleteSet RotPoly_ITEM_TARGET')
    if ChildPresent == 1:
        lx.eval('!select.deleteSet RotPoly_ITEM_CHILD')
    if ParentPresent == 1:
        lx.eval('!select.deleteSet RotPoly_ITEM_PARENT')
    lx.eval('tool.set actr.auto on')
    lx.eval('workPlane.reset')


elif TotalSafetyCheck != TotalSafetyCheckTrueValue:
    lx.out('script Stopped: your mesh does not match the requirement for that script.')
    sys.exit

lx.out('End of SMO_RotatePoly_PreserveChild')

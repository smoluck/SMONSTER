#python
#---------------------------------------
# Name:         SMO_DIS_ItemColor.py
# Version:      1.0
#
# Purpose: This script is designed to
# Define a new item Color and set the Draw Option
# to the corresponding color.
#
# Author:       Franck ELISABETH
# Website:      http://www.smoluck.com
#
# Created:      28/12/2018
# Copyright:    (c) Franck Elisabeth 2017-2022
#---------------------------------------


import modo
scene = modo.scene.current()
items = scene.selectedByType(lx.symbol.sITYPE_MESH)


ItemListColor = 0
DrawOption = 0



################################
#<----[ DEFINE VARIABLES ]---->#
################################

#####--- Define user value for all the different SafetyCheck --- START ---#####
#####

## Vertex
lx.eval("user.defNew name:SMO_SafetyCheckIteCol_VertexModeEnabled type:integer life:momentary")

## Edges
lx.eval("user.defNew name:SMO_SafetyCheckIteCol_EdgeModeEnabled type:integer life:momentary")

## Polygon
lx.eval("user.defNew name:SMO_SafetyCheckIteCol_PolygonModeEnabled type:integer life:momentary")

## Item
lx.eval("user.defNew name:SMO_SafetyCheckIteCol_ItemModeEnabled type:integer life:momentary")

#####
#####--- Define user value for all the different SafetyCheck --- END ---#####



##############################
####### SAFETY CHECK 2 #######
##############################

#####--------------------  safety check 2: Component Selection Mode type --- START --------------------#####

selType = ""
# Used to query layerservice for the list of polygons, edges or vertices.
attrType = ""

if lx.eval1( "select.typeFrom typelist:vertex;polygon;edge;item;ptag ?" ):
    selType = "vertex"
    attrType = "vert"
    
    SMO_SafetyCheckIteCol_VertexModeEnabled = 1
    SMO_SafetyCheckIteCol_EdgeModeEnabled = 0
    SMO_SafetyCheckIteCol_PolygonModeEnabled = 0
    SMO_SafetyCheckIteCol_ItemModeEnabled = 0
    
    # x.out('script Running: Vertex Component Selection Mode')
    
    
elif lx.eval1( "select.typeFrom typelist:edge;vertex;polygon;item ?" ):
    selType = "edge"
    attrType = "edge"
    
    SMO_SafetyCheckIteCol_VertexModeEnabled = 0
    SMO_SafetyCheckIteCol_EdgeModeEnabled = 1
    SMO_SafetyCheckIteCol_PolygonModeEnabled = 0
    SMO_SafetyCheckIteCol_ItemModeEnabled = 0
    
    # lx.out('script Running: Edge Component Selection Mode')
    
elif lx.eval1( "select.typeFrom typelist:polygon;vertex;edge;item ?" ):
    selType = "polygon"
    attrType = "poly"
    
    SMO_SafetyCheckIteCol_VertexModeEnabled = 0
    SMO_SafetyCheckIteCol_EdgeModeEnabled = 0
    SMO_SafetyCheckIteCol_PolygonModeEnabled = 1
    SMO_SafetyCheckIteCol_ItemModeEnabled = 0
    
    # lx.out('script Running: Polygon Component Selection Mode')


else:
    # This only fails if none of the three supported selection
    # modes have yet been used since the program started, or
    # if "item" or "ptag" (ie: materials) is the current
    # selection mode.
    
    SMO_SafetyCheckIteCol_VertexModeEnabled = 0
    SMO_SafetyCheckIteCol_EdgeModeEnabled = 0
    SMO_SafetyCheckIteCol_PolygonModeEnabled = 0
    SMO_SafetyCheckIteCol_ItemModeEnabled = 1
    
    # lx.out('script Running: Item Component Selection Mode')

#####--------------------  safety check 2: Component Selection Mode type --- END --------------------#####


# lx.out('Start of SMO_DIS_ItemColor Script')


#####--------------------  Compare SafetyCheck value and decide or not to continue the process  --- START --------------------#####
if SMO_SafetyCheckIteCol_VertexModeEnabled == 1:
    lx.eval('select.type item')
    
if SMO_SafetyCheckIteCol_EdgeModeEnabled == 1:
    lx.eval('select.type item')
     
if SMO_SafetyCheckIteCol_PolygonModeEnabled == 1:
    lx.eval('select.type item')
    
if SMO_SafetyCheckIteCol_ItemModeEnabled == 1:
    lx.eval('select.type item')


##############################
## <----( Main Macro )----> ##
##############################

CycleValue = lx.eval('item.editorColor ?')
# lx.out('Current Item Color: ', CycleValue)

if ItemListColor == 0 :
    lx.eval('item.editorColor none')





# if ItemListColor == 1 :
    # item.editorColor ?



for item in items:
    if DrawOption == 0 :
        try:
            # add draw package
            lx.eval('!item.draw mode:add type:locator item:%s' % item.id)
            DrawPack = 0
            # lx.out('NO Draw Package:',DrawPack)
        except RuntimeError:
            # Item already has package
            DrawPack = 1
            pass
    if DrawPack == 1 :
        try:
            # add draw package
            lx.eval('item.draw rem locator')
        except RuntimeError:
            # Item alread has package
            pass

#####--------------------  Compare SafetyCheck value and decide or not to continue the process  --- START --------------------#####

# if ItemListColor == 0 :
    # try:
        # lx.eval('item.editorColor none')
    # except RuntimeError:
        # pass
    # if DrawPack == 1 :
        # try:
            # lx.eval('item.channel locator$fillOptions default')
            # lx.eval('item.channel locator$wireOptions default')
            # lx.eval('item.draw rem locator')
        # except RuntimeError:
            # pass
    # if DrawPack == 0 :
        # pass



if SMO_SafetyCheckIteCol_VertexModeEnabled == 1:
    lx.eval('select.type vertex')
    
if SMO_SafetyCheckIteCol_EdgeModeEnabled == 1:
    lx.eval('select.type edge')
     
if SMO_SafetyCheckIteCol_PolygonModeEnabled == 1:
    lx.eval('select.type polygone')
    
if SMO_SafetyCheckIteCol_ItemModeEnabled == 1:
    lx.eval('select.type item')

# lx.out('End of SMO_DIS_ItemColor Script')
#####--------------------  Compare TotalSafetyCheck value and decide or not to continue the process  --- END --------------------#####
#python
#---------------------------------------
# Name:         SMO_MOD_Quadruple_Via_GuideEdge.py
# Version:      1.0
#
# Purpose: This script will quadruple an Ngon base on a selection of 2 Edges Guide and the NGon polygon selection.
#
# Author:       Franck ELISABETH
# Website:      http://www.smoluck.com
#
# Created:      21/05/2019
# Copyright:    (c) Franck Elisabeth 2017-2022
#---------------------------------------

import modo

#####--------------------  safety check 1: Polygon Selection Mode enabled --- START --------------------#####

selType = ""
# Used to query layerservice for the list of polygons, edges or vertices.
attrType = ""

if lx.eval1( "select.typeFrom typelist:vertex;polygon;edge;item;ptag ?" ):
    selType = "vertex"
    attrType = "vert"
	
    SMO_SafetyCheck_EdgeModeEnabled = 0
    lx.eval('dialog.setup info')
    lx.eval('dialog.title {Quadruple_Via_GuideEdge:}')
    lx.eval('dialog.msg {You must be in Edge Mode to run that script}')
    lx.eval('+dialog.open')
    lx.out('script Stopped: You must be in Edge Mode to run that script')
    sys.exit
    
	
elif lx.eval1( "select.typeFrom typelist:edge;vertex;polygon;item ?" ):
	selType = "edge"
	attrType = "edge"
	
	SMO_SafetyCheck_EdgeModeEnabled = 1
	lx.out('script Running: Correct Component Selection Mode')
    
	
elif lx.eval1( "select.typeFrom typelist:polygon;vertex;edge;item ?" ):
	selType = "polygon"
	attrType = "poly"

	SMO_SafetyCheck_EdgeModeEnabled = 0
	lx.eval('dialog.setup info')
	lx.eval('dialog.title {Quadruple_Via_GuideEdge:}')
	lx.eval('dialog.msg {You must be in Edge Mode to run that script}')
	lx.eval('+dialog.open')
	lx.out('script Stopped: You must be in Edge Mode to run that script')
	sys.exit


else:
	# This only fails if none of the three supported selection
    # modes have yet been used since the program started, or
    # if "item" or "ptag" (ie: materials) is the current
    # selection mode.
    SMO_SafetyCheck_EdgeModeEnabled = 0
    lx.eval('dialog.setup info')
    lx.eval('dialog.title {Quadruple_Via_GuideEdge:}')
    lx.eval('dialog.msg {You must be in Edge Mode to run that script}')
    lx.eval('+dialog.open')
    lx.out('script Stopped: You must be in Edge Mode to run that script')
    sys.exit
	
#####--------------------  safety check 1: Edge Selection Mode enabled --- END --------------------#####

# Tag Current Selection
lx.eval('select.editSet EDGE_GUIDE add {}')

lx.eval('item.componentMode polygon true')
lx.eval('select.polygon add vertex b-spline 4')
lx.eval('hide.unsel')

# get back the polygon selection from those 2 Edges
lx.eval('item.componentMode edge true')
lx.eval('select.loop')
lx.eval('select.convert vertex')
lx.eval('select.convert polygon')
lx.eval('unhide')
lx.eval('select.editSet NGON add')

# Tag in Between Edges for Bridge
lx.eval('script.run "macro.scriptservice:92663570022:macro"')
lx.eval('select.useSet EDGE_GUIDE deselect')
lx.eval('select.editSet EDGE_BRIDGE add {}')
lx.eval('item.componentMode polygon true')
lx.eval('!delete')
lx.eval('item.componentMode edge true')
lx.eval('tool.set edge.bridge on')
lx.eval('tool.attr edge.bridge mode linear')
lx.eval('tool.attr edge.bridge segments 1')
lx.eval('tool.attr edge.bridge segments 0')
lx.eval('tool.attr edge.bridge connect false')
lx.eval('tool.setAttr edge.bridge segments 0')
lx.eval('tool.doApply')

# Delete the Temp Selection Set
lx.eval('!select.deleteSet EDGE_BRIDGE')
lx.eval('!select.deleteSet EDGE_GUIDE false')
lx.eval('select.drop edge')
lx.eval('item.componentMode polygon true')
lx.eval('select.drop polygon')
lx.eval('item.componentMode edge true')

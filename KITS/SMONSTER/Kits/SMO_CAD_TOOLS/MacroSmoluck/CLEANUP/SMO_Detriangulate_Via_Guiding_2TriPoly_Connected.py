# python
"""
# Name:         SMO_Detriangulate_Via_Guiding_2TriPoly_Connected.py
# Version:      1.0
#
# Purpose:      This script is designed to:
#               Detriangulate the current mesh item by
#               using 2 triangles as guide.
#
# Author:       Franck ELISABETH
# Website:      https://www.smoluck.com
#
# Created:      22/01/2020
# Copyright:    (c) Franck Elisabeth 2017-2022
"""

import lx
import modo
import sys

scene = modo.scene.current()

# -------------------------- #
# <---( SAFETY CHECK 1 )---> #
# -------------------------- #
lx.eval("user.defNew name:SMO_SafetyCheck_Only1MeshItemSelected type:integer life:momentary")
# --------------------  safety check 1 : Only One Item Selected --- START
ItemCount = lx.eval('query layerservice layer.N ? fg')
lx.out('Selected Item count:', ItemCount)

if ItemCount != 1:
	SMO_SafetyCheck_Only1MeshItemSelected = 0
	lx.eval('dialog.setup info')
	lx.eval('dialog.title {SMO Detriangulate via guide 2 Tri Poly:}')
	lx.eval('dialog.msg {You must only select the Mesh Item layer you are working on, in Item List, to run that script}')
	lx.eval('+dialog.open')
	lx.out('Only One Item Selected result:', SMO_SafetyCheck_Only1MeshItemSelected)
	lx.out('script Stopped: Select only one Mesh Item')
	sys.exit

else:
	SMO_SafetyCheck_Only1MeshItemSelected = 1
	lx.out('Only One Item Selected:', SMO_SafetyCheck_Only1MeshItemSelected)
	lx.out('script running: right amount of Mesh Item selected')
# --------------------  safety check 1 : Only One Item Selected --- END


mesh = scene.selectedByType('mesh')[0]


# -------------------------- #
# <---( SAFETY CHECK 2 )---> #
# -------------------------- #
lx.eval("user.defNew name:SMO_SafetyCheck_PolygonModeEnabled type:integer life:momentary")
# Polygon Selection Mode enabled --- START
selType = ""
# Used to query layerservice for the list of polygons, edges or vertices.
attrType = ""

if lx.eval1( "select.typeFrom typelist:vertex;polygon;edge;item;ptag ?" ):
	selType = "vertex"
	attrType = "vert"

	SMO_SafetyCheck_PolygonModeEnabled = 0
	lx.eval('dialog.setup info')
	lx.eval('dialog.title {SMO Detriangulate via guide 2 Tri Poly:}')
	lx.eval('dialog.msg {You must be in Polygon Mode to run that script}')
	lx.eval('+dialog.open')
	lx.out('script Stopped: You must be in Polygon Mode to run that script')
	sys.exit


elif lx.eval1( "select.typeFrom typelist:edge;vertex;polygon;item ?" ):
	selType = "edge"
	attrType = "edge"

	SMO_SafetyCheck_PolygonModeEnabled = 0
	lx.eval('dialog.setup info')
	lx.eval('dialog.title {SMO Detriangulate via guide 2 Tri Poly:}')
	lx.eval('dialog.msg {You must be in Polygon Mode to run that script}')
	lx.eval('+dialog.open')
	lx.out('script Stopped: You must be in Polygon Mode to run that script')
	sys.exit

elif lx.eval1( "select.typeFrom typelist:polygon;vertex;edge;item ?" ):
	selType = "polygon"
	attrType = "poly"

	SMO_SafetyCheck_PolygonModeEnabled = 1
	lx.out('script Running: Correct Component Selection Mode')


else:
	# This only fails if none of the three supported selection
	# modes have yet been used since the program started, or
	# if "item" or "ptag" (ie: materials) is the current
	# selection mode.
	SMO_SafetyCheck_PolygonModeEnabled = 0
	lx.eval('dialog.setup info')
	lx.eval('dialog.title {SMO Detriangulate via guide 2 Tri Poly:}')
	lx.eval('dialog.msg {You must be in Polygon Mode to run that script}')
	lx.eval('+dialog.open')
	lx.out('script Stopped: You must be in Polygon Mode to run that script')
	sys.exit
# Polygon Selection Mode enabled --- END




if SMO_SafetyCheck_Only1MeshItemSelected == 1 and SMO_SafetyCheck_PolygonModeEnabled == 1 :
	lx.eval('select.editSet dgsgdsg add')
	lx.eval('select.connect')
	lx.eval('hide.unsel')
	lx.eval('select.drop polygon')
	lx.eval('select.useSet dgsgdsg select')
	lx.eval('script.run "macro.scriptservice:92663570022:macro"')
	lx.eval('select.nextMode')
	lx.eval('select.convert edge')
	lx.eval('select.contract')
	lx.eval('select.edge remove bond equal (none)')
	lx.eval('!!delete')
	lx.eval('select.nextMode')
	lx.eval('select.invert')
	lx.eval('tool.set detriangulate.meshop on')
	lx.eval('tool.setAttr detriangulate.meshop flatness 0.205')
	lx.eval('tool.doApply')
	lx.eval('select.nextMode')
	lx.eval('select.drop polygon')
	lx.eval('unhide')
	lx.eval('!select.deleteSet dgsgdsg')
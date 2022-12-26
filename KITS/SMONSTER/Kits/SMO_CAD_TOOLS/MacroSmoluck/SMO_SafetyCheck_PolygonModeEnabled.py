# python
"""
# Name:         SMO_SafetyCheck_PolygonModeEnabled
# Version: 1.0
#
# Purpose: This script is designed to test if the Polygon Selection Mode is enabled
#
# Author:       Franck ELISABETH
# Website:      https://www.smoluck.com
#
# Created:      27/12/2018
# Copyright:    (c) Franck Elisabeth 2017-2022
"""

import modo
import lx
import sys

scene = modo.scene.current()
mesh = scene.selectedByType('mesh')[0]

# --------------------  safety check: Polygon Selection Mode enabled --- START

selType = ""
# Used to query layerservice for the list of polygons, edges or vertices.
attrType = ""

if lx.eval1( "select.typeFrom typelist:vertex;polygon;edge;item;ptag ?" ):
	selType = "vertex"
	attrType = "vert"
	
	SMO_SafetyCheck_PolygonModeEnabled = 0
	lx.eval('dialog.setup info')
	lx.eval('dialog.title {SMO SafetyCheck Polygon Mode Enabled:}')
	lx.eval('dialog.msg {You must be in Polygon Mode to run that script}')
	lx.eval('+dialog.open')
	lx.out('script Stopped: You must be in Polygon Mode to run that script')
	sys.exit
	#sys.exit( "LXe_FAILED:Must be in polygon selection mode." )

	
elif lx.eval1( "select.typeFrom typelist:edge;vertex;polygon;item ?" ):
	selType = "edge"
	attrType = "edge"
	
	SMO_SafetyCheck_PolygonModeEnabled = 0
	lx.eval('dialog.setup info')
	lx.eval('dialog.title {SMO SafetyCheck Polygon Mode Enabled::}')
	lx.eval('dialog.msg {You must be in Polygon Mode to run that script}')
	lx.eval('+dialog.open')
	lx.out('script Stopped: You must be in Polygon Mode to run that script')
	sys.exit
	#sys.exit( "LXe_FAILED:Must be in polygon selection mode." )
	
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
	lx.eval('dialog.title {SMO SafetyCheck Polygon Mode Enabled::}')
	lx.eval('dialog.msg {You must be in Polygon Mode to run that script}')
	lx.eval('+dialog.open')
	lx.out('script Stopped: You must be in Polygon Mode to run that script')
	sys.exit
	#sys.exit( "LXe_FAILED:Must be in polygon selection mode." )
# --------------------  safety check: Polygon Selection Mode enabled --- END
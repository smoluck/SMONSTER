#python
#---------------------------------------
# Name:         SMO_SafetyCheck_min3PolygonSelected
# Version: 1.0
#
# Purpose: This script is designed to test if at Least 3 Polygons are selected
#
# Author:       Franck ELISABETH
# Website:      http://www.smoluck.com
#
# Created:      27/12/2018
# Copyright:    (c) Franck Elisabeth 2017-2022
#---------------------------------------
import modo

scene = modo.scene.current()
mesh = scene.selectedByType('mesh')[0]

#####--------------------  safety check: at Least 3 Polygons are selected --- START --------------------#####
CsPolys = len(mesh.geometry.polygons.selected)
lx.out('Count Selected Poly', CsPolys)

if CsPolys <= 2:
	SMO_SafetyCheck_min3PolygonSelected = 0
	lx.eval('dialog.setup info')
	lx.eval('dialog.title {SMO SafetyCheck min 3 Polygon Selected:}')
	lx.eval('dialog.msg {You must select more than 2 polygons selected to run that script}')
	lx.eval('+dialog.open')
	lx.out('script Stopped: Add more polygons to your selection')
	sys.exit

elif CsPolys >= 3:
	SMO_SafetyCheck_min3PolygonSelected = 1
	lx.out('script running: right amount of polygons in selection')
#####--------------------  safety check: at Least 3 Polygons are selected --- END --------------------#####
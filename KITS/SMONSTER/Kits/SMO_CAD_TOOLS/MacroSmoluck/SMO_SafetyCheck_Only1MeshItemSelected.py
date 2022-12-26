# python
"""
# Name:         SMO_SafetyCheck_Only1MeshItemSelected
# Version: 1.0
#
# Purpose: This script is designed to test if only one Mesh Item is selected
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

# --------------------  safety check: Only One Item Selected --- START
ItemCount = lx.eval('query layerservice layer.N ? fg')
lx.out('Selected Item count:', ItemCount)

if ItemCount != 1:
	SMO_SafetyCheck_Only1MeshItemSelected = 0
	lx.eval('dialog.setup info')
	lx.eval('dialog.title {SMO SafetyCheck Only 1 Mesh Item Selected:}')
	lx.eval('dialog.msg {You must only select the Mesh Item layer you are working on, in Item List, to run that script}')
	lx.eval('+dialog.open')
	lx.out('Only One Item Selected result:', SMO_SafetyCheck_Only1MeshItemSelected)
	lx.out('script Stopped: Select only one Mesh Item')
	sys.exit
	
else:
	SMO_SafetyCheck_Only1MeshItemSelected = 1
	lx.out('Only One Item Selected:', SMO_SafetyCheck_Only1MeshItemSelected)
	lx.out('script running: right amount of Mesh Item selected')
# --------------------  safety check: Only One Item Selected --- END
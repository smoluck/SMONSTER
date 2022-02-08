#python
#---------------------------------------
# Name:         SMO_MOD_FallOff_Mode.py
# Version: 1.0
#
# Purpose: This script is designed to
# set automaticly a defined Falloff
#
# Author:       Franck ELISABETH
# Website:      http://www.smoluck.com
#
# Created:      16/09/2019
# Copyright:    (c) Franck Elisabeth 2017-2022
#---------------------------------------

import modo
# scene = modo.scene.current()
# mesh = scene.selectedByType('mesh')[0]
# CsPolys = len(mesh.geometry.polygons.selected)
# SelItems = (lx.evalN('query sceneservice selection ? locator'))
# lx.out('In Selected items, List of their Unique Name is:',SelItems)

#FallOff_Mode = 0
################################
#<----[ DEFINE ARGUMENTS ]---->#
################################
args = lx.args()
lx.out(args)

FallOff_Mode = args[0]                      # Falloff mode:                         Linear = 0 / Cylinder = 1 / Radial = 2
# Expose the Result of the Arguments 
lx.out(FallOff_Mode)
################################
#<----[ DEFINE ARGUMENTS ]---->#
################################

lx.eval('tool.set actr.auto on')
FallOff_Status = lx.eval('falloff.state ?')
if FallOff_Status == 0:
	lx.eval('tool.set falloff.linear ?+')
else:
	lx.out('FallOff Enabled')
	

if FallOff_Status == 1:
	lx.eval('tool.clearTask falloff')
	lx.eval('tool.set falloff.linear ?+')
	lx.out("FallOff already active")
else:
	lx.out('FallOff Enabled')



if FallOff_Mode == 0:
    lx.eval('tool.set falloff.linear on')
if FallOff_Mode == 1:
    lx.eval('tool.set falloff.cylinder on')


# CALLING the FALLOFF DECAY SHAPE Pie Menu
# lx.eval('attr.formPopover {SMO_FALLOFF_DecayShape_Pie_SH:sheet}')
# CALLING the FALLOFF DECAY SHAPE Pie Menu
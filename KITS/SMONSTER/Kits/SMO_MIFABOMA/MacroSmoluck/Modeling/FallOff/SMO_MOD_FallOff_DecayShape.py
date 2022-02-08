#python
#---------------------------------------
# Name:         SMO_MOD_FallOff_DecayShape.py
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

#Decay_Shape = 0
################################
#<----[ DEFINE ARGUMENTS ]---->#
################################
args = lx.args()
lx.out(args)

Decay_Shape = args[0]                       # Decay Shape:                          Linear = 0 / EaseIn = 1 / EaseOut = 2 / Smooth = 3
# Expose the Result of the Arguments 
lx.out(Decay_Shape)
################################
#<----[ DEFINE ARGUMENTS ]---->#
################################

## <----( Linear FallOff )----> ##
if lx.eval('tool.set falloff.linear ? ') == 'on':
    # lx.eval('tool.set falloff.linear on')
    FallOff_Mode = 0
    ## Linear <----(Decay shape)----> ##
    if FallOff_Mode == 0 and Decay_Shape == 0:
        lx.eval('tool.setAttr falloff.linear shape linear')
    if FallOff_Mode == 0 and Decay_Shape == 1:
        lx.eval('tool.setAttr falloff.linear shape easeIn')
    if FallOff_Mode == 0 and Decay_Shape == 2:
        lx.eval('tool.setAttr falloff.linear shape easeOut')
    if FallOff_Mode == 0 and Decay_Shape == 3:
        lx.eval('tool.setAttr falloff.linear shape smooth')
    lx.eval('tool.doApply')
    # CALLING the FALLOFF SYMMETRY Pie Menu
    # lx.eval('attr.formPopover {SMO_FALLOFF_Sym_Pie_SH:sheet}')
    # CALLING the FALLOFF SYMMETRY Pie Menu

## <----( Cylinder FallOff )----> ##
if lx.eval('tool.set falloff.cylinder ? ') == 'on':
    # lx.eval('tool.set falloff.cylinder on')
    FallOff_Mode = 1
    ## Cylinder <----(Decay shape)----> ##
    if FallOff_Mode == 1 and Decay_Shape == 0:
        lx.eval('tool.setAttr falloff.cylinder shape linear')
    if FallOff_Mode == 1 and Decay_Shape == 1:
        lx.eval('tool.setAttr falloff.cylinder shape easeIn')
    if FallOff_Mode == 1 and Decay_Shape == 2:
        lx.eval('tool.setAttr falloff.cylinder shape easeOut')
    if FallOff_Mode == 1 and Decay_Shape == 3:
        lx.eval('tool.setAttr falloff.cylinder shape smooth')
    lx.eval('tool.doApply')




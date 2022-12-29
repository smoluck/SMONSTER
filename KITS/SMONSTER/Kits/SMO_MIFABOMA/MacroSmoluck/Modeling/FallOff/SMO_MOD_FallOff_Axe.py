# python
"""
Name:           SMO_MOD_FallOff_Axe.py

Purpose:        This script is designed to:
                Set automatically a defined Falloff

Author:         Franck ELISABETH
Website:        https://www.smoluck.com
Created:        16/09/2019
Copyright:      (c) Franck Elisabeth 2017-2022
"""

import lx

# scene = modo.scene.current()
# mesh = scene.selectedByType('mesh')[0]
# CsPolys = len(mesh.geometry.polygons.selected)
# SelItems = (lx.evalN('query sceneservice selection ? locator'))
# lx.out('In Selected items, List of their Unique Name is:',SelItems)

# Auto_AXES = 0
# ------------------------------ #
# <----( DEFINE ARGUMENTS )----> #
# ------------------------------ #
args = lx.args()
lx.out(args)

Auto_AXES = args[0]     # Axes selection:       X = 0 / Y = 1 / Z = 2
# Expose the Result of the Arguments 
lx.out(Auto_AXES)
# ------------------------------ #
# <----( DEFINE ARGUMENTS )----> #
# ------------------------------ #

# <----( Linear FallOff )----> #
if lx.eval('tool.set falloff.linear ? ') == 'on':
    lx.eval('tool.set falloff.linear on')
    FallOff_Mode = 0
    if Auto_AXES == 0:
        lx.out('Mirror on X')
        lx.eval('falloff.axisAutoSize axis:0')
        lx.eval('falloff.autoSize')
    if Auto_AXES == 1:
        lx.out('Mirror on Y')
        lx.eval('falloff.axisAutoSize axis:1')
        lx.eval('falloff.autoSize')
    if Auto_AXES == 2:
        lx.out('Mirror on Z')
        lx.eval('falloff.axisAutoSize axis:2')
        lx.eval('falloff.autoSize')

# <----( Cylinder FallOff )----> #
if lx.eval('tool.set falloff.cylinder ? ') == 'on':
    lx.eval('tool.set falloff.cylinder on')
    FallOff_Mode = 1
    if FallOff_Mode == 1 and Auto_AXES == 0:
        lx.eval('falloff.autoSize')
        lx.eval('tool.setAttr falloff.cylinder axis 0')
    if FallOff_Mode == 1 and Auto_AXES == 1:
        lx.eval('falloff.autoSize')
        lx.eval('tool.setAttr falloff.cylinder axis 1')
    if FallOff_Mode == 1 and Auto_AXES == 2:
        lx.eval('falloff.autoSize')
        lx.eval('tool.setAttr falloff.cylinder axis 2')

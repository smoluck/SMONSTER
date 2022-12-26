# python
"""
# Name:         SMO_MOD_FallOff_Sym.py
# Version: 1.0
#
# Purpose: This script is designed to
# set automaticly a defined Falloff
#
# Author:       Franck ELISABETH
# Website:      https://www.smoluck.com
#
# Created:      16/09/2019
# Copyright:    (c) Franck Elisabeth 2017-2022
"""

import modo
# scene = modo.scene.current()
# mesh = scene.selectedByType('mesh')[0]
# CsPolys = len(mesh.geometry.polygons.selected)
# SelItems = (lx.evalN('query sceneservice selection ? locator'))
# lx.out('In Selected items, List of their Unique Name is:',SelItems)

Sym_Mode = 2
# ------------------------------ #
# <----( DEFINE ARGUMENTS )----> #
# ------------------------------ #
# args = lx.args()
# lx.out(args)

# Sym_Mode = args[0]                          # Symmetry mode:                        None = 0 ### Start = 1 ### End = 2
# # Expose the Result of the Arguments 
# lx.out(Sym_Mode)
# ------------------------------ #
# <----( DEFINE ARGUMENTS )----> #
# ------------------------------ #


# <----( Linear FallOff )----> #
if lx.eval('tool.set falloff.linear ? ') == 'on':
    # lx.eval('tool.set falloff.linear on')
    FallOff_Mode = 0
    ## Linear <----( Symetry Mode )----> #
    if Sym_Mode == 0:
        lx.eval('tool.setAttr falloff.linear symmetric none')
    if Sym_Mode == 1:
        lx.eval('tool.setAttr falloff.linear symmetric start')
    if Sym_Mode == 2:
        lx.eval('tool.setAttr falloff.linear symmetric end')
    lx.eval('tool.doApply')
    # CALLING the FALLOFF AXES Pie Menu
    # lx.eval('attr.formPopover {SMO_FALLOFF_Axes_Pie_SH:sheet}')
    # CALLING the FALLOFF AXES Pie Menu

# <----( Cylinder FallOff )----> #
if lx.eval('tool.set falloff.cylinder ? ') == 'on':
    # lx.eval('tool.set falloff.cylinder on')
    FallOff_Mode = 1
    ## Cylinder <----( Symetry Mode )----> #
    if Sym_Mode == 0:
        lx.eval('tool.setAttr falloff.cylinder symmetric none')
    if Sym_Mode == 1:
        lx.eval('tool.setAttr falloff.cylinder symmetric start')
    if Sym_Mode == 2:
        lx.eval('tool.setAttr falloff.cylinder symmetric end')
    lx.eval('tool.doApply')
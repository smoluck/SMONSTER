#python
#---------------------------------------
# Name:         SMO_MOD_MirrorZ.py
# Version: 1.0
#
# Purpose: This script is designed to
# Mirror the last Polygon Selection
# from the current Layer on Axis Z.
#
# Author:       Franck ELISABETH
# Website:      http://www.smoluck.com
#
# Created:      16/09/2019
# Copyright:    (c) Franck Elisabeth 2017-2022
#---------------------------------------

import modo
scene = modo.scene.current()
mesh = scene.selectedByType('mesh')[0]
CsPolys = len(mesh.geometry.polygons.selected)
SelItems = (lx.evalN('query sceneservice selection ? locator'))
lx.out('In Selected items, List of their Unique Name is:',SelItems)
MIRROR_AXES = 2


lx.eval('tool.set actr.auto on 0')
lx.eval('select.type item')
lx.eval('item.refSystem %s' % SelItems)
lx.eval('tool.set actr.origin on')
lx.eval('select.type polygon')
lx.eval('tool.set *.mirror on')

##############################
## <----( Main Command )----> 
##############################

#Command Block Begin:  ToolAdjustment
lx.eval('tool.setAttr gen.mirror frot axis')
lx.eval('tool.setAttr gen.mirror cenX 0.0')
lx.eval('tool.setAttr gen.mirror cenY 0.0')
lx.eval('tool.setAttr gen.mirror cenZ 0.0')
if MIRROR_AXES == 0:
    lx.out('Mirror on X')
    lx.eval('tool.setAttr gen.mirror axis 0')
    lx.eval('tool.setAttr gen.mirror leftX 0.0')
    lx.eval('tool.setAttr gen.mirror leftY 1')
    lx.eval('tool.setAttr gen.mirror leftZ 0.0')
    lx.eval('tool.setAttr gen.mirror upX 0.0')
    lx.eval('tool.setAttr gen.mirror upY 0.0')
    lx.eval('tool.setAttr gen.mirror upZ 1')
if MIRROR_AXES == 1:
    lx.out('Mirror on Y')
    lx.eval('tool.setAttr gen.mirror axis 1')
    lx.eval('tool.setAttr gen.mirror leftX 0.0')
    lx.eval('tool.setAttr gen.mirror leftY 0.0')
    lx.eval('tool.setAttr gen.mirror leftZ 1')
    lx.eval('tool.setAttr gen.mirror upX 1')
    lx.eval('tool.setAttr gen.mirror upY 0.0')
    lx.eval('tool.setAttr gen.mirror upZ 0.0')
if MIRROR_AXES == 2:
    lx.out('Mirror on Z')
    lx.eval('tool.setAttr gen.mirror axis 2')
    lx.eval('tool.setAttr gen.mirror leftX 1')
    lx.eval('tool.setAttr gen.mirror leftY 0.0')
    lx.eval('tool.setAttr gen.mirror leftZ 0.0')
    lx.eval('tool.setAttr gen.mirror upX 0.0')
    lx.eval('tool.setAttr gen.mirror upY 1')
    lx.eval('tool.setAttr gen.mirror upZ 0.0')
#Command Block End:  ToolAdjustment

##############################
## <----( Main Command )----> 
##############################

lx.eval('tool.doApply')
lx.eval('select.nextMode')
lx.eval('select.drop polygon')
lx.eval('item.refSystem {}')
lx.eval('tool.set actr.auto on 0')
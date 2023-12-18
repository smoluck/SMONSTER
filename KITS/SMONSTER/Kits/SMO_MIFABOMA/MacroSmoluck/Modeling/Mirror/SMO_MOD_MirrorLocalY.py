# python
"""
Name:               SMO_MOD_MirrorLocalY.py

Purpose:            This Script is designed to:
                    Mirror the last Polygon Selection
                    from the current Layer on a defined Axis.

Author:             Franck ELISABETH
Website:            https://www.linkedin.com/in/smoluck/
Created:            16/09/2019
Copyright:          (c) Franck Elisabeth 2017-2022
"""

import lx
import modo

scene = modo.scene.current()
mesh = scene.selectedByType('mesh')[0]
CsPolys = len(mesh.geometry.polygons.selected)
SelItems = (lx.evalN('query sceneservice selection ? locator'))
lx.out('Selected items is:', SelItems)

# ------------------------------ #
# <----( DEFINE VARIABLES )----> #
# ------------------------------ #

# ---------------- Define user value for all the different SafetyCheck --- START
lx.eval("user.defNew name:SMO_SafetyCheck_PolygonModeEnabled type:integer life:momentary")
lx.eval("user.defNew name:SMO_SafetyCheck_min1PolygonSelected type:integer life:momentary")
# ---------------- Define user value for all the different SafetyCheck --- END


MIRROR_AXES = 1
# ------------------------------ #
# <----( DEFINE ARGUMENTS )----> #
# ------------------------------ #
# args = lx.args()
# lx.out(args)
# MIRROR_AXES = args[0]             # Axes selection:               X = 0 ### Y = 1 ### Z = 2
# Expose the Result of the Arguments 
# lx.out(MIRROR_AXES)
# ------------------------------ #
# <----( DEFINE ARGUMENTS )----> #
# ------------------------------ #

lx.eval('tool.set actr.auto on 0')
lx.eval('select.type item')
lx.eval('item.refSystem %s' % SelItems)
lx.eval('tool.set actr.origin on')
lx.eval('select.type polygon')
lx.eval('tool.set *.mirror on')

# -------------------------- #
# <----( Main Command )----> #
# -------------------------- #

# Command Block Begin:  ToolAdjustment5
lx.eval('tool.setAttr gen.mirror cenX 0.0')
lx.eval('tool.setAttr gen.mirror cenY 0.0')
lx.eval('tool.setAttr gen.mirror cenZ 0.0')
if MIRROR_AXES == 0:
    lx.eval('tool.setAttr gen.mirror axis 0')
    lx.eval('tool.setAttr gen.mirror leftX 0.0')
    lx.eval('tool.setAttr gen.mirror leftY 1')
    lx.eval('tool.setAttr gen.mirror leftZ 0.0')
    lx.eval('tool.setAttr gen.mirror upX 0.0')
    lx.eval('tool.setAttr gen.mirror upY 0.0')
    lx.eval('tool.setAttr gen.mirror upZ 1')
if MIRROR_AXES == 1:
    lx.eval('tool.setAttr gen.mirror axis 1')
    lx.eval('tool.setAttr gen.mirror leftX 0.0')
    lx.eval('tool.setAttr gen.mirror leftY 0.0')
    lx.eval('tool.setAttr gen.mirror leftZ 1')
    lx.eval('tool.setAttr gen.mirror upX 1')
    lx.eval('tool.setAttr gen.mirror upY 0.0')
    lx.eval('tool.setAttr gen.mirror upZ 0.0')
if MIRROR_AXES == 2:
    lx.eval('tool.setAttr gen.mirror axis 2')
    lx.eval('tool.setAttr gen.mirror leftX 1')
    lx.eval('tool.setAttr gen.mirror leftY 0.0')
    lx.eval('tool.setAttr gen.mirror leftZ 0.0')
    lx.eval('tool.setAttr gen.mirror upX 0.0')
    lx.eval('tool.setAttr gen.mirror upY 1')
    lx.eval('tool.setAttr gen.mirror upZ 0.0')
# Command Block End:  ToolAdjustment

# -------------------------- #
# <----( Main Command )----> #
# -------------------------- #

lx.eval('tool.doApply')
lx.eval('select.nextMode')
lx.eval('select.drop polygon')
lx.eval('item.refSystem {}')
lx.eval('tool.set actr.auto on 0')

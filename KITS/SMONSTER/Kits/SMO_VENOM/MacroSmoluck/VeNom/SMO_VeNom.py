# python
"""
Name:         SMO_Venom.py

Purpose:      This script is designed to:

Author:       Franck ELISABETH
Website:      https://www.linkedin.com/in/smoluck/

Created:      01/04/2020
Copyright:    (c) Franck Elisabeth 2017-2022
"""

import lx
import modo

# itemId = lx.eval('query view3dservice element.over ? ITEM')

# if itemId is None:
# lx.out('Mouse is not over any items.')
# return

# scene = modo.Scene()
# item = scene.item(itemId)

# p = lx.eval('query view3dservice element.over ? POLY')

# if p is None:
# We're over a mesh but it's not active one so poly query returns None.
# scene.select(item)
# p = lx.eval('query view3dservice element.over ? POLY')

# if p is None:
# lx.out('Cannot find polygon under the mouse.')
# return

# if not isinstance(p, tuple):
# p = [p]
# pIndex = int(p[0].split(',')[1])

# lx.out('Polygon under mouse: %s - %d' % (item.name, pIndex))


lx.eval('select.type polygon')

lx.eval('query view3dservice mouse ?')
view_under_mouse = lx.eval('query view3dservice mouse.view ?')
lx.eval('query view3dservice view.index ? %s' % view_under_mouse)
lx.eval('query view3dservice mouse.pos ?')
Item_under_mouse = lx.eval('query view3dservice element.over ? ITEM ')
Poly_under_mouse = lx.eval('query view3dservice element.over ? POLY ')
# edge_under_mouse = lx.eval('query view3dservice element.over ? EDGE ')
hitpos = lx.eval('query view3dservice mouse.hitpos ?')

lx.out(view_under_mouse)
lx.out(Item_under_mouse)
lx.out(Poly_under_mouse)
lx.out(hitpos)

lx.eval('select.drop polygon')
# lx.eval('materials.underMouse')

success = True
try:
    lx.eval('select.3DElementUnderMouse')
except:
    success = False
scene = modo.Scene()
items = scene.selected
lx.out(items)

Modo_ver = int(lx.eval('query platformservice appversion ?'))
# lx.out('Modo Version:', Modo_ver)

if success:
    # if Modo_ver < 1400:
    lx.eval('select.type polygon')
    lx.eval('smo.GC.SelectCoPlanarPoly 0 2 0')
    lx.eval('workPlane.fitSelect')
    lx.eval('select.editSet SelSet_VeNomTargetPoly add {}')
    lx.eval('select.type item')
    lx.eval('select.editSet SelSet_VeNomTarget add {}')
    lx.eval('select.type polygon')
    lx.eval('select.connect')
    lx.eval('cut')
    lx.eval('layer.new')
    lx.eval('select.type item')
    lx.eval('select.editSet SelSet_VeNomTempLayer add {}')  # Unparent maybe needed
    lx.eval('select.type polygon')
    lx.eval('paste')
    lx.eval('select.drop polygon')
    lx.eval('select.useSet SelSet_VeNomTargetPoly select')
    lx.eval('select.convert vertex')
    lx.eval('select.editSet SelSet_VeNomTargetVertex add {}')
    lx.eval('select.type item')
    lx.eval('layer.new')
    lx.eval('select.editSet SelSet_VeNomBG add {}')

    lx.eval('select.useSet SelSet_VeNomTempLayer select')
    lx.eval('hide.unsel')
    lx.eval('select.useSet SelSet_VeNomTempLayer deselect')
    lx.eval('tool.set prim.cube on')
    lx.eval('tool.attr prim.cube cenX 0.0')
    lx.eval('tool.attr prim.cube cenY 0.0')
    lx.eval('tool.attr prim.cube cenZ 0.0')
    lx.eval('tool.attr prim.cube sizeX 1.0')
    lx.eval('tool.attr prim.cube sizeY 0.0')
    lx.eval('tool.attr prim.cube sizeZ 1.0')
    lx.eval('tool.attr prim.cube axis y')
    lx.eval('tool.apply')
    lx.eval('tool.set prim.cube off 0')
    lx.eval('tool.clearTask snap')
    lx.eval('vertMap.normals "Vertex Normal"')
    lx.eval('select.drop item')
    lx.eval('select.useSet SelSet_VeNomTempLayer select')
    lx.eval('select.type vertex')
    lx.eval('select.useSet SelSet_VeNomTargetVertex select')
    lx.eval('vertMap.transferNormals true')
    lx.eval('select.drop vertex')
    lx.eval('select.type polygon')
    lx.eval('select.all')
    lx.eval('cut')

    lx.eval('select.type item')
    lx.eval('select.drop item')
    lx.eval('select.useSet SelSet_VeNomTarget select')
    lx.eval('select.type polygon')
    lx.eval('paste')
    lx.eval('select.type vertex')
    try:
        lx.eval('!select.deleteSet SelSet_VeNomTargetVertex false')
    except:
        pass
    lx.eval('select.type polygon')
    lx.eval('workPlane.state false')
    lx.eval('select.type item')
    lx.eval('unhide')
    lx.eval('select.drop item')
    lx.eval('select.useSet SelSet_VeNomTempLayer select')
    lx.eval('select.useSet SelSet_VeNomBG select')

    try:
        lx.eval('!select.deleteSet SelSet_VeNomBG')
    except:
        pass

    try:
        lx.eval('!select.deleteSet SelSet_VeNomTempLayer false')
    except:
        pass

    lx.eval('!delete')
    lx.eval('select.useSet SelSet_VeNomTarget select')
    try:
        lx.eval('!select.deleteSet SelSet_VeNomTarget false')
    except:
        pass
    lx.eval('select.type polygon')
    try:
        lx.eval('!select.deleteSet SelSet_VeNomTargetPoly false')
    except:
        pass
    lx.eval('select.type item')

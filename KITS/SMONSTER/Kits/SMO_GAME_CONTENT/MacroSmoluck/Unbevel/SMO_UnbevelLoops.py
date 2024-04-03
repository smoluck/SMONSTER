# python
import modo

lx.eval('select.type edge')

lx.eval('query view3dservice mouse ?')
view_under_mouse = lx.eval('query view3dservice mouse.view ?')
lx.eval('query view3dservice view.index ? %s' % view_under_mouse)
lx.eval('query view3dservice mouse.pos ?')
# poly_under_mouse = lx.eval('query view3dservice element.over ? POLY ')
edge_under_mouse = lx.eval('query view3dservice element.over ? EDGE ')
hitpos = lx.eval('query view3dservice mouse.hitpos ?') 

lx.out(view_under_mouse)
# lx.out(poly_under_mouse)
lx.out(edge_under_mouse)
lx.out(hitpos)


lx.eval('select.drop edge')
# lx.eval('materials.underMouse')

success = True
try:
    lx.eval('select.3DElementUnderMouse')
except:
    success = False
scene = modo.Scene()
items = scene.selected
lx.out(items)

Modo_ver = int(lx.eval ('query platformservice appversion ?'))
# lx.out('Modo Version:',Modo_ver)


if success:
    if Modo_ver < 1400:
        lx.eval('select.editSet UnbevelEdgeGuide add {}')
        lx.eval('select.type polygon')
        lx.eval('select.convert edge')
        lx.eval('select.invert')
        lx.eval('select.editSet UnbevelNoEdgeRing add {}')
        lx.eval('select.type polygon')
        
        
        
        lx.eval('select.editSet UnbevelPolyZone add {}')
        lx.eval('select.expand')
        lx.eval('select.useSet UnbevelPolyZone deselect')
        lx.eval('select.editSet UnbevelPolyBorder add {}')
        lx.eval('select.useSet UnbevelPolyZone replace')
        lx.eval('select.useSet UnbevelPolyBorder select')
        lx.eval('select.type polygon')
        lx.eval('select.polygon remove vertex curve 4')
        lx.eval('select.editSet UnbevelPolyBorder remove')
        lx.eval('select.drop polygon')
        lx.eval('select.useSet UnbevelPolyZone replace')
        lx.eval('select.useSet UnbevelPolyBorder select')
        
        
        
        lx.eval('hide.unsel')
        lx.eval('select.type edge')
        lx.eval('select.drop edge')
        lx.eval('select.useSet UnbevelEdgeGuide replace')
        lx.eval('select.edgeLoop base false m3d middle')
        lx.eval('select.ring')
        lx.eval('unhide')
        lx.eval('@unbevel.pl')
        
        
        
        lx.eval('select.drop edge')
        lx.eval('select.type polygon')
        lx.eval('select.drop polygon')
        
        
        lx.eval('select.type edge')
        lx.eval('!select.deleteSet UnbevelEdgeRing')
        lx.eval('!select.deleteSet UnbevelEdgeGuide')
        lx.eval('!select.deleteSet UnbevelNoEdgeRing')
        lx.eval('select.type polygon')
        lx.eval('!select.deleteSet UnbevelPolyZone')
        lx.eval('!select.deleteSet UnbevelPolyBorder')


if success:
    if Modo_ver >= 1400:
        lx.eval('select.editSet UnbevelEdgeGuide add {}')
        lx.eval('select.type polygon')
        lx.eval('select.convert edge')
        lx.eval('select.invert')
        lx.eval('select.editSet UnbevelNoEdgeRing add {}')
        lx.eval('select.type polygon')
        lx.eval('hide.unsel')
        lx.eval('select.type edge')
        lx.eval('select.drop edge')
        lx.eval('select.useSet UnbevelEdgeGuide replace')
        lx.eval('select.edgeLoop base false m3d middle')
        lx.eval('select.ring')
        lx.eval('select.editSet UnbevelEdgeRing add {}')
        lx.eval('select.drop edge')
        lx.eval('select.type polygon')
        lx.eval('unhide')
        lx.eval('select.drop polygon')
        lx.eval('select.drop edge')
        lx.eval('select.useSet UnbevelEdgeRing replace')
        lx.eval('edge.unbevel convergence')
        lx.eval('!select.deleteSet UnbevelEdgeRing')
        lx.eval('!select.deleteSet UnbevelEdgeGuide')
        lx.eval('!select.deleteSet UnbevelNoEdgeRing')
        lx.eval('select.type polygon')

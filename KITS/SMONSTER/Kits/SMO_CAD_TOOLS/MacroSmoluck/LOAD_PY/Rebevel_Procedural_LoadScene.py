#python

#import lx
#kitpath = lx.eval("query platformservice alias ? {kit_SMO_CAD_TOOLS:}")
#lx.eval('scene.open "%s/Scenes/Rebevel.lxo" normal' % kitpath)

import lx
kitpath = lx.eval("query platformservice alias ? {kit_SMO_CAD_TOOLS:Scenes/Rebevel.lxo}")
lx.eval('scene.open {%s} normal' % kitpath)
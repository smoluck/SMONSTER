#python

import lx
Path = lx.eval("query platformservice alias ? {kit_SMO_GAME_CONTENT:Presets}")
lx.eval('preset.do {%s/SMO_Ground_ShadowCatcher_ASS.lxp}' % Path)
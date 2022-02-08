#python

import lx
Path = lx.eval("query platformservice alias ? {kit_SMO_GAME_CONTENT:Presets}")
lx.eval('preset.do {%s/SMO_RoundedEdgeMaskMaster_ASS.lxp}' % Path)
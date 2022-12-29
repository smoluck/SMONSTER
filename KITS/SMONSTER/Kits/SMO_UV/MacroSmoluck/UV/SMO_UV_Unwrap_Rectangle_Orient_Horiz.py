# python
"""
Name:         	SMO_UV_Unwrap_Rectangle_Orient_Horiz.py

Purpose:		This script is designed to:
                Unwrap the current Polygon Selection
                using rectangle method and Orient the UV Island on U.

Author:       	Franck ELISABETH
Website:      	https://www.smoluck.com
Created:      	01/07/2018
Copyright:    	(c) Franck Elisabeth 2017-2022
"""

import lx
import sys

lx.eval('tool.set preset:"uv.unwrap" mode:on')
lx.eval('tool.apply')
# replay name:"Normalize Texel Density"
# lx.eval('texeldensity.normalize')
lx.eval('!uv.rectangle false 0.2 false false')
lx.eval('uv.orient horizontal')

# lx.eval('texeldensity.set per:island mode:all')

lx.eval('tool.viewType uv')
# replay name:"Move"
lx.eval('tool.set preset:TransformMove mode:on')

try:
    # Command Block Begin:
    lx.eval('tool.setAttr tool:"xfrm.transform" attr:TX value:"-1.0"')
    lx.eval('tool.setAttr tool:"xfrm.transform" attr:TY value:"0.0"')
    lx.eval('tool.setAttr tool:"xfrm.transform" attr:TZ value:"0.0"')
    lx.eval('tool.setAttr tool:"xfrm.transform" attr:U value:"1.0"')
    lx.eval('tool.setAttr tool:"xfrm.transform" attr:V value:"1.0"')
    # Command Block End:
except:
    sys.exit

# Launch the Move
lx.eval('tool.doapply')
lx.eval('select.nextMode')
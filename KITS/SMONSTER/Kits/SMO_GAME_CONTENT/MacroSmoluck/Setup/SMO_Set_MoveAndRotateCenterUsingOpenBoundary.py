# python
"""
Name:         SMO_Set_MoveAndRotateCenterUsingOpenBoundary.py

Purpose:      This script is designed to:
              Select an Opened Mesh_ Move and Rotate
              the Center to Open boundary centroid and rotate it (use it in item mode)

Author:       Franck ELISABETH
Website:      https://www.linkedin.com/in/smoluck/
Created:      20/06/2020
Copyright:    (c) Franck Elisabeth 2017-2022
"""

import lx

lx.eval('script.run "macro.scriptservice:92663570022:macro"')
lx.eval('poly.make auto')
lx.eval('select.convert polygon')
lx.eval('select.editSet temmmmmp add')
lx.eval('smo.GC.StarTriple')
lx.eval('select.useSet temmmmmp select')
lx.eval('select.convert vertex')
lx.eval('select.contract')
lx.eval('smo.GC.Setup.MoveRotateCenterToSelection 1 0')
lx.eval('select.drop polygon')
lx.eval('select.useSet temmmmmp select')
lx.eval('smo.GC.Setup.MoveRotateCenterToSelection 0 1')
lx.eval('select.type polygon')
lx.eval('select.useSet temmmmmp select')
lx.eval('!delete')
lx.eval('select.type item')

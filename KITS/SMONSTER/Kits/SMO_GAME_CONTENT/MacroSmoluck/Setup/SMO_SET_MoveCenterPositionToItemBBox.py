# python
"""
Name:           SMO_SET_MoveCenterPositionRoItemBBox.py

Purpose:		This script is designed to:
                This script is designed to Move the Center
                of the Item at the Center of his Bounding Box.

Author:         Franck ELISABETH
Website:        https://www.linkedin.com/in/smoluck/
Created:        28/12/2018
Copyright:      (c) Franck Elisabeth 2017-2022
"""

import lx

lx.eval('select.type polygon')
lx.eval('select.all')
lx.eval('workPlane.fitSelect')
lx.eval('select.drop polygon')
lx.eval('select.type item')
lx.eval('select.convert type:center')
lx.eval('matchWorkplanePos')
lx.eval('workPlane.reset')
lx.eval('select.type item')
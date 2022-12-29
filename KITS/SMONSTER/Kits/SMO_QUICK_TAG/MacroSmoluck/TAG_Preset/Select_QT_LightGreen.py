# python
"""
Name:           Select_QT_LightGreen.py

Purpose:        This script is designed to:
                Apply a Selection Set to the current selection of polygons
                OR
                Creating the related Command Region to this Tag

Author:         Franck ELISABETH
Website:        https://www.smoluck.com
Created:        10/01/2020
Copyright:      (c) Franck Elisabeth 2017-2022
"""

import lx

lx.eval('select.type polygon')
lx.eval('select.useSet SMO_QT_LightGreen select')

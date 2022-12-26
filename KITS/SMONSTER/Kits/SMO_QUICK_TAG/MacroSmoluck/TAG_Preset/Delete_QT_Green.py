# python
"""
# Name: Delete_QT_Green.py
# Version: 1.0
#
# Purpose: This script is designed to apply a Selection Set to the current selection of polygons
#               OR
#               Creating the related Command Region to this Tag
#
# Author:       Franck ELISABETH
# Website:      https://www.smoluck.com
#
# Created:      10/01/2020
# Copyright:    (c) Franck Elisabeth 2017-2022
"""

import lx

lx.eval('poly.pcrClear')
lx.eval('!select.deleteSet SMO_QT_Green')
lx.eval('select.drop polygon')

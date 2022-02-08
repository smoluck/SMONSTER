#python
#---------------------------------------
# Name: Delete_QT_Yellow.py
# Version: 1.0
#
# Purpose: This script is designed to apply a Selection Set to the current selection of polygons
#               OR
#               Creating the related Command Region to this Tag
#
# Author:       Franck ELISABETH
# Website:      http://www.smoluck.com
#
# Created:      10/01/2020
# Copyright:    (c) Franck Elisabeth 2017-2022
#---------------------------------------

import modo
lx.eval('poly.pcrClear')
lx.eval('!select.deleteSet SMO_QT_Yellow')
lx.eval('select.drop polygon')
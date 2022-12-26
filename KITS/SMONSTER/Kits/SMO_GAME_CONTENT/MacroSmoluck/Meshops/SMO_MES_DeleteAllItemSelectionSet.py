# python
"""
# Name:         SMO_DeleteAllItemSelectionSet.py
# Version: 1.00
#
# Purpose: This script is designed Delete every Item Selection set in the scene
#
# Author:       Franck ELISABETH
# Website:      https://www.smoluck.com
#
# Created:      29/03/2019
# Modified:		01/04/2019
# Copyright:    (c) Franck Elisabeth 2017-2022
"""


lx.eval('select.itemType mesh')
lx.eval('!select.deleteSet SOURCE_MESH true')
lx.eval('!scene.save')
lx.eval('scene.close')
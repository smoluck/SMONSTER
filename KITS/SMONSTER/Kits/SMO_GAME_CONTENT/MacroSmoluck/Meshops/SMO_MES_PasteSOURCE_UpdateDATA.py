# python
"""
# Name:         SMO_PasteSOURCE_UpdateDATA.py
# Version: 1.00
#
# Purpose: This script is designed Paste the SOURCE DATA (Polygon and UVs) and save the Scene
#
# Author:       Franck ELISABETH
# Website:      https://www.smoluck.com
#
# Created:      29/03/2019
# Modified:		01/04/2019
# Copyright:    (c) Franck Elisabeth 2017-2022
"""


lx.eval('layer.new')
lx.eval('item.name SOURCE xfrmcore')
lx.eval('item.editorColor red')
lx.eval('paste')
lx.eval('select.typeFrom item;pivot;center;edge;polygon;vertex;ptag true')
lx.eval('!scene.save')
lx.eval('scene.close')
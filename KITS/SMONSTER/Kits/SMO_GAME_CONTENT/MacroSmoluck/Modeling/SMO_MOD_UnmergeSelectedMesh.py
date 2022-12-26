# python
"""
# Name:         SMO_MOD_UnmergeSelectedMesh.py
# Version: 1.0
#
# Purpose: This script is designed to
# Unmerge / Separate all mesh item selected based on their continuity.
#
# Author:       Franck ELISABETH
# Website:      https://www.smoluck.com
#
# Created:      28/12/2018
# Copyright:    (c) Franck Elisabeth 2017-2022
"""

import modo
scene = modo.scene.current()
UnmergeSelectedMeshes = scene.selectedByType('mesh')

# ------------- ARGUMENTS ------------- #
args = lx.args()
lx.out(args)
# no RecenterCenter = 0
# RecenterCenter = 1
RecenterCenter = int(args[0])
lx.out('Recenter Center to BoundingBox:',RecenterCenter)
############### ARGUMENT ###############

# # ------------- ARGUMENTS Test
# RecenterCenter = 1
# ############### ARGUMENT ###############

lx.eval('hide.unsel')

if RecenterCenter == 1 :
    lx.eval('select.editSet name:Setup_UnmergeRecenter mode:add')


for mesh in UnmergeSelectedMeshes:
    lx.eval('layer.unmergeMeshes')

if RecenterCenter == 1 :
    lx.eval('select.useSet Setup_UnmergeRecenter replace')
    lx.eval('!select.deleteSet Setup_UnmergeRecenter false')


RecenterMeshes = scene.selectedByType('mesh')

if RecenterCenter == 1 :   
    lx.eval('center.bbox center')
    #lx.eval('@kit_SMO_GAME_CONTENT:MacroSmoluck/Setup/SMO_SET_MoveCenterPositionToItemBBox.py')
    
lx.eval('unhide')
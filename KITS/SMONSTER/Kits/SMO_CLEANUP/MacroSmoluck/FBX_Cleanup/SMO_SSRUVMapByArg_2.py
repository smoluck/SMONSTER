# python
"""
# Name:         SMO_SSRUVMapByArg.py
# Version:      1.0
#
# Purpose:      This script is designed to:
#               Search if a specific UV Map exist, select it and rename it
#               via String Argument.
#
# Author:       Franck ELISABETH
# Website:      https://www.smoluck.com
#
# Created:      17/02/2020
# Copyright:    (c) Franck Elisabeth 2017-2022
"""

import lx
import modo

scn = modo.Scene()

# # # ------------- ARGUMENTS Test
# RenameByDefault = 1
# Searched = "UVChannel_1"
# OutputName = "TargetUVMap"
# # ------------- ARGUMENTS ------------- #
args = lx.args()
lx.out(args)

RenameByDefault = bool(args[0])
lx.out('Rename Detected by Default Name:', RenameByDefault)

Searched = str(args[1])
lx.out('Searched String chain:', Searched)

OutputName = str(args[2])
lx.out('Target String chain:', OutputName)
# # ------------- ARGUMENTS ------------- #


DetectedVMapCount = len(lx.evalN('vertMap.list all ?'))
lx.out('Vmap Count:', DetectedVMapCount)
# Get the name of UV Seam map available on mesh
DetectedVMapName = lx.eval('vertMap.list txuv ?')
lx.out('UVmap Name:', DetectedVMapName)
# Get the default UV Map name of the user
DefaultUVMapName = lx.eval('pref.value application.defaultTexture ?')
lx.out('Current Default UV Map name:', DefaultUVMapName)

RenamedToDefault = 0

DefaultMeshItemList = []
DefaultMeshItemList = lx.eval('query sceneservice selection ? mesh')  # mesh item layers

for mesh in DefaultMeshItemList:
    for VMapName in DetectedVMapName:
        if VMapName.startswith('%s' % Searched):
            try:
                lx.eval('select.vertexMap {%s} txuv replace' % Searched)
            except:
                pass
    if DetectedVMapCount >= 1 and DetectedVMapName == "_____n_o_n_e_____":
        lx.out('UV map Selected')
        lx.eval('select.vertexMap {%s} txuv replace' % Searched)
        if RenameByDefault == 1:
            lx.eval('vertMap.rename {%s} {%s} txuv active' % (Searched, DefaultUVMapName))
            lx.out('Detected UV Map Renamed from %s to %s:' % (Searched, DefaultUVMapName))
            lx.eval('select.vertexMap {%s} txuv remove' % DefaultUVMapName)
            RenamedToDefault = 1
        if RenameByDefault == 0:
            lx.eval('vertMap.rename {%s} {%s} txuv active' % (Searched, OutputName))
            lx.out('Detected UV Map Renamed from %s to %s:' % (Searched, OutputName))
            lx.eval('select.vertexMap {%s} txuv remove' % OutputName)
            RenamedToDefault = 0

    elif DetectedVMapCount <= 0 and DetectedVMapName != "_____n_o_n_e_____" and RenamedToDefault == 0:
        lx.out('UV Map not Renamed, because not Detected')

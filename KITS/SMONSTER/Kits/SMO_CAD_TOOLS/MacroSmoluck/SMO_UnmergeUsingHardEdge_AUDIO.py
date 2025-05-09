# python
"""
Name:           SMO_UnmergeUsingHardEdge_AUDIO.py

Purpose:        This script is designed to:
                Cleanup Mesh over 3 axis directions (6 sides)
                Select the Mesh in Item Mode
                It only cleanup Polygons that are perfectly perpendicular to X Y Z
                Axis in both direction (Some of the code is related to the Sceneca
                LazySelect script. Thanks to him for let me integrate it here)

Author:         Franck ELISABETH
Website:        https://www.linkedin.com/in/smoluck/
Created:        28/05/2018
Copyright:      (c) Franck Elisabeth 2017-2022
"""

import lx

OriginalTimeCurrentOut = lx.eval("time.range current out:?")
# lx.out('Original Time Current Out: {%s}' % OriginalTimeCurrentOut )
OriginalTimeSceneOut = lx.eval("time.range scene out:?")
# lx.out('Original Time Scene Out: {%s}' % OriginalTimeSceneOut )

# Play an Audio File to tell that the export is done.
audiopath = lx.eval("query platformservice alias ? {kit_SMO_CAD_TOOLS:Audio/Export_FinishShort.wav}")

lx.eval('@{kit_SMO_CAD_TOOLS:MacroSmoluck/UnmergeUsingHardEdge.LXM}')

lx.eval('time.range scene out:10.0')
lx.eval('time.range current out:10.0')

# Play an Audio File to tell that the export is done.
lx.eval('audio.playFile {%s}' % audiopath)

lx.eval('time.range scene out: {%s}' % OriginalTimeSceneOut)
lx.eval('time.range current out: {%s}' % OriginalTimeCurrentOut)
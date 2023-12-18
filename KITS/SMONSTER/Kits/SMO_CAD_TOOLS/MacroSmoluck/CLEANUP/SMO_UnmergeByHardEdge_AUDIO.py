# python
"""
Name:         SMO_UnmergeByHardEdge_AUDIO.py

Purpose:      This script is designed to:
              Unmerge separate one Mesh ItemCount
              using the HardEdge as guide.
              (All Vertex Borders will be merged in the process)

Author:       Franck ELISABETH
Website:      https://www.linkedin.com/in/smoluck/
Created:      28/05/2018
Copyright:    (c) Franck Elisabeth 2017-2022
"""

import lx

OriginalTimeCurrentOut = lx.eval("time.range current out:?")
# lx.out('Original Time Current Out: {%s}' % OriginalTimeCurrentOut )
OriginalTimeSceneOut = lx.eval("time.range scene out:?")
# lx.out('Original Time Scene Out: {%s}' % OriginalTimeSceneOut )

# Play an Audio File to tell that the export is done.
audiopath = lx.eval("query platformservice alias ? {kit_SMO_CAD_TOOLS:Audio/Export_FinishShort.wav}")

lx.eval('@{kit_SMO_CAD_TOOLS:MacroSmoluck/CLEANUP/SMO_UnmergeByHardEdge.py}')

lx.eval('time.range scene out:10.0')
lx.eval('time.range current out:10.0')

# Play an Audio File to tell that the export is done.
lx.eval('audio.playFile {%s}' % audiopath)

lx.eval('time.range scene out: {%s}' % OriginalTimeSceneOut)
lx.eval('time.range current out: {%s}' % OriginalTimeCurrentOut)
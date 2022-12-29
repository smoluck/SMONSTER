# python
"""
Name:           SMO_MES_ExportMeshOpRig_QuadRemeshed_to_FBXSequence_AUDIO.py

Purpose:        This script is designed to:
                Test Export MeshOps rig as a freezed Mesh,
                over time, as an FBX sequence.
                Select the MeshOp item and run.

Author:         Franck ELISABETH
Website:        https://www.smoluck.com
Created:        28/05/2018
Copyright:      (c) Franck Elisabeth 2017-2022
"""

import lx

# @kit_SMO_GAME_CONTENT:MacroSmoluck/Meshops/SMO_MES_ExportMeshOpRig_to_FBXSequence_AUDIO.py

OriginalTimeCurrentOut = lx.eval("time.range current out:?")
# lx.out('Original Time Current Out: {%s}' % OriginalTimeCurrentOut )
OriginalTimeSceneOut = lx.eval("time.range scene out:?")
# lx.out('Original Time Scene Out: {%s}' % OriginalTimeSceneOut )

# Play an Audio File to tell that the export is done.
audiopath = lx.eval("query platformservice alias ? {kit_SMO_GAME_CONTENT:Audio/Export_FinishShort.wav}")

lx.eval('@{kit_SMO_GAME_CONTENT:MacroSmoluck/Meshops/SMO_MES_ExportMeshOpRig_QuadRemeshed_to_FBXSequence.py}')

lx.eval('time.range scene out:10.0')
lx.eval('time.range current out:10.0')

# Play an Audio File to tell that the export is done.
lx.eval('audio.playFile {%s}' % audiopath)

lx.eval('time.range scene out: {%s}' % OriginalTimeSceneOut)
lx.eval('time.range current out: {%s}' % OriginalTimeCurrentOut)
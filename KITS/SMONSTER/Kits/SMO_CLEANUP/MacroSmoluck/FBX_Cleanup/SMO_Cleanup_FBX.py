# python
"""
# Name:         SMO_Cleanup_FBX.py 1 1 1 1 1 1
# Version:      1.0
#
# Purpose:  This script is designed to:
#           Cleanup scene to get only the Meshes and remove the 3dsmax channels if present
#           
#
# Author:       Franck ELISABETH
# Website:      https://www.smoluck.com
#
# Created:      19/12/2019
# Copyright:    (c) Franck Elisabeth 2017-2022
"""

import lx

# if NoUndo == 1 :
    # lx.eval('!!app.undoSuspend')


# ############### Look at User Prefs ###############
FullAutoDelCam = lx.eval('user.value SMO_UseVal_CLEANUP_FullAuto_DeleteCam ?')
lx.out('Delete all Cameras:', FullAutoDelCam)

FullAutoDelLight = lx.eval('user.value SMO_UseVal_CLEANUP_FullAuto_DeleteLight ?')
lx.out('Delete all Lights:', FullAutoDelLight)

FullAutoEmptyMesh = lx.eval('user.value SMO_UseVal_CLEANUP_FullAuto_DeleteEmptyMesh ?')
lx.out('Delete Empty Meshes:', FullAutoEmptyMesh)

FullAutoUnparentInPlace = lx.eval('user.value SMO_UseVal_CLEANUP_FullAuto_UnparentInPlace ?')
lx.out('Unparent All Mesh in Place:', FullAutoUnparentInPlace)

FullAutoDelFBXChannels = lx.eval('user.value SMO_UseVal_CLEANUP_FullAuto_DeleteFBXChan ?')
lx.out('Delete 3DSMAX FBX Channels:', FullAutoDelFBXChannels)

FullAutoFixUVmapName = lx.eval('user.value SMO_UseVal_CLEANUP_FullAuto_RenameUV ?')
lx.out('Rename UVMap name:', FullAutoFixUVmapName)

FullAutoUpdateMat = lx.eval('user.value SMO_UseVal_CLEANUP_FullAuto_UpdateMaterials ?')
lx.out('Update Materials Smoothing Angle:', FullAutoUpdateMat)

FullAutoConvHardEdge = lx.eval('user.value SMO_UseVal_CLEANUP_FullAuto_HardEdgeWork ?')
lx.out('Convert all Mesh to HardEdge workflow:', FullAutoConvHardEdge)
# ############### Look at User Prefs ###############




if FullAutoDelCam == 1 :
    lx.eval('smo.CLEANUP.DelCam')
if FullAutoDelLight == 1 :
    lx.eval('smo.CLEANUP.DelLight')
if FullAutoEmptyMesh == 1 :
    lx.eval('smo.CLEANUP.DelEmptyMeshItem')
if FullAutoDelFBXChannels == 1 :
    lx.eval('@kit_SMO_GAME_CONTENT:MacroSmoluck/FBX_Cleanup/SMO_Cleanup_3DsMAX_FBXChannel.py')
if FullAutoUnparentInPlace == 1 :
    lx.eval('smo.CLEANUP.UnparentInPlace')
if FullAutoFixUVmapName == 1 :
    lx.eval('smo.SSRUVMapByArg 1 {UVChannel_1} {TargetUVMap}')
if FullAutoUpdateMat == 1 :
    lx.eval('smo.CLEANUP.UpdateMat')
if FullAutoConvHardEdge == 1 :
    lx.eval('smo.CLEANUP.ConvertHardEdge')



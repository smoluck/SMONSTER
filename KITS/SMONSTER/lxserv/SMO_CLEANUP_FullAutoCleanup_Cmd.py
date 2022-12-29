# python
"""
Name:         SMO_CLEANUP_FullAutoCleanup_Cmd.py

Purpose:      This script is designed to:
              Cleanup all the scene using User Defined Preferences.

Author:       Franck ELISABETH (with the help of James O'Hare)
Website:      https://www.smoluck.com
Created:      14/05/2020
Copyright:    (c) Franck Elisabeth 2017-2022
"""

import lx
import lxu

Cmd_Name = "smo.CLEANUP.FullAutoCleanup"


class SMO_Cleanup_FullAutoCleanup_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
    
    def cmd_Flags(self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO
    
    def cmd_Interact (self):
        pass
    
    def cmd_UserName (self):
        return 'SMO CLEANUP - Full Auto Cleanup'
    
    def cmd_Desc (self):
        return 'Cleanup all the scene using User Defined Preferences.'
    
    def cmd_Tooltip (self):
        return 'Cleanup all the scene using User Defined Preferences.'
    
    def cmd_Help (self):
        return 'https://twitter.com/sm0luck'
    
    def basic_ButtonName (self):
        return 'SMO CLEANUP - Full Auto Cleanup'
    
    def basic_Enable (self, msg):
        return True
        
    
    def basic_Execute(self, msg, flags):
        
        # ------------- Look at User Prefs ------------- #
        FullAutoDelCam = lx.eval('user.value SMO_UseVal_CLEANUP_FullAuto_DeleteCam ?')
        lx.out('Delete all Cameras:', FullAutoDelCam)
        
        FullAutoDelLight = lx.eval('user.value SMO_UseVal_CLEANUP_FullAuto_DeleteLight ?')
        lx.out('Delete all Lights:', FullAutoDelLight)
        
        FullAutoEmptyMesh = lx.eval('user.value SMO_UseVal_CLEANUP_FullAuto_DeleteEmptyMesh ?')
        lx.out('Delete Empty Meshes:', FullAutoEmptyMesh)
        
        FullAutoUnparentInPlace = lx.eval('user.value SMO_UseVal_CLEANUP_FullAuto_UnparentInPlace ?')
        lx.out('Unparent All Mesh in Place:', FullAutoUnparentInPlace)
        
        
        ####################
        FullAutoDelFBXChannels = lx.eval('user.value SMO_UseVal_CLEANUP_FullAuto_DeleteFBXChan ?')
        lx.out('Delete 3DSMAX FBX Channels:', FullAutoDelFBXChannels)
        
        FullAutoDelFBXChannels_FieldA = lx.eval('user.value SMO_UseVal_CLEANUP_FullAuto_FBXChan_String_A ?')
        lx.out('Searched FBX Channels Field A:', FullAutoDelFBXChannels_FieldA)
        
        FullAutoDelFBXChannels_FieldB = lx.eval('user.value SMO_UseVal_CLEANUP_FullAuto_FBXChan_String_B ?')
        lx.out('Searched FBX Channels Field B:', FullAutoDelFBXChannels_FieldB)
        
        FullAutoDelFBXChannels_FieldC = lx.eval('user.value SMO_UseVal_CLEANUP_FullAuto_FBXChan_String_C ?')
        lx.out('Searched FBX Channels Field C:', FullAutoDelFBXChannels_FieldC)
        
        FullAutoDelFBXChannels_FieldD = lx.eval('user.value SMO_UseVal_CLEANUP_FullAuto_FBXChan_String_D ?')
        lx.out('Searched FBX Channels Field D:', FullAutoDelFBXChannels_FieldD)
        
        FullAutoDelFBXChannels_FieldE = lx.eval('user.value SMO_UseVal_CLEANUP_FullAuto_FBXChan_String_E ?')
        lx.out('Searched FBX Channels Field E:', FullAutoDelFBXChannels_FieldE)
        
        FullAutoDelFBXChannels_FieldF = lx.eval('user.value SMO_UseVal_CLEANUP_FullAuto_FBXChan_String_F ?')
        lx.out('Searched FBX Channels Field F:', FullAutoDelFBXChannels_FieldF)
        
        FullAutoDelFBXChannels_FieldG = lx.eval('user.value SMO_UseVal_CLEANUP_FullAuto_FBXChan_String_G ?')
        lx.out('Searched FBX Channels Field G:', FullAutoDelFBXChannels_FieldG)
        
        FullAutoDelFBXChannels_FieldH = lx.eval('user.value SMO_UseVal_CLEANUP_FullAuto_FBXChan_String_H ?')
        lx.out('Searched FBX Channels Field H:', FullAutoDelFBXChannels_FieldH)
        
        FullAutoDelFBXChannels_FieldI = lx.eval('user.value SMO_UseVal_CLEANUP_FullAuto_FBXChan_String_I ?')
        lx.out('Searched FBX Channels Field I:', FullAutoDelFBXChannels_FieldI)
        
        FullAutoDelFBXChannels_FieldJ = lx.eval('user.value SMO_UseVal_CLEANUP_FullAuto_FBXChan_String_J ?')
        lx.out('Searched FBX Channels Field J:', FullAutoDelFBXChannels_FieldJ)
        ####################
        
        
        FullAutoFixUVmapNameToDefault = lx.eval('user.value SMO_UseVal_CLEANUP_FullAuto_RenameUVToDefault ?')
        lx.out('Rename UVMap name to Default:', FullAutoFixUVmapNameToDefault)
        
        FullAutoFixUVmapNameToUserPref = lx.eval('user.value SMO_UseVal_CLEANUP_FullAuto_RenameUVToUserPref ?')
        lx.out('Rename UVMap name to User Target:', FullAutoFixUVmapNameToUserPref)
        
        
        FullAutoUpdateMat = lx.eval('user.value SMO_UseVal_CLEANUP_FullAuto_UpdateMaterials ?')
        lx.out('Update Materials Smoothing Angle:', FullAutoUpdateMat)
        
        FullAutoConvHardEdge = lx.eval('user.value SMO_UseVal_CLEANUP_FullAuto_HardEdgeWork ?')
        lx.out('Convert all Mesh to HardEdge workflow:', FullAutoConvHardEdge)
        
        FullAutoDelPreRot = lx.eval('user.value SMO_UseVal_CLEANUP_FullAuto_DelPreRot ?')
        lx.out('Delete all Pre Rotation Transforms:', FullAutoDelPreRot)
        
        FullAutoFreezeTransf = lx.eval('user.value SMO_UseVal_CLEANUP_FullAuto_FreezeTransf ?')
        lx.out('Convert all Mesh to HardEdge workflow:', FullAutoFreezeTransf)
        
        ConvertItemIndexStyleSceneWise = lx.eval('user.value SMO_UseVal_CLEANUP_FullAuto_ConvertItemIndexStyleSceneWise ?')
        lx.out('Convert all Space and/or Underscore in Meshes/Locator/GroupLocator names to match the current Modo Prefs Index Style:', ConvertItemIndexStyleSceneWise)
        # ------------- Look at User Prefs ------------- #
        
        
        
        
        if FullAutoDelCam == 1 :
            lx.eval('smo.CLEANUP.DelCam')
        if FullAutoDelLight == 1 :
            lx.eval('smo.CLEANUP.DelLight')
        if FullAutoEmptyMesh == 1 :
            lx.eval('smo.CLEANUP.DelEmptyMeshItem')
        if FullAutoDelFBXChannels == 1 :
            if FullAutoDelFBXChannels_FieldA != "_____n_o_n_e_____" :
                lx.eval('smo.CLEANUP.DelChanByArg %s' % FullAutoDelFBXChannels_FieldA )
            if FullAutoDelFBXChannels_FieldB != "_____n_o_n_e_____" :
                lx.eval('smo.CLEANUP.DelChanByArg %s' % FullAutoDelFBXChannels_FieldB )
            if FullAutoDelFBXChannels_FieldC != "_____n_o_n_e_____" :
                lx.eval('smo.CLEANUP.DelChanByArg %s' % FullAutoDelFBXChannels_FieldC )
            if FullAutoDelFBXChannels_FieldD != "_____n_o_n_e_____" :
                lx.eval('smo.CLEANUP.DelChanByArg %s' % FullAutoDelFBXChannels_FieldD )
            if FullAutoDelFBXChannels_FieldE != "_____n_o_n_e_____" :
                lx.eval('smo.CLEANUP.DelChanByArg %s' % FullAutoDelFBXChannels_FieldE )
            if FullAutoDelFBXChannels_FieldF != "_____n_o_n_e_____" :
                lx.eval('smo.CLEANUP.DelChanByArg %s' % FullAutoDelFBXChannels_FieldF )
            if FullAutoDelFBXChannels_FieldG != "_____n_o_n_e_____" :
                lx.eval('smo.CLEANUP.DelChanByArg %s' % FullAutoDelFBXChannels_FieldG )
            if FullAutoDelFBXChannels_FieldH != "_____n_o_n_e_____" :
                lx.eval('smo.CLEANUP.DelChanByArg %s' % FullAutoDelFBXChannels_FieldH )
            if FullAutoDelFBXChannels_FieldI != "_____n_o_n_e_____" :
                lx.eval('smo.CLEANUP.DelChanByArg %s' % FullAutoDelFBXChannels_FieldI )
            if FullAutoDelFBXChannels_FieldJ != "_____n_o_n_e_____" :
                lx.eval('smo.CLEANUP.DelChanByArg %s' % FullAutoDelFBXChannels_FieldJ )
            
        if FullAutoUnparentInPlace == 1 :
            lx.eval('smo.CLEANUP.UnparentInPlace')
        if FullAutoFixUVmapNameToDefault == 1 and FullAutoFixUVmapNameToUserPref == 0 :
            lx.eval('smo.CLEANUP.SSRUVMapByUserPref 1')
        if FullAutoFixUVmapNameToDefault == 0 and FullAutoFixUVmapNameToUserPref == 1 :
            lx.eval('smo.CLEANUP.SSRUVMapByUserPref 0')
        if FullAutoUpdateMat == 1 :
            lx.eval('smo.CLEANUP.UpdateMat')
        if FullAutoConvHardEdge == 1 :
            lx.eval('smo.CLEANUP.ConvertHardEdge 0 1')
            
        if FullAutoDelPreRot == 1 and FullAutoFreezeTransf == 0 :
            lx.eval('smo.CLEANUP.DelPreTransform 1 0')
        if FullAutoDelPreRot == 1 and FullAutoFreezeTransf == 1 :
            lx.eval('smo.CLEANUP.DelPreTransform 1 1')
            
        if ConvertItemIndexStyleSceneWise == 1 :
            lx.eval('smo.CLEANUP.ConvertItemIndexStyleSceneWise')
    
lx.bless(SMO_Cleanup_FullAutoCleanup_Cmd, Cmd_Name)

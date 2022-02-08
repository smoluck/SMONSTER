#python
#---------------------------------------------
# Name:         SMO_CLEANUP_Del3DsMAX_FBXChannel_Cmd.py
# Version:      1.0
#
# Purpose:      This script is designed to:
#               Delete all 3DSMAX related Channels created
#               at FBX Export in the current scene.
#
# Author:       Franck ELISABETH
# Website:      http://www.smoluck.com
#
# Created:      19/12/2019
# Copyright:    (c) Franck Elisabeth 2017-2022
#---------------------------------------------


import lx, lxu, modo

class SMO_Cleanup_Del3DsMAX_FBXChannel_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
    def cmd_Flags(self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO
    
    def cmd_Interact (self):
        pass
    
    def cmd_UserName (self):
        return 'SMO Cleanup Del3DsMAX FBXChannel'
    
    def cmd_Desc (self):
        return 'Delete all 3DS Max Channels.'
    
    def cmd_Tooltip (self):
        return 'Delete all 3DS Max Channels.'
    
    def cmd_Help (self):
        return 'https://twitter.com/sm0luck'
    
    def basic_ButtonName (self):
        return 'SMO Cleanup Del3DsMAX FBXChannel'
    
    def cmd_Flags (self):
        return lx.symbol.fCMD_UNDO
    
    def basic_Enable (self, msg):
        return True
        
    
    def basic_Execute(self, msg, flags):
        scene = modo.scene.current()
        
        
        ####################
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
        
        #----------------------------------------#
        # Delete unnecessary FBX 3DSMax Channels #
        #----------------------------------------#
        
        lx.eval('select.itemType mesh')
        # Variables
        DelFBXChanMeshList = []
        DelFBXChanMeshList = lx.eval('query sceneservice selection ? mesh') # mesh item layers
        for mesh in DelFBXChanMeshList:
            # mesh.select(True)
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
        lx.eval('select.drop item')
        
    
lx.bless(SMO_Cleanup_Del3DsMAX_FBXChannel_Cmd, "smo.CLEANUP.Del3DsMAX.FBXChannel")
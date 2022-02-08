#python
#---------------------------------------
# Name:         SMO_CLEANUP_DelChanByArg_Cmd.py
# Version:      1.0
#
# Purpose:      This script is designed to:
#               Search if a specific channel exist
#               via String Argument and delete it
#
# Author:       Franck ELISABETH (with the help of James O'Hare)
# Website:      http://www.smoluck.com
#
# Created:      17/02/2020
# Copyright:    (c) Franck Elisabeth 2017-2022
#---------------------------------------

import lx, lxu, modo

class SMO_Cleanup_DelChanByArg_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
        self.dyna_Add("SearchString", lx.symbol.sTYPE_STRING)
        self.basic_SetFlags (0, lx.symbol.fCMDARG_OPTIONAL)             # here the (0) define the argument index.
    
    def cmd_Flags(self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO
    
    def cmd_Interact (self):
        pass
    
    def cmd_UserName (self):
        return 'SMO Cleanup DelChanByArg'
    
    def cmd_Desc (self):
        return 'Search if a specific channel exist via String Argument and delete it.'
    
    def cmd_Tooltip (self):
        return 'Search if a specific channel exist via String Argument and delete it.'
    
    def cmd_Help (self):
        return 'https://twitter.com/sm0luck'
    
    def basic_ButtonName (self):
        return 'SMO Cleanup DelChanByArg'
    
    def cmd_Flags (self):
        return lx.symbol.fCMD_UNDO
    
    def basic_Enable (self, msg):
        return True
        
    
    def basic_Execute(self, msg, flags):
        # # ############### 1 ARGUMENTS Test ###############
        # SearchStringArg = 'FBX_UDP3DSMAX'
        # # ############### ARGUMENTS ###############
        SearchString = self.dyna_String (0)
        # # ############### 1 ARGUMENTS ###############
        # args = lx.args()
        # lx.out(args)
        # SearchStringArg = SearchString
        # lx.out('Searched String chain:', SearchStringArg)
        # # ############### ARGUMENTS ###############
        
        scn = modo.Scene()
        for mesh in scn.items('mesh'):
            for channelName in mesh.channelNames:
                if channelName.startswith('%s' % SearchString ):
                    try:
                        lx.eval('select.channel {%s:%s} set' % (mesh.id, channelName))
                        lx.eval('channel.delete')
                    except:
                        pass
    
    
lx.bless(SMO_Cleanup_DelChanByArg_Cmd, "smo.CLEANUP.DelChanByArg")
# smo.CLEANUP.DelChanByArg FBX_UDP3DSMAX
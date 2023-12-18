# python
"""
Name:         SMO_GC_SelectMeshByChannelName_Cmd.py

Purpose:      This script is designed to:
              Search in all Mesh items in the Scene, if a specific channel exist via String Argument #1,
              select back the items that have that channel via Argument #2.

Author:       Franck ELISABETH
Website:      https://www.linkedin.com/in/smoluck/
Created:      28/07/2020
Copyright:    (c) Franck Elisabeth 2017-2022
"""

import lx
import lxu
import modo

Cmd_Name = "smo.GC.SelectMeshByChannelName"
# smo.GC.SelectMeshByChannelName TgLP 1


class SMO_GC_SelectMeshByChannelName_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
        self.dyna_Add("SearchString", lx.symbol.sTYPE_STRING)
        self.basic_SetFlags (0, lx.symbol.fCMDARG_OPTIONAL)             # here the (0) define the argument index.
        self.dyna_Add("Reselect", lx.symbol.sTYPE_INTEGER)
        self.basic_SetFlags (1, lx.symbol.fCMDARG_OPTIONAL)
    
    def cmd_Flags(self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO
    
    def cmd_Interact (self):
        pass
    
    def cmd_UserName (self):
        return 'SMO GC - Select Mesh By Channel Name'
    
    def cmd_Desc (self):
        return 'Search in all Mesh items in the Scene, if a specific channel exist via String Argument #1, Reselect the items that have that channel via rgument #2.'
    
    def cmd_Tooltip (self):
        return 'Search in all Mesh items in the Scene, if a specific channel exist via String Argument #1, Reselect the items that have that channel via rgument #2.'
    
    def cmd_Help (self):
        return 'https://twitter.com/sm0luck'
    
    def basic_ButtonName (self):
        return 'SMO GC - Select Mesh By Channel Name'
    
    def basic_Enable (self, msg):
        return True
    
    def basic_Execute(self, msg, flags):
        # ------------- ARGUMENTS Test
        # SearchStringArg = 'FBX_UDP3DSMAX'
        # ------------- ARGUMENTS ------------- #
        SearchString = self.dyna_String (0)
        Reselect = self.dyna_Int (1)
        # ------------- ARGUMENTS ------------- #
        # args = lx.args()
        # lx.out(args)
        # SearchStringArg = SearchString
        # lx.out('Searched String chain:', SearchStringArg)
        # ------------- ARGUMENTS ------------- #
        

        scn = modo.scene.current()
        for mesh in scn.items('mesh'):
            for channelName in mesh.channelNames:
                if channelName.startswith('%s' % SearchString ):
                    try:
                        lx.eval('select.channel {%s:%s} set' % (mesh.id, channelName))
                        lx.eval('select.item %s add' % mesh.id)
                        lx.eval('select.editSet %s add' % SearchString)
                        lx.eval('select.drop item')
                    except:
                        pass
        if Reselect == 1 :
            lx.eval('select.useSet %s select' % SearchString)
            lx.eval('!select.deleteSet %s false' % SearchString)
        
    
lx.bless(SMO_GC_SelectMeshByChannelName_Cmd, Cmd_Name)

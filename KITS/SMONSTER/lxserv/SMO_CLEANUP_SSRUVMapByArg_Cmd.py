# python
"""
# Name:         SMO_CLEANUP_SSRUVMapByArg_Cmd.py
# Version:      1.0
#
# Purpose:      This script is designed to:
#               Search if a specific Vertex Map / UVMap exist, Select it and
#               Rename it according to Arguments.
#
# Author:       Franck ELISABETH (with the help of James O'Hare)
# Website:      https://www.smoluck.com
#
# Created:      17/02/2020
# Copyright:    (c) Franck Elisabeth 2017-2022
"""

import lx
import lxu
import modo

Cmd_Name = "smo.CLEANUP.SSRUVMapByArg"
# smo.CLEANUP.SSRUVMapByArg 1 {UVChannel_1} {TargetUVMap}


class SMO_Cleanup_SSRUVMapByArg_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
        self.dyna_Add("RenameByDefault", lx.symbol.sTYPE_BOOLEAN)
        self.basic_SetFlags (0, lx.symbol.fCMDARG_OPTIONAL)             # here the (0) define the argument index.
        self.dyna_Add("SearchString", lx.symbol.sTYPE_STRING)
        self.basic_SetFlags (1, lx.symbol.fCMDARG_OPTIONAL)             # here the (1) define the argument index.
        self.dyna_Add("TargetString", lx.symbol.sTYPE_STRING)
        self.basic_SetFlags (2, lx.symbol.fCMDARG_OPTIONAL)             # here the (2) define the argument index.
    
    def cmd_Flags(self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO
    
    def cmd_Interact (self):
        pass
    
    def cmd_UserName (self):
        return 'SMO CLEANUP - Search and Select UVMap by Arg'
    
    def cmd_Desc (self):
        return 'Search if a specific UVMap exist, Select it and Rename it according to Arguments.'
    
    def cmd_Tooltip (self):
        return 'Search if a specific UVMap exist, Select it and Rename it according to Arguments.'
    
    def cmd_Help (self):
        return 'https://twitter.com/sm0luck'
    
    def basic_ButtonName (self):
        return 'SMO CLEANUP - Search and Select UVMap by Arg'
    
    def basic_Enable (self, msg):
        return True
    
    def basic_Execute(self, msg, flags):
        scn = modo.Scene()
        # # ------------- ARGUMENTS ------------- #
        RenameByDefault = self.dyna_Bool (0)
        SearchString = self.dyna_String (1)
        TargetString = self.dyna_String (2)
        # # ------------- ARGUMENTS ------------- #
        
        DetectedVMapCount = len(lx.evalN('vertMap.list all ?'))
        lx.out('Vmap Count:', DetectedVMapCount)
        # Get the name of UV Seam map available on mesh
        DetectedVMapName = lx.eval('vertMap.list txuv ?')
        lx.out('UVmap Name:', DetectedVMapName)
        # Get the default UV Map name of the user
        DefaultUVMapName =  lx.eval('pref.value application.defaultTexture ?')
        lx.out('Current Default UV Map name:', DefaultUVMapName)
        
        RenamedToDefault = 0
        
        for mesh in scn.items('mesh'):
            mesh.select(True)
            for VMapName in DetectedVMapName:
                if VMapName.startswith('%s' % SearchString ):
                    try:
                        lx.eval('select.vertexMap {%s} txuv replace' % SearchString)
                    except:
                        pass
            if DetectedVMapCount >= 1 and DetectedVMapName == "_____n_o_n_e_____" :
                lx.out('UV map Selected')
                lx.eval('select.vertexMap {%s} txuv replace' % SearchString)
                if RenameByDefault == 1 :
                    lx.eval('vertMap.rename {%s} {%s} txuv active' % (SearchString, DefaultUVMapName))
                    lx.out('Detected UV Map Renamed from %s to %s:'% (SearchString, DefaultUVMapName))
                    lx.eval('select.vertexMap {%s} txuv 3' % DefaultUVMapName)
                    lx.eval('select.vertexMap {} txuv remove')
                if RenameByDefault == 0 :
                    lx.eval('vertMap.rename {%s} {%s} txuv active' % (SearchString, TargetString))
                    lx.out('Detected UV Map Renamed from %s to %s:'% (SearchString, TargetString))
                    lx.eval('select.vertexMap {%s} txuv 3' % TargetString)
                    lx.eval('select.vertexMap {} txuv remove')
                RenamedToDefault = 1
                
            elif DetectedVMapCount <= 0 and DetectedVMapName != "_____n_o_n_e_____" and RenamedToDefault == 0:
                lx.out('UV Map not Renamed, because not Detected')
        lx.eval('select.drop item')
        
    
lx.bless(SMO_Cleanup_SSRUVMapByArg_Cmd, Cmd_Name)

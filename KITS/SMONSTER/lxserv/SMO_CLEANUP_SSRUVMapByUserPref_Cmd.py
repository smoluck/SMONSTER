#python
#---------------------------------------
# Name:         SMO_CLEANUP_SSRUVMapByUserPref_Cmd.py
# Version:      1.0
#
# Purpose:      This script is designed to:
#               Search if the user preferences Source UVMap exist, Select it
#                and Rename it to default or Target UVMap.
#
# Author:       Franck ELISABETH (with the help of James O'Hare)
# Website:      http://www.smoluck.com
#
# Created:      21/06/2020
# Copyright:    (c) Franck Elisabeth 2017-2022
#---------------------------------------

import lx, lxu, modo

class SMO_Cleanup_SSRUVMapByUserPref_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
        self.dyna_Add("Rename By Default", lx.symbol.sTYPE_BOOLEAN)
        self.basic_SetFlags (0, lx.symbol.fCMDARG_OPTIONAL)             # here the (0) define the argument index.
    
    def cmd_Flags(self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO
    
    def cmd_Interact (self):
        pass
    
    def cmd_UserName (self):
        return 'SMO Cleanup SSRUVMapByUserPref'
    
    def cmd_Desc (self):
        return 'Search if the user preferences Source UVMap exist, Select it and Rename it to default or Target UVMap.'
    
    def cmd_Tooltip (self):
        return 'Search if the user preferences Source UVMap exist, Select it and Rename it to default or Target UVMap.'
    
    def cmd_Help (self):
        return 'https://twitter.com/sm0luck'
    
    def basic_ButtonName (self):
        return 'SMO Cleanup SSRUVMapByUserPref'
    
    def cmd_Flags (self):
        return lx.symbol.fCMD_UNDO
    
    def basic_Enable (self, msg):
        return True
        
    
    def basic_Execute(self, msg, flags):
        scn = modo.Scene()
        # ############### ARGUMENTS ###############
        RenameByDefault = self.dyna_Bool (0)
        # ############### ARGUMENTS ###############

        DetectedVMapCount = len(lx.evalN('vertMap.list all ?'))
        lx.out('Vmap Count:', DetectedVMapCount)
        # Get the name of UV Seam map available on mesh
        DetectedVMapName = lx.eval('vertMap.list txuv ?')
        lx.out('UVmap Name:', DetectedVMapName)
        # Get the Default UV Map name of the user
        DefaultUVMapName =  lx.eval('pref.value application.defaultTexture ?')
        lx.out('Current Default UV Map name:', DefaultUVMapName)
         # Get the Source UV Map name of the user
        SourceUVmapName = lx.eval('user.value SMO_UseVal_CLEANUP_UVSourceName ?')
        lx.out('Source UVMap name:', SourceUVmapName)
         # Get the Target UV Map name of the user
        TargetUVmapName = lx.eval('user.value SMO_UseVal_CLEANUP_UVTargetName ?')
        lx.out('Target UVMap name:', TargetUVmapName)




        for mesh in scn.items('mesh'):
            mesh.select(True)
            for VMapName in DetectedVMapName:
                if VMapName.startswith('%s' % SourceUVmapName ):
                    try:
                        lx.eval('select.vertexMap {%s} txuv replace' % SourceUVmapName)
                    except:
                        pass
            if DetectedVMapCount >= 1 and DetectedVMapName == "_____n_o_n_e_____" :
                lx.out('UV map Selected')
                lx.eval('select.vertexMap {%s} txuv replace' % SourceUVmapName)
                if RenameByDefault == 1 :
                    lx.eval('vertMap.rename {%s} {%s} txuv active' % (SourceUVmapName, DefaultUVMapName))
                    lx.out('Detected UV Map Renamed from %s to %s:'% (SourceUVmapName, DefaultUVMapName))
                    lx.eval('select.vertexMap {%s} txuv 3' % DefaultUVMapName)
                    lx.eval('select.vertexMap {} txuv remove')
                if RenameByDefault == 0 :
                    lx.eval('vertMap.rename {%s} {%s} txuv active' % (SourceUVmapName, TargetUVmapName))
                    lx.out('Detected UV Map Renamed from %s to %s:'% (SourceUVmapName, TargetUVmapName))
                    lx.eval('select.vertexMap {%s} txuv 3' % TargetUVmapName)
                    lx.eval('select.vertexMap {} txuv remove')
                Renamed = 1

            elif DetectedVMapCount <= 0 and DetectedVMapName != "_____n_o_n_e_____" and Renamed == 0:
                lx.out('UV Map not Renamed, because not Detected')
        lx.eval('select.drop item')
        
    
lx.bless(SMO_Cleanup_SSRUVMapByUserPref_Cmd, "smo.CLEANUP.SSRUVMapByUserPref")
# smo.CLEANUP.SSRUVMapByUserPref 1
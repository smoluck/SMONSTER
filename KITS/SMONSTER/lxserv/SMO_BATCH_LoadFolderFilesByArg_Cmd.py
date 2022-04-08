#python
#---------------------------------------
# Name:         SMO_BATCH_LoadFolderFilesByArg_Cmd.py
# Version:      1.0
#
# Purpose:      This script is designed to:
#               Batch Load Files stored in a Folder and Process the data using User Defined Preferences.
#
#
# Author:       Franck ELISABETH (with the help of James O'Hare)
# Website:      http://www.smoluck.com
#
# Created:      01/10/2020
# Copyright:    (c) Franck Elisabeth 2017-2022
#---------------------------------------

import lx, lxu, os, modo

class SMO_BATCH_LoadFolderFilesByArg_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
        self.dyna_Add("Input File Format", lx.symbol.sTYPE_STRING)
        self.basic_SetFlags (0, lx.symbol.fCMDARG_OPTIONAL)             # here the (0) define the argument index.
        self.dyna_Add("Output File Format", lx.symbol.sTYPE_STRING)
        self.basic_SetFlags (1, lx.symbol.fCMDARG_OPTIONAL)
    
    def cmd_Flags(self):
        return lx.symbol.fCMD_MODEL # | lx.symbol.fCMD_UNDO

    def cmd_Interact (self):
        pass
    
    def cmd_UserName (self):
        return 'SMO Batch Load Folder Files'
    
    def cmd_Desc (self):
        return 'Batch Load Files stored in a Folder and Process the data using User Defined Preferences.'
    
    def cmd_Tooltip (self):
        return 'Batch Load Files stored in a Folder and Process the data using User Defined Preferences.'
    
    def cmd_Help (self):
        return 'https://twitter.com/sm0luck'
    
    def basic_ButtonName (self):
        return 'SMO Batch Load Folder Files'
    
    def cmd_Flags (self):
        return lx.symbol.fCMD_UNDO
    
    def basic_Enable (self, msg):
        return True
        
    
    def basic_Execute(self, msg, flags):
        
        
        ################################
        #<----[ DEFINE VARIABLES ]---->#
        ################################
        lx.eval("user.defNew name:InputFileFormat type:string life:momentary")
        lx.eval("user.defNew name:OutputFileFormat type:string life:momentary")
        
        lx.eval("user.defNew name:Target_Path type:string life:momentary")
        ################################
        
        
        # ############### ARGUMENTS ###############
        InputFileFormat = self.dyna_String (0)
        OutputFileFormat = self.dyna_String (1)
        # ############### ARGUMENTS ###############
        
        
        lx.eval ('dialog.setup dir')
        lx.eval ('dialog.title "Select the target Folder to Analyse and Process"')
        # MODO version checks.
        modo_ver = int(lx.eval ('query platformservice appversion ?'))
        if modo_ver == 801:
            lx.eval ('+dialog.open')
        else:
            lx.eval ('dialog.open')
        Target_Path = lx.eval ('dialog.result ?')
        lx.out('Path', Target_Path)
        
        
        if InputFileFormat == "DXF" :
            for dxf in os.listdir(Target_Path):
                if ".dxf" in dxf:
                    finalPath = Target_Path + "/" + dxf
                    lx.eval("!!scene.open {%s} normal" % finalPath)
                    # lx.eval("!!scene.open {%s} import" % finalPath)
                    lx.eval('smo.CLEANUP.DelCam')
                    lx.eval('smo.CLEANUP.DelLight')
                    lx.eval('smo.GC.RenameMeshesBySceneName')
                    if OutputFileFormat == "LXO" :
                        lx.eval('smo.GC.ConvertSceneTo 1 %s' % OutputFileFormat)
                        
                    lx.eval('!scene.close')
                    
                    
                    
        if InputFileFormat == "OBJ" :
            for obj in os.listdir(Target_Path):
                if ".obj" in obj:
                    finalPath = Target_Path + "/" + obj
                    lx.eval("!!scene.open {%s} normal" % finalPath)
                    # lx.eval("!!scene.open {%s} import" % finalPath)
                    lx.eval('smo.CLEANUP.DelCam')
                    lx.eval('smo.CLEANUP.DelLight')
                    lx.eval('smo.GC.RenameMeshesBySceneName')
                    if OutputFileFormat == "LXO" :
                        lx.eval('smo.GC.ConvertSceneTo 1 %s' % OutputFileFormat)
                        
                    lx.eval('!scene.close')
        

    def cmd_Query(self, index, vaQuery):
        lx.notimpl()

lx.bless(SMO_BATCH_LoadFolderFilesByArg_Cmd, "smo.BATCH.LoadFolderFilesByArg")
# smo.BATCH.LoadFolderFilesByArg {DXF} {LXO}

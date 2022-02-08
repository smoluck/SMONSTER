#python
#---------------------------------------
# Name:         SMO_BATCH_SetOutputFileTypeViaPref_Cmd.py
# Version:      1.0
#
# Purpose:      This script is designed to:
#               Set the Input Files Format using User Defined Preferences.
#
#
# Author:       Franck ELISABETH (with the help of James O'Hare)
# Website:      http://www.smoluck.com
#
# Created:      01/10/2020
# Copyright:    (c) Franck Elisabeth 2017-2022
#---------------------------------------
import lx, lxu, modo

class SMO_BATCH_SetOutputFileTypeViaPref_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
        self.dyna_Add("Input File Format", lx.symbol.sTYPE_STRING)
        self.basic_SetFlags (0, lx.symbol.fCMDARG_OPTIONAL)             # here the (0) define the argument index.
        
    
    def cmd_Flags(self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO
    
    def cmd_Interact (self):
        pass
    
    def cmd_UserName (self):
        return 'SMO Batch Set Output File Type ia Pref'
    
    def cmd_Desc (self):
        return 'Set the Output Files Format using User Defined Preferences.'
    
    def cmd_Tooltip (self):
        return 'Set the Output Files Format using User Defined Preferences.'
    
    def cmd_Help (self):
        return 'https://twitter.com/sm0luck'
    
    def basic_ButtonName (self):
        return 'SMO Batch Set Output File Type ia Pref'
    
    def cmd_Flags (self):
        return lx.symbol.fCMD_UNDO
    
    def basic_Enable (self, msg):
        return True
        
    
    def basic_Execute(self, msg, flags):
        
        
        ################################
        #<----[ DEFINE VARIABLES ]---->#
        ################################
        lx.eval("user.defNew name:OutputFileFormat type:string life:momentary")
        ################################
        
        
        # ############### ARGUMENTS ###############
        OutputFileFormat = self.dyna_String (0)
        # ############### ARGUMENTS ###############
        
        
        if OutputFileFormat == "DXF" :
            lx.eval('user.value SMO_UseVal_BATCH_OutputFiles_DXF 1')
            lx.eval('user.value SMO_UseVal_BATCH_OutputFiles_SVG 0')
            lx.eval('user.value SMO_UseVal_BATCH_OutputFiles_OBJ 0')
            lx.eval('user.value SMO_UseVal_BATCH_OutputFiles_LXO 0')
            lx.eval('user.value SMO_UseVal_BATCH_OutputFiles_FBX 0')
            
        if OutputFileFormat == "SVG" :
            lx.eval('user.value SMO_UseVal_BATCH_OutputFiles_DXF 0')
            lx.eval('user.value SMO_UseVal_BATCH_OutputFiles_SVG 1')
            lx.eval('user.value SMO_UseVal_BATCH_OutputFiles_OBJ 0')
            lx.eval('user.value SMO_UseVal_BATCH_OutputFiles_LXO 0')
            lx.eval('user.value SMO_UseVal_BATCH_OutputFiles_FBX 0')
            
        if OutputFileFormat == "OBJ" :
            lx.eval('user.value SMO_UseVal_BATCH_OutputFiles_DXF 0')
            lx.eval('user.value SMO_UseVal_BATCH_OutputFiles_SVG 0')
            lx.eval('user.value SMO_UseVal_BATCH_OutputFiles_OBJ 1')
            lx.eval('user.value SMO_UseVal_BATCH_OutputFiles_LXO 0')
            lx.eval('user.value SMO_UseVal_BATCH_OutputFiles_FBX 0')
            
        if OutputFileFormat == "LXO" :
            lx.eval('user.value SMO_UseVal_BATCH_OutputFiles_DXF 0')
            lx.eval('user.value SMO_UseVal_BATCH_OutputFiles_SVG 0')
            lx.eval('user.value SMO_UseVal_BATCH_OutputFiles_OBJ 0')
            lx.eval('user.value SMO_UseVal_BATCH_OutputFiles_LXO 1')
            lx.eval('user.value SMO_UseVal_BATCH_OutputFiles_FBX 0')
            
        if OutputFileFormat == "FBX" :
            lx.eval('user.value SMO_UseVal_BATCH_OutputFiles_DXF 0')
            lx.eval('user.value SMO_UseVal_BATCH_OutputFiles_SVG 0')
            lx.eval('user.value SMO_UseVal_BATCH_OutputFiles_OBJ 0')
            lx.eval('user.value SMO_UseVal_BATCH_OutputFiles_LXO 0')
            lx.eval('user.value SMO_UseVal_BATCH_OutputFiles_FBX 1')
            
            

    def cmd_Query(self, index, vaQuery):
        lx.notimpl()

lx.bless(SMO_BATCH_SetOutputFileTypeViaPref_Cmd, "smo.BATCH.SetOutputFileTypeViaPref")
# smo.BATCH.SetOutputFileTypeViaPref {LXO}
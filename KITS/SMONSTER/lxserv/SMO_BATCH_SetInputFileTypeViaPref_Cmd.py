#python
#---------------------------------------
# Name:         SMO_BATCH_SetInputFileTypeViaPref_Cmd.py
# Version:      1.0
#
# Purpose:      This script is designed to:
#               Set the Input Files Format using User Defined Preferences.
#
#
# Author:       Franck ELISABETH
# Website:      http://www.smoluck.com
#
# Created:      01/10/2020
# Copyright:    (c) Franck Elisabeth 2017-2022
#---------------------------------------
import lx, lxu, modo

Cmd_Name = "smo.BATCH.SetInputFileTypeViaPref"
# smo.BATCH.SetInputFileTypeViaPref {DXF}

class SMO_BATCH_SetInputFileTypeViaPref_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
        self.dyna_Add("Input File Format", lx.symbol.sTYPE_STRING)
        self.basic_SetFlags (0, lx.symbol.fCMDARG_OPTIONAL)             # here the (0) define the argument index.
    
    def cmd_Flags(self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO
    
    def cmd_Interact (self):
        pass
    
    def cmd_UserName (self):
        return 'SMO BATCH - Set Input File Type via Pref'
    
    def cmd_Desc (self):
        return 'Set the Input Files Format using User Defined Preferences.'
    
    def cmd_Tooltip (self):
        return 'Set the Input Files Format using User Defined Preferences.'
    
    def cmd_Help (self):
        return 'https://twitter.com/sm0luck'
    
    def basic_ButtonName (self):
        return 'SMO BATCH - Set Input File Type via Pref'
    
    def basic_Enable (self, msg):
        return True

    def basic_Execute(self, msg, flags):
        
        
        ################################
        #<----[ DEFINE VARIABLES ]---->#
        ################################
        lx.eval("user.defNew name:InputFileFormat type:string life:momentary")
        ################################
        
        
        # ############### ARGUMENTS ###############
        InputFileFormat = self.dyna_String (0)
        # ############### ARGUMENTS ###############
        
        
        if InputFileFormat == "DXF" :
            lx.eval('user.value SMO_UseVal_BATCH_InputFiles_DXF 1')
            lx.eval('user.value SMO_UseVal_BATCH_InputFiles_SVG 0')
            lx.eval('user.value SMO_UseVal_BATCH_InputFiles_OBJ 0')
            lx.eval('user.value SMO_UseVal_BATCH_InputFiles_LXO 0')
            lx.eval('user.value SMO_UseVal_BATCH_InputFiles_FBX 0')
            lx.eval('user.value SMO_UseVal_BATCH_InputFiles_SLDPRT 0')
            
        if InputFileFormat == "SVG" :
            lx.eval('user.value SMO_UseVal_BATCH_InputFiles_DXF 0')
            lx.eval('user.value SMO_UseVal_BATCH_InputFiles_SVG 1')
            lx.eval('user.value SMO_UseVal_BATCH_InputFiles_OBJ 0')
            lx.eval('user.value SMO_UseVal_BATCH_InputFiles_LXO 0')
            lx.eval('user.value SMO_UseVal_BATCH_InputFiles_FBX 0')
            lx.eval('user.value SMO_UseVal_BATCH_InputFiles_SLDPRT 0')
            
        if InputFileFormat == "OBJ" :
            lx.eval('user.value SMO_UseVal_BATCH_InputFiles_DXF 0')
            lx.eval('user.value SMO_UseVal_BATCH_InputFiles_SVG 0')
            lx.eval('user.value SMO_UseVal_BATCH_InputFiles_OBJ 1')
            lx.eval('user.value SMO_UseVal_BATCH_InputFiles_LXO 0')
            lx.eval('user.value SMO_UseVal_BATCH_InputFiles_FBX 0')
            lx.eval('user.value SMO_UseVal_BATCH_InputFiles_SLDPRT 0')
            
        if InputFileFormat == "LXO" :
            lx.eval('user.value SMO_UseVal_BATCH_InputFiles_DXF 0')
            lx.eval('user.value SMO_UseVal_BATCH_InputFiles_SVG 0')
            lx.eval('user.value SMO_UseVal_BATCH_InputFiles_OBJ 0')
            lx.eval('user.value SMO_UseVal_BATCH_InputFiles_LXO 1')
            lx.eval('user.value SMO_UseVal_BATCH_InputFiles_FBX 0')
            lx.eval('user.value SMO_UseVal_BATCH_InputFiles_SLDPRT 0')
            
        if InputFileFormat == "FBX" :
            lx.eval('user.value SMO_UseVal_BATCH_InputFiles_DXF 0')
            lx.eval('user.value SMO_UseVal_BATCH_InputFiles_SVG 0')
            lx.eval('user.value SMO_UseVal_BATCH_InputFiles_OBJ 0')
            lx.eval('user.value SMO_UseVal_BATCH_InputFiles_LXO 0')
            lx.eval('user.value SMO_UseVal_BATCH_InputFiles_FBX 1')
            lx.eval('user.value SMO_UseVal_BATCH_InputFiles_SLDPRT 0')

        if InputFileFormat == "SLDPRT" :
            lx.eval('user.value SMO_UseVal_BATCH_InputFiles_DXF 0')
            lx.eval('user.value SMO_UseVal_BATCH_InputFiles_SVG 0')
            lx.eval('user.value SMO_UseVal_BATCH_InputFiles_OBJ 0')
            lx.eval('user.value SMO_UseVal_BATCH_InputFiles_LXO 0')
            lx.eval('user.value SMO_UseVal_BATCH_InputFiles_FBX 0')
            lx.eval('user.value SMO_UseVal_BATCH_InputFiles_SLDPRT 1')
            

    def cmd_Query(self, index, vaQuery):
        lx.notimpl()

lx.bless(SMO_BATCH_SetInputFileTypeViaPref_Cmd, Cmd_Name)

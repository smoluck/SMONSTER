#python
#---------------------------------------
# Name:         SMO_GC_SelectMTypMesh_Cmd.py
# Version:      1.0
#
# Purpose:      This script is designed to:
#               Select corresponding LowPoly / Cage / HighPoly meshes for further FBX Export.
#
#
#
# Author:       Franck ELISABETH
# Website:      http://www.smoluck.com
#
# Created:      30/11/2020
# Copyright:    (c) Franck Elisabeth 2017-2022
#---------------------------------------

import lx, lxu, modo

Command_Name = "smo.GC.SelectMTypMesh"
# smo.GC.SelectMTypMesh 0 ------ > Select LowPoly
# smo.GC.SelectMTypMesh 1 ------ > Select Cage
# smo.GC.SelectMTypMesh 2 ------ > Select HighPoly


class SMO_GC_SelectMTypMesh_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
        self.dyna_Add("Action Method from Tags", lx.symbol.sTYPE_INTEGER)
        self.basic_SetFlags (0, lx.symbol.fCMDARG_OPTIONAL)             # here the (0) define the argument index.
        # self.dyna_Add("Initial Projection", lx.symbol.sTYPE_INTEGER)
        # self.basic_SetFlags (1, lx.symbol.fCMDARG_OPTIONAL)
        
    def cmd_Flags(self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO
    
    def cmd_Interact (self):
        pass
    
    def cmd_UserName (self):
        return 'SMO GC Select Mesh Type for Game Export'
    
    def cmd_Desc (self):
        return 'Select corresponding LowPoly / Cage / HighPoly meshes for further FBX Export.'
    
    def cmd_Tooltip (self):
        return 'Select corresponding LowPoly / Cage / HighPoly meshes for further FBX Export.'
    
    def cmd_Help (self):
        return 'https://twitter.com/sm0luck'
    
    def basic_ButtonName (self):
        return 'SMO GC Select Mesh Type for Game Export'
    
    def cmd_Flags (self):
        return lx.symbol.fCMD_UNDO
    
    def basic_Enable (self, msg):
        return True
        
    
    def basic_Execute(self, msg, flags):
        # if not self.dyna_IsSet(0):
            # return False
        scene = modo.Scene()
        
        SelectMTypTag = self.dyna_Int (0)
        
        ################################
        #<----[ DEFINE VARIABLES ]---->#
        ################################
        # lx.eval("user.defNew name:itemUniqueName type:string life:momentary")
        # lx.eval("user.defNew name:MtypeTagValue type:string life:momentary")
        # lx.eval("user.defNew name:TagDetected type:boolean life:momentary")
        # lx.eval("user.defNew name:TagDetectedCount type:integer life:momentary")
        ################################
        
        if SelectMTypTag == 0 :
            lx.eval('!select.useSet MTyp_LowPoly select')
        if SelectMTypTag == 1 :
            lx.eval('!select.useSet MTyp_Cage select')
        if SelectMTypTag == 2 :
            lx.eval('!select.useSet MTyp_HighPoly select')
        
        
    
    def cmd_Query(self, index, vaQuery):
        lx.notimpl()

lx.bless(SMO_GC_SelectMTypMesh_Cmd, Command_Name)

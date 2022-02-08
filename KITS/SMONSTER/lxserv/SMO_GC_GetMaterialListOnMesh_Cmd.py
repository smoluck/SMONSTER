#python
#---------------------------------------
# Name:         SMO_GC_GetMaterialListOnMesh_Cmd.py
# Version:      1.0
#
# Purpose:      This script is designed to
#               Get the Material List applied on current selected Mesh.
# 
#
# Author:       Franck ELISABETH
# Website:      http://www.smoluck.com
#
# Created:      12/08/2020
# Copyright:    (c) Franck Elisabeth 2017-2022
#---------------------------------------

import lx, lxu, modo

Command_Name = "smo.GC.GetMaterialListOnMesh"
#query          smo.GC.GetMaterialListOnMesh ?

############# USE CASE
# MatsOnMesh = lx.eval('smo.GC.GetMaterialListOnMesh ?')
# lx.out('The Materials on this mesh are:',MatsOnMesh)
######################

class SMO_GC_GetMaterialListOnMesh_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
        self.dyna_Add("Material Name List", lx.symbol.sTYPE_STRING)
        self.basic_SetFlags (0, lx.symbol.fCMDARG_QUERY)
    def cmd_Flags(self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO
    
    def cmd_Interact (self):
        pass
    
    def cmd_UserName (self):
        return 'SMO GC Get Material List on Mesh'
    
    def cmd_Desc (self):
        return 'Get the Material List applied on current selected Mesh.'
    
    def cmd_Tooltip (self):
        return 'Get the Material List applied on current selected Mesh.'
    
    def cmd_Help (self):
        return 'https://twitter.com/sm0luck'
    
    def basic_ButtonName (self):
        return 'SMO GC Get Material List on Mesh'
    
    def cmd_Flags (self):
        return lx.symbol.fCMD_UNDO
    
    def basic_Enable (self, msg):
        return True
        
    
    def cmd_Query(self, index, vaQuery):
        scene = modo.scene.current()
        mesh = scene.selectedByType('mesh')[0]
        geo = mesh.geometry
        materialTags = [geo.PTagByIndex(lx.symbol.i_POLYTAG_MATERIAL, x)
        
        for x in range(geo.PTagCount(lx.symbol.i_POLYTAG_MATERIAL))]
        # print(materialTags)
        MatsOnMesh = list(materialTags)
        # lx.out ('Result of Query:', MatsOnMesh)
        MatStringList = '*TTTTTTT*'.join([str(item) for item in MatsOnMesh ])
        
        
        va = lx.object.ValueArray(vaQuery)
        va.AddString(MatStringList)
        return lx.result.OK
        
lx.bless(SMO_GC_GetMaterialListOnMesh_Cmd, Command_Name)


# import modo
# scene = modo.scene.current()
# mesh = scene.selectedByType('mesh')[0]
# geo = mesh.geometry
# materialTags = [geo.PTagByIndex(lx.symbol.i_POLYTAG_MATERIAL, x)
# for x in range(geo.PTagCount(lx.symbol.i_POLYTAG_MATERIAL))]
# print(materialTags)
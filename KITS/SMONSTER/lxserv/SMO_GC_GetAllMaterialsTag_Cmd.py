#python
#---------------------------------------
# Name:         SMO_GC_GetAllMaterialsTag_Cmd.py
# Version:      1.0
#
# Purpose:      This script is designed to
#               Get all the Material Tags in the scene.
#
#
# Author:       Franck ELISABETH
# Website:      http://www.smoluck.com
#
# Created:      12/08/2020
# Copyright:    (c) Franck Elisabeth 2017-2022
#---------------------------------------

import lx, lxu, modo

Command_Name = "smo.GC.GetAllMaterialsTag"
# query:        smo.GC.GetAllMaterialsTag ?

############# USE CASE
# TestResult = lx.eval('smo.GC.GetAllMaterialsTag ?')
# lx.out('Scene have those Materials:',TestResult)
######################


class SMO_GC_GetAllMaterialsTag_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
        self.dyna_Add("All Material Name List", lx.symbol.sTYPE_STRING)
        self.basic_SetFlags (0, lx.symbol.fCMDARG_QUERY)
    def cmd_Flags(self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO
    
    def cmd_Interact (self):
        pass
    
    def cmd_UserName (self):
        return 'SMO GC GetAllMaterialsTag'
    
    def cmd_Desc (self):
        return 'Get all the Material Tags in the scene.'
    
    def cmd_Tooltip (self):
        return 'Get all the Material Tags in the scene.'
    
    def cmd_Help (self):
        return 'https://twitter.com/sm0luck'
    
    def basic_ButtonName (self):
        return 'SMO GC GetAllMaterialsTag'
    
    def cmd_Flags (self):
        return lx.symbol.fCMD_UNDO
    
    def basic_Enable (self, msg):
        return True
        
        
    def cmd_Query(self, index, vaQuery):
        scene = modo.scene.current()
        
        materials = set()
        for mesh in scene.iterItems(lx.symbol.sITYPE_MESH):
            geo = mesh.geometry
            for x in range(geo.PTagCount(lx.symbol.i_PTAG_MATR)):
                materials.add(geo.PTagByIndex(lx.symbol.i_PTAG_MATR, x))
        AllMats = list(materials)
                
        # lx.out ('Result of Query:', AllMats)
        stringList = ' '.join([str(item) for item in AllMats ])
        va = lx.object.ValueArray(vaQuery)
        va.AddString(stringList)
        return lx.result.OK
                
    
lx.bless(SMO_GC_GetAllMaterialsTag_Cmd, Command_Name)

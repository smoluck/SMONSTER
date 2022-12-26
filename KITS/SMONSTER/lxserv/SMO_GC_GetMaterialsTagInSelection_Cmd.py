# python
"""
# Name:         SMO_GC_GetMaterialsTagInSelection_Cmd.py
# Version:      1.0
#
# Purpose:      This script is designed to
#               Get the Material Tags on current selection.
#
#
# Author:       Franck ELISABETH (with the help of Tom Dymond)
# Website:      https://www.smoluck.com
#
# Created:      12/08/2020
# Copyright:    (c) Franck Elisabeth 2017-2022
"""

import lx
import lxu
import modo

Cmd_Name = "smo.GC.GetMaterialsTagInSelection"
# query:        smo.GC.GetMaterialsTagInSelection ?

# ----------- USE CASE
# TestResult = lx.eval('smo.GC.GetMaterialsTagInSelection ?')
# lx.out('Current meshes have those materials:',TestResult)
# --------------------


class SMO_GC_GetMaterialsTagInSelection_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
        self.dyna_Add("Get Materials Tag in Selection", lx.symbol.sTYPE_STRING)
        self.basic_SetFlags (0, lx.symbol.fCMDARG_QUERY)
    def cmd_Flags(self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO
    
    def cmd_Interact (self):
        pass
    
    def cmd_UserName (self):
        return 'SMO GC - Get Materials Tag on Selection'
    
    def cmd_Desc (self):
        return 'Get the Material Tags on current selection.'
    
    def cmd_Tooltip (self):
        return 'Get the Material Tags on current selection.'
    
    def cmd_Help (self):
        return 'https://twitter.com/sm0luck'
    
    def basic_ButtonName (self):
        return 'SMO GC - Get Materials Tag on Selection'
    
    def basic_Enable (self, msg):
        return True
        
    def cmd_Query(self, index, vaQuery):
        scene = modo.scene.current()
        
        materials = set()
        selection = list(scene.selectedByType('mesh'))
        for mesh in selection :
            geo = mesh.geometry
            for x in range(geo.PTagCount(lx.symbol.i_PTAG_MATR)):
                materials.add(geo.PTagByIndex(lx.symbol.i_PTAG_MATR, x))
        Mats = list(materials)
                
        # lx.out ('Result of Query:', Mats)
        
        stringList = ' '.join([str(item) for item in Mats ])
        va = lx.object.ValueArray(vaQuery)
        va.AddString(stringList)
        return lx.result.OK
                
    
lx.bless(SMO_GC_GetMaterialsTagInSelection_Cmd, Cmd_Name)

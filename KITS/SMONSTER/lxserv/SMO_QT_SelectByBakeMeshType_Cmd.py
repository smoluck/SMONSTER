# python
"""
# Name:         SMO_QuickTag_SelectByBakeMeshType_Cmd.py
# Version:      1.0
#
# Purpose:      This script is designed to:
#               Add an MTyp Tag to the current selected Mesh item. it define it as low or high poly mesh for Baking purpose.
#
#
# Author:       Franck ELISABETH
# Website:      https://www.smoluck.com
#
# Created:      25/11/2020
# Copyright:    (c) Franck Elisabeth 2017-2022
"""

import lx
import lxu
import modo

Cmd_Name = "smo.QT.SelectByBakeMeshType"
# smo.QT.SelectByBakeMeshType 0


class SMO_QT_SelectByBakeMeshType_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
        self.dyna_Add("SelectByBakeMeshType", lx.symbol.sTYPE_INTEGER)
        self.basic_SetFlags (0, lx.symbol.fCMDARG_OPTIONAL)             # here the (0) define the argument index.
    
    def cmd_Flags(self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO
    
    def cmd_Interact (self):
        pass
    
    def cmd_UserName (self):
        return 'SMO QT - Bake Mesh Type'
    
    def cmd_Desc (self):
        return 'Add an MTyp Tag to the current selected Mesh item. it define it as low or high poly mesh for Baking purpose.'
    
    def cmd_Tooltip (self):
        return 'Add an MTyp Tag to the current selected Mesh item. it define it as low or high poly mesh for Baking purpose.'
    
    def cmd_Help (self):
        return 'https://twitter.com/sm0luck'
    
    def basic_ButtonName (self):
        return 'SMO QT - Bake Mesh Type'
    
    def basic_Enable (self, msg):
        return True
    
    def basic_Execute(self, msg, flags):
        
        # ------------------------------ #
        # <----( DEFINE VARIABLES )----> #
        # ------------------------------ #
        lx.eval("user.defNew name:SelectByBakeMeshType type:integer life:momentary")
        # ------------------------------ #
        
        # # ------------- ARGUMENTS ------------- #
        SelectByBakeMeshType = self.dyna_Int (0)
        # 1 = low
        # 2 = cage
        # 3 = high
        # # ------------- ARGUMENTS ------------- #
        scene = modo.scene.current()
        searchedtag = 'MTyp'

        lx.eval('select.drop item')
        lx.eval('select.itemType mesh')
        MeshItemList = []
        MeshItemList = lx.eval('query sceneservice selection ? mesh')
        # lx.out('Mesh list:', MeshItemList)
        
        for item in MeshItemList :
            tagtypes = lx.evalN('query sceneservice item.tagTypes ? %s' % searchedtag)
            
        meshes_list = scene.selectedByType(lx.symbol.sITYPE_MESH)
        tagtypes = lx.evalN('query sceneservice      ? %s' % searchedtag)
        # lx.out('Mesh tag type:', tagtypes)
        
        # pos=MTyp.find("p")
        # lx.out('Mesh tag type:', ppos)
        
        if "MTyp" in tagtypes:
            lx.eval('select.item %s mode:set' % searchedtag)
            MTyp = lx.eval('item.tag mode:string tag:"RGCH" value:?')
                
    
    def cmd_Query(self, index, vaQuery):
        lx.notimpl()


lx.bless(SMO_QT_SelectByBakeMeshType_Cmd, Cmd_Name)

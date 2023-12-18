# python
"""
Name:         SMO_QuickTag_BakeMeshType_Cmd.py

Purpose:      This script is designed to:
              Add an MTyp Tag to the current selected Mesh item. it define it as low or high poly mesh for Baking purpose.

Author:       Franck ELISABETH
Website:      https://www.linkedin.com/in/smoluck/
Created:      25/11/2020
Copyright:    (c) Franck Elisabeth 2017-2022
"""

import lx
import lxu
import modo

Cmd_Name = "smo.QT.TagBakeMeshType"
# smo.QT.TagBakeMeshType 0


class SMO_QT_TagBakeMeshType_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
        self.dyna_Add("Tag Bake Mesh Type", lx.symbol.sTYPE_INTEGER)
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
        scene = modo.scene.current()
        # ------------------------------ #
        # <----( DEFINE VARIABLES )----> #
        # ------------------------------ #
        lx.eval("user.defNew name:Tag_BakeMeshType type:integer life:momentary")
        # ------------------------------ #
        
        
        # ------------- ARGUMENTS ------------- #
        Tag_BakeMeshType = self.dyna_Int (0)
        # 0 = Remove tag
        # 1 = low
        # 2 = cage
        # 3 = high
        # ------------- ARGUMENTS ------------- #
        
        MeshItem_List = scene.selected
        # MeshItem_List = scene.selectedByType(lx.symbol.sITYPE_MESH)
        for mesh in MeshItem_List:
            mesh.select(True)
            
            # Tag "MTyp" is for: Mesh Type
            if Tag_BakeMeshType == 0:
                lx.eval ('!item.tagRemove MTyp')
            if Tag_BakeMeshType == 1:
                lx.eval ('item.tag string MTyp LowPoly')
                lx.eval ('!smo.CB.ItemColor 8 0')
            if Tag_BakeMeshType == 2:
                lx.eval ('item.tag string MTyp Cage')
                lx.eval ('!smo.CB.ItemColor 7 0')
            if Tag_BakeMeshType == 3:
                lx.eval ('item.tag string MTyp HighPoly')
                lx.eval ('!smo.CB.ItemColor 11 0')
        
    
    def cmd_Query(self, index, vaQuery):
        lx.notimpl()


lx.bless(SMO_QT_TagBakeMeshType_Cmd, Cmd_Name)


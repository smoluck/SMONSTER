# python
"""
Name:         SMO_GC_SelectTextureLayerItem_Cmd.py

Purpose:      This script is designed to
              Select the Texture Layer Item of the current scene or query is Ident name.

Author:       Franck ELISABETH (with the help of Tom Dymond)
Website:      https://www.smoluck.com
Created:      12/08/2020
Copyright:    (c) Franck Elisabeth 2017-2022
"""

import lx
import lxu
import modo

Cmd_Name = "smo.GC.SelectTextureLayerItem"
# execute:      smo.GC.SelectTextureLayerItem
# query:        smo.GC.SelectTextureLayerItem ?

# ------ USE CASE
# TestResult = lx.eval('smo.GC.SelectTextureLayerItem ?')
# lx.out('Texture Layer item Identity name is :',TestResult)
# ---------------


class SMO_GC_SelectTextureLayerItem_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
        self.dyna_Add("TextureLayer Item Name", lx.symbol.sTYPE_STRING)
        self.basic_SetFlags (0, lx.symbol.fCMDARG_QUERY)

    def cmd_Flags(self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO
    
    def cmd_Interact (self):
        pass
    
    def cmd_UserName (self):
        return 'SMO GC - Select TextureLayer Item'
    
    def cmd_Desc (self):
        return 'Select the Texture Layer Item of the current scene.'
    
    def cmd_Tooltip (self):
        return 'Select the Texture Layer Item of the current scene.'
    
    def cmd_Help (self):
        return 'https://twitter.com/sm0luck'
    
    def basic_ButtonName (self):
        return 'SMO GC - Select TextureLayer Item'
    
    def basic_Enable (self, msg):
        return True

    def basic_Execute(self, msg, flags):
        scene = modo.scene.current()

        # Get the item count
        n = lx.eval1( 'query sceneservice item.N ?' )
        
        # Loop through the items in the scene, looking for output items
        for i in range(n):
            itemtype = lx.eval( 'query sceneservice item.type ? %s' % i )
            if itemtype == "textureLayer":
                # Get the item ID
                TextureLayerItemID = lx.eval( 'query sceneservice item.id ?')
                lx.out( 'TextureLayer Item ID:', TextureLayerItemID )
                # lx.eval ('!!user.value Smo_PolyRenderItemName {%s}' % TextureLayerItemID)
        lx.eval('select.subItem {%s} set textureLayer;light;render;environment' % TextureLayerItemID)
        
        
    def cmd_Query(self, index, vaQuery):
        scene = modo.scene.current()
        
        
        # Get the item count
        n = lx.eval1( 'query sceneservice item.N ?' )
        
        # Loop through the items in the scene, looking for output items
        for i in range(n):
            itemtype = lx.eval( 'query sceneservice item.type ? %s' % i )
            if itemtype == "textureLayer":
                # Get the item ID
                TextureLayerItemID = lx.eval( 'query sceneservice item.id ?')
                
                lx.out ('Result of Query:', TextureLayerItemID)
                va = lx.object.ValueArray(vaQuery)
                va.AddString(TextureLayerItemID)
                return lx.result.OK

    
lx.bless(SMO_GC_SelectTextureLayerItem_Cmd, Cmd_Name)

# python
"""
Name:         SMO_GC_SelectTextureLocatorItem_Cmd

Purpose:      This script is designed to
              Select the PolyRender Item of the current scene or query is Ident name.

Author:       Franck ELISABETH (with the help of Tom Dymond)
Website:      https://www.smoluck.com
Created:      12/08/2020
Copyright:    (c) Franck Elisabeth 2017-2022
"""

import lx
import lxu
import modo

Cmd_Name = "smo.GC.SelectTextureLocatorItem"
# execute:      smo.GC.SelectTextureLocatorItem
# query:        smo.GC.SelectTextureLocatorItem ?

# ------ USE CASE
# TestResult = lx.eval('smo.GC.SelectTextureLocatorItem ?')
# lx.out('Shader item Identity name is :',TestResult)
# ---------------


class SMO_GC_SelectTextureLocatorItem_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
        self.dyna_Add("TextureLocator Item Name", lx.symbol.sTYPE_STRING)
        self.basic_SetFlags (0, lx.symbol.fCMDARG_QUERY)

    def cmd_Flags(self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO
    
    def cmd_Interact (self):
        pass
    
    def cmd_UserName (self):
        return 'SMO GC - Select Texture Locator Item'
    
    def cmd_Desc (self):
        return 'Select the Shader Item of the current scene.'
    
    def cmd_Tooltip (self):
        return 'Select the Shader Item of the current scene.'
    
    def cmd_Help (self):
        return 'https://twitter.com/sm0luck'
    
    def basic_ButtonName (self):
        return 'SMO GC - Select Texture Locator Item'
    
    def basic_Enable (self, msg):
        return True
    
    def basic_Execute(self, msg, flags):
        scene = modo.scene.current()
        
        # clear selection of any item in the scene.
        lx.eval('select.clear item')
        lx.eval('select.drop schmNode')
        lx.eval('select.drop channel')
        lx.eval('select.drop link')
        
        # Get the item count
        n = lx.eval1( 'query sceneservice item.N ?' )
        
        # Loop through the items in the scene, looking for output items
        for i in range(n):
            itemtype = lx.eval( 'query sceneservice item.type ? %s' % i )
            if itemtype == "txtrLocator":
                # Get the item ID
                TextureLocatorItemID = lx.eval( 'query sceneservice item.id ?')
                # lx.out( 'PolyRender Item ID:', TextureLocatorItemID )
                lx.eval ('!!user.value Smo_PolyRenderItemName {%s}' % TextureLocatorItemID)
        lx.eval('select.subItem {%s} set textureLayer;light;render;environment' % TextureLocatorItemID)
        
        
    def cmd_Query(self, index, vaQuery):
        scene = modo.scene.current()
        
        # clear selection of any item in the scene.
        lx.eval('select.clear item')
        lx.eval('select.drop schmNode')
        lx.eval('select.drop channel')
        lx.eval('select.drop link')
        
        
        # Get the item count
        n = lx.eval1( 'query sceneservice item.N ?' )
        
        # Loop through the items in the scene, looking for output items
        for i in range(n):
            itemtype = lx.eval( 'query sceneservice item.type ? %s' % i )
            if itemtype == "txtrLocator":
                # Get the item ID
                TextureLocatorItemID = lx.eval( 'query sceneservice item.id ?')
                
                lx.out ('Result of Query:', TextureLocatorItemID)
                va = lx.object.ValueArray(vaQuery)
                va.AddString(TextureLocatorItemID)
                return lx.result.OK
                
    
lx.bless(SMO_GC_SelectTextureLocatorItem_Cmd, Cmd_Name)

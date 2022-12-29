# python
"""
Name:         SMO_GC_SelectPolyRenderItem_Cmd.py

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

Cmd_Name = "smo.GC.SelectPolyRenderItem"
# execute:      smo.GC.SelectPolyRenderItem
# query:        smo.GC.SelectPolyRenderItem ?

# ------ USE CASE
# TestResult = lx.eval('smo.GC.SelectPolyRenderItem ?')
# lx.out('Render item Identity name is :',TestResult)
# ---------------


class SMO_GC_SelectPolyRenderItem_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
        self.dyna_Add("Render Item Name", lx.symbol.sTYPE_STRING)
        self.basic_SetFlags (0, lx.symbol.fCMDARG_QUERY)

    def cmd_Flags(self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO
    
    def cmd_Interact (self):
        pass
    
    def cmd_UserName (self):
        return 'SMO GC - Select PolyRender Item'
    
    def cmd_Desc (self):
        return 'Select the PolyRender Item of the current scene.'
    
    def cmd_Tooltip (self):
        return 'Select the PolyRender Item of the current scene.'
    
    def cmd_Help (self):
        return 'https://twitter.com/sm0luck'
    
    def basic_ButtonName (self):
        return 'SMO GC - Select PolyRender Item'
    
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
            if itemtype == "polyRender":
                # Get the item ID
                PolyRenderItemID = lx.eval( 'query sceneservice item.id ?')
                # lx.out( 'PolyRender Item ID:', PolyRenderItemID )
                lx.eval ('!!user.value Smo_PolyRenderItemName {%s}' % PolyRenderItemID)
        lx.eval('select.subItem {%s} set textureLayer;light;render;environment' % PolyRenderItemID)
        
        
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
            if itemtype == "polyRender":
                # Get the item ID
                PolyRenderItemID = lx.eval( 'query sceneservice item.id ?')
                
                # lx.out ('Result of Query:', PolyRenderItemID)
                va = lx.object.ValueArray(vaQuery)
                va.AddString(PolyRenderItemID)
                return lx.result.OK
                
    
lx.bless(SMO_GC_SelectPolyRenderItem_Cmd, Cmd_Name)

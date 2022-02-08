#python
#---------------------------------------
# Name:         SMO_GC_SelectShaderItem_Cmd.py
# Version:      1.0
#
# Purpose:      This script is designed to
#               Select the PolyRender Item of the current scene or query is Ident name.
#
#
# Author:       Franck ELISABETH (with the help of Tom Dymond)
# Website:      http://www.smoluck.com
#
# Created:      12/08/2020
# Copyright:    (c) Franck Elisabeth 2017-2022
#---------------------------------------

import lx, lxu, modo

Command_Name = "smo.GC.SelectShaderItem"
# execute:      smo.GC.SelectShaderItem
# query:        smo.GC.SelectShaderItem ?

############# USE CASE
# TestResult = lx.eval('smo.GC.SelectShaderItem ?')
# lx.out('Shader item Identity name is :',TestResult)
######################


class SMO_GC_SelectShaderItem_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
        self.dyna_Add("Shader Item Name", lx.symbol.sTYPE_STRING)
        self.basic_SetFlags (0, lx.symbol.fCMDARG_QUERY)
    def cmd_Flags(self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO
    
    def cmd_Interact (self):
        pass
    
    def cmd_UserName (self):
        return 'SMO GC SelectShaderItem'
    
    def cmd_Desc (self):
        return 'Select the Shader Item of the current scene.'
    
    def cmd_Tooltip (self):
        return 'Select the Shader Item of the current scene.'
    
    def cmd_Help (self):
        return 'https://twitter.com/sm0luck'
    
    def basic_ButtonName (self):
        return 'SMO GC SelectShaderItem'
    
    def cmd_Flags (self):
        return lx.symbol.fCMD_UNDO
    
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
            if itemtype == "defaultShader":
                # Get the item ID
                ShaderItemID = lx.eval( 'query sceneservice item.id ?')
                # lx.out( 'PolyRender Item ID:', ShaderItemID )
                lx.eval ('!!user.value Smo_PolyRenderItemName {%s}' % ShaderItemID)
        lx.eval('select.subItem {%s} set textureLayer;light;render;environment' % ShaderItemID)
        
        
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
            if itemtype == "defaultShader":
                # Get the item ID
                ShaderItemID = lx.eval( 'query sceneservice item.id ?')
                
                # lx.out ('Result of Query:', ShaderItemID)
                va = lx.object.ValueArray(vaQuery)
                va.AddString(ShaderItemID)
                return lx.result.OK
                
                
    
lx.bless(SMO_GC_SelectShaderItem_Cmd, Command_Name)

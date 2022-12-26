# python
"""
# Name:         SMO_GC_GetShaderItemPosIndex_Cmd.py
# Version:      1.0
#
# Purpose:      This script is designed to
#               Get the Position Index of the Shader Item (in the Shader Tree of the current scene).
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

Cmd_Name = "smo.GC.GetShaderItemPosIndex"
# query:        smo.GC.GetShaderItemPosIndex ?

# ----------- USE CASE
# TestResult = lx.eval('smo.GC.GetShaderItemPosIndex ?')
# lx.out('Position Index of the Shader Item (in the Shader Tree) is :',TestResult)
# --------------------


class SMO_GC_GetShaderItemPosIndex_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
        self.dyna_Add("Shader Item Position Index in Shader Tree", lx.symbol.sTYPE_INTEGER)
        self.basic_SetFlags (0, lx.symbol.fCMDARG_QUERY)

    def cmd_Flags(self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO
    
    def cmd_Interact (self):
        pass
    
    def cmd_UserName (self):
        return 'SMO GC - Get Shader Item Position Index'
    
    def cmd_Desc (self):
        return 'Get the Position Index of the Shader Item (in the Shader Tree of the current scene).'
    
    def cmd_Tooltip (self):
        return 'Get the Position Index of the Shader Item (in the Shader Tree of the current scene).'
    
    def cmd_Help (self):
        return 'https://twitter.com/sm0luck'
    
    def basic_ButtonName (self):
        return 'SMO GC - Get Shader Item Position Index'
    
    def basic_Enable (self, msg):
        return True
        
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
                shader = scene.items(lx.symbol.sITYPE_DEFAULTSHADER)[0]
                ShaderItemPosIndex = shader.parentIndex
                
                # lx.out ('Result of Query:', ShaderItemPosIndex)
                va = lx.object.ValueArray(vaQuery)
                va.AddInt(ShaderItemPosIndex)
                return lx.result.OK


lx.bless(SMO_GC_GetShaderItemPosIndex_Cmd, Cmd_Name)

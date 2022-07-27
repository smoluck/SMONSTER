#python
#---------------------------------------
# Name:         SMO_GC_LoadStillImageInShaderTree_Cmd.py
# Version:      1.0
#
# Purpose:      This script is designed to
#               Select the still images (clips) Item of the current scene.
# 
#
# Author:       Franck ELISABETH (with the help of Tom Dymond)
# Website:      http://www.smoluck.com
#
# Created:      12/08/2020
# Copyright:    (c) Franck Elisabeth 2017-2022
#---------------------------------------

import lx, lxu, modo

Cmd_Name = "smo.GC.LoadStillImageInShaderTree"
# smo.GC.LoadStillImageInShaderTree

class SMO_GC_LoadStillImageInShaderTree_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
    def cmd_Flags(self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO
    
    def cmd_Interact (self):
        pass
    
    def cmd_UserName (self):
        return 'SMO GC - Select Still Image Item'
    
    def cmd_Desc (self):
        return 'Load the still images (clips) Item of the current scene to preview the PixaFlux Bake.'
    
    def cmd_Tooltip (self):
        return 'Select the still images (clips) Item of the current scene.'
    
    def cmd_Help (self):
        return 'https://twitter.com/sm0luck'
    
    def basic_ButtonName (self):
        return 'SMO GC - Select Still Image Item'
    
    def basic_Enable (self, msg):
        return True
    
    def basic_Execute(self, msg, flags):
        scene = modo.scene.current()
        
        PolyRender = lx.eval('smo.GC.SelectPolyRenderItem ?')
        # StillImage = lx.eval('!!user.value Smo_StillImageItemName ?')
        StillImage = lx.eval('smo.GC.SelectStillImageItem ?')
        
        
        videoStill =  scene.selectedByType(lx.symbol.sITYPE_VIDEOSTILL)
        lx.eval('select.subItem {%s} set textureLayer;light;render;environment' % PolyRender)
        lx.eval('texture.new clip:{%s}' % StillImage)
        lx.eval('texture.parent {%s} 1' % PolyRender)
        
        
        # Drop current item selection Scene wise
        
        lx.eval('select.clear item')
        lx.eval('select.drop schmNode')
        lx.eval('select.drop channel')
        lx.eval('select.drop link')
        
        #####--------------------  Compare TotalSafetyCheck value and decide or not to continue the process  --- END --------------------#####


lx.bless(SMO_GC_LoadStillImageInShaderTree_Cmd, Cmd_Name)

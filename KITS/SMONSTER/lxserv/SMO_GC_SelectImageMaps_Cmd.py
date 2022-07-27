#python
#---------------------------------------
# Name:         SMO_GC_SelectImageMaps_Cmd.py
# Version:      1.0
#
# Purpose:      This script is designed to
#               Select a still images (clips) Item of the current scene and set is Effect mode via arguments.
# 
#
# Author:       Franck ELISABETH (with the help of Tom Dymond)
# Website:      http://www.smoluck.com
#
# Created:      12/08/2020
# Copyright:    (c) Franck Elisabeth 2017-2022
#---------------------------------------

import lx, lxu, modo

Cmd_Name = "smo.GC.SelectImageMaps"
# smo.GC.SelectImageMaps 0

class SMO_GC_SelectImageMaps_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
        self.dyna_Add("Select it or Create image", lx.symbol.sTYPE_BOOLEAN)
        self.basic_SetFlags (0, lx.symbol.fCMDARG_OPTIONAL)                     # here the (0) define the argument index.
        self.dyna_Add("Deselect / Keep Selected", lx.symbol.sTYPE_BOOLEAN)
        self.basic_SetFlags (1, lx.symbol.fCMDARG_OPTIONAL)
        self.dyna_Add("Placement Index in Shader Tree", lx.symbol.sTYPE_INTEGER)
        self.basic_SetFlags (2, lx.symbol.fCMDARG_OPTIONAL)
        self.dyna_Add("Effect Mode", lx.symbol.sTYPE_INTEGER)
        self.basic_SetFlags (3, lx.symbol.fCMDARG_OPTIONAL)
    def cmd_Flags(self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO
    
    def cmd_Interact (self):
        pass
    
    def cmd_UserName (self):
        return 'SMO GC - Select Still Image Item'
    
    def cmd_Desc (self):
        return 'Select a still images (clips) Item of the current scene and set is Effect mode via arguments.'
    
    def cmd_Tooltip (self):
        return 'Select a still images (clips) Item of the current scene and set is Effect mode via arguments.'
    
    def cmd_Help (self):
        return 'https://twitter.com/sm0luck'
    
    def basic_ButtonName (self):
        return 'SMO GC - Select Still Image Item'
    
    def basic_Enable (self, msg):
        return True

    def basic_Execute(self, msg, flags):
        scene = modo.scene.current()
        
        
        
        ############### 4 ARGUMENTS ###############
        # 0 = Select the image
        # 1 = Create it
        ActionMode = self.dyna_Bool (0)
        
        
        # 0 = Deselect it
        # 1 = Keep it Selected
        EndAction = self.dyna_Bool (1)
        
        
        # 1 = Above Basic Material
        PlacementIndex = self.dyna_Int (2)
        
        
        # 0 = AO Map
        # 1 = Tangent Space Normal Map
        # 2 = Object Space Normal Map
        # 3 = Position Map
        # 4 = Curvature Map
        # 5 = Object ID Map
        # 6 = Thickness Map
        EffectMode = self.dyna_Int (3)
        ###########################################
        
        
        
        PolyRender = lx.eval('smo.GC.SelectPolyRenderItem ?')
        StillImage = lx.eval('smo.GC.SelectStillImageItem ?')
        
        # lx.eval('smo.GC.SelectPolyRenderItem')
        # lx.eval('smo.GC.SelectStillImageItem')
        # PolyRender = lx.eval('!!user.value Smo_PolyRenderItemName ?')
        # StillImage = lx.eval('!!user.value Smo_StillImageItemName ?')
        
        videoStill =  scene.selectedByType(lx.symbol.sITYPE_VIDEOSTILL)
        lx.eval('select.subItem {%s} set textureLayer;light;render;environment' % PolyRender)
        lx.eval('texture.new clip:{%s}' % StillImage)
        lx.eval('texture.parent {%s} 1' % PolyRender)
        
        
        # Set the Baked image to AO map Mode
        if EffectMode == 0 :
            lx.eval('shader.setEffect diffColor')
            lx.eval('item.channel textureLayer$blend multiply')
            lx.eval('item.channel textureLayer$opacity 0.8')
            
        # Set the Baked image to Tangent Space Normal map Mode
        if EffectMode == 1 :
            lx.eval('shader.setEffect normal')
            # lx.eval('item.channel videoStill$colorspace "nuke-default:linear"')
            
        # Set the Baked image to Object Space Normal map Mode
        if EffectMode == 2 :
            lx.eval('shader.setEffect diffColor')
            lx.eval('item.channel textureLayer$blend normal')
            lx.eval('item.channel textureLayer$opacity 1.0')
            
        # Set the Baked image to Position map Mode
        if EffectMode == 3 :
            lx.eval('shader.setEffect diffColor')
            lx.eval('item.channel textureLayer$blend normal')
            lx.eval('item.channel textureLayer$opacity 1.0')
            
        # Set the Baked image to Curvature map Mode
        if EffectMode == 4 :
            lx.eval('shader.setEffect diffColor')
            lx.eval('item.channel textureLayer$blend normal')
            lx.eval('item.channel textureLayer$opacity 1.0')
            
        # Set the Baked image to Object ID map Mode
        if EffectMode == 5 :
            lx.eval('shader.setEffect diffColor')
            lx.eval('item.channel textureLayer$blend normal')
            lx.eval('item.channel textureLayer$opacity 1.0')
            
        # Set the Baked image to Thickness map Mode
        if EffectMode == 6 :
            lx.eval('shader.setEffect diffColor')
            lx.eval('item.channel textureLayer$blend normal')
            lx.eval('item.channel textureLayer$opacity 1.0')
            
        if EndAction == 0 :
            # Drop current item selection Scene wise
            lx.eval('select.clear item')
            lx.eval('select.drop schmNode')
            lx.eval('select.drop channel')
            lx.eval('select.drop link')


lx.bless(SMO_GC_SelectImageMaps_Cmd, Cmd_Name)

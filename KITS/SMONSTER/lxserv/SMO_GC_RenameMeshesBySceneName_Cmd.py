# python
"""
# Name:         SMO_GC_RenameMeshesBySceneName_Cmd.py
# Version:      1.0
#
# Purpose:      This script is designed to:
#               Get the scene name and add this  name as
#               a Prefix on every Meshes in the current scene.
#               Script will save the scene in same places as the current opened scene.
#
# Author:       Franck ELISABETH (with the help of James O'Hare)
# Website:      https://www.smoluck.com
#
# Created:      30/09/2020
# Copyright:    (c) Franck Elisabeth 2017-2022
"""

from os import path

import lx
import lxu
import modo

Cmd_Name = "smo.GC.RenameMeshesBySceneName"
# smo.GC.RenameMeshesBySceneName


class SMO_GC_RenameMeshesBySceneName_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
        self.dyna_Add("SearchString", lx.symbol.sTYPE_STRING)
        self.basic_SetFlags (0, lx.symbol.fCMDARG_OPTIONAL)             # here the (0) define the argument index.
    
    def cmd_Flags(self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO
    
    def cmd_Interact (self):
        pass
    
    def cmd_UserName (self):
        return 'SMO GC - Rename Meshes By Scene Name'
    
    def cmd_Desc (self):
        return 'Get the scene name and add this  name as a Prefix on every Meshes in the current scene. Script will save the scene in same places as the current opened scene.'
    
    def cmd_Tooltip (self):
        return 'Get the scene name and add this  name as a Prefix on every Meshes in the current scene. Script will save the scene in same places as the current opened scene.'
    
    def cmd_Help (self):
        return 'https://twitter.com/sm0luck'
    
    def basic_ButtonName (self):
        return 'SMO GC - Rename Meshes By Scene Name'
    
    def basic_Enable (self, msg):
        return True
    
    def basic_Execute(self, msg, flags):
        # Get the name of the scene, wihout the filepath and extension
        scene = modo.Scene()
        scene_FileName = lx.eval('query sceneservice scene.name ? main') # Select the scene
        # lx.out('Scene Name:', scene_FileName)
        if scene_FileName:
            Scene_Name = path.splitext( path.basename(scene_FileName) )[0]
            lx.out('Scene Name:', Scene_Name)
        
        # Drop layer selection
        lx.eval('select.drop item')
        lx.eval('select.itemType mesh')
        MeshItem_List = scene.selectedByType(lx.symbol.sITYPE_MESH)
        for a in MeshItem_List:
            a.select(True)
            Mesh_Name = lx.eval('item.name ? xfrmcore')
            ModifiedName = Scene_Name + '_' + Mesh_Name 
            lx.eval('item.name {%s} xfrmcore' % ModifiedName)
        lx.eval('select.drop item')
    
    
lx.bless(SMO_GC_RenameMeshesBySceneName_Cmd, Cmd_Name)

# python
"""
# Name:         SMO_CLEANUP_ConvertItemIndexStyleSceneWise_Cmd.py
# Version:      1.0
#
# Purpose:      This script is designed to:
#               Check if the current Modo Item Index Style set in Preferences and
#               Rename all the items (Locator, GroupLocators, Meshes),
#               if they use mixed Index Style or if they use a different Index Style than the one in Modo Preferences.
#
# Author:       Franck ELISABETH
# Website:      https://www.smoluck.com
#
# Created:      27/12/2020
# Copyright:    (c) Franck Elisabeth 2017-2022
"""

import lx
import lxu
import modo

Cmd_Name = "smo.CLEANUP.ConvertItemIndexStyleSceneWise"
# smo.CLEANUP.ConvertItemIndexStyleSceneWise


class SMO_Cleanup_ConvertItemIndexStyleSceneWise_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)

    def cmd_Flags(self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO
    
    def cmd_Interact (self):
        pass
    
    def cmd_UserName (self):
        return 'SMO CLEANUP - (SceneWise) Convert Item Index Style'
    
    def cmd_Desc (self):
        return 'Check if the current Modo Item Index Style set in Preferences and Rename all the items (Locator, GroupLocators, Meshes), if they use mixed Index Style or if they use a different Index Style than the one in Modo Preferences.'
    
    def cmd_Tooltip (self):
        return 'Check if the current Modo Item Index Style set in Preferences and Rename all the items (Locator, GroupLocators, Meshes), if they use mixed Index Style or if they use a different Index Style than the one in Modo Preferences.'
    
    def cmd_Help (self):
        return 'https://twitter.com/sm0luck'
    
    def basic_ButtonName (self):
        return 'SMO CLEANUP - (SceneWise) Convert Item Index Style'
    
    def basic_Enable (self, msg):
        return True
    
    def basic_Execute(self, msg, flags):
        scene = modo.scene.current()
        # MeshItem_List = scene.selected
        lx.eval('select.itemType groupLocator')
        selitems = len(lx.evalN('query sceneservice selection ? all'))
        # lx.out('selitems',selitems)
        if selitems > 0 :
            lx.eval('smo.CLEANUP.ConvertItemIndexStyle')
            lx.eval('select.drop item')
        
        lx.eval('select.itemType locator')
        selitems = len(lx.evalN('query sceneservice selection ? all'))
        # lx.out('selitems',selitems)
        if selitems > 0 :
            lx.eval('smo.CLEANUP.ConvertItemIndexStyle')
            lx.eval('select.drop item')
        
        lx.eval('select.itemType mesh')
        selitems = len(lx.evalN('query sceneservice selection ? all'))
        # lx.out('selitems',selitems)
        if selitems > 0 :
            lx.eval('smo.CLEANUP.ConvertItemIndexStyle')
            lx.eval('select.drop item')
        
    
lx.bless(SMO_Cleanup_ConvertItemIndexStyleSceneWise_Cmd, Cmd_Name)

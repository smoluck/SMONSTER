# python
"""
Name:         SMO_CLEANUP_ConvertItemIndexStyle_Cmd.py

Purpose:      This script is designed to:
              Check if the current Modo Item Index Style set in Preferences and
              Rename all the selected items, if they use mixed Index Style or
              if they use a different Index Style than the one in Modo Preferences.

Author:       Franck ELISABETH
Website:      https://www.linkedin.com/in/smoluck/
Created:      27/12/2020
Copyright:    (c) Franck Elisabeth 2017-2022
"""

import lx
import lxu
import modo

Cmd_Name = "smo.CLEANUP.ConvertItemIndexStyle"
# smo.GC.ConvertItemIndexStyle


class SMO_Cleanup_ConvertItemIndexStyle_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)

    def cmd_Flags(self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO
    
    def cmd_Interact (self):
        pass
    
    def cmd_UserName (self):
        return 'SMO CLEANUP - Convert Item Index Style'
    
    def cmd_Desc (self):
        return 'Check if the current Modo Item Index Style set in Preferences and Rename all the selected items, if they use mixed Index Style or if they use a different Index Style than the one in Modo Preferences.'
    
    def cmd_Tooltip (self):
        return 'Check if the current Modo Item Index Style set in Preferences and Rename all the selected items, if they use mixed Index Style or if they use a different Index Style than the one in Modo Preferences.'
    
    def cmd_Help (self):
        return 'https://twitter.com/sm0luck'
    
    def basic_ButtonName (self):
        return 'SMO CLEANUP - Convert Item Index Style'
    
    def basic_Enable (self, msg):
        return True
        
    def basic_Execute(self, msg, flags):
        scene = modo.scene.current()
        Item_List = scene.selected
        for mesh in Item_List:
            mesh.select(True)
            Item_Name = lx.eval('item.name ? xfrmcore')
            # lx.out ('current item name is ', Item_Name)
            
            UserItemIndexStyle = str(lx.eval('pref.value application.indexStyle ?'))
            # lx.out ('User Item Index Style is ', UserItemIndexStyle)
            
            # Create the first list of character chains in the Duplicated Mesh : TOTAL CHAINS
            if UserItemIndexStyle == "uscore" :
                
                # check if there is space in the current item name
                InputStringChain = Item_Name.split(" ")
                # lx.out ('String Chains are:', InputStringChain)
                
                InputStringChainCount = len(InputStringChain)
                # lx.out ('The number of Chain in the Input string is:', InputStringChainCount)
                
                # If there is detected spaces in the item name, then convert the space to underscore
                if InputStringChainCount >= 2 :
                    BaseName = '_'.join(Item_Name.split(' '))
                    lx.out ('BaseName:', BaseName)
                    lx.eval('item.name {%s} xfrmcore' %BaseName)
                
            # Create the first list of character chains in the Duplicated Mesh : TOTAL CHAINS
            if UserItemIndexStyle == "sp" :
                
                # check if there is space in the current item name
                InputStringChain = Item_Name.split("_")
                # lx.out ('String Chains are:', InputStringChain)
                
                InputStringChainCount = len(InputStringChain)
                # lx.out ('The number of Chain in the Input string is:', InputStringChainCount)
                
                # If there is detected spaces in the item name, then convert the space to underscore
                if InputStringChainCount >= 2 :
                    BaseName = ' '.join(Item_Name.split('_'))
                    lx.out ('BaseName:', BaseName)
                    lx.eval('item.name {%s} xfrmcore' % BaseName)
                
        lx.eval('select.drop item')
        # scene.select(MeshItem_List)
        
    
lx.bless(SMO_Cleanup_ConvertItemIndexStyle_Cmd, Cmd_Name)


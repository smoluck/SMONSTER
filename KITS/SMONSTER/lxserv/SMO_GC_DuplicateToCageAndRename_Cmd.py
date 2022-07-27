#python
#---------------------------------------
# Name:         SMO_GC_DuplicateToCageAndRename_Cmd.py
# Version:      1.0
#
# Purpose:      This script is designed to:
#               Duplicate the current mesh, Create a morph influence set to Cage, rename it to "cage" and freeze deformers.
#               It applies different method for renaming based on User Index Style defined in Modo Preferences
#
#
# Author:       Franck ELISABETH
# Website:      http://www.smoluck.com
#
# Created:      03/12/2020
# Copyright:    (c) Franck Elisabeth 2017-2022
#---------------------------------------

import lx, lxu, modo, string

Cmd_Name = "smo.GC.DuplicateToCageAndRename"
# smo.GC.DuplicateToCageAndRename

class SMO_GC_DuplicateToCageAndRename_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
        
        # Store the currently selected item, or if nothing is selected, an empty list.
        # Wrap this is a try except, the initial launching of Modo will cause this function
        # to perform a shallow execution before the scene state is established.
        # The script will still continue to run, but it outputs a stack trace since it failed.
        # So to prevent console spew on launch when this plugin is loaded, we use the try/except.
        try:
            self.current_Selection = lxu.select.ItemSelection().current()
        except:
            self.current_Selection = []
        
        # If we do have something selected, put it in self.current_Selection
        # Using [-1] will grab the newest item that was added to your selection.
        if len(self.current_Selection) > 0:
            self.current_Selection = self.current_Selection[-1]
        else:
            self.current_Selection = None
        
        # Test the stored selection list, only if it it not empty, instantiate the variables.
        if self.current_Selection:
            # self.dyna_Add("TruncateSteps", lx.symbol.sTYPE_INTEGER)
            # self.basic_SetFlags (0, lx.symbol.fCMDARG_OPTIONAL)                 # here the (0) define the argument index.
            
            
            
            
            ################################
            #<----[ CREATE VARIABLES ]---->#
            ################################
            # lx.eval("user.defNew name:searchedStr_A type:string life:momentary")
            # lx.eval("user.defNew name:searchedStr_B type:string life:momentary")
            # lx.eval("user.defNew name:searchedStr_C type:string life:momentary")
            # lx.eval("user.defNew name:OutputPrefixString type:string life:momentary")
            # lx.eval("user.defNew name:UserItemIndexStyle type:string life:momentary")
            ################################
            
            ################################
            #<----[ DEFINE VARIABLES ]---->#
            ################################
            searchedStr_A = "low"
            searchedStr_B = "cage"
            searchedStr_C = "exploded"
            
            OutputPrefixString_B = "cage"
            OutputPrefixString_C = "lpexploded"
            
            
            
            # if UserItemIndexStyle == "sp" :
                # lx.out('Space Index Style')
            
            # if UserItemIndexStyle == "uscore" :
                # lx.out('Underscore Index Style')
            
        
    def cmd_Flags(self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO
    
    def cmd_Interact (self):
        pass
    
    def cmd_UserName (self):
        return 'SMO GC - Duplicate Mesh to Cage and Rename it'
    
    def cmd_Desc (self):
        return 'Duplicate the current mesh, Create a morph influence set to Cage, rename it to "cage" and freeze deformers. It applies different method for renaming based on User Index Style defined in Modo Preferences.'
    
    def cmd_Tooltip (self):
        return 'Duplicate the current mesh, Create a morph influence set to Cage, rename it to "cage" and freeze deformers. It applies different method for renaming based on User Index Style defined in Modo Preferences.'
    
    def cmd_Help (self):
        return 'https://twitter.com/sm0luck'
    
    def basic_ButtonName (self):
        return 'SMO GC - Duplicate Mesh to Cage and Rename it'
    
    def basic_Enable(self, msg):
        """ Perform the checks for when the command is supposed to be enabled,
        so users will be informed the command is unavailable by the button being
        grayed out.
        :param msg:
        :type msg: lx.object.Message
        """
        valid_selection = bool(modo.Scene().selectedByType('mesh'))
        return valid_selection
        
    def basic_Execute(self, msg, flags):
        if self.current_Selection is not None:
            scene = modo.Scene()
            MeshItem_List = scene.selected
            # MeshItem_List = scene.selectedByType(lx.symbol.sITYPE_MESH)
            for mesh in MeshItem_List:
                mesh.select(True)
                lx.eval('item.duplicate false locator false true')
                BaseMeshName = lx.eval('smo.GC.GetTruncateNameByStep 2 ?')
                # lx.out('Truncated name is ',BaseMeshName)
                
                NewName = BaseMeshName + '_' + "cage"
                lx.eval('item.name {%s} xfrmcore' % NewName)
                
                # Remove MTyp Tag
                lx.eval('item.tagRemove MTyp')
                
                # Set/create MTyp Tag = Cage
                lx.eval('smo.QT.TagBakeMeshType 2')
                
                
        else:
            return
        
    
lx.bless(SMO_GC_DuplicateToCageAndRename_Cmd, Cmd_Name)

# python
"""
Name:         SMO_GC_CheckMeshBakeName_Cmd.py

Purpose:      This script is designed to:
              Check if the current Mesh item have low / cage / high strings in is name.
              It applies different method for renaming based on User Index Style defined in Modo Preferences.

Author:       Franck ELISABETH
Website:      https://www.linkedin.com/in/smoluck/
Created:      03/12/2020
Copyright:    (c) Franck Elisabeth 2017-2022
"""

import lx
import lxu
import modo

Cmd_Name = "smo.GC.CheckMeshBakeName"
# smo.GC.CheckMeshBakeName ?

# ----------- USE CASE
# TestResult = lx.eval('smo.GC.CheckMeshBakeName ?')
# lx.out('Mesh Name is classified as from category : ',TestResult)
# --------------------


class SMO_GC_CheckMeshBakeName_Cmd(lxu.command.BasicCommand):
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
            # self.dyna_Add("Mesh Class type", lx.symbol.sTYPE_STRING)
            self.dyna_Add("Mesh Class type", lx.symbol.sTYPE_INTEGER)
            self.basic_SetFlags (0, lx.symbol.fCMDARG_QUERY)
            
        
    def cmd_Flags(self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO
    
    def cmd_Interact (self):
        pass
    
    def cmd_UserName (self):
        return 'SMO GC - Check Mesh Bake Name for low/cage/high'
    
    def cmd_Desc (self):
        return 'Check if the current Mesh item have low / cage / high strings in is name.'
    
    def cmd_Tooltip (self):
        return 'Check if the current Mesh item have low / cage / high strings in is name.'
    
    def cmd_Help (self):
        return 'https://twitter.com/sm0luck'
    
    def basic_ButtonName (self):
        return 'SMO GC - Check Mesh Bake Name for low/cage/high'
    
    def basic_Enable(self, msg):
        # Perform the checks for when the command is supposed to be enabled,
        # so users will be informed the command is unavailable by the button being
        # grayed out.
        # :param msg:
        # :type msg: lx.object.Message
        valid_selection = bool(modo.Scene().selectedByType('mesh'))
        return valid_selection
        
        
        
        
    def cmd_Query(self, index, vaQuery):
        if self.current_Selection is not None:
            scene = modo.scene.current()
            
            
            UserItemIndexStyle = str(lx.eval('pref.value application.indexStyle ?'))
            # lx.out ('User Item Index Style is ', UserItemIndexStyle)
            
            MeshClassName = 0
            
            if UserItemIndexStyle == "uscore" :
                searchedStr_uscore_LP = "_low"
                searchedStr_uscore_CAGE = "_cage"
                searchedStr_uscore_HP = "_high"
                
            elif UserItemIndexStyle == "sp" :
                searchedStr_sp_LP = " low"
                searchedStr_sp_CAGE = " cage"
                searchedStr_sp_HP = " high"
            
            MeshItem_List = scene.selected
            # MeshItem_List = scene.selectedByType(lx.symbol.sITYPE_MESH)
            for mesh in MeshItem_List:
                mesh.select(True)
                Mesh_Name = lx.eval('item.name ? xfrmcore')
                # lx.out ('current item name is ', Mesh_Name)
                
                
                
                if UserItemIndexStyle == "uscore" :
                    
                    InputStringChain = Mesh_Name.split("_")
                    # lx.out ('String Chains are:', InputStringChain)
                    
                    InputStringChainCount = len(InputStringChain)
                    # lx.out ('The number of Chain in the Input string is:', InputStringChainCount)
                    
                    if searchedStr_uscore_LP in Mesh_Name :
                        lx.out ('Mesh Name is classified low')
                        MeshClassName = 1
                    if searchedStr_uscore_CAGE in Mesh_Name :
                        lx.out ('Mesh Name is classified as cage')
                        MeshClassName = 2
                    if searchedStr_uscore_HP in Mesh_Name :
                        lx.out ('Mesh Name is classified as high')
                        MeshClassName = 3
                        
                    elif searchedStr_uscore_LP not in Mesh_Name and searchedStr_uscore_CAGE not in Mesh_Name and searchedStr_uscore_HP not in Mesh_Name:
                        lx.out ('Mesh Name is not classified for Baking Workflow')
                        MeshClassName = 0
                    
                    
                elif UserItemIndexStyle == "sp" :
                    
                    InputStringChain = Mesh_Name.split(" ")
                    # lx.out ('String Chains are:', InputStringChain)
                    
                    InputStringChainCount = len(InputStringChain)
                    # lx.out ('The number of Chain in the Input string is:', InputStringChainCount)
                    
                    if searchedStr_sp_LP in Mesh_Name :
                        lx.out ('Mesh Name is classified low')
                        MeshClassName = 1
                    if searchedStr_sp_CAGE in Mesh_Name :
                        lx.out ('Mesh Name is classified as cage')
                        MeshClassName = 2
                    if searchedStr_sp_HP in Mesh_Name :
                        lx.out ('Mesh Name is classified as high')
                        MeshClassName = 3
                        
                    elif searchedStr_sp_LP not in Mesh_Name and searchedStr_sp_CAGE not in Mesh_Name and searchedStr_sp_HP not in Mesh_Name:
                        lx.out ('Mesh Name is not classified for Baking Workflow')
                        MeshClassName = 0
                    
                    
                # lx.out ('Result of Query:', BaseName)
                va = lx.object.ValueArray(vaQuery)
                # va.AddString(MeshClassName)
                va.AddInt(MeshClassName)
                return lx.result.OK

        else:
            return
        
    
lx.bless(SMO_GC_CheckMeshBakeName_Cmd, Cmd_Name)

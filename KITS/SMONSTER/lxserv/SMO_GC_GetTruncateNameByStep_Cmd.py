#python
#---------------------------------------
# Name:         SMO_GC_GetTruncateNameByStep_Cmd.py
# Version:      1.0
#
# Purpose:      This script is designed to:
#               Get the Truncate Name of the current mesh item selected.
#               It applies different method for renaming based on User Index Style defined in Modo Preferences.
#
#
# Author:       Franck ELISABETH
# Website:      http://www.smoluck.com
#
# Created:      03/12/2020
# Copyright:    (c) Franck Elisabeth 2017-2022
#---------------------------------------

import lx, lxu, modo, string

Command_Name = "smo.GC.GetTruncateNameByStep"
# smo.GC.GetTruncateNameByStep 1 ?

############# USE CASE
# TestResult = lx.eval('smo.GC.GetTruncateNameByStep 2 ?')
# lx.out('Truncated name is ',TestResult)
######################


class SMO_GC_GetTruncateNameByStep_Cmd(lxu.command.BasicCommand):
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
            self.dyna_Add("TruncateSteps", lx.symbol.sTYPE_INTEGER)
            self.basic_SetFlags (0, lx.symbol.fCMDARG_OPTIONAL)                 # here the (0) define the argument index.
            self.dyna_Add("Truncated Name", lx.symbol.sTYPE_STRING)
            self.basic_SetFlags (1, lx.symbol.fCMDARG_QUERY)
            
        
    def cmd_Flags(self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO
    
    def cmd_Interact (self):
        pass
    
    def cmd_UserName (self):
        return 'SMO GC GetTruncateNameByStep'
    
    def cmd_Desc (self):
        return 'Get the Truncate Name of the current mesh item selected. It applies different method for renaming based on User Index Style defined in Modo Preferences.'
    
    def cmd_Tooltip (self):
        return 'Get the Truncate Name of the current mesh item selected. It applies different method for renaming based on User Index Style defined in Modo Preferences.'
    
    def cmd_Help (self):
        return 'https://twitter.com/sm0luck'
    
    def basic_ButtonName (self):
        return 'SMO GC GetTruncateNameByStep'
    
    def cmd_Flags (self):
        return lx.symbol.fCMD_UNDO
    
    def basic_Enable(self, msg):
        # Perform the checks for when the command is supposed to be enabled,
        # so users will be informed the command is unavailable by the button being
        # grayed out.
        # :param msg:
        # :type msg: lx.object.Message
        valid_selection = bool(modo.Scene().selectedByType('mesh'))
        return valid_selection
        
        
        
        
    def cmd_Query(self, index, vaQuery):
        if self.current_Selection is not None :
            scene = modo.scene.current()
            TruncateSteps = self.dyna_Int (0)
            MeshItem_List = scene.selected
            # MeshItem_List = scene.selectedByType(lx.symbol.sITYPE_MESH)
            
            
            
            # for mesh in MeshItem_List:
                # mesh.select(True)
                # lx.eval('smo.GC.ConvertItemIndexStyle')
            # lx.eval('select.drop item')
            # scene.select(MeshItem_List)
            
            
            
            for mesh in MeshItem_List:
                mesh.select(True)
                Mesh_Name = lx.eval('item.name ? xfrmcore')
                # lx.out ('current item name is ', Mesh_Name)
                
                UserItemIndexStyle = str(lx.eval('pref.value application.indexStyle ?'))
                # lx.out ('User Item Index Style is ', UserItemIndexStyle)
                
                # Create the first list of character chains in the Duplicated Mesh : TOTAL CHAINS
                if UserItemIndexStyle == "uscore" :
                    
                    InputStringChain = Mesh_Name.split("_")
                    # lx.out ('String Chains are:', InputStringChain)
                    
                    InputStringChainCount = len(InputStringChain)
                    # lx.out ('The number of Chain in the Input string is:', InputStringChainCount)
                    
                    
                    
                    ##########    OLD METHOD    #########
                    # if InputStringChainCount == 2 :
                        # OriginalSourceName = InputStringChain[0]
                        # lx.out ('Output string is:', OriginalSourceName)
                    # if InputStringChainCount == 3 :
                        # OriginalSourceName = InputStringChain[0] + '_' + InputStringChain[1]
                        # lx.out ('Output string is:', OriginalSourceName)
                    # if InputStringChainCount == 4 :
                        # OriginalSourceName = InputStringChain[0] + '_' + InputStringChain[1] + '_' + InputStringChain[2]
                        # lx.out ('Output string is:', OriginalSourceName)
                    # if InputStringChainCount == 5 :
                        # OriginalSourceName = InputStringChain[0] + '_' + InputStringChain[1] + '_' + InputStringChain[2] + '_' + InputStringChain[3]
                        # lx.out ('Output string is:', OriginalSourceName)                    if InputStringChainCount == 2 :
                        # OriginalSourceName = InputStringChain[0]
                        # lx.out ('Output string is:', OriginalSourceName)
                    # if InputStringChainCount == 3 :
                        # OriginalSourceName = InputStringChain[0] + '_' + InputStringChain[1]
                        # lx.out ('Output string is:', OriginalSourceName)
                    # if InputStringChainCount == 4 :
                        # OriginalSourceName = InputStringChain[0] + '_' + InputStringChain[1] + '_' + InputStringChain[2]
                        # lx.out ('Output string is:', OriginalSourceName)
                    # if InputStringChainCount == 5 :
                        # OriginalSourceName = InputStringChain[0] + '_' + InputStringChain[1] + '_' + InputStringChain[2] + '_' + InputStringChain[3]
                        # lx.out ('Output string is:', OriginalSourceName)
                    ##########    OLD METHOD    #########
                    
                    
                    
                    ##########    NEW METHOD    #########
                    if TruncateSteps == 0 and InputStringChainCount >= 1 :
                        BaseName = Mesh_Name
                        # lx.out ('base name is: ', BaseName)
                    
                    if TruncateSteps == 1 and InputStringChainCount >= 2 :
                        BaseName = '_'.join(Mesh_Name.split('_')[:-1])
                        # lx.out ('base name is: ', BaseName)
                    
                    if TruncateSteps == 2 and InputStringChainCount >= 3 :
                        BaseName = '_'.join(Mesh_Name.split('_')[:-2])
                        # lx.out ('base name is: ', BaseName)
                    
                    if TruncateSteps == 3 and InputStringChainCount >= 4 :
                        BaseName = '_'.join(Mesh_Name.split('_')[:-3])
                        # lx.out ('base name is: ', BaseName)
                    
                    if TruncateSteps == 4 and InputStringChainCount >= 5 :
                        BaseName = '_'.join(Mesh_Name.split('_')[:-4])
                        # lx.out ('base name is: ', BaseName)
                    
                    if TruncateSteps == 5 and InputStringChainCount >= 6 :
                        BaseName = '_'.join(Mesh_Name.split('_')[:-5])
                        # lx.out ('base name is: ', BaseName)
                    
                    if TruncateSteps == 6 and InputStringChainCount >= 7:
                        BaseName = '_'.join(Mesh_Name.split(' ')[:-6])
                        # lx.out ('base name is: ', BaseName)
                    
                    if TruncateSteps == 7 and InputStringChainCount >= 8:
                        BaseName = '_'.join(Mesh_Name.split(' ')[:-7])
                        # lx.out ('base name is: ', BaseName)
                    
                    if TruncateSteps == 8 and InputStringChainCount >= 9:
                        BaseName = '_'.join(Mesh_Name.split(' ')[:-8])
                        # lx.out ('base name is: ', BaseName)
                    
                    if TruncateSteps == 9 and InputStringChainCount >= 10:
                        BaseName = '_'.join(Mesh_Name.split(' ')[:-9])
                        # lx.out ('base name is: ', BaseName)
                    ##########    NEW METHOD    #########
                    
                    
                    
                    
                # Create the first list of character chains in the Duplicated Mesh : TOTAL CHAINS
                if UserItemIndexStyle == "sp":
                    InputStringChain = Mesh_Name.split(" ")
                    # lx.out ('String Chains are:', InputStringChain)
                    
                    InputStringChainCount = len(InputStringChain)
                    # lx.out ('The number of Chain in the Input string is:', InputStringChainCount)
                    
                    ##########    NEW METHOD    #########
                    if TruncateSteps == 0 and InputStringChainCount >= 1:
                        BaseName = Mesh_Name
                        # lx.out ('base name is: ', BaseName)
                    
                    if TruncateSteps == 1 and InputStringChainCount >= 2:
                        BaseName = ' '.join(Mesh_Name.split(' ')[:-1])
                        # lx.out ('base name is: ', BaseName)
                    
                    if TruncateSteps == 2 and InputStringChainCount >= 3:
                        BaseName = ' '.join(Mesh_Name.split(' ')[:-2])
                        # lx.out ('base name is: ', BaseName)
                    
                    if TruncateSteps == 3 and InputStringChainCount >= 4:
                        BaseName = ' '.join(Mesh_Name.split(' ')[:-3])
                        # lx.out ('base name is: ', BaseName)
                    
                    if TruncateSteps == 4 and InputStringChainCount >= 5:
                        BaseName = ' '.join(Mesh_Name.split(' ')[:-4])
                        # lx.out ('base name is: ', BaseName)
                    
                    if TruncateSteps == 5 and InputStringChainCount >= 6:
                        BaseName = ' '.join(Mesh_Name.split(' ')[:-5])
                        # lx.out ('base name is: ', BaseName)
                    
                    if TruncateSteps == 6 and InputStringChainCount >= 7:
                        BaseName = ' '.join(Mesh_Name.split(' ')[:-6])
                        # lx.out ('base name is: ', BaseName)
                    
                    if TruncateSteps == 7 and InputStringChainCount >= 8:
                        BaseName = ' '.join(Mesh_Name.split(' ')[:-7])
                        # lx.out ('base name is: ', BaseName)
                    
                    if TruncateSteps == 8 and InputStringChainCount >= 9:
                        BaseName = ' '.join(Mesh_Name.split(' ')[:-8])
                        # lx.out ('base name is: ', BaseName)
                    
                    if TruncateSteps == 9 and InputStringChainCount >= 10:
                        BaseName = ' '.join(Mesh_Name.split(' ')[:-9])
                        # lx.out ('base name is: ', BaseName)
                    ##########    NEW METHOD    #########
                
                
                
                
                
                
                # lx.out ('Result of Query:', BaseName)
                va = lx.object.ValueArray(vaQuery)
                va.AddString(BaseName)
                return lx.result.OK
                
                
        
        else:
            return
        
    
lx.bless(SMO_GC_GetTruncateNameByStep_Cmd, Command_Name)


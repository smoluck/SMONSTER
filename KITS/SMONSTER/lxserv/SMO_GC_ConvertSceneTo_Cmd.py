#python
#---------------------------------------
# Name:         SMO_GC_ConvertSceneTo_Cmd.py
# Version:      1.0
#
# Purpose:      This script is designed to:
#               Save the scene in same places as the current opened scene to a specified FileFormat
#               and move the files to a Folder related to the file Format if Argument 1 is true.
#
# Author:       Franck ELISABETH (with the help of James O'Hare)
# Website:      http://www.smoluck.com
#
# Created:      30/09/2020
# Copyright:    (c) Franck Elisabeth 2017-2022
#---------------------------------------

import lx, lxu, modo, string, os
from os import path

class SMO_GC_ConvertSceneTo_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
        self.dyna_Add("To Folder Mode", lx.symbol.sTYPE_INTEGER)
        self.basic_SetFlags (0, lx.symbol.fCMDARG_OPTIONAL)             # here the (0) define the argument index.
        self.dyna_Add("Output File Format", lx.symbol.sTYPE_STRING)
        self.basic_SetFlags (1, lx.symbol.fCMDARG_OPTIONAL)

    
    def cmd_Flags(self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO
    
    def cmd_Interact (self):
        pass
    
    def cmd_UserName (self):
        return 'SMO GC Convert Scene To'
    
    def cmd_Desc (self):
        return 'Save the scene in same places as the current opened scene to a specified FileFormat and move the files to a Folder related to the file Format if Argument 1 is true.'
    
    def cmd_Tooltip (self):
        return 'Save the scene in same places as the current opened scene to a specified FileFormat and move the files to a Folder related to the file Format if Argument 1 is true.'
    
    def cmd_Help (self):
        return 'https://twitter.com/sm0luck'
    
    def basic_ButtonName (self):
        return 'SMO GC Convert Scene To'
    
    def cmd_Flags (self):
        return lx.symbol.fCMD_UNDO
    
    def basic_Enable (self, msg):
        return True
        
    
    def basic_Execute(self, msg, flags):
        ToFolder =  self.dyna_Int (0)
        ConvertSceneToOutputFileFormat = self.dyna_String (1)
        
        # Get the name of the scene, wihout the filepath and extension
        scene = modo.Scene()
        
        FullScenePath = scene.filename
        lx.out('Scene Full Path:', FullScenePath)
        SceneName = path.splitext( path.basename(scene.filename) )[0]
        lx.out('Scene Name:', SceneName)
        FolderPath = os.path.abspath(os.path.join(FullScenePath, os.pardir))
        lx.out('Folder Path:', FolderPath)
        
        
        if ConvertSceneToOutputFileFormat == "LXO" :
            if ToFolder == 1 :
                OutputPath = "{}\LXO".format(FolderPath)
                lx.out('Save As Path:', OutputPath)
                SavePath_Filename = "{}\LXO\{}{}".format(FolderPath, SceneName, ".lxo")
            if ToFolder == 0 :
                SavePath_Filename = "{}\{}{}".format(FolderPath, SceneName, ".lxo")
            lx.out('Save As: FullPath:', SavePath_Filename)
            if not os.path.exists(OutputPath):
                os.makedirs(OutputPath)
            lx.eval('!scene.saveAs {%s} $LXOB false' % SavePath_Filename)
            
            
        if ConvertSceneToOutputFileFormat == "DXF" :
            if ToFolder == 1 :
                OutputPath = "{}\DXF".format(FolderPath)
                lx.out('Save As Path:', OutputPath)
                SavePath_Filename = "{}\DXF\{}{}".format(FolderPath, SceneName, ".dxf")
            if ToFolder == 0 :
                SavePath_Filename = "{}\{}{}".format(FolderPath, SceneName, ".dxf")
            lx.out('Save As: FullPath:', SavePath_Filename)
            if not os.path.exists(OutputPath):
                os.makedirs(OutputPath)
            lx.eval('!scene.saveAs {%s} DXF false' % SavePath_Filename)
            
            
        if ConvertSceneToOutputFileFormat == "SVG" :
            if ToFolder == 1 :
                OutputPath = "{}\SVG".format(FolderPath)
                lx.out('Save As Path:', OutputPath)
                SavePath_Filename = "{}\SVG\{}{}".format(FolderPath, SceneName, ".svg")
            if ToFolder == 0 :
                SavePath_Filename = "{}\{}{}".format(FolderPath, SceneName, ".svg")
            lx.out('Save As: FullPath:', SavePath_Filename)
            if not os.path.exists(OutputPath):
                os.makedirs(OutputPath)
            lx.eval('!scene.saveAs {%s} SVG false' % SavePath_Filename)


        if ConvertSceneToOutputFileFormat == "OBJ":
            if ToFolder == 1:
                OutputPath = "{}\OBJ".format(FolderPath)
                lx.out('Save As Path:', OutputPath)
                SavePath_Filename = "{}\OBJ\{}{}".format(FolderPath, SceneName, ".obj")
            if ToFolder == 0:
                SavePath_Filename = "{}\{}{}".format(FolderPath, SceneName, ".obj")
            lx.out('Save As: FullPath:', SavePath_Filename)
            if not os.path.exists(OutputPath):
                os.makedirs(OutputPath)
            lx.eval('!scene.saveAs {%s} wf_OBJ false' % SavePath_Filename)


        if ConvertSceneToOutputFileFormat == "FBX":
            if ToFolder == 1:
                OutputPath = "{}\FBX".format(FolderPath)
                lx.out('Save As Path:', OutputPath)
                SavePath_Filename = "{}\FBX\{}{}".format(FolderPath, SceneName, ".fbx")
            if ToFolder == 0:
                SavePath_Filename = "{}\{}{}".format(FolderPath, SceneName, ".fbx")
            lx.out('Save As: FullPath:', SavePath_Filename)
            if not os.path.exists(OutputPath):
                os.makedirs(OutputPath)
            lx.eval('!scene.saveAs {%s} fbx false' % SavePath_Filename)
            
            
            
            # lx.eval('scene.close')
            # lx.eval('scene.open {%s} normal' % FullScenePath)
            # lx.eval('select.drop item')
        
    
lx.bless(SMO_GC_ConvertSceneTo_Cmd, "smo.GC.ConvertSceneTo")
# smo.GC.ConvertSceneTo 1 LXO
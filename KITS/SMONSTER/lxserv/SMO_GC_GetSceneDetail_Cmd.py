# python
"""
Name:         SMO_GC_GetSceneDetail_Cmd.py

Purpose:      This Command is designed to :
              Get Details about the current scene using arguments to specify wich data chunk you need.

Author:       Franck ELISABETH
Website:      https://www.smoluck.com
Created:     20/12/2020
Copyright:    (c) Franck Elisabeth 2017-2022
"""

import lx
import lxu
import modo
import os

Cmd_Name = "smo.GC.GetSceneDetail"
# ----------- USE CASE
# Result = lx.eval('smo.GC.GetSceneDetail 4 ?')
# lx.out('Folder Path (Path Without File and Extension):',Result)
# --------------------


class SMO_GC_GetSceneDetail_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
        self.dyna_Add("Search Category", lx.symbol.sTYPE_INTEGER)
        self.basic_SetFlags (0, lx.symbol.fCMDARG_OPTIONAL)
        self.dyna_Add("Query Result", lx.symbol.sTYPE_STRING)
        self.basic_SetFlags (1, lx.symbol.fCMDARG_QUERY)

    def cmd_Flags(self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO
    
    def cmd_Interact (self):
        pass
    
    def cmd_UserName (self):
        return 'SMO GC - Get Scene Detail'
    
    def cmd_Desc (self):
        return 'Get Details about the current scene using arguments to specify wich data chunk you need.'
    
    def cmd_Tooltip (self):
        return 'Get Details about the current scene using arguments to specify wich data chunk you need.'
    
    def cmd_Help (self):
        return 'https://twitter.com/sm0luck'
    
    def basic_ButtonName (self):
        return 'SMO GC - Get Scene Detail'
    
    def basic_Enable (self, msg):
        return True
    
    def cmd_Query(self, index, vaQuery):
        if self.dyna_Int (0) is not None:
            # ------------------------------ #
            # <----( DEFINE ARGUMENTS )----> #
            # ------------------------------ #
            # args = lx.args()
            # lx.out(args)
            
            # 0 = Full Path (With Extension)
            # 1 = File Name (With Extension)
            # 2 = Partial Path (Path Without Extension)
            # 3 = File Extension
            # 4 = Folder Path (Path Without File and Extension)
            DetailType = self.dyna_Int (0)
            # lx.out('Mode:', DetailType)
            # ------------------------------ #
            # <----( DEFINE ARGUMENTS )----> #
            # ------------------------------ #
            
            
            
            scene = modo.Scene()
            # Get the name of the scene, with extension
            scene_FullPath = lx.eval('query sceneservice scene.file ? main') # Select the scene
            # lx.out('Scene Path:', scene_FullPath)
            
            # Get the filename of the scene, without the folder path, with extension
            scene_FileName = lx.eval('query sceneservice scene.name ? main') # Select the scene
            # lx.out('Scene Name with file Extension is:', scene_FileName)
            
            
            # Split the path in root and ext pair
            FileExtension = os.path.splitext(scene_FullPath)
            
            # print root and ext of the specified path 
            PartialPath = FileExtension[0]
            # lx.out('File Path without Extension:', FileExtension[0])
            FileExt = FileExtension[1]
            # lx.out('File extension type:', FileExtension[1])
            
            
            # Split the filename in name (FileName[0]) and extension (FileName[1]) pair. 
            FileName = os.path.splitext(scene_FileName)
            # lx.out('Scene Name:', FileName[0])
            
            IsItFile = os.path.isfile(scene_FullPath)
            # lx.out('Is it a file Check: ', IsItFile)
            
            if IsItFile:
                FolderPath = os.path.dirname(scene_FullPath)
                # lx.out('Folder path of current file is:', FolderPath)
                
                if DetailType == 0:
                    Result = scene_FullPath
                    # lx.out('Full Path (With Extension):', Result)
                if DetailType == 1:
                    Result = scene_FileName
                    # lx.out('File Name (With Extension):', Result)
                if DetailType == 2:
                    Result = FileExtension[0]
                    # lx.out('Partial Path (Path Without Extension):', Result)
                if DetailType == 3:
                    Result = FileExtension[1]
                    # lx.out('File Extension:', Result)
                if DetailType == 4 :
                    Result = FolderPath
                    # lx.out('Folder Path (Path Without File and Extension):', Result)
                if DetailType == 5 :
                    Result = FileName[0]
                    # lx.out('Scene File Name:', Result)
                    

                # lx.out ('Result of Query:', Result)
                va = lx.object.ValueArray(vaQuery)
                va.AddString(Result)
                return lx.result.OK
        else:
            return
        
    
lx.bless(SMO_GC_GetSceneDetail_Cmd, Cmd_Name)

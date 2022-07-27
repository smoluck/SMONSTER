# python
# ---------------------------------------
# Name:         SMO_GC_QuickCreateCameraMatchSetup_Cmd.py
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
# ---------------------------------------

import lx, lxu, modo, string, os

Cmd_Name = "smo.GC.QuickCreateCameraMatchSetup"
# smo.GC.QuickCreateCameraMatchSetup

class SMO_GC_QuickCreateCameraMatchSetup_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)

    def cmd_Flags(self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO

    def cmd_Interact(self):
        pass

    def cmd_UserName(self):
        return 'SMO GC - Quick Create CameraMatch Setup'

    def cmd_Desc(self):
        return 'Load images of specific type and create a scene with CameraMatch setup on camera. It save the scene using the Image filename.'

    def cmd_Tooltip(self):
        return 'Load images of specific type and create a scene with CameraMatch setup on camera. It save the scene using the Image filename.'

    def cmd_Help(self):
        return 'https://twitter.com/sm0luck'

    def basic_ButtonName(self):
        return 'SMO GC - Quick Create Camera Match Setup'

    def basic_Enable(self, msg):
        return True

    def basic_Execute(self, msg, flags):
        # Get the name of the scene, wihout the filepath and extension
        scene = modo.Scene()

        ################################
        # <----[ DEFINE VARIABLES ]---->#
        ################################
        lx.eval("user.defNew name:InputFileFormat type:string life:momentary")
        lx.eval("user.defNew name:OutputFileFormat type:string life:momentary")

        lx.eval("user.defNew name:Target_Path type:string life:momentary")
        ################################

        # ############### ARGUMENTS ###############
        InputFileFormat = "jpg"
        OutputFileFormat = ".lxo"

        PathSeparator = "/"
        # ############### ARGUMENTS ###############

        lx.eval('dialog.setup dir')
        lx.eval('dialog.title "Select the target Folder to Analyse and Process"')
        # MODO version checks.
        modo_ver = int(lx.eval('query platformservice appversion ?'))
        if modo_ver == 801:
            lx.eval('+dialog.open')
        else:
            lx.eval('dialog.open')
        Target_Path = lx.eval('dialog.result ?')
        # print ('Path', Target_Path)

        FilesList = []
        FilesList = os.listdir(Target_Path)
        # print (FilesList)

        TargetFileList = []
        TargetFileListPath = []
        # if InputFileFormat == "JPG" :
        for images in os.listdir(Target_Path):
            if ".jpg" or ".JPG" in images:
                # print images
                TargetFileList.append(images)
                finalPath = Target_Path + "\\" + images
                # print (finalPath)
                TargetFileListPath.append(finalPath)

                # # Convert String path to Absolute Path using OS formating
                # finalPath_AbsPath = os.path.abspath(finalPath)
                # print('Absolute Path: ', finalPath_AbsPath)
                # TargetFileListPath.append(finalPath_AbsPath)

        print (TargetFileListPath[0])

        # print (TargetFileList)
        for i in TargetFileList:
            print (i)

        print('--------------------')

        # print (TargetFileListPath)
        for item in TargetFileListPath:
            print (item)

        for i in range(0, len(TargetFileListPath)):
            # lx.eval('clipChoice.addViaCmd clip.load')
            # lx.eval('clip.load')
            path = os.path.abspath(TargetFileListPath[i])
            print (path)
            lx.eval('clip.addStill {%s}' % path)
            StillImage = lx.eval('smo.GC.SelectStillImageItem ?')
            print (StillImage)
            lx.eval('select.item {%s} add' % StillImage)
            StillItem = "{" + StillImage + "}"
            print (StillItem)
            lx.eval('select.itemType camera')
            lx.eval('select.type item')
            lx.eval('camera.image %s' % StillItem)
            lx.eval('camera.setResFromClip')
            lx.eval('camera.exifToScene focalLen:true sun:false')

            scene_export_path = os.path.splitext(path)[0] + OutputFileFormat
            print (scene_export_path)
            # scene_file_name = os.path.splitext (os.path.basename (scene_export_path))[0]
            # print (scene_file_name)
            lx.eval('select.drop item')
            lx.eval('select.itemType camera')
            lx.eval('scene.saveAs {%s} $LXOB false' % scene_export_path)
            # lx.eval('smo.GC.ConvertSceneTo 1 %s' % OutputFileFormat)
            lx.eval('!scene.close')

        # scene_FileName = lx.eval('query sceneservice scene.name ? main') # Select the scene
        # # lx.out('Scene Name:', scene_FileName)
        # if scene_FileName:
        #     Scene_Name = path.splitext( path.basename(scene_FileName) )[0]
        #     lx.out('Scene Name:', Scene_Name)
        #
        # # Drop layer selection
        # lx.eval('select.drop item')
        # lx.eval('select.itemType mesh')
        # MeshItem_List = scene.selectedByType(lx.symbol.sITYPE_MESH)
        # for a in MeshItem_List:
        #     a.select(True)
        #     Mesh_Name = lx.eval('item.name ? xfrmcore')
        #     ModifiedName = Scene_Name + '_' + Mesh_Name
        #     lx.eval('item.name {%s} xfrmcore' % ModifiedName)
        # lx.eval('select.drop item')


lx.bless(SMO_GC_QuickCreateCameraMatchSetup_Cmd, Cmd_Name)

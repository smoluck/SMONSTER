# python
"""
Name:         SMO_GC_ExportSelectedMeshesAsMeshPreset_Cmd.py

Purpose:      This script is designed to:
              Export Selected Meshes As MeshPreset LXL file into Target Path.
              (optional: Define Path destination as argument)

Author:       Franck ELISABETH
Website:      https://www.smoluck.com
Created:      12/05/2022
Copyright:    (c) Franck Elisabeth 2017-2022
"""

import lx
import lxu
import modo
import os

Cmd_Name = "smo.GC.Multi.ExportSelectedMeshesAsMeshPreset"
# smo.GC.Multi.ExportSelectedMeshesAsMeshPreset {C:\TEMP\Target}


class SMO_GC_ExportSelectedMeshesAsMeshPreset_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
        self.dyna_Add("Directory Path", lx.symbol.sTYPE_STRING)
        self.basic_SetFlags(0, lx.symbol.fCMDARG_OPTIONAL)  # here the (0) define the argument index.

    def cmd_Flags(self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO

    def cmd_Interact(self):
        pass

    def cmd_UserName(self):
        return 'SMO GC - Export Selected Meshes as MeshPreset LXL files'

    def cmd_Desc(self):
        return 'MULTI - Export Selected Meshes As MeshPreset LXL file into Target Path. (optional: Define Path destination as argument)'

    def cmd_Tooltip(self):
        return 'MULTI - Export Selected Meshes As MeshPreset LXL file into Target Path. (optional: Define Path destination as argument)'

    def cmd_Help(self):
        return 'https://twitter.com/sm0luck'

    def basic_ButtonName(self):
        return 'SMO GC - Export Selected Meshes as MeshPreset LXL files'

    def basic_Enable(self, msg):
        return True


    def basic_Execute(self, msg, flags):
        # define function for Subfolder Name
        def SetLXLTagDialog():
            lx.eval('!user.defNew SubFolderName string momentary')
            lx.eval('user.def SubFolderName username "Set a Subfolder Name for those Presets"')
            lx.eval('user.def SubFolderName dialogname "Set a Subfolder Name for those Presets"')
            try:
                lx.eval('user.value SubFolderName')
                return lx.eval('user.value SubFolderName ?')
            except:
                return ''

        # define function for Specific folder path
        def SetSpecificPathDialog():
            lx.eval('!user.defNew SpecificPath string momentary')
            lx.eval('dialog.setup dir')
            lx.eval('dialog.title "Select a Path to Export the Meshes as LXL"')
            lx.eval('dialog.open')
            SpecificPath = lx.eval('dialog.result ?')
            lx.out('Path', SpecificPath)
            try:
                return SpecificPath
            except:
                return ''

        # In case a Path is defined directly with the path argument we overwrite the path
        TargetDirPath = ""

        if self.dyna_IsSet(0):
            TargetDirPath = self.dyna_String(0)
            # print('Destination Path is set by Argument')

        SubFolderState = bool(lx.eval('user.value SMO_UseVal_GC_LXLMeshPresetToSubfolder ?'))
        SpecificFolderState = bool(lx.eval('user.value SMO_UseVal_GC_LXLMeshPresetToSpecificFolder ?'))
        print("Export to a Subfolder:", SubFolderState)
        print("Export to a Specific Folder:", SpecificFolderState)

        if not self.dyna_IsSet(0) and SpecificFolderState:
            TargetDirPath = SetSpecificPathDialog()

        if not self.dyna_IsSet(0) and not SpecificFolderState:
            DestinationPath = lx.eval("query platformservice alias ? {kit_SMO_GAME_CONTENT:SMOGC_Presets\Assets\Meshes}")
            TargetDirPath = DestinationPath


        TargetDirPath = os.path.abspath(TargetDirPath)
        scene = modo.scene.current()

        mesh = scene.selectedByType('mesh')
        # print('modo.Mesh :', mesh)
        # print('modo.Mesh list length:', len(mesh))

        TargetIDList = []
        for item in mesh:
            itemType = modo.Item(item).type
            item = lx.object.Item(item)
            # print(item)
            if itemType == "mesh":
                ID = item.Ident()
                # print(ID)
                TargetIDList.append(ID)
        # print(TargetIDList)

        lx.eval('smo.GC.DeselectAll')
        lx.eval('select.type item')

        index = -1
        for m in TargetIDList:
            index = (index + 1)
            # print('id :', index)
            scene.select(m)
            ############### PUT YOUR Command HERE to run over each item Polygons
            try:
                lx.eval('smo.GC.ExportMeshAsMeshPreset {%s}' % TargetDirPath)
                # lx.eval('smo.GC.ExportSelectedMeshesAsMeshPreset %s' % TargetDirPath)
            except:
                lx.out('Error on {%s}' % (lx.eval('item.name ? xfrmcore')))
            lx.eval('select.type item')
            lx.eval('select.drop item')
            # GOOOOOOOOOOOOD
        index = -1
        lx.eval('smo.GC.DeselectAll')
        scene.select(mesh)

        del index
        del TargetIDList


lx.bless(SMO_GC_ExportSelectedMeshesAsMeshPreset_Cmd, Cmd_Name)

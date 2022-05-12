# python
# ---------------------------------------
# Name:         SMO_GC_ExportMeshAsMeshPreset_Cmd.py
# Version:      1.0
#
# Purpose:      This script is designed to:
#               Export current Mesh As MeshPreset LXL file into Target Path.
#               (optional: Define Path destination as argument)
#
#
# Author:       Franck ELISABETH
# Website:      http://www.smoluck.com
#
# Created:      27/10/2021
# Copyright:    (c) Franck Elisabeth 2017-2022
# ---------------------------------------

import lx, lxu, os, modo, string
from os import path

Command_Name = "smo.GC.ExportMeshAsMeshPreset"
# smo.GC.ExportMeshAsMeshPreset {C:\TEMP\Target}

class SMO_GC_ExportMeshAsMeshPreset_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
        self.dyna_Add("Directory Path", lx.symbol.sTYPE_STRING)
        self.basic_SetFlags(0, lx.symbol.fCMDARG_OPTIONAL)  # here the (0) define the argument index.

    def cmd_Flags(self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO

    def cmd_Interact(self):
        pass

    def cmd_UserName(self):
        return 'SMO GC Export current Mesh as MeshPreset LXL files'

    def cmd_Desc(self):
        return 'Export current Mesh As MeshPreset LXL file into Target Path. (optional: Define Path destination as argument)'

    def cmd_Tooltip(self):
        return 'Export current Mesh As MeshPreset LXL file into Target Path. (optional: Define Path destination as argument)'

    def cmd_Help(self):
        return 'https://twitter.com/sm0luck'

    def basic_ButtonName(self):
        return 'SMO GC Export Mesh as MeshPreset LXL files'

    def basic_Enable(self, msg):
        return True

    def basic_Execute(self, msg, flags):
        scene = modo.scene.current()

        DestinationPath = ""
        # In case a Path is defined directly with the path argument we overwrite the path
        TargetDirPath = ""

        if self.dyna_IsSet(0):
            TargetDirPath = self.dyna_String(0)
            print('Destination Path is set by Argument')

        PBState = bool()
        Good = bool()
        PBState = bool(lx.eval('layout.createOrClose PresetBrowser presetBrowserPalette ?'))
        if PBState == False:
            lx.eval(
                'layout.createOrClose PresetBrowser presetBrowserPalette true Presets width:800 height:600 persistent:true style:palette')
        Good = bool(lx.eval('layout.createOrClose PresetBrowser presetBrowserPalette ?'))

        # define function to convert Radian to Degree
        def rad(a):
            return a * 57.2957795130

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
            lx.eval('dialog.title "Select a Path to open"')
            lx.eval('dialog.open')
            SpecificPath = lx.eval('dialog.result ?')
            lx.out('Path', SpecificPath)
            try:
                return SpecificPath
            except:
                return ''

        if Good == True:
            ItemSelected = scene.selected
            selectedMeshes = [item for item in ItemSelected if item.type == 'mesh']
            print(selectedMeshes)
            sceneItem = [item for item in scene.items() if item.type == 'scene']
            print(sceneItem)

            SubFolderState = bool(lx.eval('user.value SMO_UseVal_GC_LXLMeshPresetToSubfolder ?'))
            SpecificFolderState = bool(lx.eval('user.value SMO_UseVal_GC_LXLMeshPresetToSpecificFolder ?'))
            print(SubFolderState)
            print(SpecificFolderState)

            # In case a Path is defined directly with the path argument we overwrite the path
            if self.dyna_IsSet(0):
                DestinationPath = (TargetDirPath)

            if not self.dyna_IsSet(0) and SpecificFolderState == True:
                DestinationPath = SetSpecificPathDialog()

            if not self.dyna_IsSet(0) and SpecificFolderState == False:
                # Create path target , here it's the Kit Folder for Mesh Preset
                DestinationPath = lx.eval(
                    "query platformservice alias ? {kit_SMO_GAME_CONTENT:SMOGC_Presets\Assets\Meshes}")
                # lx.out('MatCap Path', MatCapKitPath)
                print('SMO GC Kit preset path:', DestinationPath)

            if SubFolderState == True:
                lx.eval('smo.GC.DeselectAll')
                for item in sceneItem:
                    SceneID = item.Ident()
                print('Current Scene ID:', SceneID)
                lx.eval('select.subItem %s set scene' % SceneID)
                LXLTag = lx.eval('item.tag mode:string tag:"LXLT" value:?')
                # print(LXLTag)
                if len(LXLTag) == 0:
                    Subfolder = SetLXLTagDialog()
                    lx.eval('item.tag mode:string tag:LXLT value:"%s"' % Subfolder)
                elif len(LXLTag) > 0:
                    print(LXLTag)
                lx.eval('smo.GC.DeselectAll')
                if len(LXLTag) == 0 and len(Subfolder) > 0:
                    FinalPath = DestinationPath + "/" + Subfolder
                if len(LXLTag) > 0:
                    FinalPath = DestinationPath + "/" + LXLTag

            if SubFolderState == False:
                FinalPath = DestinationPath

            print(FinalPath)
            FinalPath_AbsPath = os.path.abspath(FinalPath)
            print(FinalPath_AbsPath)

            # Check / Create Directory
            # try:
            #     # Create target Directory
            #     os.mkdir(FinalPath_AbsPath)
            #     print("Directory ", FinalPath_AbsPath, " Created ")
            # except FileExistsError:
            #     print("Directory ", FinalPath_AbsPath, " already exists")

            # Create target Directory if don't exist
            if not os.path.exists(FinalPath_AbsPath):
                os.mkdir(FinalPath_AbsPath)
                print("Directory ", FinalPath_AbsPath, " Created ")
            else:
                print("Directory ", FinalPath_AbsPath, " already exists")

            # print(selectedMeshes)
            print('Number of meshes selected', len(selectedMeshes))

            lx.eval('smo.GC.DeselectAll')
            scene.select(selectedMeshes)
            if len(selectedMeshes) == 1:
                MeshName = lx.eval('item.name ? xfrmcore')
                print('current mesh name', MeshName)

                ItemIdent = lx.eval('smo.GC.GetItemUniqueName ?')
                print('current Item Unique name is %s' % ItemIdent)

                TargetPath = FinalPath_AbsPath + "/" + MeshName + ".lxl"
                print(TargetPath)

                MeshPreset_AbsPath = os.path.abspath(TargetPath)
                print('destination directory path for the mesh preset ', MeshPreset_AbsPath)

                Target = modo.Scene().selected[0]
                lx.eval('smo.GC.DeselectAll')
                CheckPARENT = bool()
                try:
                    Target.parent.select()
                    ParentItem = modo.Scene().selected[0]
                    if ParentItem != None:
                        ParentIdent = ParentItem.Ident()
                        print(ParentIdent)
                        CheckPARENT = True
                    elif ParentItem == None:
                        CheckPARENT = False
                except:
                    CheckPARENT = False
                print('Parents State :', CheckPARENT)

                lx.eval('smo.GC.DeselectAll')
                scene.select(Target)

                if CheckPARENT == False:
                    lx.eval('item.refSystem %s' % ItemIdent)
                    lx.eval('workPlane.fitGeometry')
                    lx.eval('workPlane.fitSelect')
                    WPX = lx.eval('workplane.edit ? 0 0 0 0 0')
                    WPY = lx.eval('workplane.edit 0 ? 0 0 0 0')
                    WPZ = lx.eval('workplane.edit 0 0 ? 0 0 0')
                    WRX = lx.eval('workplane.edit 0 0 0 ? 0 0')
                    WRY = lx.eval('workplane.edit 0 0 0 0 ? 0')
                    WRZ = lx.eval('workplane.edit 0 0 0 0 0 ?')
                    lx.eval('workPlane.state false')
                    lx.out('World PosX:', WPX)
                    lx.out('World PosY:', WPY)
                    lx.out('World PosZ:', WPZ)
                    lx.out('World RotX:', WRX)
                    lx.out('World RotY:', WRY)
                    lx.out('World RotZ:', WRZ)
                    OffsetPos = [float(), float(), float()]
                    OffsetPos = [WPX, WPY, WPZ]
                    print(OffsetPos)
                    OffsetRot = [float(), float(), float()]
                    OffsetRot = [WRX, WRY, WRZ]
                    print(OffsetRot)
                    lx.eval('item.refSystem {}')
                    lx.eval("transform.channel pos.X 0.0")
                    lx.eval("transform.channel pos.Y 0.0")
                    lx.eval("transform.channel pos.Z 0.0")
                    lx.eval("transform.channel rot.X 0.0")
                    lx.eval("transform.channel rot.Y 0.0")
                    lx.eval("transform.channel rot.Z 0.0")

                if CheckPARENT == True:
                    WPX = lx.eval("transform.channel pos.X ?")
                    WPY = lx.eval("transform.channel pos.Y ?")
                    WPZ = lx.eval("transform.channel pos.Z ?")
                    WRX = lx.eval("transform.channel rot.X ?")
                    WRY = lx.eval("transform.channel rot.Y ?")
                    WRZ = lx.eval("transform.channel rot.Z ?")
                    lx.out('Relative PosX:', WPX)
                    lx.out('Relative PosY:', WPY)
                    lx.out('Relative PosZ:', WPZ)
                    lx.out('Relative RotX:', WRX)
                    lx.out('Relative RotY:', WRY)
                    lx.out('Relative RotZ:', WRZ)
                    lx.eval("item.parent parent:{} inPlace:1")
                    lx.eval("transform.channel pos.X 0.0")
                    lx.eval("transform.channel pos.Y 0.0")
                    lx.eval("transform.channel pos.Z 0.0")
                    lx.eval("transform.channel rot.X 0.0")
                    lx.eval("transform.channel rot.Y 0.0")
                    lx.eval("transform.channel rot.Z 0.0")

                lx.eval(
                    'mesh.presetSave filename:{%s} desc:"" "" reuseThumb:0 item:{%s}' % (MeshPreset_AbsPath, ItemIdent))
                lx.eval('select.preset path:{%s} mode:set' % MeshPreset_AbsPath)
                lx.eval('smo.GC.RenderThumbPreset')
                lx.eval('select.preset path:{%s} mode:remove' % MeshPreset_AbsPath)
                lx.eval('smo.GC.DeselectAll')
                scene.select(Target)

                if CheckPARENT == True:
                    lx.eval('select.item %s add' % ParentIdent)
                    lx.eval('item.parent')
                    lx.eval('smo.GC.DeselectAll')
                    scene.select(Target)
                    lx.eval("transform.channel pos.X {%s}" % WPX)
                    lx.eval("transform.channel pos.Y {%s}" % WPY)
                    lx.eval("transform.channel pos.Z {%s}" % WPZ)
                    lx.eval("transform.channel rot.X {%s}" % rad(WRX))
                    lx.eval("transform.channel rot.Y {%s}" % rad(WRY))
                    lx.eval("transform.channel rot.Z {%s}" % rad(WRZ))

                if CheckPARENT == False:
                    lx.eval("transform.channel pos.X {%s}" % WPX)
                    lx.eval("transform.channel pos.Y {%s}" % WPY)
                    lx.eval("transform.channel pos.Z {%s}" % WPZ)
                    lx.eval("transform.channel rot.X {%s}" % rad(WRX))
                    lx.eval("transform.channel rot.Y {%s}" % rad(WRY))
                    lx.eval("transform.channel rot.Z {%s}" % rad(WRZ))


lx.bless(SMO_GC_ExportMeshAsMeshPreset_Cmd, Command_Name)
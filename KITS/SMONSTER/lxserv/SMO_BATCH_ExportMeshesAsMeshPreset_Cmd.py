# python
# ---------------------------------------
# Name:         SMO_BATCH_ExportMeshesAsMeshPreset_Cmd.py
# Version:      1.0
#
# Purpose:      This script is designed to:
#               Batch Export Meshes As MeshPreset LXL file into Target Path.
#
#
# Author:       Franck ELISABETH
# Website:      http://www.smoluck.com
#
# Created:      27/10/2021
# Copyright:    (c) Franck Elisabeth 2017-2022
# ---------------------------------------

import lx, lxu, modo, os, string
from os import path

Cmd_Name = "smo.BATCH.ExportMeshesAsMeshPreset"

class SMO_BATCH_ExportMeshesAsMeshPreset_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)

    def cmd_Flags(self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO

    def cmd_Interact(self):
        pass

    def cmd_UserName(self):
        return 'SMO BATCH - Export Meshes As MeshPreset LXL files'

    def cmd_Desc(self):
        return 'Batch Export Meshes As MeshPreset LXL file into Target Path.'

    def cmd_Tooltip(self):
        return 'Batch Export Meshes As MeshPreset LXL file into Target Path.'

    def cmd_Help(self):
        return 'https://twitter.com/sm0luck'

    def basic_ButtonName(self):
        return 'SMO BATCH - Export Meshes As MeshPreset LXL files'

    def basic_Enable(self, msg):
        return True

    def basic_Execute(self, msg, flags):
        PBState = bool()
        Good = bool()
        PBState = bool(lx.eval('layout.createOrClose PresetBrowser presetBrowserPalette ?'))
        if PBState == False:
            lx.eval('layout.createOrClose PresetBrowser presetBrowserPalette true Presets width:800 height:600 persistent:true style:palette')
        Good = bool(lx.eval('layout.createOrClose PresetBrowser presetBrowserPalette ?'))

        if Good == True:
            scene = modo.scene.current()

            # Drop Selection
            lx.eval('smo.GC.DeselectAll')
            lx.eval('select.itemType mesh')

            items = scene.selected
            # print(items)

            MeshList = []
            for item in items:
                MeshList.append(item)
            # print (MeshList)

            DetectTransformPos = False
            DetectTransformRot = False
            for i in MeshList:
                #print('-----')
                mesh = modo.Mesh(i)
                mesh.select(True)
                lx.eval('smo.GC.ExportMeshAsMeshPreset')
                lx.eval('smo.GC.DeselectAll')


                # MeshName = i.name
                # print(MeshName)
                # MeshID = i.id
                # print(MeshID)
                # itemType = modo.Item().type
                # # print(itemType)
                # item = lx.object.Item(i)
                # item_name = item.UniqueName()
                # if itemType != "mesh":
                #     scene.deselect(item_name)
                # if itemType == "mesh":
                #     selected_Items = lxu.select.ItemSelection().current()
                #     print('lxu select:', selected_mesh)
                #     selected_mesh = scene.selected[0]
                #     print(selected_mesh)
                #     try:
                #         target_positions = selected_mesh.transforms.position.get()
                #         if target_positions != None:
                #             print('Positions: ', target_positions)
                #             DetectTransformPos = True
                #     except:
                #         DetectTransformPos = False
                #     try:
                #         target_rotations = selected_mesh.transforms.rotation.get()
                #         if target_rotations != None:
                #             print('Rotations: ', target_rotations)
                #             DetectTransformRot = True
                #     except:
                #         DetectTransformRot = False
                #     print('Pos: ', DetectTransformPos)
                #     print('Rot: ', DetectTransformRot)


lx.bless(SMO_BATCH_ExportMeshesAsMeshPreset_Cmd, Cmd_Name)

#python
#---------------------------------------
# Name:         SMO_CLEANUP_RenameInstanceBySourceMeshName_Cmd.py
# Version:      1.0
#
# Purpose:      This script is designed to:
#               Select all the Mesh instances of the current scene and rename them all to use the name of the Source Mesh.
#
#
# Author:       Franck ELISABETH (with the help of James O'Hare)
# Website:      http://www.smoluck.com
#
# Created:      10/05/2021
# Copyright:    (c) Franck Elisabeth 2017-2022
#---------------------------------------

import lx, lxu, modo

Cmd_Name = "smo.CLEANUP.RenameInstanceBySourceMeshName"
# smo.CLEANUP.RenameInstanceBySourceMeshName

class SMO_CLEANUP_RenameInstanceBySourceMeshName_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)

    def cmd_Flags(self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO

    def cmd_Interact(self):
        pass

    def cmd_UserName(self):
        return 'SMO CLEANUP - Rename Instances by Source Mesh Name'

    def cmd_Desc(self):
        return 'Select all the Mesh instances of the current scene and rename them all to use the name of the Source Mesh.'

    def cmd_Tooltip(self):
        return 'Select all the Mesh instances of the current scene and rename them all to use the name of the Source Mesh.'

    def cmd_Help(self):
        return 'https://twitter.com/sm0luck'

    def basic_ButtonName(self):
        return 'SMO CLEANUP - Rename Instances by Source Mesh Name'

    def basic_Enable(self, msg):
        return True

    def basic_Execute(self, msg, flags):
        scene = modo.scene.current()

        lx.eval('select.itemType meshInst')

        SceneMeshInstance = list(scene.selectedByType("meshInst"))
        TCount = len(SceneMeshInstance)
        # Loop through the selected items in the scene and only get Meshes and MeshInstances in the dedicated list
        TargetIDList = []
        TargetNameList = []
        for item in SceneMeshInstance:
            itemType = modo.Item(item).type
            item = lx.object.Item(item)
            item_name = item.UniqueName()
            ID = item.Ident()
            TargetIDList.append(ID)
            Name = item.UniqueName()
            TargetNameList.append(Name)
        # print('List of MeshInstances ID')
        # print(TargetIDList)
        # print('List of MeshInstances Name')
        # print(TargetNameList)
        # print('------------------------')
        # print('------------------------')

        lx.eval('smo.GC.DeselectAll')



        SourcesIDList = []
        SourcesNameList = []
        for i in range(0,len(TargetIDList)):
            lx.eval('select.item %s replace' % (TargetIDList[i]))
            # scene.select(TargetIDList[i])
            lx.eval('select.itemSourceSelected')
            item = lx.object.Item(item)
            Item_Name = lx.eval('item.name ? xfrmcore')
            # print(Item_Name)
            lx.eval('item.name {%s} xfrmcore' % Item_Name)
            InputStringChain = Item_Name.split("_low")
            BaseName = ''.join(Item_Name.split("_low"))
            lx.out ('BaseName:', BaseName)
            lx.eval('select.itemInstances')
            lx.eval('item.name {%s} xfrmcore' %BaseName)
            lx.eval('select.drop item')

        # print('List of Mesh Sources ID')
        # print(SourcesIDList)
        # print('List of Mesh Sources Name')
        # print(SourcesNameList)


lx.bless(SMO_CLEANUP_RenameInstanceBySourceMeshName_Cmd, Cmd_Name)

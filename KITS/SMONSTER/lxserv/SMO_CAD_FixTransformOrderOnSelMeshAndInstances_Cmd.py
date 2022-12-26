# python
"""
# Name:         SMO_CAD_FixTransformOrderOnSelMeshAndInstances_Cmd.py
# Version:      1.0
#
# Purpose:      This script is designed to:
#               Change the Transform Order only on Meshes and Instances that have Transform Order different than XYZ.
#
#
# Author:       Franck ELISABETH
# Website:      https://www.smoluck.com
#
# Created:      07/05/2021
# Copyright:    (c) Franck Elisabeth 2017-2022
"""

import lx
import lxu
import modo

Cmd_Name = "smo.CAD.FixTransformOrderOnSelMeshAndInstances"


class SMO_CAD_FixTransformOrderOnSelMeshAndInstances_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
        # Use ModoStandard because Unity FBX loader use XYZ
        # self.dyna_Add("Mode", lx.symbol.sTYPE_BOOLEAN)      # XYZ by default
        self.SelModeItem = bool(lx.eval1("select.typeFrom typelist:item;polygon;vertex;edge ?"))

    def cmd_Flags(self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO

    def cmd_Interact(self):
        pass

    def cmd_UserName(self):
        return 'SMO CAD - Fix Transform Order on Selected Mesh and Instances'

    def cmd_Desc(self):
        return 'Change the Transform Order only on Meshes and Instances that have Transform Order different than XYZ.'

    def cmd_Tooltip(self):
        return 'Change the Transform Order only on Meshes and Instances that have Transform Order different than XYZ.'

    def cmd_Help(self):
        return 'https://twitter.com/sm0luck'

    def basic_ButtonName(self):
        return 'SMO CAD - Fix Transform Order on Selected Mesh and Instances'

    def basic_Enable(self, msg):
        return True

    def basic_Execute(self, msg, flags):
        scene = modo.scene.current()
        if self.SelModeItem:
            SelItem = lxu.select.ItemSelection().current()
            # print SelItem

            TargetIDList = []
            TargetNameList = []
            for item in SelItem:
                itemType = modo.Item(item).type
                item = lx.object.Item(item)
                item_name = item.UniqueName()
                if itemType == "mesh" or itemType == "meshInst":
                    ID = item.Ident()
                    TargetIDList.append(ID)
                    Name = item.UniqueName()
                    TargetNameList.append(Name)
            # print(TargetIDList)
            # print(TargetNameList)

            lx.eval('smo.GC.DeselectAll')

            for item in TargetIDList:
                lx.eval('select.item {%s} add' % item)
            FilteredItems = lxu.select.ItemSelection().current()
            # print FilteredItems

            lx.eval('smo.GC.DeselectAll')

            IDToProcessList = []
            for item in TargetIDList:
                lx.eval('select.item {%s}' % item)
                if (lx.eval('transform.channel order ?')) != "xyz":
                    # print('Transform Order different than XYZ')
                    # print(lx.eval('transform.channel order ?'))
                    IDToProcessList.append(item)
            lx.eval('smo.GC.DeselectAll')
            # print(IDToProcessList)

            # IDToProcessList = []
            # for item in FilteredItems:
            #    trfrm_channels = item.itemGraph('xfrmCore').reverse()
            #    print('All Xfrm items', trfrm_channels)
            #    # Go through all channels that the instance contains
            #    # NOTE: The instance item will only contain channels that were changed in the source item. So if the source item was only moved, but not rotated, the instance will only contain translation channel
            #    for trfrm_rot in trfrm_channels:
            #        # Cache the transform id
            #        transformRot_id = trfrm_rot.id
            #        print(trfrm_rot.id)
            #        # This is the hacky part, I only filter for translation channels
            #        if 'rotation' in transformRot_id:
            #            Xform = lx.eval('channel.value ? channel:{%s:order}' % transformRot_id)
            #            print('Rotation Xfrm item', Xform)
            #            print('Current Item T Order:', (lx.eval('transform.channel order ?')))
            #            if (lx.eval('transform.channel order ?')) != "xyz":
            #                print('Transform Order different than XYZ')
            #                print(lx.eval('transform.channel order ?'))
            #                IDToProcessList.append(item)
            # print(IDToProcessList)

            ErrorList = []
            for item in IDToProcessList:
                lx.eval('select.item %s' % item)
                try:
                    lx.eval('smo.CAD.FixTransformOrder')
                except:
                    lx.out('Error on {%s}' % (lx.eval('item.name ? xfrmcore')))
                    ErrorList.append(item)
                lx.eval('smo.GC.DeselectAll')


            if len(ErrorList) > 0 :
                for item in TargetIDList:
                    lx.eval('select.item {%s} add' % item)

            ####
            del SelItem[:]
            del TargetIDList[:]
            del TargetNameList[:]
            del IDToProcessList[:]
            ####


    def cmd_Query(self, index, vaQuery):
        lx.notimpl()


lx.bless(SMO_CAD_FixTransformOrderOnSelMeshAndInstances_Cmd, Cmd_Name)

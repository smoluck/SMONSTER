# python
"""
# Name:         SMO_GC_IsolateItemAndInstances_Cmd.py
# Version:      1.0
#
# Purpose:      This script is designed to
#               Isolate current Item and his Instances.
#
#
# Author:       Franck ELISABETH (with the help of Tom Dymond for debug)
# Website:      https://www.smoluck.com
#
# Created:      02/04/2021
# Copyright:    (c) Franck Elisabeth 2017-2022
"""

import lx
import lxu
import modo

Cmd_Name = "smo.GC.IsolateItemAndInstances"
# smo.GC.IsolateItemAndInstances


class SMO_GC_IsolateItemAndInstances_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)

    def cmd_Flags(self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO

    def cmd_Interact(self):
        pass

    def cmd_UserName(self):
        return 'SMO GC - Isolate Item And Instances'

    def cmd_Desc(self):
        return 'Isolate current Item and his Instances.'

    def cmd_Tooltip(self):
        return 'Isolate current Item and his Instances.'

    def cmd_Help(self):
        return 'https://twitter.com/sm0luck'

    def basic_ButtonName(self):
        return 'SMO GC - Isolate Item And Instances'

    def basic_Enable(self, msg):
        return True

    def basic_Execute(self, msg, flags):
        scene = modo.scene.current()
        # lx.eval('select.itemSourceSelected')
        # SourceList = []
        # InstancesList = []
        RefSystemActive = bool()
        CurrentRefSystemItem = lx.eval('item.refSystem ?')
        print(CurrentRefSystemItem)

        SelItem = lxu.select.ItemSelection().current()
        print(SelItem)
        print('Selected Items count:', len(SelItem))

        if len(SelItem) >= 1:
            # Create the List of selected Instances
            InputInstIDList = []
            for item in SelItem:
                itemType = modo.Item(item).type
                item = lx.object.Item(item)
                if itemType == "meshInst":
                    ID = item.Ident()
                    InputInstIDList.append(ID)
            if InputInstIDList > 0:
                print(InputInstIDList)
                print('One or more Instances Selected')

            # Create the List of selected regular Meshes
            InputMeshIDList = []
            for item in SelItem:
                itemType = modo.Item(item).type
                item = lx.object.Item(item)
                item_name = item.UniqueName()
                if itemType == "mesh":
                    ID = item.Ident()
                    InputMeshIDList.append(ID)

            if InputMeshIDList > 0:
                print(InputMeshIDList)
                print('One or more Regular Mesh Selected')

            lx.eval('smo.GC.DeselectAll')


            OutputSourcesItems = []
            if len(InputInstIDList) > 0:
                for i in InputInstIDList:
                    lx.eval('select.item {%s} add' % i)
                # Instances = scene.selected
                InputInstances = lxu.select.ItemSelection().current()
                lx.eval('select.itemSourceSelected')

                OutputSourcesItems = lxu.select.ItemSelection().current()
                print('Mesh Items from Instances:', OutputSourcesItems)

            lx.eval('smo.GC.DeselectAll')


            InputMeshes = []
            OutputInstItems = []
            if len(InputMeshIDList) > 0:
                for i in InputMeshIDList:
                    lx.eval('select.item {%s} add' % i)
                InputMeshes = lxu.select.ItemSelection().current()
                try:
                    lx.eval('!!select.itemInstances')
                except:
                    pass

                OutputInstItems = lxu.select.ItemSelection().current()
                print('Instance Items from Regular Meshes:', OutputInstItems)

            lx.eval('smo.GC.DeselectAll')


            SourcesItems = []
            if len(InputMeshIDList) >= 1:
                SourcesItems = OutputSourcesItems + InputMeshes
            if len(InputMeshIDList) == 0:
                SourcesItems = OutputSourcesItems
            print('Total regular Mesh Items:', SourcesItems)
            scene.select(SourcesItems)

            if len(SourcesItems) >= 1:
                # Create the List of selected Instances
                try:
                    lx.eval('!!select.itemInstances')
                except:
                    pass
                OutputInstancesItems = []
                OutputInstancesItems = lxu.select.ItemSelection().current()

            TotalOutputItems = []
            TotalOutputItems = SourcesItems + OutputInstancesItems

            lx.eval('smo.GC.DeselectAll')
            scene.select(TotalOutputItems)

            # Clear Item visibility and only show the current targets Meshes and Instances
            lx.eval('unhide')
            lx.eval('hide.unsel')
            lx.eval('smo.GC.DeselectAll')

            if len(SourcesItems) >= 1:
                scene.select(SourcesItems)
                lx.eval('viewport.fitSelected')
                if len(SourcesItems) == 1:
                    scene.select(SourcesItems[0])
                    if not RefSystemActive:
                        lx.eval('item.refSystem %s' % (SourcesItems[0].Ident()))
                        lx.eval('viewport.fitSelected')
            lx.eval('smo.GC.DeselectAll')
            scene.select(SourcesItems)

            ####
            if len(InputInstIDList) > 0:
                del InputInstIDList[:]

            if len(InputMeshIDList) > 0:
                del InputMeshIDList[:]

            if len(InputMeshes) > 0:
                del InputMeshes[:]

            if len(OutputInstItems) > 0:
                del OutputInstItems[:]

            if len(OutputSourcesItems) > 0:
                del OutputSourcesItems[:]

            if len(OutputInstancesItems) > 0:
                del OutputInstancesItems[:]

            if len(SourcesItems) > 0:
                del SourcesItems[:]

            if len(TotalOutputItems) > 0:
                del TotalOutputItems[:]
            ####
        del SelItem[:]
        del CurrentRefSystemItem
        del InputInstIDList[:]
        del InputMeshIDList[:]
        del OutputSourcesItems[:]
        del InputMeshes[:]
        del OutputInstItems[:]


lx.bless(SMO_GC_IsolateItemAndInstances_Cmd, Cmd_Name)

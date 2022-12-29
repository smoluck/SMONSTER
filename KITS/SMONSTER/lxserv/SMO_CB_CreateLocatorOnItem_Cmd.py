# python
"""
Name:         SMO_CB_CreateLocatorOnMesh_Cmd.py

Purpose:      This script is designed to
              Create a Locator on first selected mesh position and parent all the selected meshes to that Locator.

Author:       Franck ELISABETH
Website:      https://www.smoluck.com
Created:      13/04/2021
Copyright:    (c) Franck Elisabeth 2017-2022
"""

import lx
import lxu
import modo

Cmd_Name = "smo.CB.CreateLocatorOnMesh"
# smo.CB.CreateLocatorOnMesh 2 1 1


class SMO_CB_CreateLocatorOnMesh_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
        self.dyna_Add("Shape", lx.symbol.sTYPE_INTEGER)
        self.basic_SetFlags(0, lx.symbol.fCMDARG_OPTIONAL)  # here the (0) define the argument index.
        self.dyna_Add("Solid", lx.symbol.sTYPE_INTEGER)
        self.basic_SetFlags(1, lx.symbol.fCMDARG_OPTIONAL)
        self.dyna_Add("Axis", lx.symbol.sTYPE_INTEGER)
        self.basic_SetFlags(2, lx.symbol.fCMDARG_OPTIONAL)

    def cmd_Flags(self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO

    def cmd_Interact(self):
        pass

    def cmd_UserName(self):
        return 'SMO CB - Create Locator on Mesh'

    def cmd_Desc(self):
        return 'Create a Locator on first selected mesh position and parent all the selected meshes to that Locator.'

    def cmd_Tooltip(self):
        return 'Create a Locator on first selected mesh position and parent all the selected meshes to that Locator.'

    def cmd_Help(self):
        return 'https://twitter.com/sm0luck'

    def basic_ButtonName(self):
        return 'SMO CB - Create Locator on Mesh'

    def basic_Enable(self, msg):
        return True

    def basic_Execute(self, msg, flags):
        scene = modo.scene.current()

        # ------------- ARGUMENTS Test
        # LocShape = 2
        # LocSolid = 0
        # LocAxis = 0
        # ------------- ARGUMENTS ------------- #

        # ------------- ARGUMENTS ------------- #
        args = lx.args()
        lx.out(args)

        # BOX = 1
        # PYRAMID = 2
        # RHOMBUS = 3
        # CYLINDER = 4
        # CONE = 5
        # SPHERE = 6
        # PLANE = 7
        # POINT = 8
        # Circle = 9
        LocShape = self.dyna_Int(0)
        # lx.out('Desired Shape:',LocShape)

        # False = 0
        # True = 1
        LocSolid = self.dyna_Int(1)
        # lx.out('Desired Solid Mode:',LocSolid)

        # X = 0
        # Y = 1
        # Z = 2
        # View = 3
        # None = 4
        LocAxis = self.dyna_Int(2)
        # lx.out('Desired Axis:',LocAxis)
        # ------------- ARGUMENTS ------------- #

        # ------------------------ #
        # <----( Main Macro )----> #
        # ------------------------ #

        SelItem = lxu.select.ItemSelection().current()
        # TCount = len(SelMeshItem)
        ##################### For Locators ######################
        ################## Test Draw Pack #####################
        # Loop through the selected items in the scene and Deselect any item that is not a Mesh
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
        print(TargetIDList)
        print(TargetNameList)

        # Deselect everything in the scene
        lx.eval('smo.GC.DeselectAll')

        LocIDList = []
        for i in range(len(TargetIDList)):
            lx.eval('select.item %s set' % TargetIDList[i])
            Tar = lxu.select.ItemSelection().current()
            for item in Tar:
                iten = lx.object.Item(item)
                TarID = item.Ident()
            lx.eval('item.create locator')
            loc = lxu.select.ItemSelection().current()
            for item in loc:
                iten = lx.object.Item(item)
                locID = item.Ident()
                LocIDList.append(locID)
            lx.eval('select.item %s set' % locID)
            lx.eval('select.item %s add' % TarID)
            lx.eval('item.parent')
            lx.eval('smo.GC.DeselectAll')
            # Switch Locator and Target: Target will be child of Locator
            lx.eval('select.item %s set' % locID)
            lx.eval('item.parent parent:{} inPlace:1')
            lx.eval('smo.CB.LocatorShape %i %i %i' % (LocShape, LocSolid, LocAxis))
            lx.eval('smo.GC.DeselectAll')
            lx.eval('select.item %s set' % TarID)
            lx.eval('select.item %s add' % locID)
            lx.eval('item.parent inPlace:1')
            lx.eval('smo.GC.DeselectAll')
        print(LocIDList)
        
        for i in range(len(LocIDList)):
            lx.eval('select.item %s add' % LocIDList[i])
        selected_locators = scene.selectedByType(lx.symbol.sITYPE_LOCATOR)


        # Define the ID of the Master Locator that drive the channel values.
        LocMaster = LocIDList[0]

        if 0 <= LocAxis <= 3 and LocShape > 0:
            if LocAxis == 0:
                if LocShape == 1 or LocShape == 2 or LocShape == 3 or LocShape == 7:
                    lx.eval('select.item %s add' % LocMaster)
                    lx.eval('channel.link add {%s:isSize.Y} {%s:isSize.Z}' % (LocMaster, LocMaster))
                if LocShape == 1 or LocShape == 2 or LocShape == 3 or LocShape == 7:
                    for i in range(1, len(LocIDList)):
                        lx.eval('channel.link add {%s:isSize.Y} {%s:isSize.Y}' % (LocMaster, LocIDList[i]))
                        lx.eval('channel.link add {%s:isSize.Y} {%s:isSize.Z}' % (LocMaster, LocIDList[i]))
                        if LocShape < 6:
                            lx.eval('channel.link add {%s:isSize.X} {%s:isSize.X}' % (LocMaster, LocIDList[i]))
                        lx.eval('channel.link add {%s:isOffset.X} {%s:isOffset.X}' % (LocMaster, LocIDList[i]))
                        lx.eval('smo.GC.DeselectAll')
                    lx.eval('select.channel {%s:isSize.Y} add' % LocMaster)
                    if LocShape < 6:
                        lx.eval('select.channel {%s:isSize.X} add' % LocMaster)
                    lx.eval('select.channel {%s:isOffset.X} add' % LocMaster)

                if LocShape == 4 or LocShape == 5 or LocShape == 6 or LocShape == 9:
                    lx.eval('select.item %s add' % LocMaster)
                    for i in range(1, len(LocIDList)):
                        lx.eval('channel.link add {%s:isRadius} {%s:isRadius}' % (LocMaster, LocIDList[i]))
                        if LocShape < 6:
                            lx.eval('channel.link add {%s:isSize.X} {%s:isSize.X}' % (LocMaster, LocIDList[i]))
                        lx.eval('channel.link add {%s:isOffset.X} {%s:isOffset.X}' % (LocMaster, LocIDList[i]))
                    lx.eval('select.channel {%s:isRadius} add' % LocMaster)
                    if LocShape < 6:
                        lx.eval('select.channel {%s:isSize.X} add' % LocMaster)
                    lx.eval('select.channel {%s:isOffset.X} add' % LocMaster)

            if LocAxis == 1:
                if LocShape == 1 or LocShape == 2 or LocShape == 3 or LocShape == 7:
                    lx.eval('select.item %s add' % LocMaster)
                    lx.eval('channel.link add {%s:isSize.X} {%s:isSize.Z}' % (LocMaster, LocMaster))
                if LocShape == 1 or LocShape == 2 or LocShape == 3 or LocShape == 7:
                    for i in range(1, len(LocIDList)):
                        lx.eval('channel.link add {%s:isSize.X} {%s:isSize.X}' % (LocMaster, LocIDList[i]))
                        lx.eval('channel.link add {%s:isSize.X} {%s:isSize.Z}' % (LocMaster, LocIDList[i]))
                        if LocShape < 6:
                            lx.eval('channel.link add {%s:isSize.Y} {%s:isSize.Y}' % (LocMaster, LocIDList[i]))
                        lx.eval('channel.link add {%s:isOffset.Y} {%s:isOffset.Y}' % (LocMaster, LocIDList[i]))
                        lx.eval('smo.GC.DeselectAll')
                    lx.eval('select.channel {%s:isSize.X} add' % LocMaster)
                    if LocShape < 6:
                        lx.eval('select.channel {%s:isSize.Y} add' % LocMaster)
                    lx.eval('select.channel {%s:isOffset.Y} add' % LocMaster)

                if LocShape == 4 or LocShape == 5 or LocShape == 6 or LocShape == 9:
                    lx.eval('select.item %s add' % LocMaster)
                    for i in range(1, len(LocIDList)):
                        lx.eval('channel.link add {%s:isRadius} {%s:isRadius}' % (LocMaster, LocIDList[i]))
                        if LocShape < 6:
                            lx.eval('channel.link add {%s:isSize.Y} {%s:isSize.Y}' % (LocMaster, LocIDList[i]))
                        lx.eval('channel.link add {%s:isOffset.Y} {%s:isOffset.Y}' % (LocMaster, LocIDList[i]))
                    lx.eval('select.channel {%s:isRadius} add' % LocMaster)
                    if LocShape < 6:
                        lx.eval('select.channel {%s:isSize.Y} add' % LocMaster)
                    lx.eval('select.channel {%s:isOffset.Y} add' % LocMaster)

            if LocAxis == 2:
                if LocShape == 1 or LocShape == 2 or LocShape == 3 or LocShape == 7:
                    lx.eval('select.item %s add' % LocMaster)
                    lx.eval('channel.link add {%s:isSize.X} {%s:isSize.Y}' % (LocMaster, LocMaster))
                if LocShape == 1 or LocShape == 2 or LocShape == 3 or LocShape == 7:
                    for i in range(1, len(LocIDList)):
                        lx.eval('channel.link add {%s:isSize.X} {%s:isSize.X}' % (LocMaster, LocIDList[i]))
                        lx.eval('channel.link add {%s:isSize.X} {%s:isSize.Y}' % (LocMaster, LocIDList[i]))
                        if LocShape < 6:
                            lx.eval('channel.link add {%s:isSize.Z} {%s:isSize.Z}' % (LocMaster, LocIDList[i]))
                        lx.eval('channel.link add {%s:isOffset.Z} {%s:isOffset.Z}' % (LocMaster, LocIDList[i]))
                        lx.eval('smo.GC.DeselectAll')
                    lx.eval('select.channel {%s:isSize.X} add' % LocMaster)
                    if LocShape < 6:
                        lx.eval('select.channel {%s:isSize.Z} add' % LocMaster)
                    lx.eval('select.channel {%s:isOffset.Z} add' % LocMaster)

                if LocShape == 4 or LocShape == 5 or LocShape == 6 or LocShape == 9:
                    lx.eval('select.item %s add' % LocMaster)
                    for i in range(1, len(LocIDList)):
                        lx.eval('channel.link add {%s:isRadius} {%s:isRadius}' % (LocMaster, LocIDList[i]))
                        if LocShape < 6:
                            lx.eval('channel.link add {%s:isSize.Z} {%s:isSize.Z}' % (LocMaster, LocIDList[i]))
                        lx.eval('channel.link add {%s:isOffset.Z} {%s:isOffset.Z}' % (LocMaster, LocIDList[i]))
                    lx.eval('select.channel {%s:isRadius} add' % LocMaster)
                    if LocShape < 6:
                        lx.eval('select.channel {%s:isSize.Z} add' % LocMaster)
                    lx.eval('select.channel {%s:isOffset.Z} add' % LocMaster)

            if LocAxis == 3:
                if LocShape == 4 or LocShape == 5 or LocShape == 6 or LocShape == 9:
                    for i in range(len(LocIDList)):
                        lx.eval('select.item %s add' % LocIDList[i])
                        lx.eval('select.channel {%s:isRadius} add' % LocIDList[i])

        lx.eval('tool.set channel.haul on')

        for i in range(len(LocIDList)):
            lx.eval('select.item %s add' % LocIDList[i])

        del TargetIDList[:]
        del TargetNameList[:]
        del LocIDList[:]


    def cmd_Query(self, index, vaQuery):
        lx.notimpl()


lx.bless(SMO_CB_CreateLocatorOnMesh_Cmd, Cmd_Name)

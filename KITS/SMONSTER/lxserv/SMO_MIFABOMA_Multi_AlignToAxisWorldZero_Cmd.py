# python
# ---------------------------------------
# Name:         SMO_MIFABOMA_Multi_AlignToAxisWorldZero_Cmd.py
# Version:      1.0
#
# Purpose:      This script is designed to
#               Align selected Mesh/Instances/Locator/GroupLocator items to World Axis.
#               It use X Y Z axis as argument for the direction.
#
# Author:       Franck ELISABETH
# Website:      http://www.smoluck.com
#
# Created:      17/08/2022
# Copyright:    (c) Franck Elisabeth 2017-2022
# ---------------------------------------

import lx, lxu, modo

Cmd_Name = "smo.MIFABOMA.Multi.AlignToAxisWorldZero"
# smo.MIFABOMA.Multi.AlignToAxisWorldZero z


class SMO_MIFABOMA_Multi_AlignToAxisWorldZero_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
        self.dyna_Add("Axis", lx.symbol.sTYPE_AXIS)

        # scenedata = modo.scene.current()
        # CheckGrpSelItems = lxu.select.ItemSelection().current()
        # for item in CheckGrpSelItems:
        #     itemType = modo.Item(item).type
        #     item = lx.object.Item(item)
        #     item_name = item.UniqueName()
        #     # print(item_name)
        #     if itemType != "mesh":
        #         scenedata.deselect(item_name)

    def cmd_Flags(self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO

    def cmd_Interact(self):
        pass

    def cmd_UserName(self):
        return 'SMO MIFABOMA - (Multi) AlignToAxisWorldZero'

    def cmd_Desc(self):
        return 'Align selected Mesh/Instances/Locator/GroupLocator items to World Axis. It use X Y Z axis as argument for the direction.'

    def cmd_Tooltip(self):
        return 'Align selected Mesh/Instances/Locator/GroupLocator items to World Axis. It use X Y Z axis as argument for the direction.'

    def cmd_Help(self):
        return 'https://twitter.com/sm0luck'

    def basic_ButtonName(self):
        return 'SMO MIFABOMA - (Multi) AlignToAxisWorldZero'

    def basic_Enable(self, msg):
        return True

    def basic_Execute(self, msg, flags):
        Axis = self.dyna_String(0)
        scene = modo.scene.current()

        # current Selection
        selitems_ksfs = scene.selected

        # selitems_ksfs = scene.selectedByType(lx.symbol.sITYPE_MESH)          # to select only Meshes              "in selection"
        # selitems_ksfs = scene.selectedByType(lx.symbol.sITYPE_GROUP)         # to select only Groups              ""
        # selitems_ksfs = scene.selectedByType(lx.symbol.sITYPE_GROUPLOCATOR)  # to select only GroupLocator        ""
        # selitems_ksfs = scene.selectedByType(lx.symbol.sITYPE_SCENE)         # to select only Scene Item          ""
        # selitems_ksfs = scene.selectedByType(lx.symbol.sITYPE_TRISURF)       # to select only StaticMeshes        ""
        # selitems_ksfs = scene.selectedByType(lx.symbol.sITYPE_VIDEOSTILL)    # to select only VideoStillImages    ""
        # selitems_ksfs = scene.selectedByType(lx.symbol.sITYPE_LOCATOR)       # to select only Locator             ""
        lx.eval('select.drop item')

        for mesh in selitems_ksfs:
            mesh.select(True)
            lx.eval('smo.MIFABOMA.AlignToAxisWorldZero %s' % Axis)
            lx.eval('select.drop item')

        scene.select(selitems_ksfs)

        del selitems_ksfs


lx.bless(SMO_MIFABOMA_Multi_AlignToAxisWorldZero_Cmd, Cmd_Name)


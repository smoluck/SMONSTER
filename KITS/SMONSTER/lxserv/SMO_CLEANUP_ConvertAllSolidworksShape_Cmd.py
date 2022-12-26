# python
"""
# Name:         SMO_CLEANUP_ConvertAllSolidWorksShape_Cmd.py
# Version:      1.0
#
# Purpose:      This script is designed to:
#               Search for all Solidworks Shape Items in the scene and convert them to regular Meshes.
#               Delete the empty meshes in the process as well.
#
#
# Author:       Franck ELISABETH
# Website:      https://www.smoluck.com
#
# Created:      11/05/2022
# Copyright:    (c) Franck Elisabeth 2017-2022
"""

import lx
import lxu
import modo

Cmd_Name = "smo.CLEANUP.ConvertAllSolidWorksShape"
# smo.CLEANUP.ConvertAllSolidWorksShape


class SMO_CLEANUP_ConvertAllSolidWorksShape_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)

    def cmd_Flags(self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO

    def cmd_Interact(self):
        pass

    def cmd_UserName(self):
        return 'SMO CLEANUP - Convert All SolidWorks Shapes to Meshes.'

    def cmd_Desc(self):
        return 'Search for all Solidworks Shape Items in the scene and convert them to regular Meshes. Delete the empty meshes in the process as well.'

    def cmd_Tooltip(self):
        return 'Search for all Solidworks Shape Items in the scene and convert them to regular Meshes. Delete the empty meshes in the process as well.'

    def cmd_Help(self):
        return 'https://twitter.com/sm0luck'

    def basic_ButtonName(self):
        return 'SMO CLEANUP - Convert All SolidWorks Shapes to Meshes'

    def basic_Enable(self, msg):
        return True

    def basic_Execute(self, msg, flags):
        scn = modo.scene.current()
        # Be sure to deselect items that are not Locators
        lx.eval('select.all')
        selected_Items = lxu.select.ItemSelection().current()
        # print(selected_Items)
        for item in selected_Items:
            itemType = modo.Item(item).type
            # print(itemType)
            item = lx.object.Item(item)
            item_name = item.UniqueName()
            if itemType != "triSurf":
                scn.deselect(item_name)
        selected_trisurf = scn.selectedByType(lx.symbol.sITYPE_TRISURF)
        # print(selected_trisurf)

        for mesh in selected_trisurf:
            mesh.select(True)
            lx.eval('item.setType.mesh locator')
        lx.eval('smo.GC.DeselectAll')


lx.bless(SMO_CLEANUP_ConvertAllSolidWorksShape_Cmd, Cmd_Name)

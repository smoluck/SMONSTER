# python
"""
Name:         SMO_CLEANUP_DelEverythingExceptMeshes_Cmd.py

Purpose:      This script is designed to:
              Select everything in the current scene, except Meshes items and
              delete all other items / materials.
              It unparent in place the current Meshes to preserve their position
              in space in case they were part of a hierarchy.

Author:       Franck ELISABETH
Website:      https://www.linkedin.com/in/smoluck/
Created:      11/05/2022
Copyright:    (c) Franck Elisabeth 2017-2022
"""

import lx
import lxu
import modo

Cmd_Name = "smo.CLEANUP.DelEverythingExceptMeshes"
# smo.CLEANUP.DelEverythingExceptMeshes


class SMO_CLEANUP_DelEverythingExceptMeshes_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)

    def cmd_Flags(self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO

    def cmd_Interact(self):
        pass

    def cmd_UserName(self):
        return 'SMO CLEANUP - Delete everything Except Meshes items'

    def cmd_Desc(self):
        return 'Select everything in the current scene, except Meshes items and delete all other items / materials. It unparent in place the current Meshes to preserve their position in space in case they were part of a hierarchy.'

    def cmd_Tooltip(self):
        return 'Select everything in the current scene, except Meshes items and delete all other items / materials. It unparent in place the current Meshes to preserve their position in space in case they were part of a hierarchy.'

    def cmd_Help(self):
        return 'https://twitter.com/sm0luck'

    def basic_ButtonName(self):
        return 'SMO CLEANUP - Delete everything Except Meshes items.'

    def basic_Enable(self, msg):
        return True

    def basic_Execute(self, msg, flags):
        scn = modo.scene.current()
        # Be sure to deselect items that are not Locators
        lx.eval('select.all')
        lx.eval('item.parent parent:{} inPlace:1')
        selected_Items = lxu.select.ItemSelection().current()
        # print(selected_Items)
        for item in selected_Items:
            itemType = modo.Item(item).type
            # print(itemType)
            item = lx.object.Item(item)
            item_name = item.UniqueName()
            if itemType == "mesh":
                scn.deselect(item_name)
        lx.eval('!delete')
        lx.eval('smo.GC.DeselectAll')


lx.bless(SMO_CLEANUP_DelEverythingExceptMeshes_Cmd, Cmd_Name)

# python
# ---------------------------------------
# Name:         SMO_GC_Multi_DeleteByLocalAxisSides_Cmd.py
# Version:      1.0
#
# Purpose:      This script is designed to
#               (for Multiple Mesh)
#               Delete vertex by Local Axis Side (positive or negative).
#
# Author:       Franck ELISABETH
# Website:      http://www.smoluck.com
#
# Created:      19/08/2022
# Copyright:    (c) Franck Elisabeth 2017-2022
# ---------------------------------------

import lx, lxu, modo

Cmd_Name = "smo.GC.Multi.DeleteByLocalAxisSides"
# smo.GC.Multi.DeleteByLocalAxisSides z true


class SMO_GC_Multi_DeleteByLocalAxisSides_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
        self.dyna_Add("Axis", lx.symbol.sTYPE_AXIS)
        self.dyna_Add("Positive Direction", lx.symbol.sTYPE_BOOLEAN)

        scenedata = modo.scene.current()
        CheckGrpSelItems = lxu.select.ItemSelection().current()
        for item in CheckGrpSelItems:
            itemType = modo.Item(item).type
            item = lx.object.Item(item)
            item_name = item.UniqueName()
            # print(item_name)
            if itemType != "mesh":
                scenedata.deselect(item_name)

    def cmd_Flags(self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO

    def cmd_Interact(self):
        pass

    def cmd_UserName(self):
        return 'SMO GC - (Multi) DeleteByLocalAxisSides'

    def cmd_Desc(self):
        return 'MULTI - Delete vertex by Local Axis Side (positive or negative).'

    def cmd_Tooltip(self):
        return 'MULTI - Delete vertex by Local Axis Side (positive or negative).'

    def cmd_Help(self):
        return 'https://twitter.com/sm0luck'

    def basic_ButtonName(self):
        return 'SMO GC - (Multi) DeleteByLocalAxisSides'

    def basic_Enable(self, msg):
        return True

    def basic_Execute(self, msg, flags):
        Axis = self.dyna_String(0)
        PositiveDir = self.dyna_Bool(1)

        scene = modo.scene.current()
        items = modo.Scene().selected

        selmeshes_ksfs = scene.selectedByType(lx.symbol.sITYPE_MESH)
        lx.eval('select.drop item')

        for mesh in selmeshes_ksfs:
            mesh.select(True)
            lx.eval('smo.GC.DeleteByLocalAxisSides %s %s' % (Axis, PositiveDir))
            lx.eval('select.drop item')

        scene.select(selmeshes_ksfs)

        del selmeshes_ksfs


lx.bless(SMO_GC_Multi_DeleteByLocalAxisSides_Cmd, Cmd_Name)

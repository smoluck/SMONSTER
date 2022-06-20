# python
# ---------------------------------------
# Name:         SMO_GC_MultiModollamaRebuildNGontoTriangle_Cmd.py
# Version:      1.0
#
# Purpose:      This Command is designed to
#               For a set of Meshes.
#               Rebuild all NGons via Modollama Triangulation command to output Triangles.
#
# Author:       Franck ELISABETH
# Website:      http://www.smoluck.com
#
# Created:      16/06/2022
# Copyright:    (c) Franck Elisabeth 2017-2022
# ---------------------------------------

import lx, lxu, modo

Command_Name = "smo.GC.MultiModollamaRebuildNGontoTriangle"
# smo.GC.MultiModollamaRebuildNGontoTriangle 1
# Modo Method = False
# Modollama Method = True

class SMO_GC_MultiModollamaRebuildNGontoTriangle_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
        self.dyna_Add("Triangulate Method: Modo or Modollama", lx.symbol.sTYPE_BOOLEAN)
        self.basic_SetFlags(0, lx.symbol.fCMDARG_OPTIONAL)  # here the (0) define the argument index.

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
        return 'SMO GC (Multi) MicroBevelHardEdgesAndUpdateToSoften'

    def cmd_Desc(self):
        return 'Rebuild all NGons via Modollama Triangulation command to output Triangles.'

    def cmd_Tooltip(self):
        return 'Rebuild all NGons via Modollama Triangulation command to output Triangles.'

    def cmd_Help(self):
        return 'https://twitter.com/sm0luck'

    def basic_ButtonName(self):
        return 'SMO GC (Multi) MicroBevelHardEdgesAndUpdateToSoften'

    def basic_Enable(self, msg):
        return True

    def basic_Execute(self, msg, flags):
        TriMethod = self.dyna_Bool(0)
        # Modo = False
        # Modollama = True
        scene = modo.scene.current()
        items = modo.Scene().selected

        selmeshitems = scene.selectedByType(lx.symbol.sITYPE_MESH)
        lx.eval('select.drop item')

        for mesh in selmeshitems:
            mesh.select(True)
            if TriMethod:
                lx.eval('smo.GC.ModollamaRebuildNGontoTriangle 1')
            if not TriMethod:
                lx.eval('smo.GC.ModollamaRebuildNGontoTriangle 0')
            lx.eval('select.drop item')

        scene.select(selmeshitems)


lx.bless(SMO_GC_MultiModollamaRebuildNGontoTriangle_Cmd, Command_Name)

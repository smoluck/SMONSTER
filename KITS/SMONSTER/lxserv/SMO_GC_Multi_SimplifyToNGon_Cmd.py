# python
# ---------------------------------------
# Name:         SMO_GC_Multi_SimplifyToNGon_Cmd.py
# Version:      1.0
#
# Purpose:      This Command is designed to
#               (for Multiple Mesh)
#               Merge every polygons that have same coplanar polygon direction to simplify a given set of meshes.
#               Via argument you can also update the HardEdges data for a better end result.
#
# Author:       Franck ELISABETH
# Website:      http://www.smoluck.com
#
# Created:      16/06/2022
# Copyright:    (c) Franck Elisabeth 2017-2022
# ---------------------------------------

import lx, lxu, modo

Cmd_Name = "smo.GC.Multi.SimplifyToNGon"
# smo.GC.Multi.SimplifyToNGon 1

class SMO_GC_Multi_SimplifyToNGon_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
        self.dyna_Add("Set HardEdge", lx.symbol.sTYPE_BOOLEAN)
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
        return 'SMO GC - (Multi) Simplify to NGon'

    def cmd_Desc(self):
        return 'Merge every polygons that have same coplanar polygon direction to simplify a given set of meshes. Via argument you can also update the HardEdges data for a better end result.'

    def cmd_Tooltip(self):
        return 'Merge every polygons that have same coplanar polygon direction to simplify a given set of meshes. Via argument you can also update the HardEdges data for a better end result.'

    def cmd_Help(self):
        return 'https://twitter.com/sm0luck'

    def basic_ButtonName(self):
        return 'SMO GC - (Multi) Simplify to NGon'

    def basic_Enable(self, msg):
        return True

    def basic_Execute(self, msg, flags):
        SetHardEdge = self.dyna_Bool(0)
        scene = modo.scene.current()
        items = modo.Scene().selected

        selmeshessssa = scene.selectedByType(lx.symbol.sITYPE_MESH)
        lx.eval('select.drop item')

        for mesh in selmeshessssa:
            mesh.select(True)
            lx.eval('smo.GC.SimplifyToNGon %s' % SetHardEdge)
            lx.eval('select.drop item')

        scene.select(selmeshessssa)


lx.bless(SMO_GC_Multi_SimplifyToNGon_Cmd, Cmd_Name)

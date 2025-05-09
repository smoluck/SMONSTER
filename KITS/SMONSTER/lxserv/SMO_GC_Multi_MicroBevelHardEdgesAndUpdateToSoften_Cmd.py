# python
"""
Name:         SMO_GC_Multi_MicroBevelHardEdgesAndUpdateToSoften_Cmd.py

Purpose:      This Command is designed to
              (for Multiple Mesh)
              Micro Bevel HardEdges (usually after a SimplyToNgon), then Soften all edges.

Author:       Franck ELISABETH
Website:      https://www.linkedin.com/in/smoluck/
Created:      16/06/2022
Copyright:    (c) Franck Elisabeth 2017-2022
"""

import lx
import lxu
import modo

Cmd_Name = "smo.GC.Multi.MicroBevelHardEdgesAndUpdateToSoften"
# smo.GC.Multi.MicroBevelHardEdgesAndUpdateToSoften [1mm]
# Using Square Brackets around values validate the use of units like "km", "m" , "cm", "mm", "um".


class SMO_GC_Multi_MicroBevelHardEdgesAndUpdateToSoften_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
        self.dyna_Add("Witdh Value", lx.symbol.sTYPE_DISTANCE)

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
        return 'SMO GC - (Multi) MicroBevel HardEdges and Soften everything'

    def cmd_Desc(self):
        return 'MULTI - Micro Bevel HardEdges (usually after a SimplyToNgon), then Soften all edges.'

    def cmd_Tooltip(self):
        return 'MULTI - Micro Bevel HardEdges (usually after a SimplyToNgon), then Soften all edges.'

    def cmd_Help(self):
        return 'https://twitter.com/sm0luck'

    def basic_ButtonName(self):
        return 'SMO GC - (Multi) MicroBevel HardEdges and and Soften everything'

    def basic_Enable(self, msg):
        return True

    def basic_Execute(self, msg, flags):
        # ------------------------------ #
        # <----( DEFINE ARGUMENTS )----> #
        # ------------------------------ #
        ChamferValue = self.dyna_Float(0)              # Width size
        # ------------------------------ #
        # <----( DEFINE ARGUMENTS )----> #
        # ------------------------------ #

        scene = modo.scene.current()
        items = modo.Scene().selected

        selmeshessss = scene.selectedByType(lx.symbol.sITYPE_MESH)
        lx.eval('select.drop item')

        for mesh in selmeshessss:
            mesh.select(True)
            lx.eval('smo.GC.MicroBevelHardEdgesAndUpdateToSoften {%s}' % ChamferValue)
            lx.eval('select.drop item')

        scene.select(selmeshessss)


lx.bless(SMO_GC_Multi_MicroBevelHardEdgesAndUpdateToSoften_Cmd, Cmd_Name)

# python
# ---------------------------------------
# Name:         SMO_GC_Setup_Multi_MoveRotateCenterToItemBBOXCenter_Cmd.py
# Version:      1.0
#
# Purpose:      This script is designed to
#               Move Center to Item BBOX Center
#
# Author:       Franck ELISABETH
# Website:      http://www.smoluck.com
#
# Created:      22/08/2022
# Copyright:    (c) Franck Elisabeth 2017-2022
# ---------------------------------------

import lx, lxu, modo

Cmd_Name = "smo.GC.Setup.Multi.MoveRotateCenterToItemBBOXCenter"
# smo.GC.Setup.Multi.MoveRotateCenterToItemBBOXCenter 1


class SMO_GC_Setup_Multi_MoveRotateCenterToItemBBOXCenter_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
        self.dyna_Add("Move Center:", lx.symbol.sTYPE_BOOLEAN)
        # self.dyna_Add("Rotate Center:", lx.symbol.sTYPE_BOOLEAN)

        self.SelModeVert = bool(lx.eval1("select.typeFrom typelist:vertex;polygon;edge;item;ptag ?"))
        self.SelModeEdge = bool(lx.eval1("select.typeFrom typelist:edge;vertex;polygon;item;ptag ?"))
        self.SelModePoly = bool(lx.eval1("select.typeFrom typelist:polygon;vertex;edge;item;ptag ?"))
        self.SelModeItem = bool(lx.eval1("select.typeFrom typelist:item;pivot;center;edge;polygon;vertex;ptag ?"))

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
        return 'SMO GC - Setup - (Multi) - Move Center to Item BBOX Center'

    def cmd_Desc(self):
        return 'MULTI - Move Center to Item BBOX Center.'

    def cmd_Tooltip(self):
        return 'MULTI - Move Center to Item BBOX Center.'

    def cmd_Help(self):
        return 'https://twitter.com/sm0luck'

    def basic_ButtonName(self):
        return 'SMO GC - Setup - (Multi) - Move Center to Item BBOX Center'

    def basic_Enable(self, msg):
        return True

    def basic_Execute(self, msg, flags):
        if self.SelModeItem:
            MoveCenter = self.dyna_Bool(0)
            # RotateCenter = self.dyna_Bool(1)

            scene = modo.scene.current()
            items = modo.Scene().selected

            selmeshes_smrcts = scene.selectedByType(lx.symbol.sITYPE_MESH)
            lx.eval('select.drop item')

            for mesh in selmeshes_smrcts:
                mesh.select(True)
                lx.eval('smo.GC.Setup.MoveRotateCenterToSelection %s %s' % (MoveCenter, 0))
                lx.eval('select.drop item')

            scene.select(selmeshes_smrcts)

            del selmeshes_smrcts
            del MoveCenter
            # del RotateCenter


lx.bless(SMO_GC_Setup_Multi_MoveRotateCenterToItemBBOXCenter_Cmd, Cmd_Name)

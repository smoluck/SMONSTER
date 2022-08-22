# python
# ---------------------------------------
# Name:         SMO_MIFABOMA_MultiAlignToAxisWorldZero_Cmd.py
# Version:      1.0
#
# Purpose:      This script is designed to
#               Align a given Mesh item to World Axis.
#               It use X Y Z axis as argument for the direction.
#
# Author:       Franck ELISABETH
# Website:      http://www.smoluck.com
#
# Created:      17/08/2022
# Copyright:    (c) Franck Elisabeth 2017-2022
# ---------------------------------------

import lx, lxu, modo

Cmd_Name = "smo.MIFABOMA.MultiAlignToAxisWorldZero"
# smo.MIFABOMA.MultiAlignToAxisWorldZero z



class SMO_MIFABOMA_MultiAlignToAxisWorldZero_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
        self.dyna_Add("Axis", lx.symbol.sTYPE_AXIS)

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
        return 'SMO MIFABOMA - (Multi) AlignToAxisWorldZero'

    def cmd_Desc(self):
        return 'Align a given Mesh item to World Axis. It use X Y Z axis as argument for the direction.'

    def cmd_Tooltip(self):
        return 'Align a given Mesh item to World Axis. It use X Y Z axis as argument for the direction.'

    def cmd_Help(self):
        return 'https://twitter.com/sm0luck'

    def basic_ButtonName(self):
        return 'SMO MIFABOMA - (Multi) AlignToAxisWorldZero'

    def basic_Enable(self, msg):
        return True

    def basic_Execute(self, msg, flags):
        Axis = self.dyna_String(0)
        scene = modo.scene.current()
        items = modo.Scene().selected

        selmeshes_ksfs = scene.selectedByType(lx.symbol.sITYPE_MESH)
        lx.eval('select.drop item')

        for mesh in selmeshes_ksfs:
            mesh.select(True)
            lx.eval('smo.MIFABOMA.AlignToAxisWorldZero %s' % Axis)
            lx.eval('select.drop item')

        scene.select(selmeshes_ksfs)

        del selmeshes_ksfs


lx.bless(SMO_MIFABOMA_MultiAlignToAxisWorldZero_Cmd, Cmd_Name)


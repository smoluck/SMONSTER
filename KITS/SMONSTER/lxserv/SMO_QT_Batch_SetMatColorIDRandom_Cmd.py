# python
# ---------------------------------------
# Name:         SMO_QT_Batch_SetMatColorIDRandom_Cmd.py
# Version:      1.0
#
# Purpose:      This script is designed to:
#               Set a random Diffuse Color override using Material Tag.
#               It can runs over Selected Meshes or SceneWide, By Items or by Polygon Islands.
#
# Author:       Franck ELISABETH
# Website:      http://www.smoluck.com
#
# Created:      12/04/2022
# Copyright:    (c) Franck Elisabeth 2017-2022
# ---------------------------------------

import lx, lxu, modo

Command_Name = "smo.QT.Batch.SetMatColorIDRandom"
# smo.QT.Batch.SetMatColorIDRandom 1 1

class SMO_QT_Batch_SetMatColorIDRandom_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
        self.dyna_Add("Mode: SceneWide (not Current Selected Meshes)", lx.symbol.sTYPE_BOOLEAN)  # SceneWide (True) or Current Selected Meshes (False)
        self.dyna_Add("Mode: By Islands (not By Item)", lx.symbol.sTYPE_BOOLEAN)  # By Islands on each Meshes (True) or By Item (False)

    def cmd_Flags(self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO

    def cmd_Interact(self):
        pass

    def cmd_UserName(self):
        return 'SMO QT - Set ColorID Random (by Material Tag) - SceneWide and/or By Islands'

    def cmd_Desc(self):
        return 'Set a random Diffuse Color override using Material Tag. It can runs over Selected Meshes or SceneWide, By Items or by Polygon Islands.'

    def cmd_Tooltip(self):
        return 'Set a random Diffuse Color override using Material Tag. It can runs over Selected Meshes or SceneWide, By Items or by Polygon Islands.'

    def cmd_Help(self):
        return 'https://twitter.com/sm0luck'

    def basic_ButtonName(self):
        return 'SMO QT - Set ColorID Random (by Material Tag) - SceneWide and/or By Islands'

    def basic_Enable(self, msg):
        return True

    def basic_Execute(self, msg, flags):
        scene = modo.scene.current()

        SceneWide = bool()
        ByIslands = bool()

        # SceneWide (True) or Current Selected Meshes (False)
        if not self.dyna_Bool(0):
            SceneWide = False
        if self.dyna_Bool(0):
            SceneWide = self.dyna_Bool(0)
        if SceneWide == True:
            lx.eval('smo.GC.DeselectAll')
            lx.eval('select.itemType mesh')

        # By Islands on each Meshes (True) or By Item (False)
        if self.dyna_Bool(1):
            ByIslands = self.dyna_Bool(1)
        if not self.dyna_Bool(1):
            ByIslands = False

        meshes_list = scene.selectedByType(lx.symbol.sITYPE_MESH)
        # print(meshes_list)

        ### Grouping and Separate meshes parts
        for mesh in meshes_list:
            mesh.select(True)
            if ByIslands == False:
                lx.eval('smo.QT.SetMatColorIDRandom')
            if ByIslands == True:
                lx.eval('smo.QT.SetMatColorIDByMeshIslands')
            lx.eval('select.type polygon')
            lx.eval('select.drop polygon')
            lx.eval('select.type item')
            lx.eval('smo.GC.DeselectAll')

lx.bless(SMO_QT_Batch_SetMatColorIDRandom_Cmd, Command_Name)
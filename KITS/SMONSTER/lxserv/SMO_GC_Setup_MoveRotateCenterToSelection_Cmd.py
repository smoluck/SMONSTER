# python
"""
Name:         SMO_GC_Setup_MoveRotateCenterToSelection_Cmd.py

Purpose:      This script is designed to:
              Move and / or Rotate the Center to Selection center (use it in item mode or Component mode).

Author:       Franck ELISABETH
Website:      https://www.smoluck.com
Created:      21/05/2021
Copyright:    (c) Franck Elisabeth 2017-2022
"""

import lx
import lxu
import modo

Cmd_Name = "smo.GC.Setup.MoveRotateCenterToSelection"
# smo.GC.Setup.MoveRotateCenterToSelection 1 1


class SMO_GC_Setup_MoveRotateCenterToSelection_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
        self.dyna_Add("Move Center to Selection Center:", lx.symbol.sTYPE_BOOLEAN)
        self.dyna_Add("Rotate Center to Selection Center:", lx.symbol.sTYPE_BOOLEAN)

        self.SelModeVert = bool(lx.eval1("select.typeFrom typelist:vertex;edge;polygon;item ?"))
        self.SelModeEdge = bool(lx.eval1("select.typeFrom typelist:edge;vertex;polygon;item ?"))
        self.SelModePoly = bool(lx.eval1("select.typeFrom typelist:polygon;vertex;edge;item ?"))
        self.SelModeItem = bool(lx.eval1("select.typeFrom typelist:item;edge;polygon;vertex ?"))

    def cmd_Flags(self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO

    def cmd_Interact(self):
        pass

    def cmd_UserName(self):
        return 'SMO GC - Setup - Move And Rotate Center'

    def cmd_Desc(self):
        return 'Move and / or Rotate the Center to Selection center (use it in item mode or Component mode).'

    def cmd_Tooltip(self):
        return 'Move and / or Rotate the Center to Selection center (use it in item mode or Component mode).'

    def cmd_Help(self):
        return 'https://twitter.com/sm0luck'

    def basic_ButtonName(self):
        return 'SMO GC - Setup - Move And Rotate Center'

    def basic_Enable(self, msg):
        return True

    def basic_Execute(self, msg, flags):
        scene = modo.scene.current()
        item_mode = bool()
        if self.SelModePoly or self.SelModeEdge or self.SelModeVert:
            lx.eval('smo.MASTER.ForceSelectMeshItemOnly')
            item_mode = False

        elif self.SelModeItem:
            item_mode = True
            lx.eval('select.type polygon')
            lx.eval('select.all')
        mesh = scene.selectedByType('mesh')[0]

        MoveCenter = self.dyna_Bool(0)
        RotateCenter = self.dyna_Bool(1)


        # BugFix to preserve the state of the RefSystem (item at origin in viewport)
        # This query only works when an item is selected.
        RefSystemActive = bool()
        CurrentRefSystemItem = lx.eval('item.refSystem ?')
        # print(CurrentRefSystemItem)
        if len(CurrentRefSystemItem) != 0:
            RefSystemActive = True
        else:
            RefSystemActive = False
        # print(RefSystemActive)



        if RefSystemActive:
            lx.eval('item.refSystem {}')


        if MoveCenter:
            if self.SelModeVert:
                lx.eval('smo.MASTER.SelectModeDetector')
                CountVert = lx.eval1('user.value SMO_SelectModeDetector_CountVertSelected ?')
                # print(CountVert)
            if self.SelModeVert and CountVert >= 2:
                lx.eval('select.convert edge')
            lx.eval('workPlane.fitSelect')
            lx.eval('select.type item')
            lx.eval('select.convert type:center')
            lx.eval('matchWorkplanePos')
            lx.eval('workPlane.reset')


            if not item_mode:
                if self.SelModePoly:
                    lx.eval('select.type polygon')
                if self.SelModeEdge:
                    lx.eval('select.type edge')
                if self.SelModeVert:
                    lx.eval('select.type vertex')

            if item_mode:
                if self.SelModeItem:
                    lx.eval('select.type item')

        if RotateCenter:
            if self.SelModeVert:
                lx.eval('smo.MASTER.SelectModeDetector')
                CountVert = lx.eval1('user.value SMO_SelectModeDetector_CountVertSelected ?')
                # print(CountVert)
            if self.SelModeVert and CountVert >= 2:
                lx.eval('select.convert edge')
            lx.eval('workPlane.fitSelect')
            lx.eval('select.type item')
            lx.eval('select.convert type:center')
            lx.eval('matchWorkplaneRot')
            lx.eval('workPlane.reset')

            if not item_mode:
                if self.SelModePoly:
                    lx.eval('select.type polygon')
                if self.SelModeEdge:
                    lx.eval('select.type edge')
                if self.SelModeVert:
                    lx.eval('select.type vertex')

            if item_mode:
                if self.SelModeItem:
                    lx.eval('select.type item')
                    lx.eval('select.type polygon')
                    lx.eval('select.drop polygon')
                    lx.eval('select.type item')


        if RefSystemActive:
            lx.eval('item.refSystem {}')
        if RefSystemActive:
            lx.eval('item.refSystem %s' % CurrentRefSystemItem)

        del MoveCenter
        del RotateCenter
        del CurrentRefSystemItem
        del item_mode


lx.bless(SMO_GC_Setup_MoveRotateCenterToSelection_Cmd, Cmd_Name)

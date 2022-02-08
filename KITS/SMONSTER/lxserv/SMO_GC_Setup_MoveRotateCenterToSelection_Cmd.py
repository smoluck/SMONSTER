# python
# ---------------------------------------------
# Name:         SMO_GC_Setup_MoveRotateCenterToSelection_Cmd.py
# Version:      1.0
#
# Purpose:      This script is designed to:
#               Select an Opened Mesh Move and Rotate
#               the Center to Open boundary centroid and rotate it (use it in item mode)
#
# Author:       Franck ELISABETH
# Website:      http://www.smoluck.com
#
# Created:      21/05/2021
# Copyright:    (c) Franck Elisabeth 2017-2022
# ---------------------------------------------


import lx, lxu, modo

Command_Name = "smo.GC.Setup.MoveRotateCenterToSelection"
# smo.GC.Setup.MoveRotateCenterToSelection 1 1

class SMO_GC_Setup_MoveRotateCenterToSelection_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
        self.dyna_Add("Move Center:", lx.symbol.sTYPE_INTEGER)
        self.dyna_Add("Rotate Center:", lx.symbol.sTYPE_INTEGER)

        self.SelModeVert = bool(lx.eval1("select.typeFrom typelist:vertex;edge;polygon;item ?"))
        self.SelModeEdge = bool(lx.eval1("select.typeFrom typelist:edge;vertex;polygon;item ?"))
        self.SelModePoly = bool(lx.eval1("select.typeFrom typelist:polygon;vertex;edge;item ?"))

    def cmd_Flags(self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO

    def cmd_Interact(self):
        pass

    def cmd_UserName(self):
        return 'SMO GC Set Move And Rotate Center Using Open Boundary'

    def cmd_Desc(self):
        return 'Select an Opened Mesh Move and Rotate the Center to Open boundary centroid and rotate it (use it in item mode)'

    def cmd_Tooltip(self):
        return 'Select an Opened Mesh Move and Rotate the Center to Open boundary centroid and rotate it (use it in item mode)'

    def cmd_Help(self):
        return 'https://twitter.com/sm0luck'

    def basic_ButtonName(self):
        return 'SMO GC Set Move And Rotate Center Using Open Boundary'

    def cmd_Flags(self):
        return lx.symbol.fCMD_UNDO

    def basic_Enable(self, msg):
        return True

    def basic_Execute(self, msg, flags):
        scene = modo.scene.current()
        if self.SelModePoly == True or self.SelModeEdge == True or self.SelModeVert == True :
            lx.eval('smo.MASTER.ForceSelectMeshItemOnly')
        mesh = scene.selectedByType('mesh')[0]

        MoveCenter = self.dyna_Int (0)
        RotateCenter = self.dyna_Int (1)


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



        if RefSystemActive == True:
            lx.eval('item.refSystem {}')


        if MoveCenter == 1:
            if self.SelModeVert == True:
                lx.eval('smo.MASTER.SelectModeDetector')
                CountVert = lx.eval1('user.value SMO_SelectModeDetector_CountVertSelected ?')
                # print(CountVert)
            if self.SelModeVert == True and CountVert >= 2:
                lx.eval('select.convert edge')
            lx.eval('workPlane.fitSelect')
            lx.eval('select.type item')
            lx.eval('select.convert type:center')
            lx.eval('matchWorkplanePos')
            lx.eval('workPlane.reset')

            if self.SelModePoly == True :
                lx.eval('select.type polygon')
            if self.SelModeEdge == True :
                lx.eval('select.type edge')
            if self.SelModeVert == True :
                lx.eval('select.type vertex')

        if RotateCenter == 1:
            if self.SelModeVert == True:
                lx.eval('smo.MASTER.SelectModeDetector')
                CountVert = lx.eval1('user.value SMO_SelectModeDetector_CountVertSelected ?')
                # print(CountVert)
            if self.SelModeVert == True and CountVert >= 2:
                lx.eval('select.convert edge')
            lx.eval('workPlane.fitSelect')
            lx.eval('select.type item')
            lx.eval('select.convert type:center')
            lx.eval('matchWorkplaneRot')
            lx.eval('workPlane.reset')

            if self.SelModePoly == True :
                lx.eval('select.type polygon')
            if self.SelModeEdge == True :
                lx.eval('select.type edge')
            if self.SelModeVert == True :
                lx.eval('select.type vertex')


        if RefSystemActive == False:
            lx.eval('item.refSystem {}')
        if RefSystemActive == True:
            lx.eval('item.refSystem %s' % CurrentRefSystemItem)

lx.bless(SMO_GC_Setup_MoveRotateCenterToSelection_Cmd, Command_Name)
# python
"""
Name:         SMO_GC_SelectVertexByLocalAxis_Cmd.py

Purpose:      This script is designed to
              select vertex based on their local position.
              it use X Y Z axis as argument and Positive or Negative Direction as selection mode.

Author:       Franck ELISABETH
Website:      https://www.smoluck.com
Created:      17/08/2022
Copyright:    (c) Franck Elisabeth 2017-2022
"""

import lx
import lxu

Cmd_Name = "smo.GC.SelectVertexByLocalAxis"
# smo.GC.SelectVertexByLocalAxis z true


class SMO_GC_SelectVertexByLocalAxis_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
        self.dyna_Add("Axis", lx.symbol.sTYPE_AXIS)
        self.dyna_Add("Direction", lx.symbol.sTYPE_BOOLEAN)
        self.SelModeVert = bool(lx.eval1("select.typeFrom typelist:vertex;polygon;edge;item;ptag ?"))
        self.SelModeEdge = bool(lx.eval1("select.typeFrom typelist:edge;vertex;polygon;item;ptag ?"))
        self.SelModePoly = bool(lx.eval1("select.typeFrom typelist:polygon;vertex;edge;item;ptag ?"))
        self.SelModeItem = bool(lx.eval1("select.typeFrom typelist:item;pivot;center;edge;polygon;vertex;ptag ?"))
        self.CompMode = int()
        if self.SelModeVert:
            self.CompMode = 1
        if self.SelModeEdge:
            self.CompMode = 2
        if self.SelModePoly:
            self.CompMode = 3
        if self.SelModeItem:
            self.CompMode = 4
        # print(self.SelModeVert)
        # print(self.SelModeEdge)
        # print(self.SelModePoly)
        # print(self.SelModeItem)
        lx.eval('select.type vertex')
        lx.eval('select.drop vertex')
        if self.CompMode == 1:
            lx.eval('select.type vertex')
        if self.CompMode == 2:
            lx.eval('select.type edge')
        if self.CompMode == 3:
            lx.eval('select.type polygon')
        if self.CompMode == 4:
            lx.eval('select.type item')

    def cmd_Flags(self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO

    def cmd_Interact(self):
        pass

    def cmd_UserName(self):
        return 'SMO GC - SelectVertexByLocalAxis'

    def cmd_Desc(self):
        return 'Select vertex based on their local position. It use X Y Z axis as argument and Positive or Negative Direction as selection mode.'

    def cmd_Tooltip(self):
        return 'Select vertex based on their local position. It use X Y Z axis as argument and Positive or Negative Direction as selection mode.'

    def cmd_Help(self):
        return 'https://twitter.com/sm0luck'

    def basic_ButtonName(self):
        return 'SMO GC - SelectVertexByLocalAxis'

    def basic_Enable(self, msg):
        return True

    def basic_Execute(self, msg, flags):
        Axis = self.dyna_String(0)
        PositiveDir = self.dyna_Bool(1)
        CurrentCompMode = self.CompMode

        lx.eval('select.type vertex')

        layer_id = lx.eval("query layerservice layer.index ? current")
        print('current item:', layer_id)
        vert_num = lx.eval("query layerservice vert.N ? all")
        print('vertex count on item:', vert_num)

        mylist = []

        for i in range(vert_num):
            vertPOS = lx.eval("query layerservice vert.workpos ? %s" % i)
            vert_pos_x = vertPOS[0]
            vert_pos_y = vertPOS[1]
            vert_pos_z = vertPOS[2]

            if not PositiveDir:
                if Axis == "x":
                    if vert_pos_x < 0.0:
                        mylist.append(i)
                if Axis == "y":
                    if vert_pos_y < 0.0:
                        mylist.append(i)
                if Axis == "z":
                    if vert_pos_z < 0.0:
                        mylist.append(i)

            if PositiveDir:
                if Axis == "x":
                    if vert_pos_x > 0.0:
                        mylist.append(i)
                if Axis == "y":
                    if vert_pos_y > 0.0:
                        mylist.append(i)
                if Axis == "z":
                    if vert_pos_z > 0.0:
                        mylist.append(i)
        # print(mylist)
        for i in range(len(mylist)):
            lx.eval("select.element %s vertex add %s" % (layer_id, mylist[i]))
            # Print result
            # lx.out(i, " ", vertPOS)

        if CurrentCompMode == 2:
            lx.eval('select.convert edge')
        if CurrentCompMode == 3:
            lx.eval('select.convert polygon')

        del mylist


lx.bless(SMO_GC_SelectVertexByLocalAxis_Cmd, Cmd_Name)


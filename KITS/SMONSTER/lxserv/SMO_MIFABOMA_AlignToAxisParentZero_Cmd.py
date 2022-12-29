# python
"""
Name:         SMO_MIFABOMA_AlignToAxisParentZero_Cmd.py

Purpose:      This script is designed to
              Align a given Mesh item to Parent Axis.
              It use X Y Z axis as argument for the direction.

Author:       Franck ELISABETH
Website:      https://www.smoluck.com
Created:      17/08/2022
Copyright:    (c) Franck Elisabeth 2017-2022
"""

import lx
import lxu
import modo

Cmd_Name = "smo.MIFABOMA.AlignToAxisParentZero"
# smo.MIFABOMA.AlignToAxisParentZero z


class SMO_MIFABOMA_AlignToAxisParentZero_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
        self.dyna_Add("Axis", lx.symbol.sTYPE_AXIS)
        self.SelModeVert = bool(lx.eval1("select.typeFrom typelist:vertex;polygon;edge;item;ptag ?"))
        self.SelModeEdge = bool(lx.eval1("select.typeFrom typelist:edge;vertex;polygon;item;ptag ?"))
        self.SelModePoly = bool(lx.eval1("select.typeFrom typelist:polygon;vertex;edge;item;ptag ?"))
        self.SelModeItem = bool(lx.eval1("select.typeFrom typelist:item;pivot;center;edge;polygon;vertex;ptag ?"))
        # print(self.SelModeVert)
        # print(self.SelModeEdge)
        # print(self.SelModePoly)
        # print(self.SelModeItem)

    def cmd_Flags(self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO

    def cmd_Interact(self):
        pass

    def cmd_UserName(self):
        return 'SMO MIFABOMA - AlignToAxisParentZero'

    def cmd_Desc(self):
        return 'Align a given Mesh item to Parent Axis. It use X Y Z axis as argument for the direction.'

    def cmd_Tooltip(self):
        return 'Align a given Mesh item to Parent Axis. It use X Y Z axis as argument for the direction.'

    def cmd_Help(self):
        return 'https://twitter.com/sm0luck'

    def basic_ButtonName(self):
        return 'SMO MIFABOMA - AlignToAxisParentZero'

    def basic_Enable(self, msg):
        return True

    def basic_Execute(self, msg, flags):
        Axis = self.dyna_String(0)

        scene = modo.Scene()

        TargetMeshes = scene.selected
        mi = modo.Item()  # selected item,
        name = mi.UniqueName()
        # print('Mesh Name is:', name)
        ident = mi.Ident()
        # print('Mesh ID is:', ident)
        p_name = []
        try:
            p = mi.Parent()
            p_name = p.UniqueName()
            p_ident = p.Ident()
            # print('Parent Name of %s  is : %s' % (name, p_name))
            # print(p_name)
        except:
            pass

        if len(p_name) != 0:
            scene.select(p.Ident())

        mRef = lx.eval('query sceneservice selection ? mesh')
        TargetXfrm = lx.eval1("query sceneservice item.xfrmPos ? " + mRef)
        # print(TargetXfrm)

        if Axis == "x":
            lx.eval('select.channel {%s:pos.X} set' % TargetXfrm)
            lx.eval('transform.channel pos.X 0.0')
        if Axis == "y":
            lx.eval('select.channel {%s:pos.Y} set' % TargetXfrm)
            lx.eval('transform.channel pos.Y 0.0')
        if Axis == "z":
            lx.eval('select.channel {%s:pos.Z} set' % TargetXfrm)
            lx.eval('transform.channel pos.Z 0.0')
        lx.eval('select.drop channel')

        if len(p_name) != 0:
            lx.eval('select.subItem %s add mesh 0 0' % p_ident)
            lx.eval('item.parent inPlace:1')
        lx.eval('smo.GC.DeselectAll')
        scene.select(TargetMeshes)

        del p_name


lx.bless(SMO_MIFABOMA_AlignToAxisParentZero_Cmd, Cmd_Name)


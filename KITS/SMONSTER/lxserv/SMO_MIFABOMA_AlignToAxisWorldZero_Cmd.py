# python
# ---------------------------------------
# Name:         SMO_MIFABOMA_AlignToAxisWorldZero_Cmd.py
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

Cmd_Name = "smo.MIFABOMA.AlignToAxisWorldZero"
# smo.MIFABOMA.AlignToAxisWorldZero z


class SMO_MIFABOMA_AlignToAxisWorldZero_Cmd(lxu.command.BasicCommand):
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
        return 'SMO MIFABOMA - AlignToAxisWorldZero'

    def cmd_Desc(self):
        return 'Align a given Mesh item to World Axis. It use X Y Z axis as argument for the direction.'

    def cmd_Tooltip(self):
        return 'Align a given Mesh item to World Axis. It use X Y Z axis as argument for the direction.'

    def cmd_Help(self):
        return 'https://twitter.com/sm0luck'

    def basic_ButtonName(self):
        return 'SMO MIFABOMA - AlignToAxisWorldZero'

    def basic_Enable(self, msg):
        return True

    def basic_Execute(self, msg, flags):
        Axis = self.dyna_String(0)

        scene = modo.Scene()
        PositiveDir = True

        DeleteDir = bool()
        if PositiveDir:
            DeleteDir = False
        if not PositiveDir:
            DeleteDir = True

        Target_Meshes = scene.selected
        mi = modo.Item()  # selected item,
        name = mi.UniqueName()
        # print('Mesh Name is:', name)
        ident = mi.Ident()
        # print('Mesh ID is:', ident)
        p_name = []
        HaveParent = bool()
        try:
            p = mi.Parent()
            p_name = p.UniqueName()
            p_ident = p.Ident()
            # print('Parent Name of %s  is : %s' % (name, p_name))
            # print(p_name)
            HaveParent = True
        except:
            HaveParent = False
            pass

        if HaveParent:
            lx.eval('!item.parent parent:{} inPlace:1')
        if not HaveParent:
            lx.eval('item.create locator applyDefaultPreset:true')
            world_item = modo.Item().Ident()
            scene.select(ident)
            scene.select(world_item, "add")
            lx.eval('item.parent inPlace:1')

        lx.eval('smo.GC.DeselectAll')
        lx.eval('item.create locator applyDefaultPreset:true')
        lo_item = modo.Item().Ident()

        # lx.eval('item.refSystem %s' % lo_item)
        scene.select(ident, "add")
        lx.eval('item.parent inPlace:1')
        scene.select(lo_item)
        lx.eval('transform.reset translation')
        lx.eval('item.parent parent:{} inPlace:1')
        scene.select(ident)
        scene.select(lo_item, "add")
        lx.eval('item.parent inPlace:1')
        scene.select(lo_item)
        locator = lx.eval('query sceneservice selection ? locator')
        LocXfrm = lx.eval1("query sceneservice item.xfrmPos ? " + locator)

        if Axis == "x":
            lx.eval('select.channel {%s:pos.X} set' % LocXfrm)
            lx.eval('transform.channel pos.X 0.0')
        if Axis == "y":
            lx.eval('select.channel {%s:pos.Y} set' % LocXfrm)
            lx.eval('transform.channel pos.Y 0.0')
        if Axis == "z":
            lx.eval('select.channel {%s:pos.Z} set' % LocXfrm)
            lx.eval('transform.channel pos.Z 0.0')
        lx.eval('select.drop channel')

        scene.select(ident)
        lx.eval('item.parent parent:{} inPlace:1')
        scene.select(lo_item)
        lx.eval('!delete')
        if not HaveParent:
            scene.select(world_item)
            lx.eval('!delete')
        scene.select(ident)

        if HaveParent:
            lx.eval('select.subItem %s add mesh 0 0' % p_ident)
            lx.eval('item.parent inPlace:1')
        lx.eval('smo.GC.DeselectAll')
        scene.select(Target_Meshes)

        del HaveParent
        del PositiveDir


lx.bless(SMO_MIFABOMA_AlignToAxisWorldZero_Cmd, Cmd_Name)


# python
# ---------------------------------------
# Name:         SMO_UV_MultiUnwrapPlanar_Cmd.py
# Version:      1.0
#
# Purpose:      This script is designed to
#               Unwrap the current Polygon Selection
#               on defined Axis.
#
# Author:       Franck ELISABETH
# Website:      http://www.smoluck.com
#
# Created:      28/12/2018
# Copyright:    (c) Franck Elisabeth 2017-2022
# ---------------------------------------

import lx, lxu, modo

Cmd_Name = "smo.UV.MultiUnwrapPlanar"
# smo.UV.MultiUnwrapPlanar 2 0

class SMO_UV_MultiUnwrapPlanar_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
        self.dyna_Add("Unwrap Projection Axis", lx.symbol.sTYPE_INTEGER)
        self.basic_SetFlags(0, lx.symbol.fCMDARG_OPTIONAL)  # here the (0) define the argument index.
        self.dyna_Add("Facing Ratio Mode", lx.symbol.sTYPE_INTEGER)
        self.basic_SetFlags(1, lx.symbol.fCMDARG_OPTIONAL)

        self.SelModeVert = bool(lx.eval1("select.typeFrom typelist:vertex;polygon;edge;item;ptag ?"))
        self.SelModeEdge = bool(lx.eval1("select.typeFrom typelist:edge;vertex;polygon;item ?"))
        self.SelModePoly = bool(lx.eval1("select.typeFrom typelist:polygon;vertex;edge;item ?"))
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
        return 'SMO UV - (Multi) Unwrap Smart MultiMeshes'

    def cmd_Desc(self):
        return 'Unwrap the current Polygon Selection on defined Axis.'

    def cmd_Tooltip(self):
        return 'Unwrap the current Polygon Selection on defined Axis.'

    def cmd_Help(self):
        return 'https://twitter.com/sm0luck'

    def basic_ButtonName(self):
        return 'SMO UV - (Multi) Unwrap Smart MultiMeshes'

    def basic_Enable(self, msg):
        return True

    def basic_Execute(self, msg, flags):
        UVProjAxe = self.dyna_Int(0)
        Similar = self.dyna_Int(1)

        scene = modo.scene.current()


        SelItem = lxu.select.ItemSelection().current()
        # print('lxu.object.Item : ', SelItem)

        mesh = scene.selectedByType('mesh')
        # print('modo.Mesh :', mesh)
        # print('modo.Mesh list length:', len(mesh))

        TargetIDList = []
        for item in mesh:
            itemType = modo.Item(item).type
            item = lx.object.Item(item)
            # print(item)
            if itemType == "mesh":
                ID = item.Ident()
                # print(ID)
                TargetIDList.append(ID)
        # print(TargetIDList)

        PolysTuple = []
        for item in mesh:
            # CsPolys = len(item.geometry.polygons.selected)
            # print('Total selected Polygons on this mesh layer', CsPolys)
            Polys = item.geometry.polygons.selected
            # print('modo.Mesh list ', Polys)
            PolysTuple.append(Polys)
        # print('Tuple (Poly ID and Mesh ID): ---)', PolysTuple)

        PolysList = list(PolysTuple)
        # print('List (Poly ID and Mesh ID): ---)', PolysList)
        # print(PolysList)
        # print('------------------')
        # print(PolysList[0])
        # print('------')
        # print(PolysList[1])
        # print('------')
        # print(PolysList[2])
        # print('------')
        # print(PolysList[3])
        # print('------')

        lx.eval('select.drop polygon')
        lx.eval('smo.GC.DeselectAll')
        lx.eval('select.type item')
        lx.eval('smo.GC.DeselectAll')

        index = -1
        for m in TargetIDList:
            index = (index + 1)
            # print('id :', index)
            scene.select(m)
            selected_mesh = scene.selectedByType('mesh')[0]
            # print('current mesh indentity :', index, selected_mesh)
            lx.eval('select.type polygon')
            lx.eval('select.drop polygon')
            for item in (PolysList[index]):
                # print(item)
                selected_mesh.geometry.polygons.select(item)
            ############### PUT YOUR Command HERE to run over each item Polygons
            try:
                lx.eval('smo.UV.UnwrapPlanar %s %s' % (UVProjAxe, Similar))
            except:
                lx.out('Error on {%s}' % (lx.eval('item.name ? xfrmcore')))
            selected_mesh.geometry.polygons.select(item, replace=True)
            lx.eval('select.type polygon')
            lx.eval('select.drop polygon')
            lx.eval('select.type item')
            lx.eval('select.drop item')
            # GOOOOOOOOOOOOD
        lx.eval('smo.GC.DeselectAll')

        for item in (PolysList):
            # print(item)
            selected_mesh.geometry.polygons.select(item)

        del index
        del TargetIDList
        del PolysList
        del PolysTuple
        lx.eval('select.type polygon')


lx.bless(SMO_UV_MultiUnwrapPlanar_Cmd, Cmd_Name)

# python
# ---------------------------------------------
# Name:         SMO_GC_Setup_Multi_MoveRotateCenterToSelection_Cmd.py
# Version:      1.0
#
# Purpose:      This script is designed to:
#               Move and / or Rotate the Center to Selection center (use it in item mode or Component mode).
#
# Author:       Franck ELISABETH
# Website:      http://www.smoluck.com
#
# Created:      22/08/2022
# Copyright:    (c) Franck Elisabeth 2017-2022
# ---------------------------------------------

import lx, lxu, modo

Cmd_Name = "smo.GC.Setup.Multi.MoveRotateCenterToSelection"
# smo.GC.Setup.Multi.MoveRotateCenterToSelection 1 0

class SMO_GC_Setup_Multi_MoveRotateCenterToSelection_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
        self.dyna_Add("Move Center to Selection Center:", lx.symbol.sTYPE_BOOLEAN)
        self.dyna_Add("Rotate Center to Selection Center:", lx.symbol.sTYPE_BOOLEAN)

        self.SelModeVert = bool(lx.eval1("select.typeFrom typelist:vertex;polygon;edge;item;ptag ?"))
        self.SelModeEdge = bool(lx.eval1("select.typeFrom typelist:edge;vertex;polygon;item ?"))
        self.SelModePoly = bool(lx.eval1("select.typeFrom typelist:polygon;vertex;edge;item ?"))
        self.SelModeItem = bool(lx.eval1("select.typeFrom typelist:item;pivot;center;edge;polygon;vertex;ptag ?"))
        # print(self.SelModeVert)
        # print(self.SelModeEdge)
        # print(self.SelModePoly)
        # print(self.SelModeItem)
        self.sel_mode = int()
        if self.SelModeVert:
            self.sel_mode = 1
        if self.SelModeEdge:
            self.sel_mode = 2
        if self.SelModePoly:
            self.sel_mode = 3
        if self.SelModeItem:
            self.sel_mode = 5

    def cmd_Flags(self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO

    def cmd_Interact(self):
        pass

    def cmd_UserName(self):
        return 'SMO GC - Setup - (Multi) Move And Rotate Center'

    def cmd_Desc(self):
        return 'Move and / or Rotate the Center to Selection center (use it in item mode or Component mode).'

    def cmd_Tooltip(self):
        return 'Move and / or Rotate the Center to Selection center (use it in item mode or Component mode).'

    def cmd_Help(self):
        return 'https://twitter.com/sm0luck'

    def basic_ButtonName(self):
        return 'SMO GC - Setup - (Multi) Move And Rotate Center'

    def basic_Enable(self, msg):
        return True

    def basic_Execute(self, msg, flags):
        MoveCenter = self.dyna_Bool(0)
        RotateCenter = self.dyna_Bool(1)

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

        ComponentTuple = []
        ComponentList = list()
        if self.sel_mode == 1:
            for item in mesh:
                # CsVertex = len(item.geometry.vertices.selected)
                # print('Total selected Vertex on this mesh layer', CsVertex)
                Vertex = item.geometry.vertices.selected
                # print('modo.Mesh list ',Vertex)
                ComponentTuple.append(Vertex)
            # print('Tuple (Vertex ID and Mesh ID): ---)', ComponentTuple)
            lx.eval('select.drop vertex')

        if self.sel_mode == 2:
            for item in mesh:
                # CsEdges = len(item.geometry.edges.selected)
                # print('Total selected Edges on this mesh layer', CsEdges)
                Edges = item.geometry.edges.selected
                # print('modo.Mesh list ',Edges)
                ComponentTuple.append(Edges)
            # print('Tuple (Edges ID and Mesh ID): ---)', ComponentTuple)
            lx.eval('select.drop edge')

        if self.sel_mode == 3:
            for item in mesh:
                # CsPolys = len(item.geometry.polygons.selected)
                # print('Total selected Polygons on this mesh layer', CsPolys)
                Polys = item.geometry.polygons.selected
                # print('modo.Mesh list ', Polys)
                ComponentTuple.append(Polys)
            # print('Tuple (Poly ID and Mesh ID): ---)', ComponentTuple)
            lx.eval('select.drop polygon')

        # if self.sel_mode == 5:
        #     for item in mesh:
        #         # CsPolys = len(item.geometry.polygons.selected)
        #         # print('Total selected Polygons on this mesh layer', CsPolys)
        #         Polys = item.geometry.polygons.selected
        #         # print('modo.Mesh list ', Polys)
        #         ComponentTuple.append(Polys)
        #     # print('Tuple (Poly ID and Mesh ID): ---)', ComponentTuple)
        #     lx.eval('select.drop polygon')

        ComponentList = list(ComponentTuple)
        # print('List (Vertex ID and Mesh ID): ---)', ComponentList)


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
            if self.sel_mode == 1:
                lx.eval('select.type vertex')
                lx.eval('select.drop vertex')
                for item in (ComponentList[index]):
                    # print(item)
                    selected_mesh.geometry.vertices.select(item)
            if self.sel_mode == 2:
                lx.eval('select.type edge')
                lx.eval('select.drop edge')
                for item in (ComponentList[index]):
                    # print(item)
                    selected_mesh.geometry.edges.select(item)
            if self.sel_mode == 3:
                lx.eval('select.type polygon')
                lx.eval('select.drop polygon')
                for item in (ComponentList[index]):
                    # print(item)
                    selected_mesh.geometry.polygons.select(item)
            if self.sel_mode == 5:
                lx.eval('select.type polygon')
                lx.eval('select.drop polygon')
                lx.eval('select.all')
            ############### PUT YOUR Command HERE to run over each item Polygons
            try:
                lx.eval('smo.GC.Setup.MoveRotateCenterToSelection %s %s' % (MoveCenter, RotateCenter))
            except:
                lx.out('Error on {%s}' % (lx.eval('item.name ? xfrmcore')))
            if self.sel_mode == 1:
                selected_mesh.geometry.vertices.select(item, replace=True)
                lx.eval('select.type vertex')
                lx.eval('select.drop vertex')
            if self.sel_mode == 2:
                selected_mesh.geometry.edges.select(item, replace=True)
                lx.eval('select.type edge')
                lx.eval('select.drop edge')
            if self.sel_mode == 3:
                selected_mesh.geometry.polygons.select(item, replace=True)
                lx.eval('select.type polygon')
                lx.eval('select.drop polygon')
            if self.sel_mode == 5:
                lx.eval('select.type polygon')
                lx.eval('select.drop polygon')
            lx.eval('select.type item')
            lx.eval('select.drop item')
            # GOOOOOOOOOOOOD
        lx.eval('smo.GC.DeselectAll')

        for item in (ComponentList):
            # print(item)
            if self.sel_mode == 1:
                selected_mesh.geometry.vertices.select(item)
            if self.sel_mode == 2:
                selected_mesh.geometry.edges.select(item)
            if self.sel_mode == 3:
                selected_mesh.geometry.polygons.select(item)

        if self.sel_mode == 1:
            scene.select(SelItem)
            lx.eval('select.type vertex')
            selected_mesh.geometry.vertices.select(ComponentList)
        if self.sel_mode == 2:
            scene.select(SelItem)
            lx.eval('select.type edge')
            selected_mesh.geometry.edges.select(ComponentList)
        if self.sel_mode == 3:
            scene.select(SelItem)
            lx.eval('select.type polygon')
            selected_mesh.geometry.polygons.select(ComponentList)
        if self.sel_mode == 5:
            scene.select(SelItem)


        del index
        del TargetIDList
        del ComponentList
        del ComponentTuple


lx.bless(SMO_GC_Setup_Multi_MoveRotateCenterToSelection_Cmd, Cmd_Name)

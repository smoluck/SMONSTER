# python
# ---------------------------------------
# Name:         SMO_UV_Multi_SmartOrient_Cmd.py
# Version:      1.0
#
# Purpose:      This script is designed to
#               Orient the current UV island based
#               on Poly or Edge Selection
#
# Author:       Franck ELISABETH
# Website:      http://www.smoluck.com
#
# Created:      28/12/2018
# Copyright:    (c) Franck Elisabeth 2017-2022
# ---------------------------------------

import lx, lxu, modo

Cmd_Name = "smo.UV.Multi.SmartOrient"


# smo.UV.Multi.SmartOrient 0

class SMO_UV_Multi_SmartOrient_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
        self.dyna_Add("Orient Direction", lx.symbol.sTYPE_INTEGER)
        self.basic_SetFlags(0, lx.symbol.fCMDARG_OPTIONAL)

        self.SelModeVert = bool(lx.eval1("select.typeFrom typelist:vertex;polygon;edge;item;ptag ?"))
        self.SelModeEdge = bool(lx.eval1("select.typeFrom typelist:edge;vertex;polygon;item ?"))
        self.SelModePoly = bool(lx.eval1("select.typeFrom typelist:polygon;vertex;edge;item ?"))
        self.SelModeItem = bool(lx.eval1("select.typeFrom typelist:item;pivot;center;edge;polygon;vertex;ptag ?"))
        # print(self.SelModeVert)
        # print(self.SelModeEdge)
        # print(self.SelModePoly)
        # print(self.SelModeItem)
        self.ComponentMode = int()
        if self.SelModePoly:
            self.ComponentMode = 3
        if self.SelModeEdge:
            self.ComponentMode = 2

    def cmd_Flags(self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO

    def cmd_Interact(self):
        pass

    def cmd_UserName(self):
        return 'SMO UV - (Multi) Smart Orient'

    def cmd_Desc(self):
        return 'MULTI - Orient the current UV Island (Horizontally or Vertically) based on Poly or Edge Selection.'

    def cmd_Tooltip(self):
        return 'MULTI - Orient the current UV Island (Horizontally or Vertically) based on Poly or Edge Selection.'

    def cmd_Help(self):
        return 'https://twitter.com/sm0luck'

    def basic_ButtonName(self):
        return 'SMO UV - (Multi) Smart Orient'

    def basic_Enable(self, msg):
        return True

    def basic_Execute(self, msg, flags):
        SO_OrientDir = self.dyna_Int(0)
        lx.eval('smo.UV.SmartOrient %s' % SO_OrientDir)
        # CM = self.ComponentMode
        # scene = modo.scene.current()
        #
        # SO_SelItem = lxu.select.ItemSelection().current()
        # # print('lxu.object.Item : ', SO_SelItem)
        #
        # mesh = scene.selectedByType('mesh')
        # # print('modo.Mesh :', mesh)
        # # print('modo.Mesh list length:', len(mesh))
        #
        # SO_TargetIDList = []
        # for item in mesh:
        #     itemType = modo.Item(item).type
        #     item = lx.object.Item(item)
        #     # print(item)
        #     if itemType == "mesh":
        #         ID = item.Ident()
        #         # print(ID)
        #         SO_TargetIDList.append(ID)
        # # print(SO_TargetIDList)
        #
        # SO_ComponentsTuple = []
        # if CM == 2:
        #     for item in mesh:
        #         # CsEdges = len(item.geometry.edges.selected)
        #         # print('Total selected Edges on this mesh layer', CsEdges)
        #         Edges = item.geometry.edges.selected
        #         # print('modo.Mesh list ', Edges)
        #         SO_ComponentsTuple.append(Edges)
        #     # print('Tuple (Edge ID and Mesh ID): ---)', SO_ComponentsTuple)
        #     SO_ComponentsList = list(SO_ComponentsTuple)
        #     # print('List (Edge ID and Mesh ID): ---)', SO_ComponentsList)
        #
        # if CM == 3:
        #     for item in mesh:
        #         # CsPolys = len(item.geometry.polygons.selected)
        #         # print('Total selected Polygons on this mesh layer', CsPolys)
        #         Polys = item.geometry.polygons.selected
        #         # print('modo.Mesh list ', Polys)
        #         SO_ComponentsTuple.append(Polys)
        #     # print('Tuple (Poly ID and Mesh ID): ---)', SO_ComponentsTuple)
        #     SO_ComponentsList = list(SO_ComponentsTuple)
        #     # print('List (Poly ID and Mesh ID): ---)', SO_ComponentsList)
        #
        # lx.eval('select.drop polygon')
        # lx.eval('smo.GC.DeselectAll')
        # lx.eval('select.type item')
        # lx.eval('smo.GC.DeselectAll')
        #
        # SO_index = -1
        # for m in SO_TargetIDList:
        #     SO_index = (SO_index + 1)
        #     # print('id :', SO_index)
        #     scene.select(m)
        #     selected_mesh = scene.selectedByType('mesh')[0]
        #     # print('current mesh indentity :', SO_index, selected_mesh)
        #
        #     if CM == 2:
        #         lx.eval('select.type edge')
        #         lx.eval('select.drop edge')
        #     if CM == 3:
        #         lx.eval('select.type polygon')
        #         lx.eval('select.drop polygon')
        #
        #     for item in (SO_ComponentsList[SO_index]):
        #         # print(item)
        #         if CM == 2:
        #             lx.eval('select.type edge')
        #             selected_mesh.geometry.edges.select(item)
        #         if CM == 3:
        #             lx.eval('select.type polygon')
        #             selected_mesh.geometry.polygons.select(item)
        #     ############### PUT YOUR Command HERE to run over each item Polygons
        #     if CM == 2:
        #         CsEdges = len(selected_mesh.geometry.edges.selected)
        #         if CsEdges > 0:
        #             try:
        #                 lx.eval('smo.UV.SmartOrient %s' % SO_OrientDir)
        #             except:
        #                 lx.out('Error on {%s}' % (lx.eval('item.name ? xfrmcore')))
        #
        #     if CM == 3:
        #         CsPolys = len(selected_mesh.geometry.polygons.selected)
        #         if CsPolys > 0:
        #             try:
        #                 lx.eval('smo.UV.SmartOrient %s' % SO_OrientDir)
        #             except:
        #                 lx.out('Error on {%s}' % (lx.eval('item.name ? xfrmcore')))
        #
        #     if CM == 2:
        #         # selected_mesh.geometry.edges.select(item, replace=True)
        #         lx.eval('select.type edge')
        #         lx.eval('select.drop edge')
        #     if CM == 3:
        #         # selected_mesh.geometry.polygons.select(item, replace=True)
        #         lx.eval('select.type polygon')
        #         lx.eval('select.drop polygon')
        #
        #     lx.eval('select.type item')
        #     lx.eval('select.drop item')
        #     # GOOOOOOOOOOOOD
        # SO_index = -1
        # lx.eval('smo.GC.DeselectAll')
        # scene.select(mesh)
        #
        # #####################################################
        # # MODO version checks.
        # # Modo 13.0 and up have UV Seam map.
        # # Version below 13.0 haven't
        # Modo_ver = int(lx.eval('query platformservice appversion ?'))
        # lx.out('Modo Version:', Modo_ver)
        # #####################################################
        #
        # # select back the Polygons
        # lx.eval('smo.GC.DeselectAll')
        # scene.select(mesh)
        # if CM == 2:
        #     lx.eval('select.type edge')
        #     for m in SO_TargetIDList:
        #         SO_index = (SO_index + 1)
        #         for item in (SO_ComponentsList[SO_index]):
        #             selected_mesh.geometry.edges.select(item)
        # if CM == 3:
        #     lx.eval('select.type polygon')
        #     for m in SO_TargetIDList:
        #         SO_index = (SO_index + 1)
        #         for item in (SO_ComponentsList[SO_index]):
        #             selected_mesh.geometry.polygons.select(item)
        #
        # del SO_index
        # del SO_TargetIDList
        # del SO_ComponentsList
        # del SO_ComponentsTuple


lx.bless(SMO_UV_Multi_SmartOrient_Cmd, Cmd_Name)

# python
# ---------------------------------------
# Name:         SMO_QT_Automatic_SetSelSetColorID_ByMeshIslands_Cmd.py
# Version:      1.00
#
# Purpose:      This script is designed to
#               Set a Diffuse Color override using Selection Set (polygons) on the selected Mesh Layers by Polygons Continuity (Islands).
#               Named the new Mat using "ColorID" as Prefix.
#
#
# Author:       Franck ELISABETH
# Website:      http://www.smoluck.com
#
# Created:      12/04/2022
# Copyright:    (c) Franck Elisabeth 2017-2022
# ---------------------------------------

import modo, lx, lxu, random

Command_Name = "smo.QT.SetSelSetColorIDByMeshIslands"
# smo.QT.SetSelSetColorIDByMeshIslands

def scene():
    return modo.scene.current()

def first_item_selected():
    return scene().selected[0]

def item_name():
    return  modo.Item(first_item_selected()).name

def item_type():
    return  modo.Item(first_item_selected()).type

def item_id():
    return  modo.Item(first_item_selected()).id

def item_is_a_mesh():
    return True if item_type() == 'mesh' else False

def mesh_layer_poly_count():
    return modo.MeshGeometry(item_id()).numPolygons

def mesh_layer_visible_poly():
    return lx.eval('query layerservice poly.N ? visible') #visible poly count

#def mesh_layer_edge_count():
#    return modo.MeshGeometry(item_id()).numEdges
#
#def mesh_layer_vert_count():
#    return modo.MeshGeometry(item_id()).numVertices

def mesh_layer_poly_list():
    return modo.Mesh(item_id()).geometry.polygons


class SMO_QT_Automatic_SetSelSetColorID_ByMeshIslands_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)

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
        return 'SMO QT - Set ColorID ByUser (by SelSet and Constant) - By Mesh Islands'

    def cmd_Desc(self):
        return 'Set a Diffuse Color override using Selection Set (polygons) on the selected Mesh Layers by Polygons Continuity (Islands). Named the new Mat using "ColorID" as Prefix.'

    def cmd_Tooltip(self):
        return 'Set a Diffuse Color override using Selection Set (polygons) on the selected Mesh Layers by Polygons Continuity (Islands). Named the new Mat using "ColorID" as Prefix.'

    def cmd_Help(self):
        return 'https://twitter.com/sm0luck'

    def basic_ButtonName(self):
        return 'SMO QT - Set ColorID ByUser (by SelSet and Constant) - By Mesh Islands'

    def cmd_Flags(self):
        return lx.symbol.fCMD_UNDO

    def basic_Enable(self, msg):
        return True

    def basic_Execute(self, msg, flags):
        if self.SelModeItem == True or self.SelModeVert == True or self.SelModeEdge == True:
            lx.eval('select.type polygon')

        if self.SelModePoly == True:
            lx.eval('smo.MASTER.ForceSelectMeshItemOnly')

        lx.eval('select.type item')
        lx.eval('hide.unsel')
        lx.eval('select.type polygon')

        # Create a list of all Polygons in the current Mesh Layer
        if item_is_a_mesh():
            if mesh_layer_poly_count() > 0:
               # for p in mesh_layer_poly_list():
               #     print p.index
               #     #PolyPack.append(p.index)
                PolyPack = list(first_item_selected().geometry.polygons)
        # print(PolyPack)

        # Selecting the first Polygon in the list, extend to connected, then try to Remove those polygons from the original list of Polygons "PolyPack".
        if item_is_a_mesh():
            while mesh_layer_visible_poly() > 0:
                #for p in PolyPack[0]:
                PolyPack[0].select()
                lx.eval('select.connect')
                sel_poly = list(first_item_selected().geometry.polygons.selected)
                BeforeRemove = len(PolyPack)
                print('Before list cleanup:', BeforeRemove)
                for item in sel_poly:
                    PolyPack.remove(item)
                del sel_poly [:]
                AfterRemove = len(PolyPack)
                print('After list cleanup:', AfterRemove)
                lx.eval('smo.QT.SetSelSetColorIDRandomConstant')
                lx.eval('hide.sel')
        lx.eval('unhide')

        lx.eval('select.type item')
        lx.eval('unhide')

        if self.SelModeItem == True:
            lx.eval('select.type item')
        if self.SelModeVert == True:
            lx.eval('select.type vertex')
        if self.SelModeEdge == True:
            lx.eval('select.type edge')

lx.bless(SMO_QT_Automatic_SetSelSetColorID_ByMeshIslands_Cmd, Command_Name)
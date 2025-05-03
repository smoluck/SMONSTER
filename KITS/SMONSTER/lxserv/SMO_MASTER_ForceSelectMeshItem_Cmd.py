# python
"""
Name:         SMO_MASTER_ForceSelectMeshItem_Cmd.py

Purpose:      This script is designed to:
              Select the Mesh Item related to current Selected Component when it's the Foreground Mesh.
              Filter only the Mesh Item to be selected at the end.

Author:       Franck ELISABETH
Website:      https://www.linkedin.com/in/smoluck/
Created:      25/04/2021
Copyright:    (c) Franck Elisabeth 2017-2022
"""

import lx
import lxu
import modo

Cmd_Name = "smo.MASTER.ForceSelectMeshItemOnly"


# smo.MASTER.ForceSelectMeshItemOnly


class SMO_MASTER_ForceSelectMeshItem_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
        self.SelModeVert = bool(lx.eval1("select.typeFrom typelist:vertex;polygon;edge;item;ptag ?"))
        self.SelModeEdge = bool(lx.eval1("select.typeFrom typelist:edge;vertex;polygon;item ?"))
        self.SelModePoly = bool(lx.eval1("select.typeFrom typelist:polygon;vertex;edge;item ?"))
        self.SelModeItem = bool(lx.eval1("select.typeFrom typelist:item;pivot;center;edge;polygon;vertex;ptag ?"))
        self.ComponentSelMode = bool()
        if self.SelModeVert is True or self.SelModeEdge is True or self.SelModePoly is True:
            self.ComponentSelMode = True
        else:
            self.ComponentSelMode = False

    def cmd_Flags(self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO

    def cmd_Interact(self):
        pass

    def cmd_UserName(self):
        return 'SMO MASTER - Force Select Foreground Mesh Item Only'

    def cmd_Desc(self):
        return 'Select the Mesh Item related to current Selected Component when it is the Foreground Mesh. Filter only the Mesh Item to be selected at the end.'

    def cmd_Tooltip(self):
        return 'Select the Mesh Item related to current Selected Component when it is the Foreground Mesh. Filter only the Mesh Item to be selected at the end.'

    def cmd_Help(self):
        return 'https://twitter.com/sm0luck'

    def basic_ButtonName(self):
        return 'SMO MASTER - Force Select Foreground Mesh Item Only'

    def basic_Enable(self, msg):
        return True

    def basic_Execute(self, msg, flags):
        scene = modo.scene.current()

        # -------------- Index Style START Procedure  -------------- #
        # Bugfix for items that cant be detected when "Index Style" is not using underscore as separator.
        # Problem caused by item.UniqueName() at line 144
        IndexStyle = lx.eval("pref.value application.indexStyle ?")
        if IndexStyle != "uscore":
            lx.eval("pref.value application.indexStyle uscore")
        # -------------------------------------------- #

        if not self.ComponentSelMode:
            index = lx.eval('query layerservice layers ? fg')
            activeItem = lx.eval('query layerservice layer.name ? %s' % index)
            # print(activeItem)
            scene.select(activeItem)

        if self.ComponentSelMode:
            SelModeVert = bool(lx.eval1("select.typeFrom typelist:vertex;polygon;edge;item;ptag ?"))
            SelModeEdge = bool(lx.eval1("select.typeFrom typelist:edge;vertex;polygon;item ?"))
            SelModePoly = bool(lx.eval1("select.typeFrom typelist:polygon;vertex;edge;item ?"))
            SelModeItem = bool(lx.eval1("select.typeFrom typelist:item;pivot;center;edge;polygon;vertex;ptag ?"))
            # print(SelModeVert)
            # print(SelModeEdge)
            # print(SelModePoly)
            # print(SelModeItem)

            TargetMesh = []
            s = set()
            sel_svc = lx.service.Selection()
            # print(sel_svc)

            if SelModePoly:
                polygon_translation_packet = lx.object.PolygonPacketTranslation(
                    sel_svc.Allocate(lx.symbol.sSELTYP_POLYGON)  # basically passing it the string 'polygon'
                )
                for index in range(sel_svc.Count(lx.symbol.iSEL_POLYGON)):
                    pointer = sel_svc.ByIndex(lx.symbol.iSEL_POLYGON, index)
                    item = lx.object.Item(polygon_translation_packet.Item(pointer))
                    mesh = lx.object.Mesh(polygon_translation_packet.Mesh(pointer))
                    # polygon_id = polygon_translation_packet.Polygon(pointer)      # Not necessary
                    s.add(item.Ident())
                    TargetMesh.append(item.Ident())
                # scene.select(TargetMesh[0])

            if SelModeEdge:
                edge_translation_packet = lx.object.EdgePacketTranslation(
                    sel_svc.Allocate(lx.symbol.sSELTYP_EDGE)  # basically passing it the string 'polygon'
                )
                for index in range(sel_svc.Count(lx.symbol.iSEL_EDGE)):
                    pointer = sel_svc.ByIndex(lx.symbol.iSEL_EDGE, index)
                    item = lx.object.Item(edge_translation_packet.Item(pointer))
                    s.add(item.Ident())
                    TargetMesh.append(item.Ident())
                # GetItemsFromEdges()
                # TargetMesh.append(GetItemsFromEdges())

            if SelModeVert:
                vertex_translation_packet = lx.object.VertexPacketTranslation(
                    sel_svc.Allocate(lx.symbol.sSELTYP_VERTEX)  # basically passing it the string 'polygon'
                )
                for index in range(sel_svc.Count(lx.symbol.iSEL_VERTEX)):
                    pointer = sel_svc.ByIndex(lx.symbol.iSEL_VERTEX, index)
                    item = lx.object.Item(vertex_translation_packet.Item(pointer))
                    mesh = lx.object.Mesh(vertex_translation_packet.Mesh(pointer))
                    # vertex_id = vertex_translation_packet.Vertex(pointer)         # Not necessary
                    s.add(item.Ident())
                    TargetMesh.append(item.Ident())
                # scene.select(TargetMesh[0])

            ListCount = len(TargetMesh)

            for i in range(0, ListCount):
                lx.eval('select.item {%s} add' % (TargetMesh[i]))

            # Filter current selected Items to select Only Mesh Items
            selected_Items = lxu.select.ItemSelection().current()
            for item in selected_Items:
                itemType = modo.Item(item).type
                item = lx.object.Item(item)
                item_name = item.UniqueName()
                if itemType != "mesh":
                    scene.deselect(item_name)

            if SelModePoly:
                lx.eval('select.type polygon')
            if SelModeEdge:
                lx.eval('select.type edge')
            if SelModeVert:
                lx.eval('select.type vertex')

        # -------------- Index Style END Procedure  -------------- #
        if IndexStyle != "uscore":
            lx.eval("pref.value application.indexStyle %s" % IndexStyle)
        # -------------------------------------------- #

            del TargetMesh


lx.bless(SMO_MASTER_ForceSelectMeshItem_Cmd, Cmd_Name)

##########
## Snippet from robberyman on Slack
# def GetItemsFromEdges():
# 	items = set()
# 	sel_svc = lx.service.Selection()
# 	edge_translation_packet = lx.object.EdgePacketTranslation(
# 		sel_svc.Allocate(lx.symbol.sSELTYP_EDGE) # basically passing it the string 'polygon'
# 		)
# 	for index in range(sel_svc.Count(lx.symbol.iSEL_EDGE)):
# 		pointer = sel_svc.ByIndex(lx.symbol.iSEL_EDGE, index)
# 		items.add(lx.object.Item(edge_translation_packet.Item(pointer)).Ident())
# 	return items
##########

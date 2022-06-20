# python
# ---------------------------------------
# Name:         SMO_GC_ModollamaRebuildNGontoTriangle_Cmd.py
# Version:      1.0
#
# Purpose:      This Command is designed to
#               Rebuild all NGons via Modollama Triangulation command to output Triangles
#
# Author:       Franck ELISABETH
# Website:      http://www.smoluck.com
#
# Created:      16/06/2022
# Copyright:    (c) Franck Elisabeth 2017-2022
# ---------------------------------------

import lx, lxu, modo

Command_Name = "smo.GC.ModollamaRebuildNGontoTriangle"
# smo.GC.ModollamaRebuildNGontoTriangle 1
# Modo Method = False
# Modollama Method = True

class SMO_GC_ModollamaRebuildNGontoTriangle_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
        self.dyna_Add("Triangulate Method: Modo or Modollama", lx.symbol.sTYPE_BOOLEAN)
        self.basic_SetFlags(0, lx.symbol.fCMDARG_OPTIONAL)  # here the (0) define the argument index.

        scenedata = modo.scene.current()
        CheckGrpSelItems = lxu.select.ItemSelection().current()
        for item in CheckGrpSelItems:
            itemType = modo.Item(item).type
            item = lx.object.Item(item)
            item_name = item.UniqueName()
            # print(item_name)
            if itemType != "mesh":
                scenedata.deselect(item_name)

    def cmd_Flags(self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO

    def cmd_Interact(self):
        pass

    def cmd_UserName(self):
        return 'SMO GC ModollamaRebuildNGontoTriangle'

    def cmd_Desc(self):
        return 'Rebuild all NGons via Modollama Triangulation command to output Triangles.'

    def cmd_Tooltip(self):
        return 'Rebuild all NGons via Modollama Triangulation command to output Triangles.'

    def cmd_Help(self):
        return 'https://twitter.com/sm0luck'

    def basic_ButtonName(self):
        return 'SMO GC ModollamaRebuildNGontoTriangle'

    def basic_Enable(self, msg):
        return True

    def basic_Execute(self, msg, flags):
        TriMethod = self.dyna_Bool(0)
        # Modo = False
        # Modollama = True

        def scene_info():
            return modo.scene.current()

        def first_item_selected():
            return scene_info().selected[0]

        def item_name():
            return modo.Item(first_item_selected()).name

        def item_type():
            return modo.Item(first_item_selected()).type

        def item_id():
            return modo.Item(first_item_selected()).id

        def item_is_a_mesh():
            return True if item_type() == 'mesh' else False

        def mesh_layer_poly_count():
            return modo.MeshGeometry(item_id()).numPolygons

        def mesh_layer_visible_poly():
            return lx.eval('query layerservice poly.N ? visible')  # visible poly count

        def mesh_layer_poly_list():
            return modo.Mesh(item_id()).geometry.polygons

        def setpref_modollama():
            lx.eval('user.value llama_keepuvbounds false')
            lx.eval('user.value llama_keepmatbounds false')
            lx.eval('user.value llama_anglethreshold 0.005')
            # lx.eval('user.value llama_iterations 8')

        def action_ngontotri():
            TriMethod = self.dyna_Bool(0)
            if item_is_a_mesh():
                scene = modo.scene.current()
                mesh = modo.Mesh()
                Mesh_A = scene.selectedByType('mesh')[0]

                # Create the monitor item
                mon = lx.Monitor()
                # mon.init(len(mesh_layer_visible_poly))
                mon.init(100)

                PolyPack = []
                # Create a list of all Polygons in the current Mesh Layer
                lx.eval('select.polygon add vertex b-spline 4')
                NgonPolySel = len(Mesh_A.geometry.polygons.selected)
                TotalNgonItem = NgonPolySel
                # print(NgonPolySel)
                if NgonPolySel > 0:
                    # for p in mesh_layer_poly_list():
                    #     print p.index
                    #     #PolyPack.append(p.index)
                    PolyPack = list(Mesh_A.geometry.polygons.selected)
                # print(PolyPack)
                lx.eval('select.drop polygon')
                lx.eval('select.type item')

                # Selecting the first Polygon in the list, extend to connected, then try to Remove those polygons from the original list of Polygons "PolyPack".
                while TotalNgonItem > 0:
                    # for p in PolyPack[0]:
                    lx.eval('select.type polygon')
                    PolyPack[0].select()
                    if TriMethod:
                        lx.eval('@SmartTriangulation.pl')
                    if not TriMethod:
                        lx.eval('poly.triple')

                    if len(Mesh_A.geometry.polygons.selected) > 0:
                        lx.eval('hide.sel')

                    # HardEdge at all Geometry Boundary
                    CountPolys = len(Mesh_A.geometry.polygons.selected)
                    if CountPolys > 0:
                        # lx.eval('select.editSet Processed_Mllama add')
                        lx.eval('hide.sel')
                        # lx.eval('!select.deleteSet SimplifyData')

                    # Update the amount of polygons on mesh
                    lx.eval('select.polygon add vertex b-spline 4')
                    del PolyPack[:]
                    PolyPack = list(Mesh_A.geometry.polygons.selected)
                    TotalNgonItem = len(PolyPack)
                    # print(PolyPack)
                    lx.eval('select.drop polygon')

                    # mon.step(1)
                    mon.step()

                lx.eval('unhide')
                lx.eval('select.type item')

        scene = modo.scene.current()
        items = modo.Scene().selected
        if TriMethod:
            setpref_modollama()
        for item in items:
            action_ngontotri()
            lx.eval('select.drop item')


lx.bless(SMO_GC_ModollamaRebuildNGontoTriangle_Cmd, Command_Name)

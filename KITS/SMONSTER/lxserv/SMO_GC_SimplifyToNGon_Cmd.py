# python
# ---------------------------------------
# Name:         SMO_GC_SimplifyToNGon_Cmd.py
# Version:      1.0
#
# Purpose:      This Command is designed to
#               Merge every polygons that have same coplanar polygon direction to simplify a given set of meshes.
#               Via argument you can also update the HardEdges data for a better end result.
#
# Author:       Franck ELISABETH
# Website:      http://www.smoluck.com
#
# Created:      15/06/2022
# Copyright:    (c) Franck Elisabeth 2017-2022
# ---------------------------------------

import lx, lxu, modo

Command_Name = "smo.GC.SimplifyToNGon"
# smo.GC.SimplifyToNGon 1

class SMO_GC_SimplifyToNGon_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
        self.dyna_Add("Set HardEdge", lx.symbol.sTYPE_BOOLEAN)
        self.basic_SetFlags(0, lx.symbol.fCMDARG_OPTIONAL)             # here the (0) define the argument index.

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
        return 'SMO GC SimplifyToNGon'
        
    def cmd_Desc(self):
        return 'Merge every polygons that have same coplanar polygon direction to simplify a given set of meshes. Via argument you can also update the HardEdges data for a better end result.'
        
    def cmd_Tooltip(self):
        return 'Merge every polygons that have same coplanar polygon direction to simplify a given set of meshes. Via argument you can also update the HardEdges data for a better end result.'
        
    def cmd_Help(self):
        return 'https://twitter.com/sm0luck'
        
    def basic_ButtonName(self):
        return 'SMO GC SimplifyToNGon'
        
    def basic_Enable(self, msg):
        return True
        
    def basic_Execute(self, msg, flags):
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
            return lx.eval('query layerservice poly.N ? visible')       # visible poly count
            
        def mesh_layer_poly_list():
            return modo.Mesh(item_id()).geometry.polygons
            
        def prepare_hardsoft():
            scene_ph = modo.scene.current()
            Mesh_Cible = scene_ph.selectedByType('mesh')[0]

            SetHardEdge = self.dyna_Bool (0)
            if SetHardEdge:
                lx.eval('hardedge.select hard')
                lx.eval('hardedge.set hard clear:true')
                lx.eval('hardedge.select soft')
                CountSoftEdges = len(Mesh_Cible.geometry.edges.selected)
                if CountSoftEdges > 0:
                    lx.eval('select.editSet Softtttt add')
                lx.eval('select.drop edge')
                lx.eval('select.type item')

        def simplifytongon():
            scene_sngon = modo.scene.current()
            Mesh_DataRaw = scene_sngon.selectedByType('mesh')[0]

            SetHardEdge = self.dyna_Bool (0)

            # print "YOU GOT ME!! I'M A MESH ITEM !!" if item_is_a_mesh() else "PLEASE TRY AGAIN!!"


            # Create the monitor item
            mon = lx.Monitor()
            # mon.init(len(mesh_layer_visible_poly))
            mon.init(100)

            PolyPack = []
            # Create a list of all Polygons in the current Mesh Layer
            if item_is_a_mesh():
                if mesh_layer_poly_count() > 0:
                    # for p in mesh_layer_poly_list():
                    #     print p.index
                    #     #PolyPack.append(p.index)
                    PolyPack = list(Mesh_DataRaw.geometry.polygons)
            # print(PolyPack)


            # Selecting the first Polygon in the list, extend to connected, then try to Remove those polygons from the original list of Polygons "PolyPack".
            if item_is_a_mesh():
                # print(mesh_layer_visible_poly())
                while mesh_layer_visible_poly() > 0:
                    # for p in PolyPack[0]:
                    lx.eval('select.type polygon')
                    PolyPack[0].select()
                    lx.eval('smo.GC.SelectCoPlanarPoly 2 1')

                    processed_poly = list(Mesh_DataRaw.geometry.polygons.selected)
                    # print(processed_poly)
                    # for item in processed_poly:
                    #     PolyPack.remove(item)

                    if len(Mesh_DataRaw.geometry.polygons.selected) > 1:
                        lx.eval('!poly.merge')

                    if SetHardEdge :
                        #HardEdge at all Geometry Boundary
                        CountSoftPolys = len(Mesh_DataRaw.geometry.polygons.selected)
                        if CountSoftPolys > 0:
                            lx.eval('select.editSet SimplifyData add')
                            lx.eval('script.run "macro.scriptservice:92663570022:macro"')
                            CountSoftEdges = len(Mesh_DataRaw.geometry.edges.selected)
                            if CountSoftEdges > 0:
                                lx.eval('hardedge.set hard')
                            lx.eval('select.drop edge')
                            try:
                                lx.eval('select.useSet Softtttt select')
                                if CountSoftEdges > 0:
                                    lx.eval('hardedge.set soft')
                            except:
                                pass
                            lx.eval('select.drop edge')
                            lx.eval('select.type polygon')
                            #lx.eval('!select.deleteSet SimplifyData')

                    # merged_poly = list(first_item_selected().geometry.polygons.selected)
                    # print(merged_poly)
                    lx.eval('smo.CAD.CopyCutAsChildOfCurrentMesh true true')
                    del PolyPack [:]

                    # Update the amount of polygons on mesh
                    if mesh_layer_poly_count() > 0:
                        # for p in mesh_layer_poly_list():
                        #     print p.index
                        # #PolyPack.append(p.index)
                        PolyPack = list(Mesh_DataRaw.geometry.polygons)
                    # print(PolyPack)

                    AfterProcessing = len(PolyPack)
                    # print('After Processing a set of Polygons, poly count left over:', AfterProcessing)
                    # for item in merged_poly:
                    #     PolyPack.remove(item)
                    del processed_poly [:]
                    # del merged_poly [:]

                    # mon.step(1)
                    mon.step()


            lx.eval('select.type item')

            lx.eval('select.itemHierarchy')
            scene_sngon.deselect(Mesh_DataRaw)
            lx.eval('select.type polygon')
            lx.eval('select.all')
            lx.eval('cut')
            scene_sngon.select(Mesh_DataRaw)
            lx.eval('paste')
            lx.eval('script.run "macro.scriptservice:92663570022:macro"')
            lx.eval('select.convert vertex')
            lx.eval('!vert.merge fixed false 0.00001 false false')
            lx.eval('select.itemHierarchy')
            scene_sngon.deselect(Mesh_DataRaw)
            lx.eval('!delete')
            scene_sngon.select(Mesh_DataRaw)

            if SetHardEdge:
                # HardEdge at all Geometry Boundary
                lx.eval('select.type edge')
                lx.eval('select.drop edge')
                lx.eval('select.type item')
            # lx.eval('select.drop item')

        def update_hardsoft():
            scene_uh = modo.scene.current()
            Mesh_Update = scene_uh.selectedByType('mesh')[0]

            lx.eval('select.type edge')
            lx.eval('select.useSet Softtttt select')
            CountSoftEdges = len(Mesh_Update.geometry.edges.selected)
            if CountSoftEdges > 0:
                lx.eval('hardedge.set soft clear:true')
            try:
                lx.eval('!select.deleteSet Softtttt')
            except:
                pass
            lx.eval('select.drop edge')
            lx.eval('select.type item')


        scene_exec = modo.scene.current()
        mesh = modo.Mesh()
        RefreshHardEdge = self.dyna_Bool(0)

        if RefreshHardEdge:
            prepare_hardsoft()

        Mesh_Source = scene_exec.selectedByType('mesh')[0]

        lx.eval('select.type polygon')
        lx.eval('select.all')
        CountPolygons = len(Mesh_Source.geometry.polygons.selected)
        if CountPolygons > 0:
            lx.eval('cut')
        lx.eval('smo.GC.CreateEmptyChildMeshMatchTransform true')
        lx.eval('select.type polygon')
        lx.eval('paste')
        lx.eval('select.drop polygon')
        lx.eval('select.type item')
        Mesh_Data = scene_exec.selectedByType('mesh')[0]

        simplifytongon()

        if RefreshHardEdge:
            update_hardsoft()

        lx.eval('select.drop item')
        scene_exec.select(Mesh_Data)
        lx.eval('select.type polygon')
        lx.eval('select.all')
        lx.eval('cut')
        lx.eval('select.type item')
        scene_exec.select(Mesh_Source)
        lx.eval('paste')
        lx.eval('select.drop polygon')

        lx.eval('select.type item')
        scene_exec.select(Mesh_Data)
        lx.eval('!delete')
        scene_exec.select(Mesh_Source)


lx.bless(SMO_GC_SimplifyToNGon_Cmd, Command_Name)

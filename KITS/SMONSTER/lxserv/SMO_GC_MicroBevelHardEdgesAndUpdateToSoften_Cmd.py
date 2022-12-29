# python
"""
Name:         SMO_GC_MicroBevelHardEdgesAndUpdateToSoften_Cmd.py

Purpose:      This Command is designed to
              Micro Bevel HardEdges (usually after a SimplyToNgon), then Soften all edges.

Author:       Franck ELISABETH
Website:      https://www.smoluck.com
Created:      16/06/2022
Copyright:    (c) Franck Elisabeth 2017-2022
"""

import lx
import lxu
import modo

Cmd_Name = "smo.GC.MicroBevelHardEdgesAndUpdateToSoften"
# smo.GC.MicroBevelHardEdgesAndUpdateToSoften [1mm]
# Using Square Brackets around values validate the use of units like "km", "m" , "cm", "mm", "um".


class SMO_GC_MicroBevelHardEdgesAndUpdateToSoften_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
        self.dyna_Add("Witdh Value", lx.symbol.sTYPE_DISTANCE)

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
        return 'SMO GC - MicroBevel HardEdges and Soften all Edges'

    def cmd_Desc(self):
        return 'Micro Bevel HardEdges (usually after a SimplyToNgon), then Soften all edges.'

    def cmd_Tooltip(self):
        return 'Micro Bevel HardEdges (usually after a SimplyToNgon), then Soften all edges.'

    def cmd_Help(self):
        return 'https://twitter.com/sm0luck'

    def basic_ButtonName(self):
        return 'SMO GC - MicroBevel HardEdges and Soften all Edges'

    def basic_Enable(self, msg):
        return True

    def basic_Execute(self, msg, flags):
        # ------------------------------ #
        # <----( DEFINE ARGUMENTS )----> #
        # ------------------------------ #
        ChamferValue = self.dyna_Float(0)              # Width size
        # ------------------------------ #
        # <----( DEFINE ARGUMENTS )----> #
        # ------------------------------ #

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

        def base_action():
            scene = modo.scene.current()
            mesh = modo.Mesh()
            Mesh_Cible = scene.selectedByType('mesh')[0]

            lx.eval('hardedge.select hard')
            CountSoftEdges = len(Mesh_Cible.geometry.edges.selected)
            if CountSoftEdges > 0:
                lx.eval('smo.GC.ChamferEdgesByUnit {%s}' % ChamferValue)
            lx.eval('hardedge.set soft')
            lx.eval('select.type item')

        scene = modo.scene.current()
        items = modo.Scene().selected
        for item in items:
            base_action()
            lx.eval('select.drop item')


lx.bless(SMO_GC_MicroBevelHardEdgesAndUpdateToSoften_Cmd, Cmd_Name)

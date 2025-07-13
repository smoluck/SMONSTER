# python
"""
Name:         SMO_UV_UVIslandToPolyPartTags_Cmd.py

Purpose:      This script is designed to
              Create polygon part tags that are related to their UVIsland by connectivity.

Author:       Franck ELISABETH
Website:      https://www.linkedin.com/in/smoluck/
Created:      29/06/2025
Copyright:    (c) Franck Elisabeth 2017-2022
"""

import lx
import lxu
import modo

Cmd_Name = "smo.UV.UVIslandToPolyPartTags"

class SMO_UV_UVIslandToPolyPartTags_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)

    def cmd_Flags(self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO

    def cmd_Interact(self):
        pass

    def cmd_UserName(self):
        return 'SMO UV - UVIsland to Polygon Part Tags'

    def cmd_Desc(self):
        return 'Create polygon part tags that are related to their UVIsland by connectivity'

    def cmd_Tooltip(self):
        return 'Create polygon part tags that are related to their UVIsland by connectivity'

    def cmd_Help(self):
        return 'https://twitter.com/sm0luck'

    def basic_ButtonName(self):
        return 'SMO UV - UVIsland to Polygon Part Tags'

    def basic_Enable(self, msg):
        return True

    def get_uv_map_name(self):
        scene = modo.scene.current()
        vmaps=set(lx.evalN('query layerservice vmaps ? selected'))
        texture=set(lx.evalN('query layerservice vmaps ? texture'))
        seltexture=list(vmaps.intersection(texture))
        selection=list(scene.selectedByType('mesh'))
        UVMap_Selected=lx.evalN('query layerservice vmaps ? selected')
        UVMap_SelectedN=len(UVMap_Selected)
        for item in selection:
            if item.geometry.vmap.uvMaps:
                UVMapsTotalCount=len(item.geometry.vmap.uvMaps)
                for uvmap in item.geometry.vmap.uvMaps:
                    lx.out('UV Map Names:', uvmap)
                if UVMapsTotalCount == 1:
                    print('UV Map {%s}:' % uvmap.name)
            return uvmap.name
        return None

    def basic_Execute(self, msg, flags):
        scene = modo.scene.current()
        mesh = scene.selectedByType('mesh')[0]
        lx.eval('select.type item')
        mesh.select(True)
        lx.eval('select.drop polygon')
        total_polys = len(mesh.geometry.polygons)
        if total_polys > 0:
            lx.eval('poly.renameTag Default "" PART')
            processed_polys = set()
            part_index = 1

            # switch to UV View
            lx.eval('tool.viewType uv')

            while len(processed_polys) < total_polys:
                for poly in mesh.geometry.polygons:
                    if poly.index not in processed_polys:
                        poly.select()
                        lx.eval('select.connect')
                        break

                # lx.eval('select.polygon add island')
                selected_indices = lx.evalN('query layerservice polys ? selected')

                selected_polys = [mesh.geometry.polygons[int(i)] for i in selected_indices]

                part_name = 'UVIsland_Part_' + str(part_index) + '_' + mesh.name
                # print(part_name)
                for poly in selected_polys:
                    # poly.setTag(lx.symbol.sTAG_PART, part_name)
                    processed_polys.add(poly.index)

                lx.eval('poly.setPart %s' % part_name)

                lx.eval('select.drop polygon')
                part_index += 1

            lx.out(f'Assigned {part_index - 1} polygon part tags based on UV Island.')

            lx.eval('select.type item')

lx.bless(SMO_UV_UVIslandToPolyPartTags_Cmd, Cmd_Name)

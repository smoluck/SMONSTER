# python
"""
# Author:       James O'Hare
# Website:      http://www.farfarer.com/
# Copyright:    (c) James O'Hare
"""

#!/usr/bin/env python
import lx, lxifc, lxu.command

class ListMaps (lxifc.Visitor):
    def __init__ (self, meshmap):
        self.meshmap = meshmap
        self.mapIDs = []

    def vis_Evaluate (self):
        self.mapIDs.append (self.meshmap.ID ())

class AverageValues (lxifc.Visitor):
    def __init__ (self,  polygon, meshMapIDs, mode):
        self.polygon = polygon
        self.meshMapIDs = meshMapIDs
        self.mode = mode

        self.value = lx.object.storage ('f', 4)
        self.value.set ((0.0,0.0,0.0,1.0))

    def vis_Evaluate (self):
        vCount = self.polygon.VertexCount ()
        vIDs = []

        for x in range(vCount):
            vIDs.append (self.polygon.VertexByIndex(x))

        for meshMapID in self.meshMapIDs:
            rgba_avg = [0.0] * 4
            for vID in vIDs:
                self.polygon.MapEvaluate (meshMapID, vID, self.value)
                rgba_value = self.value.get ()
                for x in range(4):
                    rgba_avg[x] += rgba_value[x]

            for x in range(4):
                rgba_avg[x] /= vCount
            self.value.set (rgba_avg)

            for vID in vIDs:
                self.polygon.SetMapValue (vID, meshMapID, self.value)

class AverageRGBA_Cmd(lxu.command.BasicCommand):

    def __init__(self):
        lxu.command.BasicCommand.__init__(self)

    def cmd_UserName(self):
        return 'Average RGBA Values'

    def cmd_Desc(self):
        return 'Average RGBA values for selected polygons.'

    def cmd_Tooltip(self):
        return 'Average RGBA values for selected polygons.'

    def cmd_Help(self):
        return 'http://www.farfarer.com/'

    def basic_ButtonName(self):
        return 'Average RGBA Values'

    def cmd_Flags(self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO

    def basic_Enable(self, msg):
        return True

    def cmd_Interact(self):
        pass

    def basic_Execute(self, msg, flags):
            meshMapNames = []

            mesh_svc = lx.service.Mesh ()
            mode = mesh_svc.ModeCompose ('select', 'hide lock')

            sel_svc = lx.service.Selection ()
            sel_type_vmap = sel_svc.LookupType (lx.symbol.sSELTYP_VERTEXMAP)
            vmap_pkt_trans = lx.object.VMapPacketTranslation (sel_svc.Allocate (lx.symbol.sSELTYP_VERTEXMAP))
            sel_vmap_count = sel_svc.Count (sel_type_vmap)
            for vmap_idx in range(sel_vmap_count):
                pkt = sel_svc.ByIndex (sel_type_vmap, vmap_idx)
                vmap_type = vmap_pkt_trans.Type (pkt)
                if vmap_type == lx.symbol.i_VMAP_RGBA:
                    meshMapNames.append(vmap_pkt_trans.Name (pkt))

            allMaps = False
            if len(meshMapNames) == 0:
                allMaps = True

            layer_svc = lx.service.Layer ()
            layer_scan = lx.object.LayerScan (layer_svc.ScanAllocate (lx.symbol.f_LAYERSCAN_EDIT))
            if not layer_scan.test ():
                return

            layer_scan_count = layer_scan.Count ()
            for l in range(layer_scan_count):

                mesh_item = layer_scan.MeshItem (l)

                mesh = lx.object.Mesh (layer_scan.MeshEdit (l))
                if not mesh.test ():
                    continue

                if mesh.PolygonCount () == 0:
                    continue

                polygon = lx.object.Polygon (mesh.PolygonAccessor ())
                meshmap = lx.object.MeshMap (mesh.MeshMapAccessor ())
                if not (point.test () and polygon.test () and meshmap.test()):
                    continue

                # RGBA MAPS
                meshMapIDs = []
                if not allMaps:
                    for meshMapName in meshMapNames:
                        try:
                            meshmap.SelectByName (lx.symbol.i_VMAP_RGBA, meshMapName)
                        except:
                            continue
                        else:
                            meshMapIDs.append (meshmap.ID ())
                else:
                    meshmap.FilterByType (lx.symbol.i_VMAP_RGBA)
                    mapVisitor = ListMaps (meshmap)
                    meshmap.Enumerate (lx.symbol.iMARK_ANY, mapVisitor, 0)
                    meshMapIDs = mapVisitor.mapIDs
                    meshmap.FilterByType (0)

                visitor = AverageValues (polygon, meshMapIDs, mode)
                polygon.Enumerate (mode, visitor, 0)

                layer_scan.SetMeshChange (l, lx.symbol.f_MESHEDIT_MAP_OTHER | lx.symbol.f_MESHEDIT_MAP_CONTINUITY)

            layer_scan.Apply ()

lx.bless (AverageRGBA_Cmd, 'ffr.averageRGBA')
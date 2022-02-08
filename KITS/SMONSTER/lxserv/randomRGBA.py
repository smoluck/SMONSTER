#---------------------------------------
# Author:       James O'Hare
# Website:      http://www.farfarer.com/
# Copyright:    (c) James O'Hare
#---------------------------------------

#!/usr/bin/env python

import lx, lxifc, lxu.command, random

class SetMarksVisitor (lxifc.Visitor):
    def __init__ (self, elem, marks):
        self.elem = elem
        self.marks = marks

    def vis_Evaluate (self):
        self.elem.SetMarks(self.marks)

class RandomValueVisitor (lxifc.Visitor):
    def __init__ (self, point, polygon, meshMapID, mode_valid, mode_checked):
        self.point = point
        self.polygon = polygon
        self.meshMapID = meshMapID
        self.mode_valid = mode_valid
        self.mode_checked = mode_checked

        self.value = lx.object.storage ('f', 4)
        self.value.set ((0.0,0.0,0.0,1.0))

    def vis_Evaluate (self):
        self.value.set((random.random(), random.random(), random.random(), 1.0))

        # Expand by mesh island.
        vlist = []
        vset = set()
        vID = self.point.ID()
        vset.add(vID)
        vlist.append(vID)

        while (len(vlist)):
            vID = vlist.pop()
            self.point.Select(vID)

            vCount = self.point.PointCount ()
            for x in range(vCount):
                vID2 = self.point.PointByIndex(x)
                if vID2 not in vset:
                    vset.add (vID2)
                    vlist.append (vID2)

        for vID in vset:
            self.point.Select(vID)

            if self.point.TestMarks(self.mode_valid):
                # Clear disco colours.
                for pID in (self.point.PolygonByIndex(x) for x in range(self.point.PolygonCount())):
                    self.polygon.Select(pID)
                    self.polygon.ClearMapValue (vID, self.meshMapID)

                # Set colour.
                self.point.SetMapValue(self.meshMapID, self.value)

            self.point.SetMarks(self.mode_checked)

class RandomRGBA_Cmd(lxu.command.BasicCommand):

    def __init__(self):
        lxu.command.BasicCommand.__init__(self)

    def cmd_UserName(self):
        return 'Random Vertex Colour'

    def cmd_Desc(self):
        return 'Set a random vertex colour for each mesh island.'

    def cmd_Tooltip(self):
        return 'Set a random vertex colour for each mesh island.'

    def cmd_Help(self):
        return 'http://www.farfarer.com/'

    def basic_ButtonName(self):
        return 'Random Vertex Colour'

    def cmd_Flags(self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO

    def basic_Enable(self, msg):
        return True

    def cmd_Interact(self):
        pass

    def basic_Execute(self, msg, flags):
            meshMapName = None

            mesh_svc = lx.service.Mesh ()
            mode_selected = mesh_svc.ModeCompose ('select', 'hide lock user0')
            mode_valid = mesh_svc.ModeCompose (None, 'lock user0')
            mode_checked = mesh_svc.ModeCompose ('user0', None)
            mode_clearChecked = mesh_svc.ModeCompose (None, 'user0')

            sel_svc = lx.service.Selection ()
            sel_type_vmap = sel_svc.LookupType (lx.symbol.sSELTYP_VERTEXMAP)
            vmap_pkt_trans = lx.object.VMapPacketTranslation (sel_svc.Allocate (lx.symbol.sSELTYP_VERTEXMAP))
            sel_vmap_count = sel_svc.Count (sel_type_vmap)
            for vmap_idx in range(sel_vmap_count):
                pkt = sel_svc.ByIndex (sel_type_vmap, vmap_idx)
                vmap_type = vmap_pkt_trans.Type (pkt)
                if vmap_type == lx.symbol.i_VMAP_RGBA:
                    meshMapName = vmap_pkt_trans.Name (pkt)
                    break

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

                if mesh.PointCount () == 0:
                    continue

                point = lx.object.Point (mesh.PointAccessor ())
                polygon = lx.object.Polygon (mesh.PolygonAccessor ())
                meshmap = lx.object.MeshMap (mesh.MeshMapAccessor ())
                if not (point.test() and polygon.test() and meshmap.test()):
                    continue

                changes = lx.symbol.f_MESHEDIT_MAP_OTHER | lx.symbol.f_MESHEDIT_MAP_CONTINUITY

                try:
                    meshmap.SelectByName (lx.symbol.i_VMAP_RGBA, meshMapName)
                except:
                    meshMapID = meshmap.New(lx.symbol.i_VMAP_RGBA, "Color")
                else:
                    meshMapID = meshmap.ID ()

                visitor_clear = SetMarksVisitor(point, mode_clearChecked)
                point.Enumerate (mode_checked, visitor_clear, 0)

                visitor = RandomValueVisitor (point, polygon, meshMapID, mode_valid, mode_checked)
                point.Enumerate (mode_selected, visitor, 0)

                layer_scan.SetMeshChange (l, changes)

            layer_scan.Apply ()

lx.bless (RandomRGBA_Cmd, 'ffr.randomRGBA')
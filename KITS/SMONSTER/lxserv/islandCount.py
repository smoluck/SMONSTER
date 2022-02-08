#---------------------------------------
# Author:       James O'Hare
# Website:      http://www.farfarer.com/
# Copyright:    (c) James O'Hare
#---------------------------------------

#!/usr/bin/env python

import lx, lxu.command, lxifc

class SetMarks (lxifc.Visitor):
    def __init__ (self, acc, mark):
        self.acc = acc
        self.mark = mark

    def vis_Evaluate (self):
        self.acc.SetMarks (self.mark)

class PolysByIsland (lxifc.Visitor):
    def __init__ (self, polygon, point, mark):
        self.polygon = polygon
        self.point = point
        self.mark = mark
        self.islands = 0

    def vis_Evaluate (self):
        inner = set ()
        outer = set ()

        outer.add (self.polygon.ID ())

        while len(outer) > 0:
            polygon_ID = outer.pop ()

            self.polygon.Select (polygon_ID)
            self.polygon.SetMarks (self.mark)
            inner.add (polygon_ID)

            num_points = self.polygon.VertexCount ()
            for v in range(num_points):
                self.point.Select (self.polygon.VertexByIndex (v))
                num_polys = self.point.PolygonCount ()
                for p in range(num_polys):
                    vert_polygon_ID = self.point.PolygonByIndex (p)
                    if vert_polygon_ID not in inner:
                        outer.add (vert_polygon_ID)

        self.islands += 1

class IslandCount_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__ (self)

        self.dyna_Add ('count', lx.symbol.sTYPE_INTEGER)
        self.basic_SetFlags (0, lx.symbol.fCMDARG_OPTIONAL | lx.symbol.fCMDARG_READONLY | lx.symbol.fCMDARG_HIDDEN)

        self.dyna_Add ('selected', lx.symbol.sTYPE_BOOLEAN)
        self.basic_SetFlags (1, lx.symbol.fCMDARG_OPTIONAL)

    def cmd_Flags(self):
        return lx.symbol.fCMD_UNDO

    def basic_Enable(self, msg):
        return True

    def cmd_UserName(self):
        return 'Polygon Island Count'

    def basic_ButtonName(self):
        return 'Polygon Island Count'

    def arg_UIHints (self, index, hints):
        if index == 0:
            hints.Label ('Island Count')
        if index == 1:
            hints.Label ('Selected Polygons Only')

    def get_IslandCount(self):
        selected_only = self.dyna_Bool (1, False)

        islands = 0
        layer_count = 0

        layer_svc = lx.service.Layer ()
        layer_scan = lx.object.LayerScan (layer_svc.ScanAllocate (lx.symbol.f_LAYERSCAN_ACTIVE | lx.symbol.f_LAYERSCAN_MARKPOLYS))
        if layer_scan.test ():
            # Sort out mark modes we'll need.
            mesh_svc = lx.service.Mesh ()
            mark_mode_checked = mesh_svc.ModeCompose ('user0', None)
            mark_mode_unchecked = mesh_svc.ModeCompose (None, 'user0')
            if selected_only:
                mark_mode_iterate = mesh_svc.ModeCompose ('select', 'lock hide user0')
            else:
                mark_mode_iterate = mesh_svc.ModeCompose (None, 'lock hide user0')

            layer_count = layer_scan.Count()

            for n in range(layer_count):
                mesh = lx.object.Mesh (layer_scan.MeshBase (n))
                if not mesh.test ():
                    continue

                polygon_count = mesh.PolygonCount ()
                if polygon_count == 0:
                    continue

                polygon = lx.object.Polygon (mesh.PolygonAccessor ())
                point = lx.object.Point (mesh.PointAccessor ())
                if not polygon.test () or not point.test ():
                    continue

                # Clear the checked marks on any polygons that are marked as checked.
                visClear = SetMarks (polygon, mark_mode_unchecked)
                polygon.Enumerate (mark_mode_checked, visClear, 0)

                # Now grab the island of any polygon that's marked as unchecked.
                # All polygons added to an island get marked as checked as we go.
                visIslands = PolysByIsland (polygon, point, mark_mode_checked)
                polygon.Enumerate (mark_mode_iterate, visIslands, 0)

                islands += visIslands.islands

            layer_scan.Apply ()

        return (layer_count, islands)

    def basic_Execute(self, msg, flags):
        layer_count, islands = self.get_IslandCount()

        msg = 'Found %s polygon island%s across %s mesh%s.' % (islands, '' if islands == 1 else 's', layer_count, '' if layer_count == 1 else 'es')

        lx.eval ('dialog.setup style:info')
        lx.eval ('dialog.title "Polygon Islands"')
        lx.eval ('dialog.msg "%s"' % msg)
        lx.eval ('dialog.open')

        lx.out (msg)

    def cmd_Query(self,index,vaQuery):
        if index == 0:
            va = lx.object.ValueArray ()
            va.set (vaQuery)
            layer_count, islands = self.get_IslandCount()
            va.AddInt (islands)
        return lx.result.OK

lx.bless (IslandCount_Cmd, 'ffr.islandCount')
# python
# ---------------------------------------
# Author:       James O'Hare
# Website:      http://www.farfarer.com/
# Copyright:    (c) James O'Hare
# ---------------------------------------

# !/usr/bin/env python

import lx, lxu, lxifc, lxu.command


class ListVMaps(lxifc.Visitor):
    def __init__(self, meshmap):
        self.meshmap = meshmap
        self.meshmap_IDs = []

    def vis_Evaluate(self):
        self.meshmap_IDs.append(self.meshmap.ID())


class RotateVMapsVert(lxifc.Visitor):
    def __init__(self, point, matrix, normalmaps, basismaps):
        self.point = point
        self.matrix = matrix
        self.normalmaps = normalmaps
        self.basismaps = basismaps

        self.normalvalue = lx.object.storage('f', 3)
        self.basisvalue = lx.object.storage('f', 6)

    def vis_Evaluate(self):
        for normalmap in self.normalmaps:
            if self.point.MapValue(normalmap, self.normalvalue):
                normal = self.normalvalue.get()
                normal = self.matrix.MultiplyVector(normal)
                self.normalvalue.set(normal)
                self.point.SetMapValue(normalmap, self.normalvalue)

        for basismap in self.basismaps:
            if self.point.MapValue(basismap, self.basisvalue):
                basis = self.basisvalue.get()
                tangent = (basis[0], basis[1], basis[2])
                bitangent = (basis[3], basis[4], basis[5])
                tangent = self.matrix.MultiplyVector(tangent)
                bitangent = self.matrix.MultiplyVector(bitangent)
                basis = (tangent[0], tangent[1], tangent[2], bitangent[0], bitangent[1], bitangent[2])
                self.basisvalue.set(basis)
                self.point.SetMapValue(basismap, self.basisvalue)


class RotateVMapsPoly(lxifc.Visitor):
    def __init__(self, polygon, matrix, normalmaps, basismaps):
        self.polygon = polygon
        self.matrix = matrix
        self.normalmaps = normalmaps
        self.basismaps = basismaps

        self.normalvalue = lx.object.storage('f', 3)
        self.basisvalue = lx.object.storage('f', 6)

    def vis_Evaluate(self):
        for x in range(self.polygon.VertexCount()):
            pointID = self.polygon.VertexByIndex(x)

            for normalmap in self.normalmaps:
                if self.polygon.MapValue(normalmap, pointID, self.normalvalue):
                    normal = self.normalvalue.get()
                    normal = self.matrix.MultiplyVector(normal)
                    self.normalvalue.set(normal)
                    self.polygon.SetMapValue(pointID, normalmap, self.normalvalue)

            for basismap in self.basismaps:
                if self.polygon.MapValue(basismap, pointID, self.basisvalue):
                    basis = self.basisvalue.get()
                    tangent = (basis[0], basis[1], basis[2])
                    bitangent = (basis[3], basis[4], basis[5])
                    tangent = self.matrix.MultiplyVector(tangent)
                    bitangent = self.matrix.MultiplyVector(bitangent)
                    basis = (tangent[0], tangent[1], tangent[2], bitangent[0], bitangent[1], bitangent[2])
                    self.basisvalue.set(basis)
                    self.polygon.SetMapValue(pointID, basismap, self.basisvalue)


class ResetMeshTransform_Cmd(lxu.command.BasicCommand):

    # ______________________________________________________________________________________________ SETUP AND INITIALISATION

    def __init__(self):
        lxu.command.BasicCommand.__init__(self)

    def cmd_UserName(self):
        return 'Reset Transform'

    def basic_ButtonName(self):
        return 'Reset Transform'

    def cmd_Desc(self):
        return 'Resets transform and fixes normal/tangent basis maps to account.'

    def cmd_Tooltip(self):
        return 'Resets transform and fixes normal/tangent basis maps to account.'

    def cmd_Help(self):
        return 'http://www.farfarer.com/'

    def cmd_Flags(self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO

    def basic_Enable(self, msg):
        return True

    def cmd_Interact(self):
        pass

    def basic_Execute(self, msg, flags):
        sel_svc = lx.service.Selection()
        scn_svc = lx.service.Scene()

        time = sel_svc.GetTime()
        scene = lx.object.Scene(lxu.select.SceneSelection().current())
        chan_read = lx.object.ChannelRead(scene.Channels(None, time))

        mesh_item = None

        layer_svc = lx.service.Layer()

        layer_scan = lx.object.LayerScan(layer_svc.ScanAllocate(lx.symbol.f_LAYERSCAN_EDIT))
        if not layer_scan.test():
            return

        layer_scan_count = layer_scan.Count()
        for layer_idx in range(layer_scan_count):
            item = layer_scan.MeshItem(layer_idx)
            if not item.test():
                return

            mesh = layer_scan.MeshEdit(layer_idx)
            if not mesh.test():
                return

            point = lx.object.Point(mesh.PointAccessor())
            polygon = lx.object.Polygon(mesh.PolygonAccessor())
            meshmap = lx.object.MeshMap(mesh.MeshMapAccessor())

            visitor = ListVMaps(meshmap)

            visitor.meshmap_IDs = []
            meshmap.FilterByType(lx.symbol.i_VMAP_NORMAL)
            meshmap.Enumerate(lx.symbol.iMARK_ANY, visitor, 0)
            normalmaps = tuple(visitor.meshmap_IDs)

            visitor.meshmap_IDs = []
            meshmap.FilterByType(lx.symbol.i_VMAP_TBASIS)
            meshmap.Enumerate(lx.symbol.iMARK_ANY, visitor, 0)
            basismaps = tuple(visitor.meshmap_IDs)

            meshmap.FilterByType(0)

            matrix_idx = item.ChannelLookup(lx.symbol.sICHAN_XFRMCORE_WROTMATRIX)
            matrix_value = lx.object.Value(chan_read.ValueObj(item, matrix_idx))
            matrix = lx.object.Matrix()
            matrix.set(matrix_value)

            visRotV = RotateVMapsVert(point, matrix, normalmaps, basismaps)
            point.Enumerate(lx.symbol.iMARK_ANY, visRotV, 0)

            visRotP = RotateVMapsPoly(polygon, matrix, normalmaps, basismaps)
            polygon.Enumerate(lx.symbol.iMARK_ANY, visRotP, 0)

            layer_scan.SetMeshChange(layer_idx, lx.symbol.f_MESHEDIT_MAP_OTHER)

        layer_scan.Apply()

        lx.eval('transform.freeze')


lx.bless(ResetMeshTransform_Cmd, 'ffr.resetMeshTransform')

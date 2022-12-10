#python
#---------------------------------------
# Name:         SMO_GC_FixVertexWithNullVNormData_Cmd.py
# Version:      1.0
#
# Purpose:      This script is designed to
#               Check current selected mesh, analyse the vertex data of Vertex Normal Maps.
#               If those value are Null, it select the vertex and apply a Set Vertex Normal command.
#               If you add the argument True it will automatically fix those vertex.
#
#
# Author:       Franck ELISABETH (with the help of Andreas Ranman (aka Roberyman))
# Website:      http://www.smoluck.com
#
# Created:      07/12/2021
# Copyright:    (c) Franck Elisabeth 2017-2022
#---------------------------------------

import modo, lx, lxifc, lxu
import lxu.command as SAC

Cmd_Name = "smo.GC.FixVertexWithNullVNormData"
# smo.GC.FixVertexWithNullVNormData

class InvalidMeshMapVisitor(lxifc.Visitor):
    """ Used to enumerate polygons to select invalid or zero value
    float3 vmaps. """
    def __init__(self, mesh, polygon, mesh_map):
        """

        :param mesh:
        :type mesh: lx.object.Mesh
        :param polygon:
        :type polygon: lx.object.Polygon
        :param mesh_map:
        :type mesh_map: lx.object.MeshMap

        """
        self.mesh = mesh
        self.polygon = polygon
        self.mesh_map = mesh_map

        self.value = lx.object.storage("f", 3)
        self.selection_service = lx.service.Selection()
        self.vertex_pointer_package = lx.object.VertexPacketTranslation(
            self.selection_service.Allocate(lx.symbol.sSELTYP_VERTEX))

    def vis_Evaluate(self):
        for point_index in range(self.polygon.VertexCount()):
            point_id = self.polygon.VertexByIndex(point_index)
            result = self.polygon.MapEvaluate(self.mesh_map.ID(), point_id, self.value)

            # Potential issue with precision for "null" vertex normals, float zero comparision
            # consider using py3 math isclose
            if not result or self.value.get() == (0.0, 0.0, 0.0):
                self.selection_service.Select(
                    lx.symbol.iSEL_VERTEX,
                    self.vertex_pointer_package.Packet(point_id, self.polygon.ID(), self.mesh)
                )

def SelectInvalidVNorm():
    """ """
    layer_service = lx.service.Layer()
    layer_scan = lx.object.LayerScan(
        layer_service.ScanAllocate(lx.symbol.f_LAYERSCAN_EDIT))
    VNMapName = lx.eval('pref.value application.defaultVertexNormals ?')

    selection_service = lx.service.Selection()
    selection_service.StartBatch()
    selection_service.Drop(lx.symbol.iSEL_VERTEX)
    for layer_index in range(layer_scan.Count()):
        mesh = lx.object.Mesh(layer_scan.MeshEdit(layer_index))
        polygon = lx.object.Polygon(mesh.PolygonAccessor())
        mesh_map = lx.object.MeshMap(mesh.MeshMapAccessor())

        if not all((mesh.test(), polygon.test(), mesh_map.test())):
            lx.out("Accessor tests failed.")
            return

        try:
            mesh_map.SelectByName(lx.symbol.i_VMAP_NORMAL, VNMapName)
        except LookupError:
            lx.out("No VMAP Normal with the name %s" % VNMapName)
            return

        visitor = InvalidMeshMapVisitor(mesh, polygon, mesh_map)
        polygon.Enumerate(lx.symbol.iMARK_ANY, visitor, 0)

        layer_scan.SetMeshChange(layer_index, lx.symbol.f_MESHEDIT_GEOMETRY)

    layer_scan.Apply()
    selection_service.EndBatch()

# if __name__ == "__main__":
#     SelectInvalidVNorm()

class SMO_GC_FixVertexWithNullVNormData_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
        self.dyna_Add("AutoFix Missing VertexNormal Data", lx.symbol.sTYPE_BOOLEAN)
        self.basic_SetFlags(0, lx.symbol.fCMDARG_OPTIONAL)  # here the (0) define the argument index.

    def cmd_Flags(self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO

    def cmd_Interact(self):
        pass

    def cmd_UserName(self):
        return 'SMO GC - Select or  AutoFix Vertex with Null Vertex Normal Data'

    def cmd_Desc(self):
        return 'Check current selected mesh, analyse the vertex data of Vertex Normal Maps. If those value are Null, it select the vertex and apply a Set Vertex Normal command. If you add the argument True it will automatically fix those vertex.'

    def cmd_Tooltip(self):
        return 'Check current selected mesh, analyse the vertex data of Vertex Normal Maps. If those value are Null, it select the vertex and apply a Set Vertex Normal command. If you add the argument True it will automatically fix those vertex.'

    def cmd_Help(self):
        return 'https://twitter.com/sm0luck'

    def basic_ButtonName(self):
        return 'SMO GC - Select or  AutoFix Vertex with Null Vertex Normal Data'

    def basic_Enable(self, msg):
        return True

    def basic_Execute(self, msg, flags):
        AutoFixMissingVNrmData = self.dyna_Bool(0)
        SelectInvalidVNorm()
        lx.eval('select.convert polygon')
        if AutoFixMissingVNrmData:
            lx.eval('smo.GC.SetVertexNormal')
        lx.eval('select.type vertex')



lx.bless(SMO_GC_FixVertexWithNullVNormData_Cmd, Cmd_Name)

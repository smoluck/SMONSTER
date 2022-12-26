# python
# ---------------------------------------
# Author:       James O'Hare
# Website:      http://www.farfarer.com/
# Copyright:    (c) James O'Hare
# ---------------------------------------

# !/usr/bin/env python

import lx, lxifc, lxu.command


class SelectByColor_Vis(lxifc.Visitor):
    def __init__(self, mesh, point, vmapID, rgb, selMode, sel_svc, vtx_pkt_trans, sel_type_vert):
        self.mesh = mesh
        self.point = point
        self.vmapID = vmapID
        self.rgb = rgb
        self.selMode = selMode
        self.sel_svc = sel_svc
        self.vtx_pkt_trans = vtx_pkt_trans
        self.sel_type_vert = sel_type_vert

        self.storage = lx.object.storage('f', 4)

    def vis_Evaluate(self):
        if self.point.MapValue(self.vmapID, self.storage):
            vrgb = self.storage.get()
            for x, y in zip(self.rgb, vrgb):
                if x != y:
                    return

            pkt = self.vtx_pkt_trans.Packet(self.point.ID(), 0, self.mesh)
            if self.selMode in ('set', 'add'):
                self.sel_svc.Select(self.sel_type_vert, pkt)
            elif self.selMode == 'remove':
                self.sel_svc.Deselect(self.sel_type_vert, pkt)


select_modes = (('set', 'add', 'remove'), ('Set', 'Add', 'Remove'))


class OptionPopup(lxifc.UIValueHints):
    def __init__(self, items):
        self._items = items

    def uiv_Flags(self):
        return lx.symbol.fVALHINT_POPUPS

    def uiv_PopCount(self):
        return len(self._items[0])

    def uiv_PopUserName(self, index):
        return self._items[1][index]

    def uiv_PopInternalName(self, index):
        return self._items[0][index]


class SelectByColor_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
        self.dyna_Add('color', lx.symbol.sTYPE_COLOR)
        self.dyna_Add('mode', lx.symbol.sTYPE_STRING)
        self.basic_SetFlags(1, lx.symbol.fCMDARG_OPTIONAL)

    def cmd_Interact(self):
        pass

    def cmd_UserName(self):
        return 'Select by Color'

    def cmd_Desc(self):
        return 'Select vertices with a given color.'

    def cmd_Tooltip(self):
        return 'Select vertices with a given color.'

    def cmd_Help(self):
        return 'http://www.farfarer.com/'

    def basic_ButtonName(self):
        return 'Select by Color'

    def cmd_Flags(self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO

    def basic_Enable(self, msg):
        return True

    def cmd_DialogInit(self):
        if not self.dyna_IsSet(1):
            self.attr_SetString(1, 'set')

    def arg_UIValueHints(self, index):
        if index == 1:
            return OptionPopup(select_modes)

    def basic_Execute(self, msg, flags):
        color = self.dyna_String(0, None)
        if color:
            rgb = tuple(map(float, color.split(" ")))
            if len(rgb) != 3:
                return

        selMode = self.dyna_String(1, 'set')

        if selMode not in ('set', 'add', 'remove'):
            return

        # Grab the active and background layers.
        layer_svc = lx.service.Layer()
        layer_scan = lx.object.LayerScan(
            layer_svc.ScanAllocate(lx.symbol.f_LAYERSCAN_ACTIVE | lx.symbol.f_LAYERSCAN_MARKVERTS))
        if not layer_scan.test():
            return

        # Early out if there are no active layers.
        layer_count = layer_scan.Count()
        if layer_count < 1:
            return

        sel_svc = lx.service.Selection()

        vmap_name = None
        vmap_type = None
        sel_type_vmap = sel_svc.LookupType(lx.symbol.sSELTYP_VERTEXMAP)
        vmap_pkt_trans = lx.object.VMapPacketTranslation(sel_svc.Allocate(lx.symbol.sSELTYP_VERTEXMAP))
        sel_vmap_count = sel_svc.Count(sel_type_vmap)
        for vmap_idx in range(sel_vmap_count):
            pkt = sel_svc.ByIndex(sel_type_vmap, vmap_idx)
            vmap_type = vmap_pkt_trans.Type(pkt)
            if vmap_type in (lx.symbol.i_VMAP_RGBA, lx.symbol.i_VMAP_RGB):
                vmap_name = vmap_pkt_trans.Name(pkt)
                break

        if vmap_name is None:
            return

        # Only deal with visible and unlocked verts.
        mesh_svc = lx.service.Mesh()
        mode = mesh_svc.ModeCompose(None, 'hide lock')

        sel_type_vert = sel_svc.LookupType(lx.symbol.sSELTYP_VERTEX)
        vtx_pkt_trans = lx.object.VertexPacketTranslation(sel_svc.Allocate(lx.symbol.sSELTYP_VERTEX))

        visitor = SelectByColor_Vis(None, None, 0, rgb, selMode, sel_svc, vtx_pkt_trans, sel_type_vert)

        if selMode == 'set':
            sel_svc.Clear(sel_type_vert)

        sel_svc.StartBatch()

        for x in range(layer_count):
            # Grab the meshes and their point and meshmap accessors.
            mesh = lx.object.Mesh(layer_scan.MeshBase(0))
            if not mesh.test():
                continue

            # Early out if there are no points in the active layer.
            point_count = mesh.PointCount()
            if point_count < 1:
                continue

            point = lx.object.Point(mesh.PointAccessor())
            if not point.test():
                continue

            meshmap = lx.object.MeshMap(mesh.MeshMapAccessor())
            if not meshmap.test():
                continue

            try:
                meshmap.SelectByName(vmap_type, vmap_name)
            except:
                continue

            # Select the vertices.
            visitor.mesh = mesh
            visitor.point = point
            visitor.vmapID = meshmap.ID()
            point.Enumerate(mode, visitor, 0)

        sel_svc.EndBatch()

        layer_scan.Apply()


lx.bless(SelectByColor_Cmd, 'ffr.selectByColor')

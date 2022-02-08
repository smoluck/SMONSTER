#---------------------------------------
# Author:       James O'Hare
# Website:      http://www.farfarer.com/
# Copyright:    (c) James O'Hare
#---------------------------------------

#!/usr/bin/env python

import lx, lxu, lxifc, lxu.command

class MeshPicker (lxu.command.BasicHints):
    def __init__ (self):
        scn_svc = lx.service.Scene ()
        self.mesh_itype = scn_svc.ItemTypeLookup (lx.symbol.sITYPE_MESH)

    def uiv_Flags (self):
        return lx.symbol.fVALHINT_ITEMS | lx.symbol.fVALHINT_ITEMS_NONE

    def uiv_ItemTest (self, item):
        return (lx.object.Item (item).Type () == self.mesh_itype)

class TagTypePopup (lxifc.UIValueHints):
    def __init__(self):
        self._internal = ['MATR', 'PART', 'PICK']
        self._user = ['Material', 'Part', 'Selection Set']

    def uiv_Flags(self):
        return lx.symbol.fVALHINT_POPUPS | lx.symbol.fVALHINT_POPUP_DIRECT

    def uiv_PopCount(self):
        return 3

    def uiv_PopUserName(self,index):
        return self._user[index]

    def uiv_PopInternalName(self,index):
        return self._internal[index]

class RenameTag (lxifc.Visitor):
    def __init__ (self, tagID, oldValue, newValue):
        self.tagID = tagID
        self.oldValue = oldValue
        self.newValue = newValue
        self.tag = lx.object.StringTag()

    def setElement (self, element):
        self.element = element
        self.tag.set(self.element)

    def vis_Evaluate (self):
        try:
            tag = self.tag.Get(self.tagID)
        except LookupError:
            pass # Polygon has no tag of this type.
        else:
            if tag == self.oldValue:
                self.tag.Set(self.tagID, self.newValue)

class RenamePTag_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)

        self.dyna_Add ('tagType', lx.symbol.sTYPE_STRING)

        self.dyna_Add ('oldName', lx.symbol.sTYPE_STRING)

        self.dyna_Add ('newName', lx.symbol.sTYPE_STRING)

        self.dyna_Add ('selected', lx.symbol.sTYPE_BOOLEAN)
        self.basic_SetFlags(3, lx.symbol.fCMDARG_OPTIONAL)

        self.dyna_Add ('item', '&item')
        self.basic_SetFlags(4, lx.symbol.fCMDARG_OPTIONAL)

    def cmd_Flags(self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO

    def basic_Enable(self, msg):
        return True

    def arg_UIValueHints(self, index):
        if index == 0:
            return TagTypePopup()
        if index == 4:
            return MeshPicker ()

    def cmd_UserName(self):
        return 'Rename Polygon Tags'

    def basic_ButtonName(self):
        return 'Rename Polygon Tags'

    def arg_UIHints (self, index, hints):
        if index == 0:
            hints.Label ('Tag Type')
        elif index == 1:
            hints.Label ('Rename From')
        elif index == 2:
            hints.Label ('Rename To')
        elif index == 3:
            hints.Label ('Selected Only')
        elif index == 4:
            hints.Label ('Item')

    def basic_Execute(self, msg, flags):
        tagID_str = self.dyna_String(0, None)

        if tagID_str and len(tagID_str) == 4:
            tagID = lxu.lxID4(tagID_str)
        else:
            # Invalid tag.
            return

        oldValue = self.dyna_String(1, None)
        newValue = self.dyna_String(2, None)

        if not (oldValue and newValue):
            # Invalid values.
            return

        ident = self.dyna_String(4, None)
        item = None

        if ident:
            scene = lx.object.Scene(lxu.select.SceneSelection ().current ())
            try:
                item = scene.ItemLookupIdent(ident)
            except LookupError:
                # Item not found.
                return

        selectedOnly = (self.dyna_Int(3, 0) == 1)
        if selectedOnly:
            mesh_svc = lx.service.Mesh ()
            mode = mesh_svc.ModeCompose ('select', 'hide lock')
        else:
            mode = lx.symbol.iMARK_ANY

        visitor = RenameTag (tagID, oldValue, newValue)

        layer_svc = lx.service.Layer ()
        if item:
            layer_scan = lx.object.LayerScan (layer_svc.ScanAllocateItem (item, lx.symbol.f_LAYERSCAN_EDIT))
        else:
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
            if not polygon.test ():
                continue

            visitor.setElement (polygon)
            polygon.Enumerate (mode, visitor, 0)

            layer_scan.SetMeshChange (l, lx.symbol.f_MESHEDIT_POL_TAGS)

        layer_scan.Apply ()

lx.bless (RenamePTag_Cmd, 'ffr.renamePTag')
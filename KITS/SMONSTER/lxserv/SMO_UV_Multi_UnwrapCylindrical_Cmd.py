# python
# ---------------------------------------
# Name:         SMO_UV_UnwrapCylindrical_Cmd.py
# Version:      1.0
#
# Purpose:      This script is designed to
#               Unwrap the current Polygon Selection
#               using Cylindrical Mode on Defined Axis.
#
# Author:       Franck ELISABETH
# Website:      http://www.smoluck.com
#
# Created:      28/12/2018
# Copyright:    (c) Franck Elisabeth 2017-2022
# ---------------------------------------

import lx, lxu, modo, sys

Cmd_Name = "smo.UV.Multi.UnwrapCylindrical"
# smo.UV.Multi.UnwrapCylindrical 2 0 0

class SMO_UV_Multi_UnwrapCylindrical_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
        self.dyna_Add("UV Projection Axis", lx.symbol.sTYPE_INTEGER)
        self.dyna_Add("Rectangle Mode", lx.symbol.sTYPE_INTEGER)
        self.dyna_Add("Select by Loop Mode", lx.symbol.sTYPE_INTEGER)

        self.SelModeVert = bool(lx.eval1("select.typeFrom typelist:vertex;polygon;edge;item;ptag ?"))
        self.SelModeEdge = bool(lx.eval1("select.typeFrom typelist:edge;vertex;polygon;item ?"))
        self.SelModePoly = bool(lx.eval1("select.typeFrom typelist:polygon;vertex;edge;item ?"))
        self.SelModeItem = bool(lx.eval1("select.typeFrom typelist:item;pivot;center;edge;polygon;vertex;ptag ?"))
        # print(self.SelModeVert)
        # print(self.SelModeEdge)
        # print(self.SelModePoly)
        # print(self.SelModeItem)

    def cmd_Flags(self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO

    def cmd_Interact(self):
        pass

    def cmd_UserName(self):
        return 'SMO UV - (Multi) Unwrap Cylindrical'

    def cmd_Desc(self):
        return 'MULTI - Unwrap the current Polygon Selection using Cylindrical Mode on Defined Axis.'

    def cmd_Tooltip(self):
        return 'MULTI - Unwrap the current Polygon Selection using Cylindrical Mode on Defined Axis.'

    def cmd_Help(self):
        return 'https://twitter.com/sm0luck'

    def basic_ButtonName(self):
        return 'SMO UV - (Multi) Unwrap Cylindrical'

    def basic_Enable(self, msg):
        return True

    def basic_Execute(self, msg, flags):
        UC_UVProjAxe = self.dyna_Int(0)
        UC_IsRectangle = self.dyna_Int(1)
        UC_SelectByLoop = self.dyna_Int(2)

        scene = modo.scene.current()

        UC_SelItem = lxu.select.ItemSelection().current()
        # print('lxu.object.Item : ', UC_SelItem)

        mesh = scene.selectedByType('mesh')
        # print('modo.Mesh :', mesh)
        # print('modo.Mesh list length:', len(mesh))

        UC_TargetIDList = []
        for item in mesh:
            itemType = modo.Item(item).type
            item = lx.object.Item(item)
            # print(item)
            if itemType == "mesh":
                ID = item.Ident()
                # print(ID)
                UC_TargetIDList.append(ID)
        # print(UC_TargetIDList)

        UC_PolysTuple = []
        for item in mesh:
            # CsPolys = len(item.geometry.polygons.selected)
            # print('Total selected Polygons on this mesh layer', CsPolys)
            Polys = item.geometry.polygons.selected
            # print('modo.Mesh list ', Polys)
            UC_PolysTuple.append(Polys)
        # print('Tuple (Poly ID and Mesh ID): ---)', UC_PolysTuple)

        UC_PolysList = list(UC_PolysTuple)
        # print('List (Poly ID and Mesh ID): ---)', UC_PolysList)
        # print(UC_PolysList)
        # print('------------------')
        # print(UC_PolysList[0])
        # print('------')
        # print(UC_PolysList[1])
        # print('------')
        # print(UC_PolysList[2])
        # print('------')
        # print(UC_PolysList[3])
        # print('------')

        lx.eval('select.drop polygon')
        lx.eval('smo.GC.DeselectAll')
        lx.eval('select.type item')
        lx.eval('smo.GC.DeselectAll')

        UC_index = -1
        for m in UC_TargetIDList:
            UC_index = (UC_index + 1)
            # print('id :', UC_index)
            scene.select(m)
            selected_mesh = scene.selectedByType('mesh')[0]
            # print('current mesh indentity :', UC_index, selected_mesh)
            lx.eval('select.type polygon')
            lx.eval('select.drop polygon')
            for item in (UC_PolysList[UC_index]):
                # print(item)
                selected_mesh.geometry.polygons.select(item)
                ############### PUT YOUR Command HERE to run over each item Polygons
                try:
                    lx.eval('smo.UV.UnwrapCylindrical %s %s %s' % (UC_UVProjAxe, UC_IsRectangle, UC_SelectByLoop))
                except:
                    lx.out('Error on {%s}' % (lx.eval('item.name ? xfrmcore')))
                selected_mesh.geometry.polygons.select(item, replace=True)
            lx.eval('select.type polygon')
            lx.eval('select.drop polygon')
            lx.eval('select.type item')
            lx.eval('select.drop item')
            # GOOOOOOOOOOOOD
        UC_index = -1
        lx.eval('smo.GC.DeselectAll')
        scene.select(mesh)
        lx.eval('select.type polygon')

        #####################################################
        # Repack in area or in 0-1 Space based on Preferences
        # Auto Update UV Seam map   Off = 0
        # Auto Update UV Seam map   On = 1
        AutoUpdateUVSeamCutMapState = lx.eval('user.value SMO_UseVal_UV_AutoUpdateUVSeamCutMapState ?')
        lx.out('Auto Update UV Seam Cut Map state:', AutoUpdateUVSeamCutMapState)

        # Repack Off = 0
        # Repack On = 1
        RePack = lx.eval('user.value SMO_UseVal_UV_RepackAfterUnwrap ?')
        lx.out('Auto RePack state:', RePack)

        # Multi_Repack Off = 0
        # Multi_Repack On = 1
        Multi_RePack = lx.eval('user.value SMO_UseVal_UV_RepackMultipleMeshAfterUnwrap ?')
        lx.out('Auto RePack Multiple Meshes together state:', Multi_RePack)

        # FixFlip Off = 0
        # FixFlip On = 1
        FixFlip = lx.eval('user.value SMO_UseVal_UV_FixFlip ?')
        lx.out('Auto Fix Flipped UVs state:', FixFlip)

        # Relocate in Area = 0
        # Relocate in Area = 1
        RelocateInArea = lx.eval('user.value SMO_UseVal_UV_RelocateInArea ?')
        lx.out('Relocate In Area state:', RelocateInArea)

        AutoExpandSel = lx.eval('user.value SMO_UseVal_UV_AutoExpandSelectionState ?')
        lx.out('Auto Expand Selection state:', AutoExpandSel)

        AutoHideState = lx.eval('user.value SMO_UseVal_UV_HideAfterUnwrap ?')
        lx.out('Auto Hide state:', AutoHideState)

        # MODO version checks.
        # Modo 13.0 and up have UV Seam map.
        # Version below 13.0 haven't
        Modo_ver = int(lx.eval('query platformservice appversion ?'))
        lx.out('Modo Version:', Modo_ver)
        #####################################################
        if Multi_RePack:
            if UC_UVProjAxe == 0 and RelocateInArea:
                lx.eval('smo.UV.SelectUVArea -2 0')
                lx.eval('hide.unsel')
                lx.eval('smo.UV.NormalizePackByArea 0 0 -2 0')
                lx.eval('unhide')

            if UC_UVProjAxe == 1 and RelocateInArea:
                lx.eval('smo.UV.SelectUVArea -1 0')
                lx.eval('hide.unsel')
                lx.eval('smo.UV.NormalizePackByArea 0 0 -1 0')
                lx.eval('unhide')

            if UC_UVProjAxe == 2 and RelocateInArea:
                lx.eval('smo.UV.SelectUVArea -1 1')
                lx.eval('hide.unsel')
                lx.eval('smo.UV.NormalizePackByArea 0 0 -1 1')
                lx.eval('unhide')

            if UC_UVProjAxe == 3 and RelocateInArea:
                lx.eval('smo.UV.SelectUVArea -2 1')
                lx.eval('hide.unsel')
                lx.eval('smo.UV.NormalizePackByArea 0 0 -2 1')
                lx.eval('unhide')

            if not RelocateInArea:
                lx.eval('smo.UV.SelectUVArea 0 0')
                lx.eval('hide.unsel')
                lx.eval('smo.UV.NormalizePackByArea 0 0 0 0')
                lx.eval('unhide')

        if AutoUpdateUVSeamCutMapState and Modo_ver >= 1300:
            lx.eval('smo.UV.UpdateUVSeamCutMap')
            lx.eval('view3d.showUVSeam true active')

        # select back the Polygons
        lx.eval('smo.GC.DeselectAll')
        scene.select(mesh)
        lx.eval('select.type polygon')

        if AutoHideState:
            # for item in (UC_PolysList):
            #     # print(item)
            #     selected_mesh.geometry.polygons.select(item)
            lx.eval('select.useSet UV_DONE select')
            lx.eval('hide.sel')

        del UC_index
        del UC_TargetIDList
        del UC_PolysList
        del UC_PolysTuple
        lx.eval('select.type polygon')


lx.bless(SMO_UV_Multi_UnwrapCylindrical_Cmd, Cmd_Name)

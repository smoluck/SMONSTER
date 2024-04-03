# python
"""
Name:         SMO_UV_Multi_UnwrapRectangleOrient_Cmd.py

Purpose:      This script is designed to
              (for Multiple Mesh)
              Unwrap the current Polygon Selection
              on defined Axis.

Author:       Franck ELISABETH
Website:      https://www.linkedin.com/in/smoluck/
Created:      26/08/2022
Copyright:    (c) Franck Elisabeth 2017-2022
"""

import lx
import lxu
import modo

Cmd_Name = "smo.UV.Multi.UnwrapRectangleOrient"
# smo.UV.Multi.UnwrapRectangleOrient 0


class SMO_UV_Multi_UnwrapRectangleOrient_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
        self.dyna_Add("Orient Direction", lx.symbol.sTYPE_INTEGER)
        self.basic_SetFlags(0, lx.symbol.fCMDARG_OPTIONAL)  # here the (0) define the argument index.

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
        return 'SMO UV - Unwrap Rectangle and Orient'

    def cmd_Desc(self):
        return 'MULTI - Unwrap the current Polygon Selection using Rectangle method and Orient the UV Island on defined direction (Via Arguments).'

    def cmd_Tooltip(self):
        return 'MULTI - Unwrap the current Polygon Selection using Rectangle method and Orient the UV Island on defined direction (Via Arguments).'

    def cmd_Help(self):
        return 'https://twitter.com/sm0luck'

    def basic_ButtonName(self):
        return 'SMO UV - Unwrap Rectangle and Orient'

    def basic_Enable(self, msg):
        return True

    def basic_Execute(self, msg, flags):
        Int_OrientDir = self.dyna_Int(0)

        # MODO version checks.
        # Modo 13.0 and up have UV Seam map.
        # Version below 13.0 haven't
        Modo_ver = int(lx.eval ('query platformservice appversion ?'))
        # lx.out('Modo Version:',Modo_ver)

        scene = modo.scene.current()


        SelItem = lxu.select.ItemSelection().current()
        # print('lxu.object.Item : ', SelItem)

        mesh = scene.selectedByType('mesh')
        # print('modo.Mesh :', mesh)
        # print('modo.Mesh list length:', len(mesh))

        MURO_TargetIDList = []
        for item in mesh:
            itemType = modo.Item(item).type
            item = lx.object.Item(item)
            # print(item)
            if itemType == "mesh":
                ID = item.Ident()
                # print(ID)
                MURO_TargetIDList.append(ID)
        # print(TMURO_argetIDList)

        MURO_PolysTuple = []
        for item in mesh:
            # CsPolys = len(item.geometry.polygons.selected)
            # print('Total selected Polygons on this mesh layer', CsPolys)
            Polys = item.geometry.polygons.selected
            # print('modo.Mesh list ', Polys)
            MURO_PolysTuple.append(Polys)
        # print('Tuple (Poly ID and Mesh ID): ---)', MURO_PolysTuple)

        MURO_PolysList = list(MURO_PolysTuple)
        # print('List (Poly ID and Mesh ID): ---)', MURO_PolysList)
        # print(MURO_PolysList)
        # print('------------------')
        # print(MURO_PolysList[0])
        # print('------')
        # print(MURO_PolysList[1])
        # print('------')
        # print(MURO_PolysList[2])
        # print('------')
        # print(MURO_PolysList[3])
        # print('------')

        lx.eval('select.drop polygon')
        lx.eval('smo.GC.DeselectAll')
        lx.eval('select.type item')
        lx.eval('smo.GC.DeselectAll')

        index = -1
        for n in MURO_TargetIDList:
            index = (index + 1)
            # print('id :', index)
            scene.select(n)
            selected_mesh = scene.selectedByType('mesh')[0]
            # print('current mesh identity :', index, selected_mesh)
            lx.eval('select.type polygon')
            lx.eval('select.drop polygon')
            for item in (MURO_PolysList[index]):
                # print(item)
                selected_mesh.geometry.polygons.select(item)
                ############### PUT YOUR Command HERE to run over each item Polygons
            try:
                lx.eval('smo.UV.UnwrapRectangleOrient %s' % Int_OrientDir)
            except:
                lx.out('Error on {%s}' % (lx.eval('item.name ? xfrmcore')))
                selected_mesh.geometry.polygons.select(item, replace=True)
            lx.eval('select.type polygon')
            lx.eval('select.drop polygon')
            lx.eval('select.type item')
            lx.eval('select.drop item')
            # GOOOOOOOOOOOOD
        lx.eval('smo.GC.DeselectAll')
        scene.select(mesh)
        lx.eval('select.type polygon')

        #####################################################
        # Repack in area or in 0-1 Space based on Preferences
        # Auto Update UV Seam map   Off = 0
        # Auto Update UV Seam map   On = 1
        AutoUpdateUVSeamCutMapState = lx.eval('user.value SMO_UseVal_UV_AutoUpdateUVSeamCutMapState ?')
        lx.out('Auto Update UV Seam Cut Map state:',AutoUpdateUVSeamCutMapState)

        # Repack Off = 0
        # Repack On = 1
        RePack = lx.eval('user.value SMO_UseVal_UV_RepackAfterUnwrap ?')
        lx.out('RePack state:', RePack)

        # Multi_Repack Off = 0
        # Multi_Repack On = 1
        Multi_RePack = lx.eval('user.value SMO_UseVal_UV_RepackMultipleMeshAfterUnwrap ?')
        lx.out('Auto RePack Multiple Meshes together state:', Multi_RePack)

        # Relocate in Area = 0
        # Relocate in Area = 1
        RelocateInArea = lx.eval('user.value SMO_UseVal_UV_RelocateInArea ?')
        lx.out('Relocate In Area state:', RelocateInArea)

        # Fit UVs
        if RelocateInArea:
            if not RePack:
                lx.eval('uv.fit entire gapsByPixel:8.0 udim:1002')

            if RePack:
                lx.eval('uv.fit entire gapsByPixel:8.0 udim:1002')
                lx.eval('smo.UV.NormalizePackByArea 0 0 1 0')

        if not RelocateInArea:
            if not RePack:
                lx.eval('uv.fit entire gapsByPixel:8.0 udim:1001')

            if RePack:
                lx.eval('uv.fit entire gapsByPixel:8.0 udim:1001')
                lx.eval('unhide')
                lx.eval('smo.UV.SelectUVArea 0 0')
                lx.eval('hide.unsel')
                lx.eval('smo.UV.NormalizePackByArea 0 0 0 0')
        #####################################################

        # select back the Polygons
        lx.eval('smo.GC.DeselectAll')
        scene.select(mesh)
        lx.eval('select.type polygon')
        for item in MURO_PolysList:
            # print(item)
            selected_mesh.geometry.polygons.select(item)

        if Multi_RePack:
            lx.eval('smo.UV.NormalizePackByArea 0 0 0 0')

        lx.eval('smo.GC.DeselectAll')
        scene.select(mesh)
        lx.eval('select.type polygon')
        for item in MURO_PolysList:
            # print(item)
            selected_mesh.geometry.polygons.select(item)

        if AutoUpdateUVSeamCutMapState == True and Modo_ver >= 1300:
            lx.eval('smo.UV.UpdateUVSeamCutMap')
            lx.eval('view3d.showUVSeam true active')

        AutoHideState = lx.eval('user.value SMO_UseVal_UV_HideAfterUnwrap ?')
        if AutoHideState:
            lx.eval('select.useSet UV_DONE select')
            lx.eval('hide.sel')

        del index
        del MURO_TargetIDList
        del MURO_PolysList
        del MURO_PolysTuple
        lx.eval('select.type polygon')


lx.bless(SMO_UV_Multi_UnwrapRectangleOrient_Cmd, Cmd_Name)

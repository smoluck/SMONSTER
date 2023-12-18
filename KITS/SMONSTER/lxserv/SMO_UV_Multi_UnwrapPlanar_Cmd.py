# python
"""
Name:         SMO_UV_Multi_UnwrapPlanar_Cmd.py

Purpose:      This script is designed to
              (for Multiple Mesh)
              Unwrap the current Polygon Selection
              on defined Axis.

Author:       Franck ELISABETH
Website:      https://www.linkedin.com/in/smoluck/
Created:      28/12/2018
Copyright:    (c) Franck Elisabeth 2017-2022
"""

import lx
import lxu
import modo

Cmd_Name = "smo.UV.Multi.UnwrapPlanar"
# smo.UV.Multi.UnwrapPlanar 2 0


class SMO_UV_Multi_UnwrapPlanar_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
        self.dyna_Add("Unwrap Projection Axis", lx.symbol.sTYPE_INTEGER)
        self.basic_SetFlags(0, lx.symbol.fCMDARG_OPTIONAL)  # here the (0) define the argument index.
        self.dyna_Add("Facing Ratio Mode", lx.symbol.sTYPE_INTEGER)
        self.basic_SetFlags(1, lx.symbol.fCMDARG_OPTIONAL)

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
        return 'SMO UV - (Multi) Unwrap Planar MultiMeshes'

    def cmd_Desc(self):
        return 'MULTI - Unwrap the current Polygon Selection on defined Axis.'

    def cmd_Tooltip(self):
        return 'MULTI - Unwrap the current Polygon Selection on defined Axis.'

    def cmd_Help(self):
        return 'https://twitter.com/sm0luck'

    def basic_ButtonName(self):
        return 'SMO UV - (Multi) Unwrap Planar MultiMeshes'

    def basic_Enable(self, msg):
        return True

    def basic_Execute(self, msg, flags):
        MUP_UVProjAxe = self.dyna_Int(0)
        MUP_Similar = self.dyna_Int(1)

        scene = modo.scene.current()

        # ###
        # lx.out('<------------- START -------------->')
        # lx.out('<--- UV Map Safety Check --->')
        # ###
        # Create a UV Map automatically in case there is no UVMaps
        # DefaultUVMapName = lx.eval('pref.value application.defaultTexture ?')
        # print(DefaultUVMapName)
        #
        # m = modo.Mesh()
        # print(m.name)
        # maps = m.geometry.vmaps.getMapsByType([lx.symbol.i_VMAP_TEXTUREUV])  # same as m.geometry.vmaps.uvMaps
        # print(maps)
        # print(len(maps))
        #
        # if len(maps) == 0:
        # #     lx.eval('vertMap.new {%s} txuv' % DefaultUVMapName)
        # #     print('New UVMap created')
        # #     print('UV map name is: %s' % DefaultUVMapName)
        # #
        # if len(maps) == 1:
        # #     lx.eval('select.vertexMap {%s} txuv replace' % maps[0].name)
        # #
        # if len(maps) > 1:
        # #     # get the current select UV Map name
        # #     print(lx.eval('vertMap.list type:txuv ?'))
        #
        # SelectedMeshUVMapsCount = len(maps)
        # UVUnwrapPlanar_UVMapName = (lx.eval('vertMap.list type:txuv ?'))
        # lx.out('Selected Mesh UV Maps Name:', UVUnwrapPlanar_UVMapName)
        #
        # lx.eval('smo.GC.ClearSelectionVmap 1 1')
        # lx.eval("select.vertexMap {%s} txuv replace" % UVUnwrapPlanar_UVMapName)
        # ###
        # lx.out('<- UV Map Safety Check ->')
        # lx.out('<------------- END -------------->')
        # ###

        MUP_SelItem = lxu.select.ItemSelection().current()
        # print('lxu.object.Item : ', MUP_SelItem)

        mesh = scene.selectedByType('mesh')
        print('modo.Mesh :', mesh)
        print('modo.Mesh list length:', len(mesh))

        MUP_TargetIDList = []
        for item in mesh:
            itemType = modo.Item(item).type
            item = lx.object.Item(item)
            # print(item)
            if itemType == "mesh":
                ID = item.Ident()
                # print(ID)
                MUP_TargetIDList.append(ID)
        # print(MUP_TargetIDList)

        MUP_PolysTuple = []
        for item in mesh:
            # CsPolys = len(item.geometry.polygons.selected)
            # print('Total selected Polygons on this mesh layer', CsPolys)
            Polys = item.geometry.polygons.selected
            # print('modo.Mesh list ', Polys)
            MUP_PolysTuple.append(Polys)
        # print('Tuple (Poly ID and Mesh ID): ---)', MUP_PolysTuple)

        MUP_PolysList = list(MUP_PolysTuple)
        # print('List (Poly ID and Mesh ID): ---)', MUP_PolysList)
        # print(MUP_PolysList)
        # print('------------------')
        # print(MUP_PolysList[0])
        # print('------')
        # print(MUP_PolysList[1])
        # print('------')
        # print(MUP_PolysList[2])
        # print('------')
        # print(MUP_PolysList[3])
        # print('------')

        lx.eval('select.drop polygon')
        lx.eval('smo.GC.DeselectAll')
        lx.eval('select.type item')
        lx.eval('smo.GC.DeselectAll')

        index = -1
        if len(mesh) > 1:
            for n in MUP_TargetIDList:
                index = (index + 1)
                # print('id :', index)
                scene.select(n)
                selected_mesh = scene.selectedByType('mesh')[0]
                # print('current mesh identity :', index, selected_mesh)
                lx.eval('select.type polygon')
                lx.eval('select.drop polygon')
                for item in (MUP_PolysList[index]):
                    # print(item)
                    selected_mesh.geometry.polygons.select(item)

                    ############### PUT YOUR Command HERE to run over each item Polygons
                try:
                    # lx.eval('smo.UV.AutoCreateUVMap')
                    lx.eval('smo.UV.UnwrapPlanar %s %s' % (MUP_UVProjAxe, MUP_Similar))
                except:
                    lx.out('Error on {%s}' % (lx.eval('item.name ? xfrmcore')))
                selected_mesh.geometry.polygons.select(item, replace=True)

                lx.eval('select.type polygon')
                lx.eval('select.drop polygon')
                lx.eval('select.type item')
                lx.eval('select.drop item')
                # GOOOOOOOOOOOOD
        index = -1

        if len(mesh) == 1:
            scene.select(mesh)
            lx.eval('select.type polygon')
            for item in (MUP_PolysList[index]):
                # print(item)
                selected_mesh = scene.selectedByType('mesh')[0]
                selected_mesh.geometry.polygons.select(item)
            # lx.eval('smo.UV.AutoCreateUVMap')
            lx.eval('smo.UV.UnwrapPlanar %s %s' % (MUP_UVProjAxe, MUP_Similar))

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
        Modo_ver = int(lx.eval ('query platformservice appversion ?'))
        lx.out('Modo Version:', Modo_ver)
        #####################################################
        if Multi_RePack:
            if MUP_UVProjAxe == 0 and RelocateInArea:
                lx.eval('smo.UV.SelectUVArea -2 0')
                lx.eval('hide.unsel')
                lx.eval('smo.UV.NormalizePackByArea 0 0 -2 0')
                lx.eval('unhide')

            if MUP_UVProjAxe == 1 and RelocateInArea:
                lx.eval('smo.UV.SelectUVArea -1 0')
                lx.eval('hide.unsel')
                lx.eval('smo.UV.NormalizePackByArea 0 0 -1 0')
                lx.eval('unhide')

            if MUP_UVProjAxe == 2 and RelocateInArea:
                lx.eval('smo.UV.SelectUVArea -1 1')
                lx.eval('hide.unsel')
                lx.eval('smo.UV.NormalizePackByArea 0 0 -1 1')
                lx.eval('unhide')

            if MUP_UVProjAxe == 3 and RelocateInArea:
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
            # for item in (MUP_PolysList):
            #     # print(item)
            #     selected_mesh.geometry.polygons.select(item)
            # if MUP_Similar == 1:
            #     lx.eval('smo.GC.Multi.SelectCoPlanarPoly 0 2 0')
            # if MUP_Similar == 2:
            #     lx.eval('smo.GC.Multi.SelectCoPlanarPoly 1 2 1000')
            # if MUP_Similar == 3:
            #     lx.eval('smo.GC.Multi.SelectCoPlanarPoly 2 2 1000')
            # lx.eval('hide.sel')
            lx.eval('select.useSet UV_DONE select')
            lx.eval('hide.sel')

        del index
        del MUP_TargetIDList
        del MUP_PolysList
        del MUP_PolysTuple
        lx.eval('select.type polygon')


lx.bless(SMO_UV_Multi_UnwrapPlanar_Cmd, Cmd_Name)

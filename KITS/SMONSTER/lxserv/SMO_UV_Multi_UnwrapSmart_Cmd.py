# python
# ---------------------------------------
# Name:         SMO_UV_Multi_UnwrapSmart_Cmd.py
# Version:      1.0
#
# Purpose:      This script is designed to
#               (for Multiple Mesh)
#               Unwrap the current Polygon Selection or via a set of Edges
#               with various Unwrap Method, Rectangle Mode and Autoloop function using Arguments.
#
# Author:       Franck ELISABETH
# Website:      http://www.smoluck.com
#
# Created:      28/12/2018
# Copyright:    (c) Franck Elisabeth 2017-2022
# ---------------------------------------

import lx, lxu, modo

Cmd_Name = "smo.UV.Multi.UnwrapSmart"
# smo.UV.Multi.UnwrapSmart 2 0

class SMO_UV_Multi_UnwrapSmart_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
        self.dyna_Add("Unwrap Method", lx.symbol.sTYPE_INTEGER)
        self.basic_SetFlags(0, lx.symbol.fCMDARG_OPTIONAL)  # here the (0) define the argument index.
        self.dyna_Add("Initial Projection", lx.symbol.sTYPE_INTEGER)
        self.basic_SetFlags(1, lx.symbol.fCMDARG_OPTIONAL)
        self.dyna_Add("Rectangle Mode", lx.symbol.sTYPE_INTEGER)
        self.basic_SetFlags(2, lx.symbol.fCMDARG_OPTIONAL)
        self.dyna_Add("Select by Loop Mode", lx.symbol.sTYPE_INTEGER)
        self.basic_SetFlags(3, lx.symbol.fCMDARG_OPTIONAL)

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
        return 'SMO UV - (Multi) Unwrap Smart MultiMeshes'

    def cmd_Desc(self):
        return 'MULTI - Unwrap the current Polygon Selection or via a set of Edges with various Unwrap Method, Rectangle Mode and Autoloop function using Arguments.'

    def cmd_Tooltip(self):
        return 'MULTI - Unwrap the current Polygon Selection or via a set of Edges with various Unwrap Method, Rectangle Mode and Autoloop function using Arguments.'

    def cmd_Help(self):
        return 'https://twitter.com/sm0luck'

    def basic_ButtonName(self):
        return 'SMO UV - (Multi) Unwrap Smart MultiMeshes'

    def basic_Enable(self, msg):
        return True

    def basic_Execute(self, msg, flags):
        MUS_UnwrapMethod = self.dyna_Int(0)
        MUS_InitProjection = self.dyna_Int(1)
        MUS_IsRectangle = self.dyna_Int(2)
        MUS_SelectByLoop = self.dyna_Int(3)

        scene = modo.scene.current()

        # MODO version checks.
        # Modo 13.0 and up have UV Seam map.
        # Version below 13.0 haven't
        Modo_ver = int(lx.eval ('query platformservice appversion ?'))
        lx.out('Modo Version:', Modo_ver)

        ############### 5 ARGUMENTS ###############
        args = lx.args()
        lx.out(args)

        # Conformal= 0
        # Angle Based = 1
        UnwrapMethod = MUS_UnwrapMethod
        lx.out('Desired Unwrap Method:', UnwrapMethod)

        # Planar = 0
        # Group Normal = 1
        InitProjection = MUS_InitProjection
        lx.out('Initial Projection Mode:', InitProjection)

        # Current Selection is not Rectangle = 0
        # Current Selection is Rectangle = 1
        IsRectangle = MUS_IsRectangle
        lx.out('Rectangle Post pass:', IsRectangle)

        # Current Selection = 0
        # current selection + Add loop = 1
        SelectByLoop = MUS_SelectByLoop
        lx.out('Select by loop state:', SelectByLoop)
        ############### ARGUMENTS ###############

        selType = ""
        # Used to query layerservice for the list of polygons, edges or vertices.
        attrType = ""

        if lx.eval1("select.typeFrom typelist:vertex;polygon;edge;item;ptag ?"):
            selType = "vertex"
            attrType = "vert"
            SMO_SafetyCheck_MUS_PolygonModeEnabled = 0
            SMO_SafetyCheck_MUS_EdgeModeEnabled = 0
            SMO_SafetyCheck_MUS_VertexModeEnabled = 1
        elif lx.eval1("select.typeFrom typelist:edge;vertex;polygon;item ?"):
            selType = "edge"
            attrType = "edge"
            SMO_SafetyCheck_MUS_VertexModeEnabled = 0
            SMO_SafetyCheck_MUS_EdgeModeEnabled = 1
            SMO_SafetyCheck_MUS_PolygonModeEnabled = 0
        elif lx.eval1("select.typeFrom typelist:polygon;vertex;edge;item ?"):
            selType = "polygon"
            attrType = "poly"
            SMO_SafetyCheck_MUS_VertexModeEnabled = 0
            SMO_SafetyCheck_MUS_EdgeModeEnabled = 0
            SMO_SafetyCheck_MUS_PolygonModeEnabled = 1
            lx.out('script Running: Polygon Component Selection Mode')
        else:
            SMO_SafetyCheck_MUS_VertexModeEnabled = 0
            SMO_SafetyCheck_MUS_EdgeModeEnabled = 0
            SMO_SafetyCheck_MUS_PolygonModeEnabled = 0



        if SMO_SafetyCheck_MUS_PolygonModeEnabled == 1:
            # ###
            # lx.out('<------------- START -------------->')
            # lx.out('<--- UV Map Safety Check --->')
            # ###
            # # Create a UV Map automatically in case there is no UVMaps
            # DefaultUVMapName = lx.eval('pref.value application.defaultTexture ?')
            # # print(DefaultUVMapName)
            #
            m = modo.Mesh()
            # # print(m.name)
            # maps = m.geometry.vmaps.getMapsByType([lx.symbol.i_VMAP_TEXTUREUV])  # same as m.geometry.vmaps.uvMaps
            # # print(maps)
            # # print(len(maps))
            #
            # # if len(maps) == 0:
            # #     lx.eval('vertMap.new {%s} txuv' % DefaultUVMapName)
            # #     print('New UVMap created')
            # #     print('UV map name is: %s' % DefaultUVMapName)
            # #
            # # if len(maps) == 1:
            # #     lx.eval('select.vertexMap {%s} txuv replace' % maps[0].name)
            # #
            # # if len(maps) > 1:
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

            MUS_SelItem = lxu.select.ItemSelection().current()
            # print('lxu.object.Item : ', MMUS_SelItem)

            mesh = scene.selectedByType('mesh')
            print('modo.Mesh :', mesh)
            print('modo.Mesh list length:', len(mesh))

            MUS_TargetIDList = []
            for item in mesh:
                itemType = modo.Item(item).type
                item = lx.object.Item(item)
                # print(item)
                if itemType == "mesh":
                    ID = item.Ident()
                    # print(ID)
                    MUS_TargetIDList.append(ID)
            # print(MUS_TargetIDList)

            MUS_PolysTuple = []
            for item in mesh:
                # CsPolys = len(item.geometry.polygons.selected)
                # print('Total selected Polygons on this mesh layer', CsPolys)
                Polys = item.geometry.polygons.selected
                # print('modo.Mesh list ', Polys)
                MUS_PolysTuple.append(Polys)
            # print('Tuple (Poly ID and Mesh ID): ---)', MUS_PolysTuple)

            MUS_PolysList = list(MUS_PolysTuple)
            # print('List (Poly ID and Mesh ID): ---)', MUS_PolysList)
            # print(MUS_PolysList)
            # print('------------------')
            # print(MUS_PolysList[0])
            # print('------')
            # print(MUS_PolysList[1])
            # print('------')
            # print(MUS_PolysList[2])
            # print('------')
            # print(MUS_PolysList[3])
            # print('------')

            lx.eval('select.drop polygon')
            lx.eval('smo.GC.DeselectAll')
            lx.eval('select.type item')
            lx.eval('smo.GC.DeselectAll')

            index = -1
            if len(mesh) > 1:
                for n in MUS_TargetIDList:
                    index = (index + 1)
                    # print('id :', index)
                    scene.select(n)
                    selected_mesh = scene.selectedByType('mesh')[0]
                    # print('current mesh identity :', index, selected_mesh)
                    lx.eval('select.type polygon')
                    lx.eval('select.drop polygon')
                    for item in (MUS_PolysList[index]):
                        # print(item)
                        selected_mesh.geometry.polygons.select(item)
                        ############### PUT YOUR Command HERE to run over each item Polygons
                    try:
                        # lx.eval('smo.UV.AutoCreateUVMap')
                        lx.eval('smo.UV.UnwrapSmart %s %s %s %s' % (UnwrapMethod, InitProjection, IsRectangle, SelectByLoop))
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
                scene.select(m)
                lx.eval('select.type polygon')
                for item in (MUS_PolysList[index]):
                    # print(item)
                    selected_mesh = scene.selectedByType('mesh')[0]
                    selected_mesh.geometry.polygons.select(item)
                # lx.eval('smo.UV.AutoCreateUVMap')
                lx.eval('smo.UV.UnwrapSmart %s %s %s %s' % (UnwrapMethod, InitProjection, IsRectangle, SelectByLoop))

            lx.eval('smo.GC.DeselectAll')
            scene.select(mesh)
            lx.eval('select.type polygon')


        if SMO_SafetyCheck_MUS_EdgeModeEnabled == 1:
            # ###
            # lx.out('<------------- START -------------->')
            # lx.out('<--- UV Map Safety Check --->')
            # ###
            # # Create a UV Map automatically in case there is no UVMaps
            # DefaultUVMapName = lx.eval('pref.value application.defaultTexture ?')
            # # print(DefaultUVMapName)
            #
            m = modo.Mesh()
            # # print(m.name)
            # maps = m.geometry.vmaps.getMapsByType([lx.symbol.i_VMAP_TEXTUREUV])  # same as m.geometry.vmaps.uvMaps
            # # print(maps)
            # # print(len(maps))
            #
            # # if len(maps) == 0:
            # #     lx.eval('vertMap.new {%s} txuv' % DefaultUVMapName)
            # #     print('New UVMap created')
            # #     print('UV map name is: %s' % DefaultUVMapName)
            # #
            # # if len(maps) == 1:
            # #     lx.eval('select.vertexMap {%s} txuv replace' % maps[0].name)
            # #
            # # if len(maps) > 1:
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

            MUS_SelItem = lxu.select.ItemSelection().current()
            # print('lxu.object.Item : ', MMUS_SelItem)

            mesh = scene.selectedByType('mesh')
            print('modo.Mesh :', mesh)
            print('modo.Mesh list length:', len(mesh))

            MUS_TargetIDList = []
            for item in mesh:
                itemType = modo.Item(item).type
                item = lx.object.Item(item)
                # print(item)
                if itemType == "mesh":
                    ID = item.Ident()
                    # print(ID)
                    MUS_TargetIDList.append(ID)
            # print(MUS_TargetIDList)

            MUS_EdgesTuple = []
            for item in mesh:
                # CsEdges = len(item.geometry.edges.selected)
                # print('Total selected Edges on this mesh layer', CsEdges)
                Edges = item.geometry.edges.selected
                # print('modo.Mesh list ', Edges)
                MUS_EdgesTuple.append(Edges)
            # print('Tuple (Edge ID and Mesh ID): ---)', MUS_EdgesTuple)

            MUS_EdgesList = list(MUS_EdgesTuple)
            # print('List (Poly ID and Mesh ID): ---)', MUS_EdgesList)
            # print(MUS_EdgesList)
            # print('------------------')
            # print(MUS_EdgesList[0])
            # print('------')
            # print(MUS_EdgesList[1])
            # print('------')
            # print(MUS_EdgesList[2])
            # print('------')
            # print(MUS_EdgesList[3])
            # print('------')

            lx.eval('select.drop edge')
            lx.eval('smo.GC.DeselectAll')
            lx.eval('select.type item')
            lx.eval('smo.GC.DeselectAll')

            index = -1
            if len(mesh) > 1:
                for n in MUS_TargetIDList:
                    index = (index + 1)
                    # print('id :', index)
                    scene.select(n)
                    selected_mesh = scene.selectedByType('mesh')[0]
                    # print('current mesh identity :', index, selected_mesh)
                    lx.eval('select.type edge')
                    lx.eval('select.drop edge')
                    for item in (MUS_EdgesList[index]):
                        # print(item)
                        selected_mesh.geometry.edges.select(item)
                        ############### PUT YOUR Command HERE to run over each item Polygons
                    try:
                        # lx.eval('smo.UV.AutoCreateUVMap')
                        lx.eval('smo.UV.UnwrapSmart %s %s %s %s' % (UnwrapMethod, InitProjection, IsRectangle, SelectByLoop))
                    except:
                        lx.out('Error on {%s}' % (lx.eval('item.name ? xfrmcore')))
                    selected_mesh.geometry.edges.select(item, replace=True)
                    lx.eval('select.type edge')
                    lx.eval('select.drop edge')
                    lx.eval('select.type item')
                    lx.eval('select.drop item')
                    # GOOOOOOOOOOOOD
            index = -1

            if len(mesh) == 1:
                scene.select(mesh)
                lx.eval('select.type edge')
                for item in (MUS_EdgesList[index]):
                    # print(item)
                    selected_mesh = scene.selectedByType('mesh')[0]
                    selected_mesh.geometry.edges.select(item)
                # lx.eval('smo.UV.AutoCreateUVMap')
                lx.eval('smo.UV.UnwrapSmart %s %s %s %s' % (UnwrapMethod, InitProjection, IsRectangle, SelectByLoop))

            lx.eval('smo.GC.DeselectAll')
            scene.select(mesh)
            lx.eval('select.type edge')

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

        #####################################################
        if Multi_RePack:
            if RelocateInArea:
                if UnwrapMethod == 0 and IsRectangle == 0:
                    lx.eval('smo.UV.SelectUVArea 0 -1')
                    lx.eval('hide.unsel')
                    lx.eval('smo.UV.NormalizePackByArea 0 0 0 -1')
                    lx.eval('unhide')

                if UnwrapMethod == 1 and IsRectangle == 0:
                    lx.eval('smo.UV.SelectUVArea 1 -1')
                    lx.eval('hide.unsel')
                    lx.eval('smo.UV.NormalizePackByArea 0 0 1 -1')
                    lx.eval('unhide')

                if UnwrapMethod == 0 and IsRectangle == 1:
                    lx.eval('smo.UV.SelectUVArea 0 -2')
                    lx.eval('hide.unsel')
                    lx.eval('smo.UV.NormalizePackByArea 0 0 0 -2')
                    lx.eval('unhide')

            if not RelocateInArea:
                lx.eval('unhide')
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
            # for item in (MUS_PolysList):
            #     # print(item)
            #     selected_mesh.geometry.polygons.select(item)
            # if MUS_Similar == 1:
            #     lx.eval('smo.GC.Multi.SelectCoPlanarPoly 0 2 0')
            # if MUS_Similar == 2:
            #     lx.eval('smo.GC.Multi.SelectCoPlanarPoly 1 2 1000')
            # if MUS_Similar == 3:
            #     lx.eval('smo.GC.Multi.SelectCoPlanarPoly 2 2 1000')
            # lx.eval('hide.sel')
            lx.eval('select.useSet UV_DONE select')
            lx.eval('hide.sel')

        del index
        del MUS_TargetIDList

        if SMO_SafetyCheck_MUS_PolygonModeEnabled == 1:
            del MUS_PolysList
            del MUS_PolysTuple
            lx.eval('select.type polygon')

        if SMO_SafetyCheck_MUS_EdgeModeEnabled == 1:
            del MUS_EdgesList
            del MUS_EdgesTuple
            lx.eval('select.type edge')


lx.bless(SMO_UV_Multi_UnwrapSmart_Cmd, Cmd_Name)

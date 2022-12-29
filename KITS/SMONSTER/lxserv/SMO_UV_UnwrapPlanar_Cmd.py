# python
"""
Name:         SMO_UV_UnwrapPlanar_Cmd.py

Purpose:      This script is designed to
              Unwrap the current Polygon Selection
              on defined Axis.

Author:       Franck ELISABETH
Website:      https://www.smoluck.com
Created:      28/12/2018
Copyright:    (c) Franck Elisabeth 2017-2022
"""

import lx
import lxu
import modo
import sys

Cmd_Name = "smo.UV.UnwrapPlanar"
# smo.UV.UnwrapPlanar 2 0


class SMO_UV_UnwrapPlanar_Cmd(lxu.command.BasicCommand):
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
        return 'SMO UV - Unwrap Planar'

    def cmd_Desc(self):
        return 'Unwrap the current Polygon Selection on defined Axis.'

    def cmd_Tooltip(self):
        return 'Unwrap the current Polygon Selection on defined Axis.'

    def cmd_Help(self):
        return 'https://twitter.com/sm0luck'

    def basic_ButtonName(self):
        return 'SMO UV - Unwrap Planar'

    def basic_Enable(self, msg):
        return True

    def basic_Execute(self, msg, flags):
        scene = modo.scene.current()
        # mesh = scene.selectedByType('mesh')[0]
        # Force to select the current Mesh Item if it is not selected in the Item List
        lx.eval('smo.MASTER.ForceSelectMeshItemOnly')
        lx.eval('smo.UV.AutoCreateUVMap')
        meshes = scene.selectedByType('mesh')


        # BugFix to preserve the state of the RefSystem (item at origin in viewport)
        # This query only works when an item is selected.
        RefSystemActive = bool()
        CurrentRefSystemItem = lx.eval('item.refSystem ?')
        # print(CurrentRefSystemItem)
        if len(CurrentRefSystemItem) != 0:
            RefSystemActive = True
        else:
            RefSystemActive = False
        # print(RefSystemActive)


        # MODO version checks.
        # Modo 13.0 and up have UV Seam map.
        # Version below 13.0 haven't
        Modo_ver = int(lx.eval('query platformservice appversion ?'))
        lx.out('Modo Version:', Modo_ver)


        Int_UVProjAxe = self.dyna_Int(0)
        Int_Similar = self.dyna_Int(1)


        # ------------- ARGUMENTS ------------- #
        args = lx.args()
        lx.out(args)

        # Axe X = 0
        # Axe Y = 1
        # Axe Z = 2
        # Selection Aligned = 3
        UVProjAxe = Int_UVProjAxe
        lx.out('Desired Axe change:', UVProjAxe)

        # Current Selection = 0
        # Current Selection Similar Touching = 1
        # Current Selection Similar Object = 2
        # Current Selection Similar Layer = 3
        Similar = Int_Similar
        lx.out('Similar state:', Similar)
        # ------------- ARGUMENTS ------------- #

        # Auto Update UV Seam map   Off = 0
        # Auto Update UV Seam map   On = 1
        AutoUpdateUVSeamCutMapState = lx.eval('user.value SMO_UseVal_UV_AutoUpdateUVSeamCutMapState ?')
        lx.out('Auto Update UV Seam Cut Map state:', AutoUpdateUVSeamCutMapState)

        # Repack Off = 0
        # Repack On = 1
        RePack = lx.eval('user.value SMO_UseVal_UV_RepackAfterUnwrap ?')
        lx.out('Auto RePack state:', RePack)

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

        # ------------- ARGUMENTS Test
        # UVProjAxe = 1
        # Similar = 0
        # ------------- ARGUMENTS ------------- #


        # ------------------------------ #
        # <----( DEFINE VARIABLES )----> #
        # ------------------------------ #
        # ---------------- Define user value for all the different SafetyCheck --- START
        #####
        lx.eval("user.defNew name:SMO_SafetyCheck_UVUnwrapPlanar_VertexModeEnabled type:integer life:momentary")
        lx.eval("user.defNew name:SMO_SafetyCheck_UVUnwrapPlanar_EdgeModeEnabled type:integer life:momentary")
        lx.eval("user.defNew name:SMO_SafetyCheck_UVUnwrapPlanar_PolygonModeEnabled type:integer life:momentary")
        lx.eval("user.defNew name:SMO_SafetyCheck_UVUnwrapPlanar_min1PolygonSelected type:integer life:momentary")
        ## Selected UVmap Count
        lx.eval("user.defNew name:SMO_SafetyCheck_UVUnwrapPlanar_UVMapCount type:boolean life:momentary")
        ## Selected UVmap Name
        lx.eval("user.defNew name:UVUnwrapPlanar_UVMapName type:string life:momentary")
        #####
        # ---------------- Define user value for all the different SafetyCheck --- END

        # Deselect all other VertexMaps other than UV Maps
        lx.eval('smo.GC.ClearSelectionVmap 2 1')
        lx.eval('smo.GC.ClearSelectionVmap 3 1')
        lx.eval('smo.GC.ClearSelectionVmap 4 1')
        lx.eval('smo.GC.ClearSelectionVmap 5 1')
        lx.eval('smo.GC.ClearSelectionVmap 6 1')
        lx.eval('smo.GC.ClearSelectionVmap 7 1')
        lx.eval('smo.GC.ClearSelectionVmap 8 1')

        # ----------------------------------------- #
        # <---( SAFETY CHECK 1 )---> UVMap Selected #
        # ----------------------------------------- #

        ###
        lx.out('<------------- START -------------->')
        lx.out('<--- UV Map Safety Check --->')
        ###
        # Create a UV Map automatically in case there is no UVMaps
        DefaultUVMapName = lx.eval('pref.value application.defaultTexture ?')
        # print(DefaultUVMapName)

        m = modo.Mesh()
        # print(m.name)
        maps = m.geometry.vmaps.getMapsByType([lx.symbol.i_VMAP_TEXTUREUV])  # same as m.geometry.vmaps.uvMaps
        # print(maps)
        # print(len(maps))

        # if len(maps) == 0:
        #     lx.eval('vertMap.new {%s} txuv' % DefaultUVMapName)
        #     print('New UVMap created')
        #     print('UV map name is: %s' % DefaultUVMapName)
        #
        # if len(maps) == 1:
        #     lx.eval('select.vertexMap {%s} txuv replace' % maps[0].name)
        #
        # if len(maps) > 1:
        #     # get the current select UV Map name
        #     print(lx.eval('vertMap.list type:txuv ?'))

        # Update Maps List
        maps = m.geometry.vmaps.getMapsByType([lx.symbol.i_VMAP_TEXTUREUV])  # same as m.geometry.vmaps.uvMaps

        SelectedMeshUVMapsCount = len(maps)
        UVUnwrapPlanar_UVMapName = lx.eval('vertMap.list type:txuv ?')
        lx.out('Selected Mesh UV Maps Name:', UVUnwrapPlanar_UVMapName)

        lx.eval('smo.GC.ClearSelectionVmap 1 1')
        lx.eval("select.vertexMap {%s} txuv replace" % UVUnwrapPlanar_UVMapName)

        SMO_SafetyCheck_UVUnwrapPlanar_UVMapCount = True
        if SelectedMeshUVMapsCount > 1:
            lx.eval('dialog.setup info')
            lx.eval('dialog.title {SMONSTER - UV - Unwrap Planar:}')
            lx.eval('dialog.msg {Please select Only One Vertex Map and run that script again.}')
            lx.eval('dialog.open')
            SMO_SafetyCheck_UVUnwrapPlanar_UVMapCount = False
            sys.exit()

        if SelectedMeshUVMapsCount < 1:
            lx.eval('dialog.setup info')
            lx.eval('dialog.title {SMONSTER - UV - Unwrap Planar:}')
            lx.eval('dialog.msg {You must have a UV map selected to run this script.}')
            lx.eval('dialog.open')
            SMO_SafetyCheck_UVUnwrapPlanar_UVMapCount = False
            sys.exit()

        if SelectedMeshUVMapsCount == 1 :
            SMO_SafetyCheck_UVUnwrapPlanar_UVMapCount = True

        # UserUVMapName = lx.eval1('query layerservice vmap.name ? %s' % UVmap_Selected)
        # lx.out('USER UV Map Name:', UserUVMapName)
        ###
        lx.out('<- UV Map Safety Check ->')
        lx.out('<------------- END -------------->')
        ###
        ###############################################

        # -------------------------- #
        # <---( SAFETY CHECK 2 )---> #
        # -------------------------- #

        # --------------------  safety check 1 : Only One Item Selected --- START
        try:
            # test if there is actually an item layer selected
            meshseam = modo.Scene().selected[0]
            mesh = scene.selectedByType('mesh')[0]
            # if this command return an error then i will select the corresponding mesh layer on the next step.
        except:
            # -------------------------- #
            # <---( SAFETY CHECK 3 )---> #
            # -------------------------- #

            # Polygon or Edge Selection Mode enabled --- START

            selType = ""
            # Used to query layerservice for the list of polygons, edges or vertices.
            attrType = ""

            if lx.eval1("select.typeFrom typelist:vertex;polygon;edge;item;ptag ?"):
                selType = "vertex"
                attrType = "vert"

                SMO_SafetyCheck_UVUnwrapPlanar_PolygonModeEnabled = 0
                SMO_SafetyCheck_UVUnwrapPlanar_EdgeModeEnabled = 0
                SMO_SafetyCheck_UVUnwrapPlanar_VertexModeEnabled = 1
                lx.eval('dialog.setup info')
                lx.eval('dialog.title {SMONSTER - UV - Unwrap Planar:}')
                lx.eval('dialog.msg {You must be in Polygon or Edge Mode to run that script}')
                lx.eval('+dialog.open')
                lx.out('script Stopped: You must be in Polygon or Edge Mode to run that script')
                sys.exit
                # sys.exit( "LXe_FAILED:Must be in polygon selection mode." )


            elif lx.eval1("select.typeFrom typelist:edge;vertex;polygon;item ?"):
                selType = "edge"
                attrType = "edge"

                SMO_SafetyCheck_UVUnwrapPlanar_VertexModeEnabled = 0
                SMO_SafetyCheck_UVUnwrapPlanar_EdgeModeEnabled = 1
                SMO_SafetyCheck_UVUnwrapPlanar_PolygonModeEnabled = 0
                SelectByLoop = 0
                lx.out('script Running: Edge Component Selection Mode')

            elif lx.eval1("select.typeFrom typelist:polygon;vertex;edge;item ?"):
                selType = "polygon"
                attrType = "poly"

                SMO_SafetyCheck_UVUnwrapPlanar_VertexModeEnabled = 0
                SMO_SafetyCheck_UVUnwrapPlanar_EdgeModeEnabled = 0
                SMO_SafetyCheck_UVUnwrapPlanar_PolygonModeEnabled = 1
                lx.out('script Running: Polygon Component Selection Mode')


            else:
                # This only fails if none of the three supported selection
                # modes have yet been used since the program started, or
                # if "item" or "ptag" (ie: materials) is the current
                # selection mode.
                SMO_SafetyCheck_UVUnwrapPlanar_VertexModeEnabled = 0
                SMO_SafetyCheck_UVUnwrapPlanar_EdgeModeEnabled = 0
                SMO_SafetyCheck_UVUnwrapPlanar_PolygonModeEnabled = 0
                lx.eval('dialog.setup info')
                lx.eval('dialog.title {SMONSTER - UV - Unwrap Planar:}')
                lx.eval('dialog.msg {You must be in Polygon Mode to run that script}')
                lx.eval('+dialog.open')
                lx.out('script Stopped: You must be in Polygon Mode to run that script')
                sys.exit
                # sys.exit( "LXe_FAILED:Must be in polygon selection mode." )
            # Polygon or Edge Selection Mode enabled --- END

            ItemLayerName = lx.eval('query layerservice layer.name ? 1')
            lx.out('Item Layer name is:', ItemLayerName)
            ItemLayerID = lx.eval('query layerservice layer.ID ?')
            lx.out('Item Layer ID is:', ItemLayerID)
            lx.eval('select.type item')
            lx.eval('select.item %s add' % ItemLayerID)
            if SMO_SafetyCheck_UVUnwrapPlanar_EdgeModeEnabled == 1:
                lx.eval('select.type edge')
            elif SMO_SafetyCheck_UVUnwrapPlanar_PolygonModeEnabled == 1:
                lx.eval('select.type polygon')
            mesh = scene.selectedByType('mesh')[0]
            meshseam = modo.Scene().selected[0]

        ItemCount = lx.eval('query layerservice layer.N ? selected')
        lx.out('ItemCount', ItemCount)

        if ItemCount != 1:
            SMO_SafetyCheck_Only1MeshItemSelected = 0
            lx.eval('dialog.setup info')
            lx.eval('dialog.title {SMONSTER - UV - Unwrap Planar:}')
            lx.eval(
                'dialog.msg {You must select the Mesh Item layer you are working on, in Item List, to run that script}')
            lx.eval('+dialog.open')
            lx.out('Only One Item Selected result:', SMO_SafetyCheck_Only1MeshItemSelected)
            lx.out('script Stopped: Select only one Mesh Item')
            sys.exit()

        elif ItemCount == 1:
            SMO_SafetyCheck_Only1MeshItemSelected = 1
            lx.out('Only One Item Selected:', SMO_SafetyCheck_Only1MeshItemSelected)
            lx.out('script running: right amount of Mesh Item selected')
        # --------------------  safety check 2 : Only One Item Selected --- END

        CsPolys = len(mesh.geometry.polygons.selected)
        if CsPolys == 0:
            lx.eval('select.type polygon')
            lx.eval('select.all')

        CsPolys = len(mesh.geometry.polygons.selected)
        SelItems = (lx.evalN('query sceneservice selection ? locator'))
        lx.out('Selected items is:', SelItems)

        # # ------------- UV SEAM Map Detection

        # #Define the UV Seam vmap name Search case.
        # lx.eval("user.defNew name:UnwrapPlanar_DesiredUVSEAMmapName type:string life:momentary")
        # UnwrapPlanar_DesiredUVSEAMmapName = 'UV Seam'

        # #Define the UV Seam vmap name Search case.
        # lx.eval("user.defNew name:UnwrapPlanar_NoUVSeamMap type:string life:momentary")
        # UnwrapPlanar_NoUVSeamMap = '_____n_o_n_e_____'

        # Get the number of UV Seam map available on mesh
        # DetectedUVSEAMmapCount = len(lx.evalN('vertMap.list seam ?'))
        # lx.out('UV SEAM Map Count:', DetectedUVSEAMmapCount)

        # Get the name of UV Seam map available on mesh
        # DetectedUVSEAMmapName = lx.eval('vertMap.list seam ?')
        # lx.out('UV SEAM Map Name:', DetectedUVSEAMmapName)
        # # ------------- UV SEAM Map Detection

        # #####
        # ---------------- Define user value for all the different SafetyCheck --- END

        # if Modo_ver >= 1300 :
        # ## UVSEAM Map Selection Check ##
        # lx.out('<--- UVSEAM Map Safety Check --->')
        # lx.out('<---------- START ---------->')
        # if DetectedUVSEAMmapName == UnwrapPlanar_NoUVSeamMap:
        # lx.eval('vertMap.list seam ?')
        # lx.eval('vertMap.list seam _____n_e_w_____')
        # lx.eval('vertMap.new "UV Seam" seam true {0.78 0.78 0.78} 2.0')
        # lx.eval('vertMap.list seam "UV Seam"')

        # elif DetectedUVSEAMmapName == UnwrapPlanar_DesiredUVSEAMmapName:
        # lx.out('UV Map and UVSEAM Map Selected')
        # lx.eval('vertMap.list seam "UV Seam"')
        # UserUVSEAMmapName = lx.eval1('query layerservice vmap.name ? %s' %UVSEAM_Selected)
        # lx.out('USER UVSEAM Map Name:', UserUVSEAMmapName)

        # lx.out('<----------- END ----------->')
        # ------------------------------ #

        # -------------------------- #
        # <---( SAFETY CHECK 2 )---> #
        # -------------------------- #

        # at Least 1 Polygons is selected --- START
        lx.out('Count Selected Poly', CsPolys)

        if CsPolys < 1:
            SMO_SafetyCheck_UVUnwrapPlanar_min1PolygonSelected = 0
            lx.eval('dialog.setup info')
            lx.eval('dialog.title {SMONSTER - UV - Unwrap Planar:}')
            lx.eval('dialog.msg {You must select at least 1 polygon to run that script}')
            lx.eval('+dialog.open')
            lx.out('script Stopped: Add more polygons to your selection')

        elif CsPolys >= 1:
            SMO_SafetyCheck_UVUnwrapPlanar_min1PolygonSelected = 1
            lx.out('script running: right amount of polygons in selection')
        # at Least 1 Polygons is selected --- END

        # -------------------------- #
        # <---( SAFETY CHECK 2 )---> #
        # -------------------------- #

        # Polygon or Edge Selection Mode enabled --- START

        selType = ""
        # Used to query layerservice for the list of polygons, edges or vertices.
        attrType = ""

        if lx.eval1("select.typeFrom typelist:vertex;polygon;edge;item;ptag ?"):
            selType = "vertex"
            attrType = "vert"

            SMO_SafetyCheck_UVUnwrapPlanar_PolygonModeEnabled = 0
            SMO_SafetyCheck_UVUnwrapPlanar_EdgeModeEnabled = 0
            SMO_SafetyCheck_UVUnwrapPlanar_VertexModeEnabled = 1
            lx.eval('dialog.setup info')
            lx.eval('dialog.title {Unwrap_Smart:}')
            lx.eval('dialog.msg {You must be in Polygon or Edge Mode to run that script}')
            lx.eval('+dialog.open')
            lx.out('script Stopped: You must be in Polygon or Edge Mode to run that script')
            sys.exit
            # sys.exit( "LXe_FAILED:Must be in polygon selection mode." )


        elif lx.eval1("select.typeFrom typelist:edge;vertex;polygon;item ?"):
            selType = "edge"
            attrType = "edge"

            SMO_SafetyCheck_UVUnwrapPlanar_VertexModeEnabled = 0
            SMO_SafetyCheck_UVUnwrapPlanar_EdgeModeEnabled = 1
            SMO_SafetyCheck_UVUnwrapPlanar_PolygonModeEnabled = 0
            SelectByLoop = 0
            lx.out('script Running: Edge Component Selection Mode')

        elif lx.eval1("select.typeFrom typelist:polygon;vertex;edge;item ?"):
            selType = "polygon"
            attrType = "poly"

            SMO_SafetyCheck_UVUnwrapPlanar_VertexModeEnabled = 0
            SMO_SafetyCheck_UVUnwrapPlanar_EdgeModeEnabled = 0
            SMO_SafetyCheck_UVUnwrapPlanar_PolygonModeEnabled = 1
            lx.out('script Running: Polygon Component Selection Mode')



        else:
            # This only fails if none of the three supported selection
            # modes have yet been used since the program started, or
            # if "item" or "ptag" (ie: materials) is the current
            # selection mode.
            SMO_SafetyCheck_UVUnwrapPlanar_VertexModeEnabled = 0
            SMO_SafetyCheck_UVUnwrapPlanar_EdgeModeEnabled = 0
            SMO_SafetyCheck_UVUnwrapPlanar_PolygonModeEnabled = 0
            lx.eval('dialog.setup info')
            lx.eval('dialog.title {Unwrap_Smart:}')
            lx.eval('dialog.msg {You must be in Polygon Mode to run that script}')
            lx.eval('+dialog.open')
            lx.out('script Stopped: You must be in Polygon Mode to run that script')
            sys.exit
            # sys.exit( "LXe_FAILED:Must be in polygon selection mode." )
        # Polygon or Edge Selection Mode enabled --- END

        # ---------------- Define current value for the Prerequisite TotalSafetyCheck --- START
        #####
        TotalSafetyCheckTrueValue = 3
        lx.out('Desired Value', TotalSafetyCheckTrueValue)
        TotalSafetyCheck = (
                    SMO_SafetyCheck_Only1MeshItemSelected + SMO_SafetyCheck_UVUnwrapPlanar_PolygonModeEnabled + SMO_SafetyCheck_UVUnwrapPlanar_min1PolygonSelected)
        lx.out('Current Value', TotalSafetyCheck)
        #####
        # ---------------- Define current value for the Prerequisite TotalSafetyCheck --- END

        # BugFix Selection Facing ratio value = flat 2 degree
        LazySelectUserValue = 2

        # -------------------------- #
        # <----( Main Macro : )----> #
        # -------------------------- #
        if SMO_SafetyCheck_UVUnwrapPlanar_UVMapCount:
            # ---------------- Compare TotalSafetyCheck value and decide or not to continue the process  --- START
            if TotalSafetyCheck == TotalSafetyCheckTrueValue:
                lx.eval('select.type item')
                lx.eval('item.refSystem %s' % SelItems[0])
                lx.eval('select.type polygon')
                if Similar == 1:
                    # LazySelectUserValue = lx.eval('user.value sene_LS_facingRatio ?')
                    # lx.out('Lazy Select Value:', LazySelectUserValue)
                    # lx.eval('user.value sene_LS_facingRatio 2')
                    # lx.eval('@lazySelect.pl selectTouching 2')
                    lx.eval('smo.GC.SelectCoPlanarPoly 0 2 0')
                    # lx.eval('user.value sene_LS_facingRatio {%s}' % LazySelectUserValue)
                if Similar == 2:
                    # LazySelectUserValue = lx.eval('user.value sene_LS_facingRatio ?')
                    # lx.out('Lazy Select Value:', LazySelectUserValue)
                    # lx.eval('user.value sene_LS_facingRatio 2')
                    # lx.eval('@lazySelect.pl selectOnObject')
                    lx.eval('smo.GC.SelectCoPlanarPoly 1 2 1000')
                    # lx.eval('user.value sene_LS_facingRatio {%s}' % LazySelectUserValue)
                if Similar == 3:
                    # LazySelectUserValue = lx.eval('user.value sene_LS_facingRatio ?')
                    # lx.out('Lazy Select Value:', LazySelectUserValue)
                    # lx.eval('user.value sene_LS_facingRatio 2')
                    # lx.eval('@lazySelect.pl selectAll')
                    lx.eval('smo.GC.SelectCoPlanarPoly 2 2 1000')
                    # lx.eval('user.value sene_LS_facingRatio {%s}' % LazySelectUserValue)
                if AutoExpandSel:
                    lx.eval('select.expand')
                # replay name:"Edit Selection Set"
                lx.eval('select.editSet name:UV_DONE mode:add')

                if UVProjAxe == 0:
                    lx.eval('select.editSet name:UV_DONE_X mode:add')

                if UVProjAxe == 1:
                    lx.eval('select.editSet name:UV_DONE_Y mode:add')

                if UVProjAxe == 2:
                    lx.eval('select.editSet name:UV_DONE_Z mode:add')

                if UVProjAxe == 3:
                    lx.eval('select.editSet name:UV_DONE_FREE mode:add')
                    lx.eval('workPlane.fitSelect')
                    lx.eval('tool.set actr.origin on')

                # Isolate selection
                lx.eval('hide.unsel')

                lx.eval('tool.set preset:"uv.create" mode:on')
                lx.eval('tool.setAttr uv.create proj planar')
                # lx.eval('tool.setAttr tool:"uv.create" attr:proj value:planar')
                lx.eval('tool.setAttr tool:"uv.create" attr:mode value:manual')
                # Important Set the UV Map to work on by Name
                lx.eval('tool.setAttr tool:"uv.create" attr:newmap value:false')
                lx.eval('tool.setAttr uv.create name %s' % UVUnwrapPlanar_UVMapName)

                ## Do a Projection on specific axis via Arguments
                # Command Block Begin:
                if UVProjAxe == 0:
                    lx.eval('tool.setAttr uv.create axis 0')
                if UVProjAxe == 1:
                    lx.eval('tool.setAttr uv.create axis 1')
                if UVProjAxe == 2:
                    lx.eval('tool.setAttr uv.create axis 2')
                if UVProjAxe == 3:
                    lx.eval('tool.setAttr uv.create axis 1')

                try:
                    lx.eval('tool.setAttr tool:"uv.create" attr:sizX value:"0.1"')
                    lx.eval('tool.setAttr tool:"uv.create" attr:sizY value:"0.1"')
                    lx.eval('tool.setAttr tool:"uv.create" attr:sizZ value:"0.1"')
                    lx.eval('tool.setAttr tool:"uv.create" attr:cenX value:"0.0"')
                    lx.eval('tool.setAttr tool:"uv.create" attr:cenY value:"0.0"')
                    lx.eval('tool.setAttr tool:"uv.create" attr:cenZ value:"0.0"')

                except:
                    sys.exit
                # Command Block End:
                lx.eval('tool.doapply')
                lx.eval('tool.set preset:"uv.create" mode:off')

                # Selection Aligned = 3
                if UVProjAxe == 3:
                    lx.eval('tool.set actr.origin off')
                    lx.eval('workPlane.reset')

                lx.eval('tool.viewType uv')

                # FixFlipped UVs Passes --> Start
                if FixFlip:
                    lx.eval('select.drop polygon')
                    lx.eval('smo.UV.FixFlipped 0')
                    lx.eval('select.drop polygon')
                # FixFlipped UVs Passes --> End

                # replay name:"Fit UVs"
                lx.eval('uv.fit entire gapsByPixel:8.0 udim:1001')

                if RelocateInArea:
                    # replay name:"Move"
                    lx.eval('tool.set preset:TransformMove mode:on')

                    # BLALBALBLA
                    try:
                        ## Do a Projection on specific axis via Arguments
                        if UVProjAxe == 0 and RelocateInArea == True:
                            # Command Block Begin:
                            lx.eval('tool.setAttr tool:"xfrm.transform" attr:U value:"-2.0"')
                            lx.eval('tool.setAttr tool:"xfrm.transform" attr:V value:"-0.0"')
                            # Command Block End:
                        if UVProjAxe == 1 and RelocateInArea == True:
                            # Command Block Begin:
                            lx.eval('tool.setAttr tool:"xfrm.transform" attr:U value:"-1.0"')
                            lx.eval('tool.setAttr tool:"xfrm.transform" attr:V value:"0.0"')
                            # Command Block End:
                        if UVProjAxe == 2 and RelocateInArea == True:
                            # Command Block Begin:
                            lx.eval('tool.setAttr tool:"xfrm.transform" attr:U value:"-1.0"')
                            lx.eval('tool.setAttr tool:"xfrm.transform" attr:V value:"1.0"')
                            # Command Block End:
                        if UVProjAxe == 3 and RelocateInArea == True:
                            # Command Block Begin:
                            lx.eval('tool.setAttr tool:"xfrm.transform" attr:U value:"-2.0"')
                            lx.eval('tool.setAttr tool:"xfrm.transform" attr:V value:"1.0"')
                            # Command Block End:
                        # if RelocateInArea == False :
                        #     # Command Block Begin:
                        #     lx.eval('tool.setAttr tool:"xfrm.transform" attr:U value:"0.0"')
                        #     lx.eval('tool.setAttr tool:"xfrm.transform" attr:V value:"0.0"')
                        #     # Command Block End:
                    except:
                        sys.exit

                    # Launch the Move
                    lx.eval('tool.doapply')
                    lx.eval('tool.set preset:TransformMove mode:off')

                # if Modo_ver >= 1300:
                # lx.eval ('select.all')
                # lx.eval ('uv.selectBorder')
                # lx.eval ('seam.add')
                # lx.eval ('select.drop edge')
                # lx.eval ('select.type polygon')
                # lx.eval ('select.drop polygon')

                lx.eval('unhide')
                if RePack:
                    if UVProjAxe == 0 and RelocateInArea:
                        lx.eval('smo.UV.SelectUVArea -2 0')
                        lx.eval('hide.unsel')
                        lx.eval('smo.UV.NormalizePackByArea 0 0 -2 0')
                        lx.eval('unhide')

                    if UVProjAxe == 1 and RelocateInArea:
                        lx.eval('smo.UV.SelectUVArea -1 0')
                        lx.eval('hide.unsel')
                        lx.eval('smo.UV.NormalizePackByArea 0 0 -1 0')
                        lx.eval('unhide')

                    if UVProjAxe == 2 and RelocateInArea:
                        lx.eval('smo.UV.SelectUVArea -1 1')
                        lx.eval('hide.unsel')
                        lx.eval('smo.UV.NormalizePackByArea 0 0 -1 1')
                        lx.eval('unhide')

                    if UVProjAxe == 3 and RelocateInArea:
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

                AutoHideState = lx.eval('user.value SMO_UseVal_UV_HideAfterUnwrap ?')
                if AutoHideState:
                    lx.eval('select.useSet UV_DONE select')
                    lx.eval('hide.sel')

                lx.eval('select.type item')
                lx.eval('item.refSystem {}')
                lx.eval('select.type polygon')

            if not RefSystemActive:
                lx.eval('item.refSystem {}')
            if RefSystemActive:
                lx.eval('item.refSystem %s' % CurrentRefSystemItem)


        elif TotalSafetyCheck != TotalSafetyCheckTrueValue:
            lx.out('script Stopped: your mesh does not match the requirement for that script.')
            sys.exit

        lx.out('End of Unwrap Planar Script')
        # ---------------- Compare TotalSafetyCheck value and decide or not to continue the process  --- END


lx.bless(SMO_UV_UnwrapPlanar_Cmd, Cmd_Name)

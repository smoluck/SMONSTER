# python
"""
Name:         SMO_UV_UnwrapSmart_Cmd.py

Purpose:      This script is designed to
              Unwrap the current Polygon Selection or via a set of Edges
              with various Unwrap Method, Rectangle Mode and Autoloop function using Arguments.

Author:       Franck ELISABETH
Website:      https://www.linkedin.com/in/smoluck/
Created:      28/12/2018
Copyright:    (c) Franck Elisabeth 2017-2022
"""

import lx
import lxu
import modo
import sys

Cmd_Name = "smo.UV.UnwrapSmart"
# smo.UV.UnwrapSmart 0 0 0 0


class SMO_UV_UnwrapSmart_Cmd(lxu.command.BasicCommand):
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
        return 'SMO UV - Unwrap Smart'

    def cmd_Desc(self):
        return 'MULTI - Unwrap the current Polygon Selection or via a set of Edges with various Unwrap Method, Rectangle Mode and Autoloop function using Arguments.'

    def cmd_Tooltip(self):
        return 'MULTI - Unwrap the current Polygon Selection or via a set of Edges with various Unwrap Method, Rectangle Mode and Autoloop function using Arguments.'

    def cmd_Help(self):
        return 'https://twitter.com/sm0luck'

    def basic_ButtonName(self):
        return 'SMO UV - Unwrap Smart'

    def basic_Enable(self, msg):
        return True

    def basic_Execute(self, msg, flags):
        scene = modo.scene.current()

        # Force to select the current Mesh Item if it is not selected in the Item List
        lx.eval('smo.MASTER.ForceSelectMeshItemOnly')
        lx.eval('smo.UV.AutoCreateUVMap')

        mesh = scene.selectedByType('mesh')[0]
        # meshes = scene.selectedByType('mesh')

        # MODO version checks.
        # Modo 13.0 and up have UV Seam map.
        # Version below 13.0 haven't
        Modo_ver = int(lx.eval('query platformservice appversion ?'))
        # lx.out('Modo Version:', Modo_ver)

        US_UnwrapMethod = self.dyna_Int(0)
        US_InitProjection = self.dyna_Int(1)
        US_IsRectangle = self.dyna_Int(2)
        US_SelectByLoop = self.dyna_Int(3)

        # ------------- ARGUMENT ------------- #
        args = lx.args()
        lx.out(args)

        # Conformal= 0
        # Angle Based = 1
        UnwrapMethod = US_UnwrapMethod
        lx.out('Desired Unwrap Method:', UnwrapMethod)

        # Planar = 0
        # Group Normal = 1
        InitProjection = US_InitProjection
        lx.out('Initial Projection Mode:', InitProjection)

        # Current Selection is not Rectangle = 0
        # Current Selection is Rectangle = 1
        IsRectangle = US_IsRectangle
        lx.out('Rectangle Post pass:', IsRectangle)

        # Current Selection = 0
        # current selection + Add loop = 1
        SelectByLoop = US_SelectByLoop
        lx.out('Select by loop state:', SelectByLoop)
        # ------------- ARGUMENTS ------------- #

        # Auto Update UV Seam map   Off = 0
        # Auto Update UV Seam map   On = 1
        AutoUpdateUVSeamCutMapState = lx.eval('user.value SMO_UseVal_UV_AutoUpdateUVSeamCutMapState ?')
        lx.out('Auto Update UV Seam Cut Map state:', AutoUpdateUVSeamCutMapState)

        # Repack Off = 0
        # Repack On = 1
        RePack = lx.eval('user.value SMO_UseVal_UV_RepackAfterUnwrap ?')
        lx.out('RePack state:', RePack)

        # Relax UV Off = 0
        # Relax UV On = 1
        RelaxUV = lx.eval('user.value SMO_UseVal_UV_RelaxPostProcess ?')
        lx.out('RelaxUV state:', RelaxUV)

        UVRelaxIterCount = lx.eval('user.value SMO_UseVal_UV_RelaxIterCount ?')
        lx.out('RelaxUV iteration count:', UVRelaxIterCount)

        # Relocate in Area = 0
        # Relocate in Area = 1
        RelocateInArea = lx.eval('user.value SMO_UseVal_UV_RelocateInArea ?')
        lx.out('Relocate In Area state:', RelocateInArea)

        AutoExpandSel = lx.eval('user.value SMO_UseVal_UV_AutoExpandSelectionState ?')
        lx.out('Auto Expand Selection state:', AutoExpandSel)

        # ------------- ARGUMENTS Test
        # UnwrapMethod = 0          --> Conformal
        # InitProjection = 1        --> Group Normal
        # IsRectangle = 0
        # SelectByLoop = 0
        # ------------- ARGUMENTS ------------- #

        # ------------------------------ #
        # <----( DEFINE VARIABLES )----> #
        # ------------------------------ #
        # ---------------- Define user value for all the different SafetyCheck --- START
        #####
        lx.eval("user.defNew name:SMO_SafetyCheck_UVUnwrapSmart_PolygonModeEnabled type:integer life:momentary")
        lx.eval("user.defNew name:SMO_SafetyCheck_UVUnwrapSmart_min1PolygonSelected type:integer life:momentary")

        lx.eval("user.defNew name:SMO_SafetyCheck_UVUnwrapSmart_EdgeModeEnabled type:integer life:momentary")
        lx.eval("user.defNew name:SMO_SafetyCheck_UVUnwrapSmart_min3EdgeSelected type:integer life:momentary")

        lx.eval("user.defNew name:TotalSafetyCheckPolygon type:integer life:momentary")
        lx.eval("user.defNew name:TotalSafetyCheckEdge type:integer life:momentary")

        ## Selected UVmap Count
        lx.eval("user.defNew name:SMO_SafetyCheck_UVUnwrapSmart_UVMapCount type:boolean life:momentary")
        ## Selected UVmap Name
        lx.eval("user.defNew name:UVUnwrapSmart_UVMapName type:string life:momentary")
        #####
        # ---------------- Define user value for all the different SafetyCheck --- END

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
        lx.out('<------------- START -------------->')
        lx.out('<--- UV Map Safety Check --->')

        # Get info about the selected UVMap.
        lx.eval('smo.UV.GetUVMapCountName 0 1 1')
        SelectedMeshUVMapsCount = lx.eval('user.value SMO_UV_SelectedMeshUVmapCount ?')
        lx.out('Selected Mesh UV Maps Count:', SelectedMeshUVMapsCount)
        UVUnwrapSmart_UVMapName = lx.eval('user.value SMO_UV_SelectedMeshUVmapName ?')
        lx.out('Selected Mesh UV Maps Name:', UVUnwrapSmart_UVMapName)

        lx.eval('smo.GC.ClearSelectionVmap 1 1')
        lx.eval('select.vertexMap %s txuv replace' % UVUnwrapSmart_UVMapName)

        SMO_SafetyCheck_UVUnwrapSmart_UVMapCount = True
        if SelectedMeshUVMapsCount > 1:
            lx.eval('dialog.setup info')
            lx.eval('dialog.title {SMONSTER - UV - Unwrap Smart:}')
            lx.eval('dialog.msg {Please select Only One Vertex Map and run that script again.}')
            lx.eval('dialog.open')
            SMO_SafetyCheck_UVUnwrapSmart_UVMapCount = False
            sys.exit()

        if SelectedMeshUVMapsCount < 1:
            lx.eval('dialog.setup info')
            lx.eval('dialog.title {SMONSTER - UV - Unwrap Smart:}')
            lx.eval('dialog.msg {You must have a UV map selected to run this script.}')
            lx.eval('dialog.open')
            SMO_SafetyCheck_UVUnwrapSmart_UVMapCount = False
            sys.exit()

        if SelectedMeshUVMapsCount == 1:
            SMO_SafetyCheck_UVUnwrapSmart_UVMapCount = True


        # UserUVMapName = lx.eval1('query layerservice vmap.name ? %s' % UVmap_Selected)
        # lx.out('USER UV Map Name:', UserUVMapName)
        lx.out('<- UV Map Safety Check ->')
        lx.out('<------------- END -------------->')
        ###############################################

        # -------------------------- #
        # <---( SAFETY CHECK 1 )---> #
        # -------------------------- #

        # --------------------  safety check 1 : Only One Item Selected --- START
        try:
            # test if there is actually an item layer selected
            mesh = scene.selectedByType('mesh')[0]
            meshseam = modo.Scene().selected[0]
            # if this command return an error then i will select the corresponding mesh layer on the next step.
        except:
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

                SMO_SafetyCheck_UVUnwrapSmart_PolygonModeEnabled = 0
                SMO_SafetyCheck_UVUnwrapSmart_EdgeModeEnabled = 0
                SMO_SafetyCheck_UVUnwrapSmart_VertexModeEnabled = 1
                lx.eval('dialog.setup info')
                lx.eval('dialog.title {SMONSTER - UV - Unwrap Smart:}')
                lx.eval('dialog.msg {You must be in Polygon or Edge Mode to run that script}')
                lx.eval('+dialog.open')
                lx.out('script Stopped: You must be in Polygon or Edge Mode to run that script')
                sys.exit
                # sys.exit( "LXe_FAILED:Must be in polygon selection mode." )


            elif lx.eval1("select.typeFrom typelist:edge;vertex;polygon;item ?"):
                selType = "edge"
                attrType = "edge"

                SMO_SafetyCheck_UVUnwrapSmart_VertexModeEnabled = 0
                SMO_SafetyCheck_UVUnwrapSmart_EdgeModeEnabled = 1
                SMO_SafetyCheck_UVUnwrapSmart_PolygonModeEnabled = 0
                SelectByLoop = 0
                lx.out('script Running: Edge Component Selection Mode')

            elif lx.eval1("select.typeFrom typelist:polygon;vertex;edge;item ?"):
                selType = "polygon"
                attrType = "poly"

                SMO_SafetyCheck_UVUnwrapSmart_VertexModeEnabled = 0
                SMO_SafetyCheck_UVUnwrapSmart_EdgeModeEnabled = 0
                SMO_SafetyCheck_UVUnwrapSmart_PolygonModeEnabled = 1
                lx.out('script Running: Polygon Component Selection Mode')


            else:
                # This only fails if none of the three supported selection
                # modes have yet been used since the program started, or
                # if "item" or "ptag" (ie: materials) is the current
                # selection mode.
                SMO_SafetyCheck_UVUnwrapSmart_VertexModeEnabled = 0
                SMO_SafetyCheck_UVUnwrapSmart_EdgeModeEnabled = 0
                SMO_SafetyCheck_UVUnwrapSmart_PolygonModeEnabled = 0
                lx.eval('dialog.setup info')
                lx.eval('dialog.title {SMONSTER - UV - Unwrap Smart:}')
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
            if SMO_SafetyCheck_UVUnwrapSmart_EdgeModeEnabled == 1:
                lx.eval('select.type edge')
            elif SMO_SafetyCheck_UVUnwrapSmart_PolygonModeEnabled == 1:
                lx.eval('select.type polygon')
            mesh = scene.selectedByType('mesh')[0]
            meshseam = modo.Scene().selected[0]

        ItemCount = lx.eval('query layerservice layer.N ? selected')
        lx.out('ItemCount', ItemCount)

        if ItemCount != 1:
            SMO_SafetyCheck_Only1MeshItemSelected = 0
            lx.eval('dialog.setup info')
            lx.eval('dialog.title {SMONSTER - UV - Unwrap Smart:}')
            lx.eval(
                'dialog.msg {You must select the Mesh Item layer you are working on, in Item List, to run that script}')
            lx.eval('+dialog.open')
            lx.out('Only One Item Selected result:', SMO_SafetyCheck_Only1MeshItemSelected)
            lx.out('script Stopped: Select only one Mesh Item')
            sys.exit

        elif ItemCount == 1:
            SMO_SafetyCheck_Only1MeshItemSelected = 1
            lx.out('Only One Item Selected:', SMO_SafetyCheck_Only1MeshItemSelected)
            lx.out('script running: right amount of Mesh Item selected')
        # --------------------  safety check 1 : Only One Item Selected --- END

        CsPolys = len(mesh.geometry.polygons.selected)
        CsEdges = len(mesh.geometry.edges.selected)

        # # ------------- UV SEAM Map Detection

        # #Define the UV Seam vmap name Search case.
        # lx.eval("user.defNew name:UVUnwrapSmart_DesiredUVSEAMmapName type:string life:momentary")
        # UVUnwrapSmart_DesiredUVSEAMmapName = 'UV Seam'

        # #Define the UV Seam vmap name Search case.
        # lx.eval("user.defNew name:UVUnwrapSmart_NoUVSeamMap type:string life:momentary")
        # UVUnwrapSmart_NoUVSeamMap = '_____n_o_n_e_____'

        # Get the number of UV Seam map available on mesh
        # DetectedUVSEAMmapCount = len(lx.evalN('vertMap.list seam ?'))
        # lx.out('UV SEAM Map Count:', DetectedUVSEAMmapCount)

        # Get the name of UV Seam map available on mesh
        # DetectedUVSEAMmapName = lx.eval('vertMap.list seam ?')
        # lx.out('UV SEAM Map Name:', DetectedUVSEAMmapName)
        # # ------------- UV SEAM Map Detection

        # #####
        # ---------------- Define user value for all the different SafetyCheck --- END

        # if Modo_ver >= 1300:
        # ## UVSEAM Map Selection Check ##
        # lx.out('<--- UVSEAM Map Safety Check --->')
        # lx.out('<---------- START ---------->')
        # if DetectedUVSEAMmapName == UVUnwrapSmart_NoUVSeamMap:
        # lx.eval('vertMap.list seam ?')
        # lx.eval('vertMap.list seam _____n_e_w_____')
        # lx.eval('vertMap.new "UV Seam" seam true {0.78 0.78 0.78} 2.0')
        # lx.eval('vertMap.list seam "UV Seam"')

        # elif DetectedUVSEAMmapName == UVUnwrapSmart_DesiredUVSEAMmapName:
        # lx.out('UV Map and UVSEAM Map Selected')
        # lx.eval('vertMap.list seam "UV Seam"')
        # UserUVSEAMmapName = lx.eval1('query layerservice vmap.name ? %s' %UVSEAM_Selected)
        # lx.out('USER UVSEAM Map Name:', UserUVSEAMmapName)

        # lx.out('<----------- END ----------->')
        # ------------------------------ #

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

            SMO_SafetyCheck_UVUnwrapSmart_PolygonModeEnabled = 0
            SMO_SafetyCheck_UVUnwrapSmart_EdgeModeEnabled = 0
            SMO_SafetyCheck_UVUnwrapSmart_VertexModeEnabled = 1
            lx.eval('dialog.setup info')
            lx.eval('dialog.title {SMONSTER - UV - Unwrap Smart:}')
            lx.eval('dialog.msg {You must be in Polygon or Edge Mode to run that script}')
            lx.eval('+dialog.open')
            lx.out('script Stopped: You must be in Polygon or Edge Mode to run that script')
            sys.exit
            # sys.exit( "LXe_FAILED:Must be in polygon selection mode." )


        elif lx.eval1("select.typeFrom typelist:edge;vertex;polygon;item ?"):
            selType = "edge"
            attrType = "edge"

            SMO_SafetyCheck_UVUnwrapSmart_VertexModeEnabled = 0
            SMO_SafetyCheck_UVUnwrapSmart_EdgeModeEnabled = 1
            SMO_SafetyCheck_UVUnwrapSmart_PolygonModeEnabled = 0
            SelectByLoop = 0
            lx.out('script Running: Edge Component Selection Mode')

        elif lx.eval1("select.typeFrom typelist:polygon;vertex;edge;item ?"):
            selType = "polygon"
            attrType = "poly"

            SMO_SafetyCheck_UVUnwrapSmart_VertexModeEnabled = 0
            SMO_SafetyCheck_UVUnwrapSmart_EdgeModeEnabled = 0
            SMO_SafetyCheck_UVUnwrapSmart_PolygonModeEnabled = 1
            lx.out('script Running: Polygon Component Selection Mode')



        else:
            # This only fails if none of the three supported selection
            # modes have yet been used since the program started, or
            # if "item" or "ptag" (ie: materials) is the current
            # selection mode.
            SMO_SafetyCheck_UVUnwrapSmart_VertexModeEnabled = 0
            SMO_SafetyCheck_UVUnwrapSmart_EdgeModeEnabled = 0
            SMO_SafetyCheck_UVUnwrapSmart_PolygonModeEnabled = 0
            lx.eval('dialog.setup info')
            lx.eval('dialog.title {SMONSTER - UV - Unwrap Smart:}')
            lx.eval('dialog.msg {You must be in Polygon Mode to run that script}')
            lx.eval('+dialog.open')
            lx.out('script Stopped: You must be in Polygon Mode to run that script')
            sys.exit
            # sys.exit( "LXe_FAILED:Must be in polygon selection mode." )
        # Polygon or Edge Selection Mode enabled --- END

        # -------------------------- #
        # <---( SAFETY CHECK 3 )---> #
        # -------------------------- #

        # at Least 1 Polygons is selected --- START
        if SMO_SafetyCheck_UVUnwrapSmart_PolygonModeEnabled == 1 and SMO_SafetyCheck_UVUnwrapSmart_EdgeModeEnabled == 0:
            lx.out('Count Selected Poly', CsPolys)

            if CsPolys < 1:
                SMO_SafetyCheck_UVUnwrapSmart_min1PolygonSelected = 0
                SMO_SafetyCheck_UVUnwrapSmart_min3EdgeSelected = 0
                lx.eval('dialog.setup info')
                lx.eval('dialog.title {SMONSTER - UV - Unwrap Smart:}')
                lx.eval('dialog.msg {You must select at least 1 Polygon or 3 Edges to run that script}')
                lx.eval('+dialog.open')
                lx.out('script Stopped: Add more Polygons to your selection')
                sys.exit

            elif CsPolys >= 1:
                SMO_SafetyCheck_UVUnwrapSmart_min1PolygonSelected = 1
                SMO_SafetyCheck_UVUnwrapSmart_min3EdgeSelected = 0
                lx.out('script running: right amount of polygons in selection')
        # at Least 1 Polygons is selected --- END

        # at Least 3 Edges are selected --- START
        if SMO_SafetyCheck_UVUnwrapSmart_EdgeModeEnabled == 1 and SMO_SafetyCheck_UVUnwrapSmart_PolygonModeEnabled == 0:
            lx.out('Count Selected Edges', CsEdges)

            if CsEdges <= 2:
                SMO_SafetyCheck_UVUnwrapSmart_min1PolygonSelected = 0
                SMO_SafetyCheck_UVUnwrapSmart_min3EdgeSelected = 0
                lx.eval('dialog.setup info')
                lx.eval('dialog.title {SMONSTER - UV - Unwrap Smart:}')
                lx.eval('dialog.msg {You must select at least 1 Polygon or 3 Edges to run that script}')
                lx.eval('+dialog.open')
                lx.out('script Stopped: Add more Edges to your selection')
                sys.exit

            elif CsEdges >= 3:
                SMO_SafetyCheck_UVUnwrapSmart_min1PolygonSelected = 0
                SMO_SafetyCheck_UVUnwrapSmart_min3EdgeSelected = 1
                lx.out('script running: right amount of Edges in selection')
        # at Least 3 Edges are selected --- END

        # ---------------- Define current value for the Prerequisite TotalSafetyCheck --- START
        #####
        TotalSafetyCheckTrueValuePoly = 3
        lx.out('Desired Value for Polygon Mode', TotalSafetyCheckTrueValuePoly)

        TotalSafetyCheckTrueValueEdge = 7
        lx.out('Desired Value for Edge Mode', TotalSafetyCheckTrueValueEdge)

        TotalSafetyCheckPolygon = (
                    SMO_SafetyCheck_Only1MeshItemSelected + SMO_SafetyCheck_UVUnwrapSmart_PolygonModeEnabled + SMO_SafetyCheck_UVUnwrapSmart_min1PolygonSelected)
        lx.out('Current Polygon Check Value', TotalSafetyCheckPolygon)

        TotalSafetyCheckEdge = (
                    SMO_SafetyCheck_Only1MeshItemSelected + SMO_SafetyCheck_UVUnwrapSmart_EdgeModeEnabled + SMO_SafetyCheck_UVUnwrapSmart_min3EdgeSelected + 4)
        lx.out('Current Edge Check Value', TotalSafetyCheckEdge)

        #####
        # ---------------- Define current value for the Prerequisite TotalSafetyCheck --- END

        ###############################################
        # <----( Main Macro for Polygon Mode )----> #
        ###############################################
        if SMO_SafetyCheck_UVUnwrapSmart_UVMapCount:
            AutoHideState = lx.eval('user.value SMO_UseVal_UV_HideAfterUnwrap ?')
            # ---------------- Compare TotalSafetyCheck value and decide or not to continue the process  --- START
            if TotalSafetyCheckPolygon == TotalSafetyCheckTrueValuePoly:
                if SelectByLoop == 1:
                    # replay name:"Edit Selection Set"
                    lx.eval('select.editSet name:UV_Selection mode:add')
                    lx.eval('select.convert edge')
                    lx.eval('select.editSet name:UV_AllEdgeSel mode:add')
                    lx.eval('select.type polygon')
                    lx.eval('script.run "macro.scriptservice:92663570022:macro"')
                    lx.eval('select.editSet name:UV_BoundEdgeSel mode:add')
                    lx.eval('select.useSet UV_AllEdgeSel select')
                    lx.eval('select.useSet UV_BoundEdgeSel deselect')
                    lx.eval('select.editSet name:UV_CutEdgeSel mode:add')
                    lx.eval('select.type polygon')
                    lx.eval('select.loop')

                    if AutoExpandSel:
                        lx.eval('select.expand')

                # if AutoExpandSel == True and SelectByLoop == 0:
                #     lx.eval('select.editSet name:UV_Selection mode:add')
                #     lx.eval('select.convert edge')
                #     lx.eval('select.editSet name:UV_AllEdgeSel mode:add')
                #     lx.eval('select.type polygon')
                #     lx.eval('script.run "macro.scriptservice:92663570022:macro"')
                #     lx.eval('select.editSet name:UV_BoundEdgeSel mode:add')
                #     lx.eval('select.useSet UV_AllEdgeSel select')
                #     lx.eval('select.useSet UV_BoundEdgeSel deselect')
                #     lx.eval('select.editSet name:UV_CutEdgeSel mode:add')
                #     lx.eval('select.type polygon')
                #     lx.eval('select.expand')
                #     lx.eval('hide.unsel')
                #     lx.eval('select.drop polygon')
                #     lx.eval('select.useSet UV_Selection select')
                #     lx.eval('select.expand')

                if AutoExpandSel and SelectByLoop == 0 and IsRectangle == 1:
                    lx.eval('select.editSet name:UV_Selection mode:add')
                    lx.eval('select.convert edge')
                    lx.eval('select.editSet name:UV_AllEdgeSel mode:add')
                    lx.eval('select.type polygon')
                    lx.eval('script.run "macro.scriptservice:92663570022:macro"')
                    lx.eval('select.editSet name:UV_BoundEdgeSel mode:add')
                    lx.eval('select.useSet UV_AllEdgeSel select')
                    lx.eval('select.useSet UV_BoundEdgeSel deselect')
                    lx.eval('select.editSet name:UV_CutEdgeSel mode:add')
                    lx.eval('select.type polygon')
                    lx.eval('hide.unsel')
                    lx.eval('select.type edge')
                    lx.eval('select.ring')
                    lx.eval('select.editSet name:UV_Ring mode:add')
                    lx.eval('select.useSet UV_CutEdgeSel deselect')
                    lx.eval('select.editSet name:UV_RingExtremity mode:add')
                    lx.eval('select.type polygon')
                    lx.eval('unhide')
                    lx.eval('select.expand')
                    lx.eval('hide.unsel')
                    lx.eval('select.drop polygon')
                    lx.eval('select.type edge')
                    lx.eval('select.useSet UV_BoundEdgeSel select')
                    lx.eval('select.useSet UV_RingExtremity deselect')
                    lx.eval('select.ring')
                    lx.eval('select.convert polygon')
                    lx.eval('select.editSet name:UV_DONE mode:add')
                    lx.eval('hide.unsel')

                if AutoExpandSel and SelectByLoop == 0 and IsRectangle == 0:
                    lx.eval('select.expand')

                # Isolate selection
                lx.eval('hide.unsel')

                #######################################
                # Tag Selection Set Poly for UV Done
                if SelectByLoop == 1 and AutoExpandSel:
                    lx.eval('select.type edge')
                    lx.eval('select.loop')
                    lx.eval('select.editSet name:UV_CutEdgeSel mode:add')
                    lx.eval('select.type polygon')
                    lx.eval('select.editSet name:UV_DONE mode:add')

                if not AutoExpandSel:
                    lx.eval('select.editSet name:UV_DONE mode:add')

                if AutoExpandSel and SelectByLoop == 0 and IsRectangle == 0:
                    lx.eval('select.editSet name:UV_DONE mode:add')
                #######################################

                if SelectByLoop == 1:
                    lx.eval('select.drop polygon')
                    lx.eval('select.type edge')
                    lx.eval('script.run "macro.scriptservice:92663570022:macro"')
                    lx.eval('select.useSet UV_CutEdgeSel select')

                lx.eval('tool.set uv.unwrap on')

                ## Do a Projection on specific axis via Arguments
                # Command Block Begin:
                lx.eval('tool.attr uv.unwrap seam select')

                if UnwrapMethod == 0:
                    lx.eval('tool.attr uv.unwrap mode lscm')
                if UnwrapMethod == 1:
                    lx.eval('tool.attr uv.unwrap mode abf')
                if InitProjection == 0:
                    lx.eval('tool.attr uv.unwrap project planar')
                if InitProjection == 1:
                    lx.eval('tool.attr uv.unwrap project normal')
                if IsRectangle == 1 and SelectByLoop == 1:
                    lx.eval('tool.attr uv.unwrap mode abf')
                    lx.eval('tool.attr uv.unwrap project normal')

                lx.eval('tool.setAttr uv.unwrap iter 99')
                # Command Block End:

                lx.eval('tool.doapply')
                lx.eval('tool.set uv.unwrap off')

                lx.eval('tool.viewType uv')

                # Relax Passes --> Start
                if RelaxUV:
                    lx.eval('select.type polygon')
                    lx.eval('select.all')
                    if IsRectangle == 1 and SelectByLoop == 1:
                        lx.eval('select.type edge')
                    lx.eval('smo.UV.Relax %s' % UVRelaxIterCount)
                # Relax Passes --> End

                if IsRectangle == 1 and SelectByLoop == 1:
                    lx.eval('uv.split')
                    lx.eval('select.type polygon')
                    lx.eval('!uv.rectangle false')

                lx.eval('tool.viewType uv')

                if IsRectangle == 1 and SelectByLoop == 0:
                    lx.eval('select.all')
                    lx.eval('!uv.rectangle false')

                lx.eval('uv.orient horizontal')

                # replay name:"Fit UVs"
                lx.eval('uv.fit entire gapsByPixel:8.0 udim:1001')

                RelocateInArea = lx.eval('user.value SMO_UseVal_UV_RelocateInArea ?')
                print('Relocate In Area state:', RelocateInArea)
                lx.out('Relocate In Area state:', RelocateInArea)

                if RelocateInArea:
                    # replay name:"Move"
                    lx.eval('tool.set preset:TransformMove mode:on')

                    ## Move UVs on Right Side depending on the Method used
                    if UnwrapMethod == 0:
                        # Command Block Begin:
                        lx.eval('tool.setAttr tool:"xfrm.transform" attr:U value:"0.0"')
                        lx.eval('tool.setAttr tool:"xfrm.transform" attr:V value:"-1.0"')
                        # Command Block End:
                    if UnwrapMethod == 1:
                        # Command Block Begin:
                        lx.eval('tool.setAttr tool:"xfrm.transform" attr:U value:"1.0"')
                        lx.eval('tool.setAttr tool:"xfrm.transform" attr:V value:"-1.0"')
                        # Command Block End:
                    if IsRectangle == 1:
                        # Command Block Begin:
                        lx.eval('tool.setAttr tool:"xfrm.transform" attr:U value:"0.0"')
                        lx.eval('tool.setAttr tool:"xfrm.transform" attr:V value:"-2.0"')
                        # Command Block End:
                    ## Move UVs on Right Side depending on the Method used

                    # Launch the Move
                    lx.eval('tool.doapply')
                    lx.eval('tool.set preset:TransformMove mode:off')

                if SelectByLoop == 1:
                    # replay name:"Edit Selection Set"
                    lx.eval('!select.deleteSet UV_Selection false')
                    lx.eval('select.type edge')
                    lx.eval('!select.deleteSet UV_AllEdgeSel false')
                    lx.eval('!select.deleteSet UV_BoundEdgeSel false')
                    lx.eval('!select.deleteSet UV_CutEdgeSel false')
                    lx.eval('select.type polygon')

                if AutoExpandSel and SelectByLoop == 0 and IsRectangle == 1:
                    lx.eval('!select.deleteSet UV_Selection false')
                    lx.eval('select.type edge')
                    lx.eval('!select.deleteSet UV_AllEdgeSel false')
                    lx.eval('!select.deleteSet UV_AllEdgeSel false')
                    lx.eval('!select.deleteSet UV_BoundEdgeSel false')
                    lx.eval('!select.deleteSet UV_CutEdgeSel false')
                    lx.eval('!select.deleteSet UV_Ring false')
                    lx.eval('!select.deleteSet UV_RingExtremity false')
                    lx.eval('select.type polygon')

                # ## 2022_04_07 Bug with Unhide that can't be recorded as undoable.
                # lx.eval('tool.viewType xyz')
                # lx.eval('unhide')
                # lx.eval('tool.viewType uv')

                lx.eval('unhide')

                lx.eval('select.drop polygon')
                if RePack:
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

                if AutoHideState:
                    lx.eval('select.useSet UV_DONE select')
                    lx.eval('hide.sel')

            ###############################################
            # <----( Main Macro for Edge Mode )----> #
            ###############################################

            # ---------------- Compare TotalSafetyCheck value and decide or not to continue the process  --- START
            if TotalSafetyCheckEdge == TotalSafetyCheckTrueValueEdge:
                lx.eval('select.type polygon')
                lx.eval('select.all')
                lx.eval('select.editSet name:UV_DONE mode:add')
                lx.eval('select.drop polygon')
                lx.eval('select.type edge')

                lx.eval('tool.set uv.unwrap on')

                ## Do a Projection on specific axis via Arguments
                # Command Block Begin:
                lx.eval('tool.attr uv.unwrap seam select')

                if UnwrapMethod == 0:
                    lx.eval('tool.attr uv.unwrap mode lscm')
                if UnwrapMethod == 1:
                    lx.eval('tool.attr uv.unwrap mode abf')
                if InitProjection == 0:
                    lx.eval('tool.attr uv.unwrap project planar')
                if InitProjection == 1:
                    lx.eval('tool.attr uv.unwrap project normal')
                if IsRectangle == 1:
                    lx.eval('tool.attr uv.unwrap mode abf')
                    lx.eval('tool.attr uv.unwrap project normal')

                lx.eval('tool.setAttr uv.unwrap iter 99')
                # Command Block End:

                lx.eval('tool.doapply')
                lx.eval('tool.set uv.unwrap off')

                lx.eval('tool.viewType uv')

                lx.eval('select.type polygon')
                lx.eval('select.all')

                # Relax Passes --> Start
                if RelaxUV:
                    lx.eval('smo.UV.Relax %s' % UVRelaxIterCount)
                # Relax Passes --> End

                if IsRectangle == 1:
                    lx.eval('select.all')
                    lx.eval('!uv.rectangle false')

                lx.eval('select.all')
                lx.eval('uv.orient horizontal')

                # replay name:"Fit UVs"
                lx.eval('uv.fit entire gapsByPixel:8.0 udim:1001')

                RelocateInArea = lx.eval('user.value SMO_UseVal_UV_RelocateInArea ?')
                print('Relocate In Area state:', RelocateInArea)

                if RelocateInArea:
                    # replay name:"Move"
                    lx.eval('tool.set preset:TransformMove mode:on')

                    ## Move UVs on Right Side depending on the Method used
                    if UnwrapMethod == 0:
                        # Command Block Begin:
                        lx.eval('tool.setAttr tool:"xfrm.transform" attr:U value:"0.0"')
                        lx.eval('tool.setAttr tool:"xfrm.transform" attr:V value:"-1.0"')
                        # Command Block End:
                    if UnwrapMethod == 1:
                        # Command Block Begin:
                        lx.eval('tool.setAttr tool:"xfrm.transform" attr:U value:"1.0"')
                        lx.eval('tool.setAttr tool:"xfrm.transform" attr:V value:"-1.0"')
                        # Command Block End:
                    if IsRectangle == 1:
                        # Command Block Begin:
                        lx.eval('tool.setAttr tool:"xfrm.transform" attr:U value:"0.0"')
                        lx.eval('tool.setAttr tool:"xfrm.transform" attr:V value:"-2.0"')
                        # Command Block End:
                    ## Move UVs on Right Side depending on the Method used

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

                # ## 2022_04_07 Bug with Unhide that can't be recorded as undoable.
                # lx.eval('tool.viewType xyz')
                # lx.eval('unhide')
                # lx.eval('tool.viewType uv')

                lx.eval('unhide')

                lx.eval('select.drop polygon')
                if RePack:
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

                if AutoHideState:
                    lx.eval('select.useSet UV_DONE select')
                    lx.eval('hide.sel')

                lx.eval('select.type edge')
                lx.eval('select.drop edge')

        if SMO_SafetyCheck_UVUnwrapSmart_PolygonModeEnabled == 1 and SMO_SafetyCheck_UVUnwrapSmart_EdgeModeEnabled == 0:
            if TotalSafetyCheckPolygon != TotalSafetyCheckTrueValuePoly:
                lx.out('script Stopped: your mesh does not match the requirement for that script.')
                sys.exit

        if SMO_SafetyCheck_UVUnwrapSmart_PolygonModeEnabled == 0 and SMO_SafetyCheck_UVUnwrapSmart_EdgeModeEnabled == 1:
            if TotalSafetyCheckEdge != TotalSafetyCheckTrueValueEdge:
                lx.out('script Stopped: your mesh does not match the requirement for that script.')
                sys.exit

        # ---------------- Compare TotalSafetyCheck value and decide or not to continue the process  --- END


lx.bless(SMO_UV_UnwrapSmart_Cmd, Cmd_Name)

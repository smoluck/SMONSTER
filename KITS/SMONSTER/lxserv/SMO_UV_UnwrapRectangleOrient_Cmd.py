# python
"""
Name:         SMO_UV_UnwrapRectangleOrient_Cmd.py

Purpose:      This script is designed to
              Unwrap the current Polygon Selection using Rectangle method
              and Orient the UV Island on defined direction (Via Arguments).

Author:       Franck ELISABETH
Website:      https://www.smoluck.com
Created:      01/07/2018
Copyright:    (c) Franck Elisabeth 2017-2022
"""

import lx
import lxu
import modo
import sys

Cmd_Name = "smo.UV.UnwrapRectangleOrient"
# smo.UV.UnwrapRectangleOrient 0


class SMO_UV_UnwrapRectangleOrient_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
        self.dyna_Add("Orient Direction", lx.symbol.sTYPE_INTEGER)
        self.basic_SetFlags(0, lx.symbol.fCMDARG_OPTIONAL)  # here the (0) define the argument index.

    def cmd_Flags(self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO

    def cmd_Interact(self):
        pass

    def cmd_UserName(self):
        return 'SMO UV - Unwrap Rectangle and Orient'

    def cmd_Desc(self):
        return 'Unwrap the current Polygon Selection using Rectangle method and Orient the UV Island on defined direction (Via Arguments).'

    def cmd_Tooltip(self):
        return 'Unwrap the current Polygon Selection using Rectangle method and Orient the UV Island on defined direction (Via Arguments).'

    def cmd_Help(self):
        return 'https://twitter.com/sm0luck'

    def basic_ButtonName(self):
        return 'SMO UV - Unwrap Rectangle and Orient'

    def basic_Enable(self, msg):
        return True

    def basic_Execute(self, msg, flags):
        scene = modo.scene.current()

        # Force to select the current Mesh Item if it is not selected in the Item List
        lx.eval('smo.MASTER.ForceSelectMeshItemOnly')
        lx.eval('smo.UV.AutoCreateUVMap')

        meshes = scene.selectedByType('mesh')

        # MODO version checks.
        # Modo 13.0 and up have UV Seam map.
        # Version below 13.0 haven't
        Modo_ver = int(lx.eval('query platformservice appversion ?'))
        lx.out('Modo Version:', Modo_ver)

        Int_OrientDir = self.dyna_Int(0)

        # ------------- ARGUMENTS ------------- #
        args = lx.args()
        lx.out(args)
        # Orient U = 0
        # Orient V = 1
        OrientDir = Int_OrientDir
        lx.out('Orient Direction:', OrientDir)
        # ------------- ARGUMENTS ------------- #

        # Auto Update UV Seam map   Off = 0
        # Auto Update UV Seam map   On = 1
        AutoUpdateUVSeamCutMapState = lx.eval('user.value SMO_UseVal_UV_AutoUpdateUVSeamCutMapState ?')
        lx.out('Auto Update UV Seam Cut Map state:', AutoUpdateUVSeamCutMapState)

        # Repack Off = 0
        # Repack On = 1
        RePack = lx.eval('user.value SMO_UseVal_UV_RepackAfterUnwrap ?')
        lx.out('RePack state:', RePack)

        # Relocate in Area = 0
        # Relocate in Area = 1
        RelocateInArea = lx.eval('user.value SMO_UseVal_UV_RelocateInArea ?')
        lx.out('Relocate In Area state:', RelocateInArea)

        # ------------- ARGUMENTS Test
        # Orient_Dir = 0
        # ------------- ARGUMENT ------------- #

        # ------------------------------ #
        # <----( DEFINE VARIABLES )----> #
        # ------------------------------ #
        # ---------------- Define user value for all the different SafetyCheck --- START
        #####
        lx.eval("user.defNew name:SMO_SafetyCheck_UVUnwrapRectOri_VertexModeEnabled type:integer life:momentary")
        lx.eval("user.defNew name:SMO_SafetyCheck_UVUnwrapRectOri_EdgeModeEnabled type:integer life:momentary")
        lx.eval("user.defNew name:SMO_SafetyCheck_UVUnwrapRectOri_PolygonModeEnabled type:integer life:momentary")
        lx.eval("user.defNew name:SMO_SafetyCheck_UVUnwrapRectOri_min1PolygonSelected type:integer life:momentary")
        ## UVmap Selected Count
        lx.eval("user.defNew name:SMO_SafetyCheck_UVUnwrapRectOri_UVMapCount type:boolean life:momentary")
        #####
        # ---------------- Define user value for all the different SafetyCheck --- END

        lx.eval('smo.GC.ClearSelectionVmap 3 1')
        lx.eval('smo.GC.ClearSelectionVmap 4 1')
        lx.eval('smo.GC.ClearSelectionVmap 5 1')
        lx.eval('smo.GC.ClearSelectionVmap 6 1')
        lx.eval('smo.GC.ClearSelectionVmap 7 1')

        # ----------------------------------------- #
        # <---( SAFETY CHECK 1 )---> UVMap Selected #
        # ----------------------------------------- #
        lx.out('<------------- START -------------->')
        lx.out('<--- UV Map Safety Check --->')

        # Get info about the selected UVMap.         UVMapsCount = len(item.geometry.vmaps.uvMaps)
        lx.eval('smo.UV.GetUVMapCountName 0 1 1')
        SelectedMeshUVMapsCount = lx.eval('user.value SMO_UV_SelectedMeshUVmapCount ?')
        lx.out('Selected Mesh UV Maps Count:', SelectedMeshUVMapsCount)
        SelectedMeshUVMapsName = lx.eval('user.value SMO_UV_SelectedMeshUVmapName ?')
        lx.out('Selected Mesh UV Maps Name:', SelectedMeshUVMapsName)

        if SelectedMeshUVMapsCount > 1:
            lx.eval('dialog.setup info')
            lx.eval('dialog.title {SMONSTER - UV - Rectangle and Orient:}')
            lx.eval('dialog.msg {Please select Only One Vertex Map and run that script again.}')
            lx.eval('dialog.open')
            SMO_SafetyCheck_UVUnwrapRectOri_UVMapCount = False
            sys.exit()

        if SelectedMeshUVMapsCount < 1:
            lx.eval('dialog.setup info')
            lx.eval('dialog.title {SMONSTER - UV - Rectangle and Orient:}')
            lx.eval('dialog.msg {You must have a UV map selected to run this script.}')
            lx.eval('dialog.open')
            SMO_SafetyCheck_UVUnwrapRectOri_UVMapCount = False
            sys.exit()

        if SelectedMeshUVMapsCount == 1:
            SMO_SafetyCheck_UVUnwrapRectOri_UVMapCount = True

        # UserUVMapName = lx.eval1('query layerservice vmap.name ? %s' % UVmap_Selected)
        # lx.out('USER UV Map Name:', UserUVMapName)
        lx.out('<- UV Map Safety Check ->')
        lx.out('<------------- END -------------->')
        ###############################################

        # -------------------------- #
        # <---( SAFETY CHECK 2 )---> #
        # -------------------------- #

        # --------------------  safety check 2 : Only One Item Selected --- START
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

                SMO_SafetyCheckUVUnwrapSmart_PolygonModeEnabled = 0
                SMO_SafetyCheckUVUnwrapSmart_EdgeModeEnabled = 0
                SMO_SafetyCheckUVUnwrapSmart_VertexModeEnabled = 1
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

                SMO_SafetyCheckUVUnwrapSmart_VertexModeEnabled = 0
                SMO_SafetyCheckUVUnwrapSmart_EdgeModeEnabled = 1
                SMO_SafetyCheckUVUnwrapSmart_PolygonModeEnabled = 0
                SelectByLoop = 0
                lx.out('script Running: Edge Component Selection Mode')

            elif lx.eval1("select.typeFrom typelist:polygon;vertex;edge;item ?"):
                selType = "polygon"
                attrType = "poly"

                SMO_SafetyCheckUVUnwrapSmart_VertexModeEnabled = 0
                SMO_SafetyCheckUVUnwrapSmart_EdgeModeEnabled = 0
                SMO_SafetyCheckUVUnwrapSmart_PolygonModeEnabled = 1
                lx.out('script Running: Polygon Component Selection Mode')


            else:
                # This only fails if none of the three supported selection
                # modes have yet been used since the program started, or
                # if "item" or "ptag" (ie: materials) is the current
                # selection mode.
                SMO_SafetyCheckUVUnwrapSmart_VertexModeEnabled = 0
                SMO_SafetyCheckUVUnwrapSmart_EdgeModeEnabled = 0
                SMO_SafetyCheckUVUnwrapSmart_PolygonModeEnabled = 0
                lx.eval('dialog.setup info')
                lx.eval('dialog.title {Unwrap_Smart:}')
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
            if SMO_SafetyCheckUVUnwrapSmart_EdgeModeEnabled == 1:
                lx.eval('select.type edge')
            elif SMO_SafetyCheckUVUnwrapSmart_PolygonModeEnabled == 1:
                lx.eval('select.type polygon')
            mesh = scene.selectedByType('mesh')[0]
            meshseam = modo.Scene().selected[0]

        ItemCount = lx.eval('query layerservice layer.N ? selected')
        lx.out('ItemCount', ItemCount)

        if ItemCount != 1:
            SMO_SafetyCheck_UVUnwrapRectOri_Only1MeshItemSelected = 0
            lx.eval('dialog.setup info')
            lx.eval('dialog.title {SMO Smart Unwrap:}')
            lx.eval(
                'dialog.msg {You must select the Mesh Item layer you are working on, in Item List, to run that script}')
            lx.eval('+dialog.open')
            lx.out('Only One Item Selected result:', SMO_SafetyCheck_UVUnwrapRectOri_Only1MeshItemSelected)
            lx.out('script Stopped: Select only one Mesh Item')
            sys.exit

        elif ItemCount == 1:
            SMO_SafetyCheck_UVUnwrapRectOri_Only1MeshItemSelected = 1
            lx.out('Only One Item Selected:', SMO_SafetyCheck_UVUnwrapRectOri_Only1MeshItemSelected)
            lx.out('script running: right amount of Mesh Item selected')
        # --------------------  safety check 2 : Only One Item Selected --- END

        CsPolys = len(mesh.geometry.polygons.selected)
        SelItems = (lx.evalN('query sceneservice selection ? locator'))
        lx.out('Selected items is:', SelItems)

        # # ------------- UV SEAM Map Detection

        # #Define the UV Seam vmap name Search case.
        # lx.eval("user.defNew name:UnwrapRectOri_DesiredUVSEAMmapName type:string life:momentary")
        # UnwrapRectOri_DesiredUVSEAMmapName = 'UV Seam'

        # #Define the UV Seam vmap name Search case.
        # lx.eval("user.defNew name:UnwrapRectOri_NoUVSeamMap type:string life:momentary")
        # UnwrapRectOri_NoUVSeamMap = '_____n_o_n_e_____'

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
        # if DetectedUVSEAMmapName == UnwrapRectOri_NoUVSeamMap:
        # lx.eval('vertMap.list seam ?')
        # lx.eval('vertMap.list seam _____n_e_w_____')
        # lx.eval('vertMap.new "UV Seam" seam true {0.78 0.78 0.78} 2.0')
        # lx.eval('vertMap.list seam "UV Seam"')

        # elif DetectedUVSEAMmapName == UnwrapRectOri_DesiredUVSEAMmapName:
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
            SMO_SafetyCheck_UVUnwrapRectOri_min1PolygonSelected = 0
            lx.eval('dialog.setup info')
            lx.eval('dialog.title {Unwrap Planar:}')
            lx.eval('dialog.msg {You must select at least 1 polygon to run that script}')
            lx.eval('+dialog.open')
            lx.out('script Stopped: Add more polygons to your selection')
            sys.exit

        elif CsPolys >= 1:
            SMO_SafetyCheck_UVUnwrapRectOri_min1PolygonSelected = 1
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

            SMO_SafetyCheckUVUnwrapSmart_PolygonModeEnabled = 0
            SMO_SafetyCheckUVUnwrapSmart_EdgeModeEnabled = 0
            SMO_SafetyCheckUVUnwrapSmart_VertexModeEnabled = 1
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

            SMO_SafetyCheckUVUnwrapSmart_VertexModeEnabled = 0
            SMO_SafetyCheckUVUnwrapSmart_EdgeModeEnabled = 1
            SMO_SafetyCheckUVUnwrapSmart_PolygonModeEnabled = 0
            SelectByLoop = 0
            lx.out('script Running: Edge Component Selection Mode')

        elif lx.eval1("select.typeFrom typelist:polygon;vertex;edge;item ?"):
            selType = "polygon"
            attrType = "poly"

            SMO_SafetyCheckUVUnwrapSmart_VertexModeEnabled = 0
            SMO_SafetyCheckUVUnwrapSmart_EdgeModeEnabled = 0
            SMO_SafetyCheckUVUnwrapSmart_PolygonModeEnabled = 1
            lx.out('script Running: Polygon Component Selection Mode')



        else:
            # This only fails if none of the three supported selection
            # modes have yet been used since the program started, or
            # if "item" or "ptag" (ie: materials) is the current
            # selection mode.
            SMO_SafetyCheckUVUnwrapSmart_VertexModeEnabled = 0
            SMO_SafetyCheckUVUnwrapSmart_EdgeModeEnabled = 0
            SMO_SafetyCheckUVUnwrapSmart_PolygonModeEnabled = 0
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
                    SMO_SafetyCheck_UVUnwrapRectOri_Only1MeshItemSelected + SMO_SafetyCheckUVUnwrapSmart_PolygonModeEnabled + SMO_SafetyCheck_UVUnwrapRectOri_min1PolygonSelected)
        lx.out('Current Value', TotalSafetyCheck)
        #####
        # ---------------- Define current value for the Prerequisite TotalSafetyCheck --- END

        # -------------------------- #
        # <----( Main Macro : )----> #
        # -------------------------- #

        if SMO_SafetyCheck_UVUnwrapRectOri_UVMapCount:
            # ---------------- Compare TotalSafetyCheck value and decide or not to continue the process  --- START
            if TotalSafetyCheck == TotalSafetyCheckTrueValue:

                # Tag the UV as Done
                lx.eval('select.editSet name:UV_DONE mode:add')

                lx.eval('tool.set preset:"uv.unwrap" mode:on')
                lx.eval('tool.apply')
                lx.eval('tool.doapply')
                lx.eval('select.nextMode')
                # replay name:"Normalize Texel Density"
                # lx.eval('texeldensity.normalize')
                lx.eval('!uv.rectangle false 0.2 false false')
                if OrientDir == 0:
                    lx.eval('uv.orient horizontal')
                if OrientDir == 1:
                    lx.eval('uv.orient perpendicular')

                # lx.eval('texeldensity.set per:island mode:all')

                lx.eval('tool.viewType uv')

                # Fit UVs
                if OrientDir == 0 and RePack == False and RelocateInArea == True:
                    lx.eval('uv.fit entire gapsByPixel:8.0 udim:1002')
                if OrientDir == 0 and RePack == True and RelocateInArea == True:
                    lx.eval('uv.fit entire gapsByPixel:8.0 udim:1002')
                    lx.eval('smo.UV.NormalizePackByArea 0 0 1 0')

                if OrientDir == 1 and RePack == False and RelocateInArea == True:
                    lx.eval('uv.fit entire gapsByPixel:8.0 udim:1012')
                if OrientDir == 1 and RePack == True and RelocateInArea == True:
                    lx.eval('uv.fit entire gapsByPixel:8.0 udim:1012')
                    lx.eval('smo.UV.NormalizePackByArea 0 0 1 1')

                if RePack == False and RelocateInArea == False:
                    lx.eval('uv.fit entire gapsByPixel:8.0 udim:1001')

                if RePack == True and RelocateInArea == False:
                    lx.eval('uv.fit entire gapsByPixel:8.0 udim:1001')
                    lx.eval('unhide')
                    lx.eval('smo.UV.SelectUVArea 0 0')
                    lx.eval('hide.unsel')
                    lx.eval('smo.UV.NormalizePackByArea 0 0 0 0')

                if AutoUpdateUVSeamCutMapState == True and Modo_ver >= 1300:
                    lx.eval('smo.UV.UpdateUVSeamCutMap')
                    lx.eval('view3d.showUVSeam true active')

                AutoHideState = lx.eval('user.value SMO_UseVal_UV_HideAfterUnwrap ?')
                if AutoHideState:
                    lx.eval('select.useSet UV_DONE select')
                    lx.eval('hide.sel')



            elif TotalSafetyCheck != TotalSafetyCheckTrueValue:
                lx.out('script Stopped: your mesh does not match the requirement for that script.')
                sys.exit

            lx.out('End of Unwrap Planar Script')
            # ---------------- Compare TotalSafetyCheck value and decide or not to continue the process  --- END


lx.bless(SMO_UV_UnwrapRectangleOrient_Cmd, Cmd_Name)

# python
"""
Name:         SMO_UV_UnwrapCylindrical_Cmd.py

Purpose:      This script is designed to
              Unwrap the current Polygon Selection
              using Cylindrical Mode on Defined Axis.

Author:       Franck ELISABETH
Website:      https://www.smoluck.com
Created:      28/12/2018
Copyright:    (c) Franck Elisabeth 2017-2022
"""

import lx
import lxu
import modo
import sys

Cmd_Name = "smo.UV.UnwrapCylindrical"
# smo.UV.UnwrapCylindrical 2 0 0


class SMO_UV_UnwrapCylindrical_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
        self.dyna_Add("UV Projection Axis", lx.symbol.sTYPE_INTEGER)
        self.basic_SetFlags(0, lx.symbol.fCMDARG_OPTIONAL)  # here the (0) define the argument index.
        self.dyna_Add("Rectangle Mode", lx.symbol.sTYPE_INTEGER)
        self.basic_SetFlags(1, lx.symbol.fCMDARG_OPTIONAL)
        self.dyna_Add("Select by Loop Mode", lx.symbol.sTYPE_INTEGER)
        self.basic_SetFlags(2, lx.symbol.fCMDARG_OPTIONAL)

    def cmd_Flags(self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO

    def cmd_Interact(self):
        pass

    def cmd_UserName(self):
        return 'SMO UV - Unwrap Cylindrical'

    def cmd_Desc(self):
        return 'Unwrap the current Polygon Selection using Cylindrical Mode on Defined Axis.'

    def cmd_Tooltip(self):
        return 'Unwrap the current Polygon Selection using Cylindrical Mode on Defined Axis.'

    def cmd_Help(self):
        return 'https://twitter.com/sm0luck'

    def basic_ButtonName(self):
        return 'SMO UV - Unwrap Cylindrical'

    def basic_Enable(self, msg):
        return True

    def basic_Execute(self, msg, flags):
        scene = modo.scene.current()
        # Force to select the current Mesh Item if it is not selected in the Item List
        lx.eval('smo.MASTER.ForceSelectMeshItemOnly')
        lx.eval('smo.UV.AutoCreateUVMap')

        mesh = scene.selectedByType('mesh')[0]
        # meshes = scene.selectedByType('mesh')
        meshseam = modo.Scene().selected[0]
        CsPolys = len(mesh.geometry.polygons.selected)
        SelItems = (lx.evalN('query sceneservice selection ? locator'))
        lx.out('Selected items is:', SelItems)

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
        Int_IsRectangle = self.dyna_Int(1)
        Int_SelectByLoop = self.dyna_Int(2)

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
        # Current Selection is Rectangle = 1
        IsRectangle = Int_IsRectangle
        lx.out('Rectangle state:', IsRectangle)

        # Current Selection = 0
        # current selection + Add loop = 1
        SelectByLoop = Int_SelectByLoop
        lx.out('Select by loop state:', SelectByLoop)
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

        # Relax UV Off = 0
        # Relax UV On = 1
        RelaxUV = lx.eval('user.value SMO_UseVal_UV_RelaxPostProcess ?')
        lx.out('RelaxUV state:', RelaxUV)

        UVRelaxIterCount = lx.eval('user.value SMO_UseVal_UV_RelaxIterCount ?')
        lx.out('RelaxUV iteration count:', UVRelaxIterCount)

        # Bugfix to disable Auto RelaxUV Island if the Unwrap Rectangle was True, in order to keep Rectangle result in output.
        if IsRectangle == 1:
            RelaxUV = 0

        # Relocate in Area = 0
        # Relocate in Area = 1
        RelocateInArea = lx.eval('user.value SMO_UseVal_UV_RelocateInArea ?')
        lx.out('Relocate In Area state:', RelocateInArea)

        # ------------- ARGUMENTS Test
        # UVProjAxe = 2
        # IsRectangle = 1
        # SelectByLoop = 1
        # ------------- ARGUMENTS ------------- #

        # ------------------------------ #
        # <----( DEFINE VARIABLES )----> #
        # ------------------------------ #
        # ---------------- Define user value for all the different SafetyCheck --- START
        #####
        lx.eval("user.defNew name:SMO_SafetyCheck_UVUnwrapCyl_PolygonModeEnabled type:integer life:momentary")
        lx.eval("user.defNew name:SMO_SafetyCheck_UVUnwrapCyl_min1PolygonSelected type:integer life:momentary")

        ## Selected UVmap Count
        lx.eval("user.defNew name:SMO_SafetyCheck_UVUnwrapCyl_UVMapCount type:boolean life:momentary")
        ## Selected UVmap Name
        lx.eval("user.defNew name:UVUnwrapCyl_UVMapName type:string life:momentary")
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
        UVUnwrapCyl_UVMapName = lx.eval('user.value SMO_UV_SelectedMeshUVmapName ?')
        lx.out('Selected Mesh UV Maps Name:', UVUnwrapCyl_UVMapName)

        lx.eval('smo.GC.ClearSelectionVmap 1 1')
        lx.eval('select.vertexMap %s txuv replace' % UVUnwrapCyl_UVMapName)

        if SelectedMeshUVMapsCount > 1:
            lx.eval('dialog.setup info')
            lx.eval('dialog.title {SMONSTER - UV - Unwrap Cylindrical:}')
            lx.eval('dialog.msg {Please select Only One Vertex Map and run that script again.}')
            lx.eval('dialog.open')
            SMO_SafetyCheck_UVUnwrapCyl_UVMapCount = False
            sys.exit()

        if SelectedMeshUVMapsCount < 1:
            lx.eval('dialog.setup info')
            lx.eval('dialog.title {SMONSTER - UV - Unwrap Cylindrical:}')
            lx.eval('dialog.msg {You must have a UV map selected to run this script.}')
            lx.eval('dialog.open')
            SMO_SafetyCheck_UVUnwrapCyl_UVMapCount = False
            sys.exit()

        if SelectedMeshUVMapsCount == 1:
            SMO_SafetyCheck_UVUnwrapCyl_UVMapCount = True

        # UserUVMapName = lx.eval1('query layerservice vmap.name ? %s' % UVmap_Selected)
        # lx.out('USER UV Map Name:', UserUVMapName)
        lx.out('<- UV Map Safety Check ->')
        lx.out('<------------- END -------------->')
        ###############################################

        # -------------------------- #
        # <---( SAFETY CHECK 2 )---> #
        # -------------------------- #

        # Polygon Selection Mode enabled --- START

        selType = ""
        # Used to query layerservice for the list of polygons, edges or vertices.
        attrType = ""

        if lx.eval1("select.typeFrom typelist:vertex;polygon;edge;item;ptag ?"):
            selType = "vertex"
            attrType = "vert"

            SMO_SafetyCheck_UVUnwrapCyl_PolygonModeEnabled = 0
            lx.eval('dialog.setup info')
            lx.eval('dialog.title {SMONSTER - UV - Unwrap Cylindrical}')
            lx.eval('dialog.msg {You must be in Polygon Mode to run that script}')
            lx.eval('+dialog.open')
            lx.out('script Stopped: You must be in Polygon Mode to run that script')
            sys.exit
            # sys.exit( "LXe_FAILED:Must be in polygon selection mode." )


        elif lx.eval1("select.typeFrom typelist:edge;vertex;polygon;item ?"):
            selType = "edge"
            attrType = "edge"

            SMO_SafetyCheck_UVUnwrapCyl_PolygonModeEnabled = 0
            lx.eval('dialog.setup info')
            lx.eval('dialog.title {SMONSTER - UV - Unwrap Cylindrical:}')
            lx.eval('dialog.msg {You must be in Polygon Mode to run that script}')
            lx.eval('+dialog.open')
            lx.out('script Stopped: You must be in Polygon Mode to run that script')
            sys.exit
            # sys.exit( "LXe_FAILED:Must be in polygon selection mode." )

        elif lx.eval1("select.typeFrom typelist:polygon;vertex;edge;item ?"):
            selType = "polygon"
            attrType = "poly"

            SMO_SafetyCheck_UVUnwrapCyl_PolygonModeEnabled = 1
            lx.out('script Running: Correct Component Selection Mode')


        else:
            # This only fails if none of the three supported selection
            # modes have yet been used since the program started, or
            # if "item" or "ptag" (ie: materials) is the current
            # selection mode.
            SMO_SafetyCheck_UVUnwrapCyl_PolygonModeEnabled = 0
            lx.eval('dialog.setup info')
            lx.eval('dialog.title {SMONSTER - UV - Unwrap Cylindrical:}')
            lx.eval('dialog.msg {You must be in Polygon Mode to run that script}')
            lx.eval('+dialog.open')
            lx.out('script Stopped: You must be in Polygon Mode to run that script')
            sys.exit
            # sys.exit( "LXe_FAILED:Must be in polygon selection mode." )
        # Polygon Selection Mode enabled --- END

        # -------------------------- #
        # <---( SAFETY CHECK 3 )---> #
        # -------------------------- #

        # at Least 1 Polygons is selected --- START
        lx.out('Count Selected Poly', CsPolys)

        if CsPolys < 1:
            SMO_SafetyCheck_UVUnwrapCyl_min1PolygonSelected = 0
            lx.eval('dialog.setup info')
            lx.eval('dialog.title {SMONSTER - UV - Unwrap Cylindrical:}')
            lx.eval('dialog.msg {You must select at least 1 polygon to run that script}')
            lx.eval('+dialog.open')
            lx.out('script Stopped: Add more polygons to your selection')
            sys.exit

        elif CsPolys >= 1:
            SMO_SafetyCheck_UVUnwrapCyl_min1PolygonSelected = 1
            lx.out('script running: right amount of polygons in selection')
        # at Least 1 Polygons is selected --- END

        # # ------------- UV SEAM Map Detection

        # #Define the UV Seam vmap name Search case.
        # lx.eval("user.defNew name:UVUnwrapCyl_DesiredUVSEAMmapName type:string life:momentary")
        # UVUnwrapCyl_DesiredUVSEAMmapName = 'UV Seam'

        # #Define the UV Seam vmap name Search case.
        # lx.eval("user.defNew name:UVUnwrapCyl_NoUVSeamMap type:string life:momentary")
        # UVUnwrapCyl_NoUVSeamMap = '_____n_o_n_e_____'

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
        # if DetectedUVSEAMmapName == UVUnwrapCyl_NoUVSeamMap:
        # lx.eval('vertMap.list seam ?')
        # lx.eval('vertMap.list seam _____n_e_w_____')
        # lx.eval('vertMap.new "UV Seam" seam true {0.78 0.78 0.78} 2.0')
        # lx.eval('vertMap.list seam "UV Seam"')

        # elif DetectedUVSEAMmapName == UVUnwrapCyl_DesiredUVSEAMmapName:
        # lx.out('UV Map and UVSEAM Map Selected')
        # lx.eval('vertMap.list seam "UV Seam"')
        # UserUVSEAMmapName = lx.eval1('query layerservice vmap.name ? %s' %UVSEAM_Selected)
        # lx.out('USER UVSEAM Map Name:', UserUVSEAMmapName)

        # lx.out('<----------- END ----------->')
        # ------------------------------ #

        # ---------------- Define current value for the Prerequisite TotalSafetyCheck --- START
        #####
        TotalSafetyCheckTrueValue = 2
        lx.out('Desired Value', TotalSafetyCheckTrueValue)
        TotalSafetyCheck = (
                    SMO_SafetyCheck_UVUnwrapCyl_PolygonModeEnabled + SMO_SafetyCheck_UVUnwrapCyl_min1PolygonSelected)
        lx.out('Current Value', TotalSafetyCheck)
        #####
        # ---------------- Define current value for the Prerequisite TotalSafetyCheck --- END

        # ------------------------ #
        # <----( Main Macro )----> #
        # ------------------------ #

        # ---------------- Compare TotalSafetyCheck value and decide or not to continue the process  --- START
        lx.eval('select.type item')
        lx.eval('item.refSystem %s' % SelItems)
        lx.eval('select.type polygon')
        if TotalSafetyCheck == TotalSafetyCheckTrueValue:
            if SelectByLoop == 1:
                lx.eval('select.loop')

            # Tag the UV as Done
            lx.eval('select.editSet name:UV_DONE mode:add')

            if UVProjAxe == 0:
                lx.eval('select.editSet name:UV_DONE_X mode:add')

            if UVProjAxe == 1:
                lx.eval('select.editSet name:UV_DONE_Y mode:add')

            if UVProjAxe == 2:
                lx.eval('select.editSet name:UV_DONE_Z mode:add')

            if UVProjAxe == 3:
                lx.eval('select.editSet name:UV_DONE_FREE mode:add')
                lx.eval('select.convert edge')
                lx.eval('select.contract')
                lx.eval('workPlane.fitSelect')
                lx.eval('select.drop edge')
                lx.eval('select.type polygon')
                lx.eval('tool.set actr.origin on')

            # Isolate selection
            lx.eval('hide.unsel')

            lx.eval('tool.set preset:"uv.create" mode:on')
            lx.eval('tool.setAttr uv.create proj cylindrical')
            lx.eval('tool.setAttr tool:"uv.create" attr:mode value:automatic')

            lx.eval('tool.setAttr tool:"uv.create" attr:newmap value:false')
            lx.eval('tool.setAttr uv.create name %s' % UVUnwrapCyl_UVMapName)

            ## Do a Projection on specific axis via Arguments
            # Command Block Begin:
            if UVProjAxe == 0:
                lx.eval('tool.setAttr uv.create axis 0')
            if UVProjAxe == 1:
                lx.eval('tool.setAttr uv.create axis 1')
            if UVProjAxe == 2:
                lx.eval('tool.setAttr uv.create axis 2')
            if UVProjAxe == 3:
                lx.eval('tool.setAttr uv.create axis 0')
            # Command Block End:

            try:
                # Command Block Begin:  
                lx.eval('tool.setAttr tool:"uv.create" attr:sizX value:"0.1"')
                lx.eval('tool.setAttr tool:"uv.create" attr:sizY value:"0.1"')
                lx.eval('tool.setAttr tool:"uv.create" attr:sizZ value:"0.1"')
                lx.eval('tool.setAttr tool:"uv.create" attr:cenX value:"0.0"')
                lx.eval('tool.setAttr tool:"uv.create" attr:cenY value:"0.0"')
                lx.eval('tool.setAttr tool:"uv.create" attr:cenZ value:"0.0"')
                # Command Block End:
            except:
                sys.exit

            lx.eval('tool.doapply')

            lx.eval('tool.set preset:"uv.create" mode:off')

            # Selection Aligned = 3
            if UVProjAxe == 3:
                lx.eval('tool.set actr.origin off')
                lx.eval('workPlane.reset')

            lx.eval('tool.viewType uv')

            if IsRectangle == 1:
                lx.eval('!uv.rectangle false')

            # FixFlipped UVs Passes --> Start
            if FixFlip:
                lx.eval('select.drop polygon')
                lx.eval('smo.UV.FixFlipped 0')
                lx.eval('select.drop polygon')
            # FixFlipped UVs Passes --> End

            # Relax Passes --> Start
            if RelaxUV:
                lx.eval('select.type polygon')
                lx.eval('select.all')
                lx.eval('smo.UV.Relax %s' % UVRelaxIterCount)
            # Relax Passes --> End

            # Orient Horizontaly
            lx.eval('select.type polygon')
            lx.eval('select.all')
            lx.eval('smo.UV.SmartOrient 0')

            # replay name:"Fit UVs"
            lx.eval('uv.fit entire gapsByPixel:8.0 udim:1001')

            if RelocateInArea:
                # replay name:"Move"
                lx.eval('tool.set preset:TransformMove mode:on')

                try:
                    ## Do a Projection on specific axis via Arguments
                    if UVProjAxe == 0 and RelocateInArea == True:
                        # Command Block Begin:
                        lx.eval('tool.setAttr tool:"xfrm.transform" attr:U value:"-2.0"')
                        lx.eval('tool.setAttr tool:"xfrm.transform" attr:V value:"-2.0"')
                        # Command Block End:
                    if UVProjAxe == 1 and RelocateInArea == True:
                        # Command Block Begin:
                        lx.eval('tool.setAttr tool:"xfrm.transform" attr:U value:"-1.0"')
                        lx.eval('tool.setAttr tool:"xfrm.transform" attr:V value:"-2.0"')
                        # Command Block End:
                    if UVProjAxe == 2 and RelocateInArea == True:
                        # Command Block Begin:
                        lx.eval('tool.setAttr tool:"xfrm.transform" attr:U value:"-1.0"')
                        lx.eval('tool.setAttr tool:"xfrm.transform" attr:V value:"-1.0"')
                        # Command Block End:
                    if UVProjAxe == 3 and RelocateInArea == True:
                        # Command Block Begin:
                        lx.eval('tool.setAttr tool:"xfrm.transform" attr:U value:"-2.0"')
                        lx.eval('tool.setAttr tool:"xfrm.transform" attr:V value:"-1.0"')
                        # Command Block End:
                except:
                    sys.exit

                # Launch the Move
                lx.eval('tool.doapply')
                lx.eval('tool.set preset:TransformMove mode:off')

            # if Modo_ver >= 1300:
            # lx.eval('smo.UV.UpdateUVSeamCutMap')

            # if Modo_ver >= 1300:
            # lx.eval('select.all')
            # lx.eval('uv.selectBorder')
            # lx.eval('seam.add')
            # lx.eval('select.drop edge')
            # lx.eval('select.type polygon')
            # lx.eval('select.drop polygon')

            lx.eval('unhide')

            if RePack == True and UVProjAxe == 0 and RelocateInArea == True:
                lx.eval('smo.UV.SelectUVArea -2 -2')
                lx.eval('hide.unsel')
                lx.eval('smo.UV.NormalizePackByArea 0 0 -2 -2')
                lx.eval('unhide')

            if RePack == True and UVProjAxe == 1 and RelocateInArea == True:
                lx.eval('smo.UV.SelectUVArea -1 -2')
                lx.eval('hide.unsel')
                lx.eval('smo.UV.NormalizePackByArea 0 0 -1 -2')
                lx.eval('unhide')

            if RePack == True and UVProjAxe == 2 and RelocateInArea == True:
                lx.eval('smo.UV.SelectUVArea -1 -1')
                lx.eval('hide.unsel')
                lx.eval('smo.UV.NormalizePackByArea 0 0 -1 -1')
                lx.eval('unhide')

            if RePack == True and UVProjAxe == 3 and RelocateInArea == True:
                lx.eval('smo.UV.SelectUVArea -2 -1')
                lx.eval('hide.unsel')
                lx.eval('smo.UV.NormalizePackByArea 0 0 -2 -1')
                lx.eval('unhide')

            if RePack == True and RelocateInArea == False:
                lx.eval('smo.UV.SelectUVArea 0 0')
                lx.eval('hide.unsel')
                lx.eval('smo.UV.NormalizePackByArea 0 0 0 0')
                lx.eval('unhide')

            if AutoUpdateUVSeamCutMapState == True and Modo_ver >= 1300:
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

        # ---------------- Compare TotalSafetyCheck value and decide or not to continue the process  --- END


lx.bless(SMO_UV_UnwrapCylindrical_Cmd, Cmd_Name)

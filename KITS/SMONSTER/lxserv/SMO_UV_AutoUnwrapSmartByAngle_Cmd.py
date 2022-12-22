# python
# ---------------------------------------
# Name:         SMO_UV_AutoUnwrapSmartByAngle_Cmd.py
# Version:      1.0
#
# Purpose:      This script is designed to
#               Auto Unwrap the current Mesh item by using Sharp Edges
#               defined by a Min and Max Angle as Seams.
#
# Author:       Franck ELISABETH
# Website:      http://www.smoluck.com
#
# Created:      21/12/2022
# Copyright:    (c) Franck Elisabeth 2017-2022
# ---------------------------------------

import lx, lxu, modo, sys

Cmd_Name = "smo.UV.AutoUnwrapSmartByAngle"
# smo.UV.AutoUnwrapSmartByAngle 1 0 88 180

class SMO_UV_AutoUnwrapSmartByAngle_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
        self.dyna_Add("Unwrap Method: (Conformal) False or True (Angle Based)", lx.symbol.sTYPE_BOOLEAN)
        # self.basic_SetFlags(0, lx.symbol.fCMDARG_OPTIONAL)  # here the (0) define the argument index.
        self.dyna_Add("Initial Projection: (Planar) False or True (Group Normal)", lx.symbol.sTYPE_BOOLEAN)
        # self.basic_SetFlags(1, lx.symbol.fCMDARG_OPTIONAL)
        self.dyna_Add("Minimum Angle", lx.symbol.sTYPE_FLOAT)
        # self.basic_SetFlags(2, lx.symbol.fCMDARG_OPTIONAL)
        self.dyna_Add("Maximum Angle", lx.symbol.sTYPE_FLOAT)
        # self.basic_SetFlags(3, lx.symbol.fCMDARG_OPTIONAL)

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
        return 'SMO UV - Auto Unwrap Smart By Angle'

    def cmd_Desc(self):
        return 'Auto Unwrap the current Mesh item by using Sharp Edges defined by a Min and Max Angle as Seams.'

    def cmd_Tooltip(self):
        return 'Auto Unwrap the current Mesh item by using Sharp Edges defined by a Min and Max Angle as Seams.'

    def cmd_Help(self):
        return 'https://twitter.com/sm0luck'

    def basic_ButtonName(self):
        return 'SMO UV - Auto Unwrap Smart By Angle'

    def basic_Enable(self, msg):
        return True

    def basic_Execute(self, msg, flags):
        scene = modo.scene.current()

        SelCompMode = int()
        if self.SelModeVert:
            SelCompMode = 1
        if self.SelModeEdge:
            SelCompMode = 2
        if self.SelModePoly:
            SelCompMode = 3
        if self.SelModeItem:
            SelCompMode = 5

        # Force to select the current Mesh Item if it is not selected in the Item List
        lx.eval('smo.MASTER.ForceSelectMeshItemOnly')
        lx.eval('smo.UV.AutoCreateUVMap')

        mesh = scene.selectedByType('mesh')[0]
        # meshes = scene.selectedByType('mesh')

        # MODO version checks.
        # Modo 13.0 and up have UV Seam map.
        # Version below 13.0 haven't
        Modo_ver = int(lx.eval('query platformservice appversion ?'))
        lx.out('Modo Version:', Modo_ver)



        if self.dyna_IsSet(0):
            AUSBA_UnwrapMethod = self.dyna_Bool(0)

        if self.dyna_IsSet(1):
            AUSBA_InitProjection = self.dyna_Bool(1)

        if self.dyna_IsSet(2):
            AUSBA_MinAngle = self.dyna_Float(2)

        if self.dyna_IsSet(3):
            AUSBA_MaxAngle = self.dyna_Float(3)

        ############### 5 ARGUMENTS ###############
        args = lx.args()
        lx.out(args)

        # Conformal= 0
        # Angle Based = 1
        UnwrapMethod = AUSBA_UnwrapMethod
        lx.out('Desired Unwrap Method:', UnwrapMethod)

        # Planar = 0
        # Group Normal = 1
        InitProjection = AUSBA_InitProjection
        lx.out('Initial Projection Mode:', InitProjection)

        # 89.0 Degree
        MinAngle = AUSBA_MinAngle
        lx.out('Minimum Angle is:', MinAngle)

        # 180 Degree
        MaxAngle = AUSBA_MaxAngle
        lx.out('Maximum Angle is:', MaxAngle)
        ############### ARGUMENTS ###############

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

        # ############### 4 ARGUMENTS Test ###############
        # UnwrapMethod = 0          --> Conformal
        # InitProjection = 1        --> Group Normal
        # IsRectangle = 0
        # ############### ARGUMENTS ###############

        ################################
        # <----[ DEFINE VARIABLES ]---->#
        ################################
        #####--- Define user value for all the different SafetyCheck --- START ---#####
        #####
        lx.eval("user.defNew name:SMO_SafetyCheck_AUSBA_PolygonModeEnabled type:integer life:momentary")
        lx.eval("user.defNew name:SMO_SafetyCheck_AUSBA_min1PolygonSelected type:integer life:momentary")

        lx.eval("user.defNew name:SMO_SafetyCheck_AUSBA_EdgeModeEnabled type:integer life:momentary")
        lx.eval("user.defNew name:SMO_SafetyCheck_AUSBA_min3EdgeSelected type:integer life:momentary")

        ## Selected UVmap Count
        lx.eval("user.defNew name:SMO_SafetyCheck_AUSBA_UVMapCount type:boolean life:momentary")
        ## Selected UVmap Name
        lx.eval("user.defNew name:AUSBA_UVMapName type:string life:momentary")
        #####
        #####--- Define user value for all the different SafetyCheck --- END ---#####

        lx.eval('smo.GC.ClearSelectionVmap 2 1')
        lx.eval('smo.GC.ClearSelectionVmap 3 1')
        lx.eval('smo.GC.ClearSelectionVmap 4 1')
        lx.eval('smo.GC.ClearSelectionVmap 5 1')
        lx.eval('smo.GC.ClearSelectionVmap 6 1')
        lx.eval('smo.GC.ClearSelectionVmap 7 1')
        lx.eval('smo.GC.ClearSelectionVmap 8 1')

        ###################################################
        ####### SAFETY CHEC K 1 - One UVMap Selected #######
        ###################################################
        lx.out('<------------- START -------------->')
        lx.out('<--- UV Map Safety Check --->')

        # Get info about the selected UVMap.
        lx.eval('smo.UV.GetUVMapCountName 0 1 1')
        SelectedMeshUVMapsCount = lx.eval('user.value SMO_UV_SelectedMeshUVmapCount ?')
        lx.out('Selected Mesh UV Maps Count:', SelectedMeshUVMapsCount)
        AUSBA_UVMapName = lx.eval('user.value SMO_UV_SelectedMeshUVmapName ?')
        lx.out('Selected Mesh UV Maps Name:', AUSBA_UVMapName)

        lx.eval('smo.GC.ClearSelectionVmap 1 1')
        lx.eval('select.vertexMap %s txuv replace' % AUSBA_UVMapName)

        SMO_SafetyCheck_AUSBA_UVMapCount = bool()
        if SelectedMeshUVMapsCount > 1:
            lx.eval('dialog.setup info')
            lx.eval('dialog.title {SMONSTER - UV - Auto Unwrap Smart By Angle:}')
            lx.eval('dialog.msg {Please select Only One Vertex Map and run that script again.}')
            lx.eval('dialog.open')
            SMO_SafetyCheck_AUSBA_UVMapCount = False
            sys.exit()

        if SelectedMeshUVMapsCount < 1:
            lx.eval('dialog.setup info')
            lx.eval('dialog.title {SMONSTER - UV - Auto Unwrap Smart By Angle:}')
            lx.eval('dialog.msg {You must have a UV map selected to run this script.}')
            lx.eval('dialog.open')
            SMO_SafetyCheck_AUSBA_UVMapCount = False
            sys.exit()

        if SelectedMeshUVMapsCount == 1:
            SMO_SafetyCheck_AUSBA_UVMapCount = True

        # UserUVMapName = lx.eval1('query layerservice vmap.name ? %s' % UVmap_Selected)
        # lx.out('USER UV Map Name:', UserUVMapName)
        lx.out('<- UV Map Safety Check ->')
        lx.out('<------------- END -------------->')
        ###############################################

        #####-------------------- safety check 1 : Only One Item Selected --- END --------------------#####

        ###############################################
        ## <----( Main Macro for Polygon Mode )----> ##
        ###############################################
        if SMO_SafetyCheck_AUSBA_UVMapCount == True:
            AutoHideState = lx.eval('user.value SMO_UseVal_UV_HideAfterUnwrap ?')
            #####--------------------  Compare TotalSafetyCheck value and decide or not to continue the process  --- START --------------------#####
            if SelCompMode != 3:
                lx.eval('select.type polygon')
            lx.eval('select.editSet name:UV_DONE mode:add')
            lx.eval('select.type edge')
            lx.eval('select.drop edge')
            lx.eval('select.edgeSharp 89.55 180.0')
            lx.eval('smo.UV.UnwrapSmart %s %s 0 0' % (UnwrapMethod, InitProjection))
            if AutoHideState:
                lx.eval('select.type polygon')
                lx.eval('unhide')
            lx.eval('tool.viewType uv')
            # lx.eval('uv.orient horizontal')

            # # replay name:"Fit UVs"
            # lx.eval('uv.fit entire gapsByPixel:8.0 udim:1001')

            if AutoUpdateUVSeamCutMapState and Modo_ver >= 1300:
                lx.eval('smo.UV.UpdateUVSeamCutMap')
                lx.eval('view3d.showUVSeam true active')

            lx.eval('select.type polygon')
            lx.eval('select.drop polygon')
            lx.eval('select.uvOverlap {%s} true true false false false true' % AUSBA_UVMapName)
            lx.eval('select.connect uv')
            lx.eval('smo.UV.MoveToUVArea -1 0')
            lx.eval('smo.UV.NormalizePackByArea 0 0 -1 0')
            lx.eval('unhide')
            lx.eval('smo.UV.SelectUVArea 0 0')
            lx.eval('smo.UV.NormalizePackByArea 0 0 0 0')
            lx.eval('select.drop polygon')

            if SelCompMode == 1:
                lx.eval('select.type vertex')
            if SelCompMode == 2:
                lx.eval('select.type edge')
            if SelCompMode == 5:
                lx.eval('select.type item')
        #####--------------------  Compare TotalSafetyCheck value and decide or not to continue the process  --- END --------------------#####


lx.bless(SMO_UV_AutoUnwrapSmartByAngle_Cmd, Cmd_Name)

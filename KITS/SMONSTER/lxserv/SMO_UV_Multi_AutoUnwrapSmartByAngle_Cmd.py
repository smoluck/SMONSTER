# python
"""
Name:         SMO_UV_Multi_AutoUnwrapSmartByAngle_Cmd.py

Purpose:      This script is designed to
              (for Multiple Mesh)
              MULTI - Auto Unwrap the current Mesh item by using Sharp Edges
              defined by a Min and Max Angle as Seams.

Author:       Franck ELISABETH
Website:      https://www.linkedin.com/in/smoluck/
Created:      21/12/2022
Copyright:    (c) Franck Elisabeth 2017-2022
"""

import lx
import lxu
import modo

Cmd_Name = "smo.UV.Multi.AutoUnwrapSmartByAngle"
# smo.UV.Multi.AutoUnwrapSmartByAngle 88 180


class SMO_UV_Multi_AutoUnwrapSmartByAngle_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
        self.dyna_Add("Unwrap Method: (Conformal) 0 or 1 (Angle Based)", lx.symbol.sTYPE_BOOLEAN)
        # self.basic_SetFlags(0, lx.symbol.fCMDARG_OPTIONAL)  # here the (0) define the argument index.
        self.dyna_Add("Initial Projection: (Planar) 0 or 1 (Group Normal)", lx.symbol.sTYPE_BOOLEAN)
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
        return 'SMO UV - (Multi) Auto Unwrap Smart By Angle'

    def cmd_Desc(self):
        return 'MULTI - Auto Unwrap the current Mesh item by using Sharp Edges defined by a Min and Max Angle as Seams.'

    def cmd_Tooltip(self):
        return 'MULTI - Auto Unwrap the current Mesh item by using Sharp Edges defined by a Min and Max Angle as Seams.'

    def cmd_Help(self):
        return 'https://twitter.com/sm0luck'

    def basic_ButtonName(self):
        return 'SMO UV - (Multi) Auto Unwrap Smart By Angle'

    def basic_Enable(self, msg):
        return True

    def basic_Execute(self, msg, flags):
        MAUSBA_UnwrapMethod = self.dyna_Bool(0)
        MAUSBA_InitProjection = self.dyna_Bool(1)
        MAUSBA_MinAngle = self.dyna_Float(2)
        MAUSBA_MaxAngle = self.dyna_Float(3)

        SelCompMode = int()
        if self.SelModeVert:
            SelCompMode = 1
        if self.SelModeEdge:
            SelCompMode = 2
        if self.SelModePoly:
            SelCompMode = 3
        if self.SelModeItem:
            SelCompMode = 5

        scn = modo.scene.current()

        # MODO version checks.
        # Modo 13.0 and up have UV Seam map.
        # Version below 13.0 haven't
        Modo_ver = int(lx.eval ('query platformservice appversion ?'))
        lx.out('Modo Version:', Modo_ver)

        # ------------- ARGUMENT ------------- #
        args = lx.args()
        lx.out(args)

        # Conformal= 0
        # Angle Based = 1
        UnwrapMethod = MAUSBA_UnwrapMethod
        lx.out('Desired Unwrap Method:', UnwrapMethod)

        # Planar = 0
        # Group Normal = 1
        InitProjection = MAUSBA_InitProjection
        lx.out('Initial Projection Mode:', InitProjection)

        # 89.0 Degree
        MinAngle = MAUSBA_MinAngle
        lx.out('Minimum Angle is:', MinAngle)

        # 180 Degree
        MaxAngle = MAUSBA_MaxAngle
        lx.out('Maximum Angle is:', MaxAngle)
        # ------------- ARGUMENTS ------------- #

        m = modo.Mesh()
        MAUSBA_SelItem = lxu.select.ItemSelection().current()
        # print('lxu.object.Item : ', MMAUSBA_SelItem)

        mesh = scn.selectedByType('mesh')
        print('modo.Mesh :', mesh)
        print('modo.Mesh list length:', len(mesh))

        MAUSBA_TargetIDList = []
        for item in mesh:
            itemType = modo.Item(item).type
            item = lx.object.Item(item)
            # print(item)
            if itemType == "mesh":
                ID = item.Ident()
                # print(ID)
                MAUSBA_TargetIDList.append(ID)
        # print(MAUSBA_TargetIDList)

        MAUSBA_PolysTuple = []
        for item in mesh:
            # CsPolys = len(item.geometry.polygons.selected)
            # print('Total selected Polygons on this mesh layer', CsPolys)
            Polys = item.geometry.polygons.selected
            # print('modo.Mesh list ', Polys)
            MAUSBA_PolysTuple.append(Polys)
        # print('Tuple (Poly ID and Mesh ID): ---)', MAUSBA_PolysTuple)

        MAUSBA_PolysList = list(MAUSBA_PolysTuple)
        # print('List (Poly ID and Mesh ID): ---)', MAUSBA_PolysList)
        # print(MAUSBA_PolysList)
        # print('------------------')
        # print(MAUSBA_PolysList[0])
        # print('------')
        # print(MAUSBA_PolysList[1])
        # print('------')
        # print(MAUSBA_PolysList[2])
        # print('------')
        # print(MAUSBA_PolysList[3])
        # print('------')

        lx.eval('select.type item')

        index = -1
        if len(mesh) > 1:
            for n in MAUSBA_TargetIDList:
                index = (index + 1)
                # print('id :', index)
                scn.select(n)
                selected_mesh = scn.selectedByType('mesh')[0]
                # print('current mesh identity :', index, selected_mesh)
                lx.eval('smo.UV.AutoUnwrapSmartByAngle %s %s %s %s' % (UnwrapMethod, InitProjection, MinAngle, MaxAngle))
        index = -1

        if len(mesh) == 1:
            scn.select(m)
            lx.eval('smo.UV.AutoUnwrapSmartByAngle %s %s %s %s' % (UnwrapMethod, InitProjection, MinAngle, MaxAngle))

        lx.eval('smo.GC.DeselectAll')
        scn.select(mesh)

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
            lx.eval('select.type polygon')
            lx.eval('select.drop polygon')
            lx.eval('smo.UV.SelectUVArea -1 0')
            lx.eval('smo.UV.NormalizePackByArea 0 0 -1 0')
            lx.eval('unhide')
            lx.eval('smo.UV.SelectUVArea 0 0')
            lx.eval('smo.UV.NormalizePackByArea 0 0 0 0')
            lx.eval('select.drop polygon')
            lx.eval('unhide')

        if AutoUpdateUVSeamCutMapState and Modo_ver >= 1300:
            lx.eval('smo.UV.UpdateUVSeamCutMap')
            lx.eval('view3d.showUVSeam true active')

        lx.eval('smo.GC.DeselectAll')
        scn.select(mesh)
        lx.eval('select.type polygon')

        if AutoHideState and not RelocateInArea:
            lx.eval('unhide')
            lx.eval('smo.UV.SelectUVArea -1 0')
            lx.eval('select.editSet UV_DONE remove')
            lx.eval('select.drop polygon')
            lx.eval('select.useSet UV_DONE select')
            lx.eval('hide.sel')

        if SelCompMode == 1:
            lx.eval('select.type vertex')
        if SelCompMode == 2:
            lx.eval('select.type edge')
        if SelCompMode == 3:
            lx.eval('select.type polygon')
        if SelCompMode == 5:
            lx.eval('select.type item')

        del index
        del MAUSBA_TargetIDList
        del MAUSBA_PolysList
        del MAUSBA_PolysTuple


lx.bless(SMO_UV_Multi_AutoUnwrapSmartByAngle_Cmd, Cmd_Name)

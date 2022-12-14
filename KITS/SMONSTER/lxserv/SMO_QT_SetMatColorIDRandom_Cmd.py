# python
# ---------------------------------------
# Name:         SMO_QT_SetMatColorIDRandom_Cmd.py
# Version:      1.00
#
# Purpose:      This script is designed to
#               Set a random Diffuse Color using Material Tag (polygons) on the selected Mesh Layers.
#               Named the new Mat using "ColorID" as Prefix.
#
# Author:       Franck ELISABETH
# Website:      http://www.smoluck.com
#
# Created:      19/01/2021
# Copyright:    (c) Franck Elisabeth 2017-2022
# ---------------------------------------

import modo, lx, lxu

Cmd_Name = "smo.QT.SetMatColorIDRandom"
# smo.QT.SetMatColorIDRandom

class SMO_QT_SetMatColorIDRandom_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
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
        return 'SMO QT - Set ColorID Random (by Material)'

    def cmd_Desc(self):
        return 'Set a random Diffuse Color using Material Tag (polygons) on the selected Mesh Layers. Named the new Mat using "ColorID" as Prefix.'

    def cmd_Tooltip(self):
        return 'Set a random Diffuse Color using Material Tag (polygons) on the selected Mesh Layers. Named the new Mat using "ColorID" as Prefix.'

    def cmd_Help(self):
        return 'https://twitter.com/sm0luck'

    def basic_ButtonName(self):
        return 'SMO QT - Set ColorID Random (by Material)'

    def basic_Enable(self, msg):
        return True

    def basic_Execute(self, msg, flags):
        scene = modo.scene.current()
        ColorID_Suffix = "ColorID"
        ByItemMode = bool()

        # Check Current status of SMO SmartMaterial to turn it to TRUE if needed
        SMO_UseVal_GC_OriginalModoMaterialOverride = bool()
        SMO_UseVal_GC_OriginalModoMaterialOverride = lx.eval('user.value SMO_UseVal_GC_OriginalModoMaterialOverride ?')
        if SMO_UseVal_GC_OriginalModoMaterialOverride:
            lx.eval('user.value SMO_UseVal_GC_OriginalModoMaterialOverride false')
        SMO_UseVal_GC_MatNameSuffix = ""
        SMO_UseVal_GC_MatNameSuffix = lx.eval('user.value SMO_UseVal_GC_MatNameSuffix ?')
        if SMO_UseVal_GC_MatNameSuffix != "":
            lx.eval('user.value SMO_UseVal_GC_MatNameSuffix ""')

        if self.SelModeItem:
            lx.eval('smo.MASTER.ForceSelectMeshItemOnly')
            lx.eval('select.type polygon')
            lx.eval('select.all')
            ByItemMode = True

        if self.SelModePoly:
            lx.eval('smo.MASTER.ForceSelectMeshItemOnly')
            ByItemMode = False

        # mesh = scene.selectedByType('mesh')[0]
        # CsPolys = len(mesh.geometry.polygons.selected)
        meshes = scene.selectedByType('mesh')
        # lx.eval('query layerservice layer.id ? main')  # select main layer
        # ItemUniqueName = lx.eval('query layerservice layer.id ? main')  # store the Unique name of the current mesh layer
        # lx.out('Item Unique Name:', ItemUniqueName)

        ################################
        # <----[ DEFINE VARIABLES ]---->#
        ################################
        lx.eval("user.defNew name:SceneConstantID type:integer life:momentary")
        lx.eval("user.defNew name:ColorID_Suffix type:string life:momentary")
        lx.eval("user.defNew name:ColorIDMatName type:string life:momentary")
        lx.eval("user.defNew name:IDNum type:string life:momentary")
        lx.eval("user.defNew name:Const_Suffix type:string life:momentary")
        lx.eval("user.defNew name:ColorIDConstantName type:string life:momentary")

        PrstColorIDRed = 0
        PrstColorIDMagenta = 1
        PrstColorIDPink = 2
        PrstColorIDBrown = 3
        PrstColorIDOrange = 4
        PrstColorIDYellow = 5
        PrstColorIDGreen = 6
        PrstColorIDLightGreen = 7
        PrstColorIDCyan = 8
        PrstColorIDBlue = 9
        PrstColorIDLightBlue = 10
        PrstColorIDUltramarine = 11
        PrstColorIDPurple = 12
        PrstColorIDLightPurple = 13
        PrstColorIDDarkGrey = 14
        PrstColorIDGrey = 15
        PrstColorIDWhite = 16

        ###########  Check User Values  ###########
        GC_OriginalModoMaterialOverride = bool(lx.eval('user.value SMO_UseVal_GC_OriginalModoMaterialOverride ?'))
        GC_MatDefaultSmooAngle = lx.eval('user.value SMO_UseVal_GC_MatDefaultSmooAngle ?')
        GC_WeightByPolyArea = lx.eval('user.value SMO_UseVal_GC_WeightByPolyArea ?')

        # Override for creating Modo Materials.
        # GC_MatShadingModel = lx.eval('user.value SMO_UseVal_GC_MatShadingModel ?')
        GC_MatShadingModel = 3

        GC_ConstantColorOverride = bool(lx.eval('user.value SMO_UseVal_GC_ConstantColorOverride ?'))
        GC_MatNameSuffix = lx.eval('user.value SMO_UseVal_GC_MatNameSuffix ?')
        Separator = lx.eval('pref.value application.indexStyle ?')
        # print(GC_MatNameSuffix)

        lx.eval('smo.QT.SelectBaseShader')
        SceneShaderItemID = []
        for item in scene.items(itype='defaultShader', superType=True):
            if item.name == "Base Shader":
                SceneShaderItemID.append(item.id)
        print('Base Shader item Id is:', SceneShaderItemID[0])

        # scene.select(SceneShaderItemID[0])

        def uNameItem():
            item = modo.item.Item()
            return item.UniqueName()

        def ItemIdent():
            item = modo.item.Item()
            return item.Ident()

        QTChannelExist = bool()
        IDNum = int()

        try:
            lx.eval(
                '!channel.create MatColorIDGlobalCount integer useMin:true default:(-1.0) username:MatColorIDGlobalCount')
            SceneConstantID = (-1)
            QTChannelExist = False
        except RuntimeError:  # diffuse amount is zero.
            lx.eval('select.channel {%s:MatColorIDGlobalCount@lmb=x} set' % SceneShaderItemID[0])
            QTChannelExist = True
            # lx.out('ColorID  Global Count channel already created')
            pass

        if QTChannelExist:
            SceneConstantID = lx.eval('!item.channel MatColorIDGlobalCount ?')
            # lx.out('Constant ID Max in scene', SceneConstantID)
        # print(QTChannelExist)

        print(SceneConstantID)

        if SceneConstantID == (-1):
            IDNum = 0
        if SceneConstantID >= 0:
            IDNum = int(SceneConstantID) + 1
        print(IDNum)
        lx.eval('!item.channel MatColorIDGlobalCount %i' % IDNum)
        ColorIDMatName = ("%s_%s" % (ColorID_Suffix, IDNum))
        # lx.out('Color ID Selection set name:', ColorIDMatName)

        if Separator == "none":
            Sep = ""
            Text = ColorID_Suffix
        if Separator == "sp":
            Sep = " "
            Text = ColorID_Suffix + Sep + str(IDNum)
        if Separator == "uscore":
            Sep = "_"
            Text = ColorID_Suffix + Sep + str(IDNum)
        if Separator == "brak":
            SepA = "("
            SepB = ")"
            Text = ColorID_Suffix + SepA + str(IDNum) + SepB
        if Separator == "brak-sp":
            SepA = " ("
            SepB = ") "
            Text = ColorID_Suffix + SepA + str(IDNum) + SepB
        # print(Text)

        if IDNum <= 16:
            if IDNum == PrstColorIDRed:
                TarCol = '1.0 0.0844 0.0382'
            if IDNum == PrstColorIDMagenta:
                TarCol = '0,8632 0,0802 0,3968'
            if IDNum == PrstColorIDPink:
                TarCol = '0.807 0.1946 0.1946'
            if IDNum == PrstColorIDBrown:
                TarCol = '0.402 0.2232 0.0704'
            if IDNum == PrstColorIDOrange:
                TarCol = '1.0 0.4793 0.0497'
            if IDNum == PrstColorIDYellow:
                TarCol = '1.0 0,8149 0,0452'
            if IDNum == PrstColorIDGreen:
                TarCol = '0,0423 0,7682 0,0423'
            if IDNum == PrstColorIDLightGreen:
                TarCol = '0.2832 0.9131 0.2832'
            if IDNum == PrstColorIDCyan:
                TarCol = '0,0382 0,9911 0,7454'
            if IDNum == PrstColorIDBlue:
                TarCol = '0,0529 0,5029 1.0'
            if IDNum == PrstColorIDLightBlue:
                TarCol = '0,2232 0,624 1.0'
            if IDNum == PrstColorIDUltramarine:
                TarCol = '0.1274 0.2502 1.0'
            if IDNum == PrstColorIDPurple:
                TarCol = '0,3763 0,2423 0,8308'
            if IDNum == PrstColorIDLightPurple:
                TarCol = '0.624 0.4179 1.0'
            if IDNum == PrstColorIDDarkGrey:
                TarCol = '0,2423 0,2423 0,2423'
            if IDNum == PrstColorIDGrey:
                TarCol = '0.4852 0.4852 0.4852'
            if IDNum == PrstColorIDWhite:
                TarCol = '0.855 0.855 0.855'
        if IDNum > 16:
            BACKGROUND_DEFAULT = '0.5 0.5 0.5'
            TarCol = BACKGROUND_DEFAULT

        print('Base Target Color is: %s' % TarCol)
        R = (TarCol.split(' ')[0])
        G = (TarCol.split(' ')[1])
        B = (TarCol.split(' ')[2])
        # print('Red Color is: %s' % R)
        # print('Green Color is: %s' % G)
        # print('Blue Color is: %s' % B)

        Modo_ver = int(lx.eval('query platformservice appversion ?'))
        lx.out('Modo Version:', Modo_ver)

        def SetColorOnNode(IDNum):
            if IDNum == PrstColorIDRed:
                return lx.eval('item.editorColor red')
            elif IDNum == PrstColorIDMagenta:
                return lx.eval('item.editorColor magenta')
            elif IDNum == PrstColorIDPink:
                return lx.eval('item.editorColor pink')
            elif IDNum == PrstColorIDBrown:
                return lx.eval('item.editorColor brown')
            elif IDNum == PrstColorIDOrange:
                return lx.eval('item.editorColor orange')
            elif IDNum == PrstColorIDYellow:
                return lx.eval('item.editorColor yellow')
            elif IDNum == PrstColorIDGreen:
                return lx.eval('item.editorColor green')
            elif IDNum == PrstColorIDLightGreen:
                return lx.eval('item.editorColor lightgreen')
            elif IDNum == PrstColorIDCyan:
                return lx.eval('item.editorColor cyan')
            elif IDNum == PrstColorIDBlue:
                return lx.eval('item.editorColor blue')
            elif IDNum == PrstColorIDLightBlue:
                return lx.eval('item.editorColor lightblue')
            elif IDNum == PrstColorIDUltramarine:
                return lx.eval('item.editorColor ultramarine')
            elif IDNum == PrstColorIDPurple:
                return lx.eval('item.editorColor purple')
            elif IDNum == PrstColorIDLightPurple:
                return lx.eval('item.editorColor lightpurple')
            elif IDNum == PrstColorIDDarkGrey:
                return lx.eval('item.editorColor darkgrey')
            elif IDNum == PrstColorIDGrey:
                return lx.eval('item.editorColor grey')
            elif IDNum == PrstColorIDWhite:
                return lx.eval('item.editorColor white')
            else:
                return lx.eval('item.editorColor none')

        ###### Modo
        if GC_MatShadingModel < 4:
            if GC_OriginalModoMaterialOverride == False:
                lx.eval('smo.GC.SetNewMaterialSmartRename 0 {%s} {%s %s %s}' % (ColorIDMatName, R, G, B))
            if GC_OriginalModoMaterialOverride == True:
                lx.eval('poly.setMaterial {%s} {%s %s %s} 0.8 0.04 true false type:default' % (ColorIDMatName, R, G, B))
                lx.eval('material.new {} true false'.format(ColorIDMatName))
            SetColorOnNode(IDNum)
        ###### Unreal
        if GC_MatShadingModel == 4:
            if GC_OriginalModoMaterialOverride == False:
                lx.eval('smo.GC.SetNewMaterialSmartRename 0 {%s} {%s %s %s}' % (ColorIDMatName, R, G, B))
            if GC_OriginalModoMaterialOverride == True:
                lx.eval('poly.setMaterial {%s} {%s %s %s} 0.8 0.04 true false type:unreal' % (ColorIDMatName, R, G, B))
                lx.eval('material.new {} true false unreal'.format(ColorIDMatName))
            SetColorOnNode(IDNum)
        ###### Unity
        if GC_MatShadingModel == 5:
            if GC_OriginalModoMaterialOverride == False:
                lx.eval('smo.GC.SetNewMaterialSmartRename 0 {%s} {%s %s %s}' % (ColorIDMatName, R, G, B))
            if GC_OriginalModoMaterialOverride == True:
                lx.eval(
                    'poly.setMaterial {%s} {%s %s %s} 0.8 0.04 true false false type:unity' % (ColorIDMatName, R, G, B))
                lx.eval('material.new {} true false unity'.format(ColorIDMatName))
            SetColorOnNode(IDNum)
        ###### glTF
        if GC_MatShadingModel == 6:
            if GC_OriginalModoMaterialOverride == False:
                lx.eval('smo.GC.SetNewMaterialSmartRename 0 {%s} {%s %s %s}' % (ColorIDMatName, R, G, B))
            if GC_OriginalModoMaterialOverride == True:
                lx.eval(
                    'poly.setMaterial {%s} {%s %s %s} 0.8 0.04 true false false type:gltf' % (ColorIDMatName, R, G, B))
                lx.eval('material.new {} true false gltf'.format(ColorIDMatName))
            SetColorOnNode(IDNum)
        ###### AxF
        if GC_MatShadingModel == 7:
            if GC_OriginalModoMaterialOverride == False:
                lx.eval('smo.GC.SetNewMaterialSmartRename 0 {%s} {%s %s %s}' % (ColorIDMatName, R, G, B))
            if GC_OriginalModoMaterialOverride == True:
                lx.eval('poly.setMaterial {%s} {%s %s %s} 0.8 0.04 true false type:axf' % (ColorIDMatName, R, G, B))
                lx.eval('material.new {} true false axf'.format(ColorIDMatName))
            SetColorOnNode(IDNum)

        ###### Modo Shader
        if GC_MatShadingModel < 4:
            for mask in scene.selectedByType('mask'):
                for child in mask.childrenByType('advancedMaterial'):
                    child.name = Text.format(mask.name)

                    # Smoothing Angle:
                    lx.eval('item.channel advancedMaterial$smAngle {%s}' % GC_MatDefaultSmooAngle)

                    # Shading Model:
                    ###### Traditionnal
                    if GC_MatShadingModel == 0:
                        lx.eval('item.channel advancedMaterial$brdfType blinn')
                    ###### Energy Conserving
                    if GC_MatShadingModel == 1:
                        lx.eval('item.channel advancedMaterial$brdfType ashikhmin')
                    ###### Physically Based
                    if GC_MatShadingModel == 2:
                        lx.eval('item.channel advancedMaterial$brdfType gtr')
                    ###### Principled
                    if GC_MatShadingModel == 3:
                        lx.eval('item.channel advancedMaterial$brdfType principled')

                    if Modo_ver < 1520:
                        # Weight By Polygon Area:
                        if GC_WeightByPolyArea == 0:
                            lx.eval('material.smoothWeight area false')
                        if GC_WeightByPolyArea == 1:
                            lx.eval('material.smoothWeight area true')

                    if Modo_ver >= 1520:
                        # Weight By Polygon Area:
                        if GC_WeightByPolyArea == 0:
                            lx.eval('material.smoothAreaWeight none')
                        if GC_WeightByPolyArea == 1:
                            lx.eval('material.smoothAreaWeight area')
                        if GC_WeightByPolyArea == 2:
                            lx.eval('material.smoothAreaWeight full')

        SelItem = lxu.select.ItemSelection().current()
        # print(SelItem)

        for item in SelItem:
            itemType = modo.Item(item).type
            # print(itemType)
            Mat_Model = lx.object.Item(item)
            # print(Mat_Model)
            Mat_ModelName = Mat_Model.UniqueName()
            # print(Mat_ModelName)
            Mat_ModelID = Mat_Model.Ident()
            # print(Mat_ModelID)
            #######################################################
            if GC_MatShadingModel == 3 and itemType != "principled":
                scene.deselect(Mat_ModelName)
            if GC_MatShadingModel == 4 and itemType != "unrealShader":
                scene.deselect(Mat_ModelName)
            if GC_MatShadingModel == 5 and itemType != "unityShader":
                scene.deselect(Mat_ModelName)
            if GC_MatShadingModel == 6 and itemType != "glTFShader":
                scene.deselect(Mat_ModelName)
            if GC_MatShadingModel == 7 and itemType != "AxFShader":
                scene.deselect(Mat_ModelName)

        # MaterialItemLX = lxu.select.ItemSelection().current()
        # for item in MaterialItemLX:
        #    # itemType = modo.Item(item).type
        #    # print (itemType)
        #    MaterialItem = lx.object.Item(item)
        #    print (MaterialItem)
        #    MaterialItemName = MaterialItem.UniqueName()
        #    print (MaterialItemName)
        #    MaterialItemID = MaterialItem.Ident()
        #    print (MaterialItemID)

        lx.eval('smo.GC.DeselectAll')

        #############
        # ## Parent current ColorID Mask under BaseShader even if there is other Shader items in the scene
        # lx.eval('smo.GC.DeselectAll')
        # lx.eval('smo.QT.SelectBaseShader')
        # baseShad = lx.eval('query sceneservice defaultShader.parent ? {Base Shader}')
        # # print(baseShad)
        # scene.select(GrpMask)
        # TargetGrpMask = ItemIdent()
        # # print(TargetGrpMask)
        # lx.eval('texture.parent {%s} {%s} item:{%s}' % (baseShad, NewID, TargetGrpMask))
        #############

        ###
        # Make sure Advanced Material in the latest created Grp Mask is using the right Color code for the item
        def SetColorOnAdvMaterial(IDNum, ColorIDMatName):
            MainGrpPresence = False
            indddex = 0
            MatchingGrpMask = []
            for item in scene.items(itype='mask', superType=True):
                if item.name.startswith('ColorID_'):
                    MainGrpPresence = True
                    MatchingGrpMask.append(item.Ident())
            for item in MatchingGrpMask:
                scene.select(item)
                for mask in scene.selectedByType('mask'):
                    for child in mask.childrenByType('advancedMaterial'):
                        cname = child.name
                        if cname == ColorIDMatName:
                            cid = cname.split('_')[1]
                            scene.select(child)
                            SetColorOnNode(indddex)
                            # print(cname)
                            # print(cid)
                            lx.eval('smo.GC.DeselectAll')
                indddex = indddex + 1
            del indddex
            del MatchingGrpMask
            return

        if IDNum <= 16:
            SetColorOnAdvMaterial(IDNum, ColorIDMatName)
        ###

        ###
        # Add the latest Material to the main Grp_ColorID folder/GrpMask
        # lx.eval('smo.QT.SelectBaseShader')
        # baseShad = lx.eval('query sceneservice defaultShader.parent ? {Base Shader}')
        # lx.eval('smo.GC.DeselectAll')

        GrpPresence = False
        GrpTarget = []
        GrpColorIdent = []
        for item in scene.items(itype='mask', superType=True):
            # lx.out('Default Base Shader found:',item)
            if item.name == "Grp_ColorID":
                GrpPresence = True
                # print(item)
                GrpTarget.append(item.Ident())
                print(GrpTarget[0])
        print(GrpPresence)

        if not GrpPresence:
            # Here we catch the MAINGrpMask "Grp_ColorID"
            GrpColorID = scene.addItem('mask', name='Grp_ColorID')
            print(GrpColorID.Ident())
            GrpTarget.append(GrpColorID.Ident())
            GrpColorIdent = GrpColorID.Ident()
            SourceGrpMask = []
            for item in scene.items(itype='mask', superType=True):
                if item.name.startswith('ColorID_'):
                    SubGrpPresence = True
                    SourceGrpMask.append(item.Ident())
            lx.eval('texture.parent {%s} 99 item:{%s}' % (GrpColorIdent, SourceGrpMask[0]))
        ##########################################################
        ##########################Marker##########################
        ##########################################################

        print(ColorIDMatName)
        if GrpPresence:
            GrpColorIdent = GrpTarget[0]
            # scene.select(GrpTarget[0])
            SourceGrpMask = []
            for item in scene.items(itype='mask', superType=True):
                test = ColorIDMatName
                if item.name.startswith('ColorID_' + str(IDNum)):
                    SourceGrpMask.append(item.Ident())
                    print(SourceGrpMask[0])
            lx.eval('texture.parent {%s} {%s} item:{%s}' % (GrpColorIdent, IDNum, SourceGrpMask[0]))

        # renderItem = scene.renderItem
        # AllMasks = []
        # for mGrp in renderItem.childrenByType("mask", 1):
        #    AllMasks.append(mGrp.index)
        # print(max(AllMasks))
        # PosID = 0
        # PosID = max(AllMasks)
        # print(PosID)
        # print(SceneShaderItemID[0])
        # print(GrpColorIdent)
        #
        # lx.eval('texture.parent {%s} {%s} item:{%s}' % (SceneShaderItemID[0], PosID, GrpColorIdent))


lx.bless(SMO_QT_SetMatColorIDRandom_Cmd, Cmd_Name)

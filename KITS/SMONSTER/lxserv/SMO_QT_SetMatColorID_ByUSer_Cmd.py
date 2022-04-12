# python
# ---------------------------------------
# Name:         SMO_GC_SetMatColorID_ByUser_Cmd.py
# Version:      1.0
#
# Purpose:      This script is designed to
#               Set a random Diffuse Color using Material Tag (polygons) on the selected Mesh Layers.
#               Named the new Mat using "ColorID" as Prefix. Color ID Number set by User value in Popup field.
#
#
# Author:       Franck ELISABETH
# Website:      http://www.smoluck.com
#
# Created:      19/01/2021
# Copyright:    (c) Franck Elisabeth 2017-2022
# ---------------------------------------

import lx, lxu, modo

Command_Name = "smo.QT.SetMatColorIDByUser"
# smo.QT.SetMatColorIDByUser

ColorID_Suffix = "ColorID"

def SetColorIDByNumberCheckSceneMaxColorID():
    # Select the Base Shader to create and place ColorID group on top of current Material Groups
    scene = modo.scene.current()
    # lx.eval('smo.QT.SelectBaseShader')
    SceneShaderItemList = []
    SceneShaderItemName = []
    for item in scene.items(itype='defaultShader', superType=True):
        # lx.out('Default Base Shader found:',item)
        SceneShaderItemList.append(item)
        print(item.id)
        SceneShaderItemName.append(item.id)
    scene.select(SceneShaderItemList[0])
    print(SceneShaderItemName)

    QTChannelExist = bool()
    NewID = int()
    IDNum = int()

    try:
        lx.eval('!channel.create SelSetColorIDConstantGlobalCount integer useMin:true default:(-1.0) username:SelSetColorIDConstantGlobalCount')
        SceneConstantID = (-1)
        QTChannelExist = False
    except RuntimeError:  # diffuse amount is zero.
        lx.eval('select.channel {%s:SelSetColorIDConstantGlobalCount@lmb=x} set' % SceneShaderItemName[0])
        QTChannelExist = True
        lx.out('ColorID  Global Count channel already created')
        pass

    if QTChannelExist == True:
        SceneConstantID = lx.eval('!item.channel SelSetColorIDConstantGlobalCount ?')
        lx.out('Constant ID Max in scene', SceneConstantID)
        # print(QTChannelExist)
        # print(SceneConstantID)
        return (SceneConstantID)

class SMO_GC_SetMatColorID_ByUser_Cmd(lxu.command.BasicCommand):
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
        return 'SMO QT - Set ColorID ByUser (by Material)'

    def cmd_Desc(self):
        return 'Set a random Diffuse Color using Material Tag (polygons) on the selected Mesh Layers. Named the new Mat using "ColorID" as Prefix. Color ID Number set by User value in Popup field.'

    def cmd_Tooltip(self):
        return 'Set a random Diffuse Color using Material Tag (polygons) on the selected Mesh Layers. Named the new Mat using "ColorID" as Prefix. Color ID Number set by User value in Popup field.'

    def cmd_Help(self):
        return 'https://twitter.com/sm0luck'

    def basic_ButtonName(self):
        return 'SMO QT - Set ColorID ByUser (by Material)'

    def cmd_Flags(self):
        return lx.symbol.fCMD_UNDO

    def basic_Enable(self, msg):
        return True

    def basic_Execute(self, msg, flags):
        scene = modo.scene.current()

        try:
            #####--- Define User Value for Count --- START ---#####
            #####
            #Create a user value that define the ID Number for the Command.
            lx.eval("user.defNew name:IDNumber type:integer life:momentary")
            #Set the title name for the dialog window
            lx.eval('user.def IDNumber dialogname "SMO QT - Color ID - IDNumber"')
            #Set the input field name for the value that the users will see
            lx.eval("user.def IDNumber username {Set the Color ID Number}")
            #The '?' before the user.value calls a popup to have the user set the value
            lx.eval("?user.value IDNumber")
            #Now that the user set the value, i can query it
            UserInput_IDNumber = lx.eval("user.value IDNumber ?")
            lx.out('User ID Number:',UserInput_IDNumber)
            IDNum = UserInput_IDNumber
        except:
            pass

        if self.SelModePoly == True:
            lx.eval('smo.MASTER.ForceSelectMeshItemOnly')

        lx.out('MODE PRESET ACTIVATED')

        # mesh = scene.selectedByType('mesh')[0]
        # CsPolys = len(mesh.geometry.polygons.selected)
        meshes = scene.selectedByType('mesh')
        lx.eval('query layerservice layer.id ? main')  # select main layer
        ItemUniqueName = lx.eval('query layerservice layer.id ? main')  # store the Unique name of the current mesh layer
        # lx.out('Item Unique Name:', ItemUniqueName)

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

        print('Target Color is: %s' % TarCol)

        ################################
        # <----[ DEFINE VARIABLES ]---->#
        ################################

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
        R = (TarCol.split(' ')[0])
        G = (TarCol.split(' ')[1])
        B = (TarCol.split(' ')[2])
        print('Red Color is: %s' % R)
        print('Green Color is: %s' % G)
        print('Blue Color is: %s' % B)

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
        print(Text)

        # #####--- Define user value for all the different SafetyCheck --- START ---#####
        # #####
        # lx.eval("user.defNew name:SMO_SafetyCheck_PolygonModeEnabled type:integer life:momentary")
        # lx.eval("user.defNew name:SMO_SafetyCheck_min1PolygonSelected type:integer life:momentary")
        # #####
        # #####--- Define user value for all the different SafetyCheck --- END ---#####

        #####--- Define user value for all the different SafetyCheck --- START ---#####
        #####
        lx.eval("user.defNew name:SceneConstantID type:integer life:momentary")
        lx.eval("user.defNew name:ColorID_Suffix type:string life:momentary")
        lx.eval("user.defNew name:NewID type:string life:momentary")
        lx.eval("user.defNew name:Const_Suffix type:string life:momentary")
        lx.eval("user.defNew name:ColorIDConstantName type:string life:momentary")
        ###################

        # ##############################
        # ####### SAFETY CHECK 1 #######
        # ##############################
        #
        # #####--------------------  safety check 1: Polygon Selection Mode enabled --- START --------------------#####
        #
        # selType = ""
        # # Used to query layerservice for the list of polygons, edges or vertices.
        # attrType = ""
        #
        # if lx.eval1("select.typeFrom typelist:vertex;polygon;edge;item;ptag ?"):
        #     selType = "vertex"
        #     attrType = "vert"
        #
        #     SMO_SafetyCheck_PolygonModeEnabled = 0
        #     lx.eval('dialog.setup info')
        #     lx.eval('dialog.title {SMO QT - Set ColorID:}')
        #     lx.eval('dialog.msg {You must be in Polygon Mode to run that script}')
        #     lx.eval('+dialog.open')
        #     lx.out('script Stopped: You must be in Polygon Mode to run that script')
        #     sys.exit
        #     # sys.exit( "LXe_FAILED:Must be in polygon selection mode." )
        #
        #
        # elif lx.eval1("select.typeFrom typelist:edge;vertex;polygon;item ?"):
        #     selType = "edge"
        #     attrType = "edge"
        #
        #     SMO_SafetyCheck_PolygonModeEnabled = 0
        #     lx.eval('dialog.setup info')
        #     lx.eval('dialog.title {SMO QT - Set ColorID:}')
        #     lx.eval('dialog.msg {You must be in Polygon Mode to run that script}')
        #     lx.eval('+dialog.open')
        #     lx.out('script Stopped: You must be in Polygon Mode to run that script')
        #     sys.exit
        #     # sys.exit( "LXe_FAILED:Must be in polygon selection mode." )
        #
        # elif lx.eval1("select.typeFrom typelist:polygon;vertex;edge;item ?"):
        #     selType = "polygon"
        #     attrType = "poly"
        #
        #     SMO_SafetyCheck_PolygonModeEnabled = 1
        #     lx.out('script Running: Correct Component Selection Mode')
        #
        #
        # else:
        #     # This only fails if none of the three supported selection
        #     # modes have yet been used since the program started, or
        #     # if "item" or "ptag" (ie: materials) is the current
        #     # selection mode.
        #     SMO_SafetyCheck_PolygonModeEnabled = 0
        #     lx.eval('dialog.setup info')
        #     lx.eval('dialog.title {SMO QT - Set ColorID:}')
        #     lx.eval('dialog.msg {You must be in Polygon Mode to run that script}')
        #     lx.eval('+dialog.open')
        #     lx.out('script Stopped: You must be in Polygon Mode to run that script')
        #     sys.exit
        #     # sys.exit( "LXe_FAILED:Must be in polygon selection mode." )
        # #####--------------------  safety check 1: Polygon Selection Mode enabled --- END --------------------#####
        #
        # ##############################
        # ####### SAFETY CHECK 2 #######
        # ##############################
        #
        # #####--------------------  safety check 2: at Least 1 Polygons is selected --- START --------------------#####
        # lx.out('Count Selected Poly', CsPolys)
        #
        # if CsPolys < 1:
        #     SMO_SafetyCheck_min1PolygonSelected = 0
        #     lx.eval('dialog.setup info')
        #     lx.eval('dialog.title {SMO QT - Set ColorID:}')
        #     lx.eval('dialog.msg {You must select at least 1 polygon to run that script}')
        #     lx.eval('+dialog.open')
        #     lx.out('script Stopped: Add more polygons to your selection')
        #     sys.exit
        #
        # elif CsPolys >= 1:
        #     SMO_SafetyCheck_min1PolygonSelected = 1
        #     lx.out('script running: right amount of polygons in selection')
        # #####--------------------  safety check 2: at Least 1 Polygons is selected --- END --------------------#####
        #
        # #####--- Define current value for the Prerequisite TotalSafetyCheck --- START ---#####
        # #####
        # TotalSafetyCheckTrueValue = 2
        # lx.out('Desired Value', TotalSafetyCheckTrueValue)
        # TotalSafetyCheck = (SMO_SafetyCheck_PolygonModeEnabled + SMO_SafetyCheck_min1PolygonSelected)
        # lx.out('Current Value', TotalSafetyCheck)
        # #####
        # #####--- Define current value for the Prerequisite TotalSafetyCheck --- END ---#####

        ##############################
        ## <----( Main Macro )----> ##
        ##############################

        # #####--------------------  Compare TotalSafetyCheck value and decide or not to continue the process  --- START --------------------#####
        # if TotalSafetyCheck == TotalSafetyCheckTrueValue:
        # Select the Base Shader to create and place ColorID group on top of current Material Groups
        # lx.eval('smo.QT.SelectBaseShader')
        SceneShaderItemList = []
        SceneShaderItemName = []
        for item in scene.items(itype='defaultShader', superType=True):
            # lx.out('Default Base Shader found:',item)
            SceneShaderItemList.append(item)
            print(item.id)
            SceneShaderItemName.append(item.id)
        scene.select(SceneShaderItemList[0])
        print(SceneShaderItemName)

        QTChannelExist = bool()
        NewID = int()

        try:
            lx.eval('!channel.create SelSetColorIDConstantGlobalCount integer useMin:true default:(-1.0) username:SelSetColorIDConstantGlobalCount')
            SceneConstantID = (-1)
            QTChannelExist = False
        except RuntimeError:  # diffuse amount is zero.
            lx.eval('select.channel {%s:SelSetColorIDConstantGlobalCount@lmb=x} set' % SceneShaderItemName[0])
            QTChannelExist = True
            # lx.out('ColorID  Global Count channel already created')
            pass

        if QTChannelExist == True:
            SceneConstantID = lx.eval('!item.channel SelSetColorIDConstantGlobalCount ?')
            lx.out('Constant ID Max in scene', SceneConstantID)
        print(QTChannelExist)

        ColorID_Suffix = "ColorID"
        print(SceneConstantID)

        if SceneConstantID == (-1):
            NewID = 0
        if SceneConstantID >= 0:
            NewID = int(SceneConstantID) + 1
        print(NewID)
        lx.eval('!item.channel MatColorIDGlobalCount %i' % NewID)
        ColorIDMatName = ("%s_%s" % (ColorID_Suffix, NewID))

        Modo_ver = int(lx.eval('query platformservice appversion ?'))
        lx.out('Modo Version:', Modo_ver)
        scene = modo.Scene()

        ###### Modo
        if GC_MatShadingModel < 4:
            if GC_OriginalModoMaterialOverride == False:
                lx.eval('smo.GC.SetNewMaterialSmartRename {%s} {%s %s %s}' % (ColorIDMatName, R, G, B))
            if GC_OriginalModoMaterialOverride == True:
                lx.eval('poly.setMaterial {%s} {%s %s %s} 0.8 0.04 true false type:default' % (ColorIDMatName, R, G, B))
                lx.eval('material.new {} true false'.format(ColorIDMatName))
        ###### Unreal
        if GC_MatShadingModel == 4:
            if GC_OriginalModoMaterialOverride == False:
                lx.eval('smo.GC.SetNewMaterialSmartRename {%s} {%s %s %s}' % (ColorIDMatName, R, G, B))
            if GC_OriginalModoMaterialOverride == True:
                lx.eval('poly.setMaterial {%s} {%s %s %s} 0.8 0.04 true false type:unreal' % (ColorIDMatName, R, G, B))
                lx.eval('material.new {} true false unreal'.format(ColorIDMatName))
        ###### Unity
        if GC_MatShadingModel == 5:
            if GC_OriginalModoMaterialOverride == False:
                lx.eval('smo.GC.SetNewMaterialSmartRename {%s} {%s %s %s}' % (ColorIDMatName, R, G, B))
            if GC_OriginalModoMaterialOverride == True:
                lx.eval('poly.setMaterial {%s} {%s %s %s} 0.8 0.04 true false false type:unity' % (ColorIDMatName, R, G, B))
                lx.eval('material.new {} true false unity'.format(ColorIDMatName))
        ###### glTF
        if GC_MatShadingModel == 6:
            if GC_OriginalModoMaterialOverride == False:
                lx.eval('smo.GC.SetNewMaterialSmartRename {%s} {%s %s %s}' % (ColorIDMatName, R, G, B))
            if GC_OriginalModoMaterialOverride == True:
                lx.eval('poly.setMaterial {%s} {%s %s %s} 0.8 0.04 true false false type:gltf' % (ColorIDMatName, R, G, B))
                lx.eval('material.new {} true false gltf'.format(ColorIDMatName))
        ###### AxF
        if GC_MatShadingModel == 7:
            if GC_OriginalModoMaterialOverride == False:
                lx.eval('smo.GC.SetNewMaterialSmartRename {%s} {%s %s %s}' % (ColorIDMatName, R, G, B))
            if GC_OriginalModoMaterialOverride == True:
                lx.eval('poly.setMaterial {%s} {%s %s %s} 0.8 0.04 true false type:axf' % (ColorIDMatName, R, G, B))
                lx.eval('material.new {} true false axf'.format(ColorIDMatName))

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
        print(SelItem)

        for item in SelItem:
            itemType = modo.Item(item).type
            print(itemType)
            Mat_Model = lx.object.Item(item)
            print(Mat_Model)
            Mat_ModelName = Mat_Model.UniqueName()
            print(Mat_ModelName)
            Mat_ModelID = Mat_Model.Ident()
            print(Mat_ModelID)
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
        # scene.select(MaterialItemName)
        # scene.select(mesh)
        scene.select(meshes)

        del (R, G, B, GC_OriginalModoMaterialOverride, GC_MatDefaultSmooAngle, GC_WeightByPolyArea, GC_MatShadingModel, GC_ConstantColorOverride, GC_MatNameSuffix)

lx.bless(SMO_GC_SetMatColorID_ByUser_Cmd, Command_Name)
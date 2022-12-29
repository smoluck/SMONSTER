# python
"""
Name:         SMO_GC_SetMatColorID_ByUser_Cmd.py

Purpose:      This script is designed to
              Set a random Diffuse Color using Material Tag (polygons) on the selected Mesh Layers.
              Named the new Mat using "ColorID" as Prefix. Color ID Number set by User value in Popup field.

Author:       Franck ELISABETH
Website:      https://www.smoluck.com
Created:      19/01/2021
Copyright:    (c) Franck Elisabeth 2017-2022
"""

import lx
import lxu
import modo
import sys

if sys.version_info < (3, 0):
    xrange = range

Cmd_Name = "smo.QT.SetMatColorIDByUser"
# smo.QT.SetMatColorIDByUser


def uNameItem():
    item = modo.item.Item()
    return item.UniqueName()


def ItemIdent():
    item = modo.item.Item()
    return item.Ident()


def getTargetGrpMaskName(IDNum):
    CID_Suffix = "ColorID"
    Separator = lx.eval('pref.value application.indexStyle ?')
    ColorIDMatName = ""
    if Separator == "none":
        Sep = ""
        ColorIDMatName = CID_Suffix
    if Separator == "sp":
        Sep = " "
        ColorIDMatName = CID_Suffix + Sep + str(IDNum)
    if Separator == "uscore":
        Sep = "_"
        ColorIDMatName = CID_Suffix + Sep + str(IDNum)
    if Separator == "brak":
        SepA = "("
        SepB = ")"
        ColorIDMatName = CID_Suffix + SepA + str(IDNum) + SepB
    if Separator == "brak-sp":
        SepA = " ("
        SepB = ") "
        ColorIDMatName = CID_Suffix + SepA + str(IDNum) + SepB
    return ColorIDMatName


# print(getTargetGrpMaskName(IDNum))


def SetColorOnNode(IDNum):
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


# SetColorOnNode(IDNum)


def GetBaseShader():
    scn = modo.scene.current()
    # lx.eval('smo.QT.SelectBaseShader')
    RenderItemBaseShader = []
    SceneShaderItemName = []
    for item in scn.items(itype='defaultShader', superType=True):
        if item.name == "Base Shader":
            # lx.out('Default Base Shader found:',item)
            RenderItemBaseShader.append(item)
            # print(item.id)
            SceneShaderItemName.append(item.id)
    return SceneShaderItemName


# print(GetBaseShader())


# test if there is already MaxColorID in the "Base Shader" Render Item by checking the presence of the Channel "MatColorIDGlobalCount"
def SetColorIDByNumberCheckSceneMaxColorID(IDNum):
    # Select the Base Shader to create and place ColorID group on top of current Material Groups
    scn = modo.scene.current()
    # lx.eval('smo.QT.SelectBaseShader')
    RenderItemBaseShader = []
    SceneShaderItemName = []
    for item in scn.items(itype='defaultShader', superType=True):
        if item.name == "Base Shader":
            # lx.out('Default Base Shader found:',item)
            RenderItemBaseShader.append(item)
            # print(item.id)
            SceneShaderItemName.append(item.id)
    scn.select(RenderItemBaseShader[0])
    # print(SceneShaderItemName)
    QTChannelExist = bool()
    SceneCurrentConstantID = 0

    # Test the Base Shader item and check if the needed Channel exist
    try:
        lx.eval(
            '!channel.create MatColorIDGlobalCount integer useMin:true default:(%s) username:MatColorIDGlobalCount' % SceneCurrentConstantID)
        QTChannelExist = False
    except RuntimeError:  # diffuse amount is zero.
        lx.eval('select.channel {%s:MatColorIDGlobalCount@lmb=x} set' % SceneShaderItemName[0])
        SceneCurrentConstantID = lx.eval('!item.channel MatColorIDGlobalCount ?')
        QTChannelExist = True
        # print('ColorID  Global Count channel already created')
        pass

    # print(QTChannelExist)
    # print(IDNum)
    # print(SceneCurrentConstantID)
    ValuesList = [int(IDNum), int(SceneCurrentConstantID)]
    MaxValue = max(ValuesList)
    # print('the Maximum ColorID desired in scene is: %s' % MaxValue)

    # Now that we're sure we have a channel created, we select it
    try:
        lx.eval(
            '!channel.create MatColorIDGlobalCount integer useMin:true default:(-1.0) username:MatColorIDGlobalCount')
        QTChannelExist = False
    except RuntimeError:  # diffuse amount is zero.
        lx.eval('select.channel {%s:MatColorIDGlobalCount@lmb=x} set' % SceneShaderItemName[0])
        QTChannelExist = True
        # print('ColorID  Global Count channel already created')
        pass

    if QTChannelExist:
        # print('Quick Tag Channel is defined:', QTChannelExist)
        SceneCurrentConstantID = lx.eval('!item.channel MatColorIDGlobalCount ?')
        if SceneCurrentConstantID < 0:
            SceneCurrentConstantID = 0
        if SceneCurrentConstantID >= 0:
            SceneCurrentConstantID = MaxValue
            lx.eval('!item.channel MatColorIDGlobalCount %s' % MaxValue)
        # print('Constant ID Max in scene', SceneCurrentConstantID)

    if not QTChannelExist:
        lx.eval(
            '!channel.create MatColorIDGlobalCount integer useMin:true default:(-1.0) username:MatColorIDGlobalCount')
        lx.eval('!item.channel MatColorIDGlobalCount %i' % MaxValue)
    scn.deselect(RenderItemBaseShader[0])
    return QTChannelExist, MaxValue, RenderItemBaseShader[0]


# print(SetColorIDByNumberCheckSceneMaxColorID(IDNum))
# print('ColorIDCount Channel already exist: %s' % SetColorIDByNumberCheckSceneMaxColorID(IDNum)[0])
# print('ColorIDCount Channel Value is: %s' % SetColorIDByNumberCheckSceneMaxColorID(IDNum)[1])
# print('Base Shader RenderItem call is: %s' % SetColorIDByNumberCheckSceneMaxColorID(IDNum)[2])


# tGet the MaxColorID in the "Base Shader" Render Item
def GetColorIDByNumberCheckSceneMaxColorID():
    # Select the Base Shader to create and place ColorID group on top of current Material Groups
    scn = modo.scene.current()
    scn.select(GetBaseShader()[0])
    MaxID = lx.eval('!item.channel MatColorIDGlobalCount ?')
    # print(MaxID)
    scn.deselect(GetBaseShader()[0])
    return MaxID


def ListGrpMaskColorIDSelSet(IDNum):
    scn = modo.scene.current()
    GrpMaskPresence = False
    ListGrpMaskColorID = []
    for item in scn.items(itype='mask', superType=True):
        if item.name.startswith('ColorID_'):
            GrpMaskPresence = True
            ListGrpMaskColorID.append(item.Ident())
    return ListGrpMaskColorID


# print(ListGrpMaskColorIDSelSet(IDNum))


# test if there is already a Grp Mask for that specific desired Color ID
def IsThereTargetGrpMaskColorIDSelSet(ListGrpMaskColorID, IDNum):
    scn = modo.scene.current()
    GrpMaskAlreadyThere = False
    ListTargetGrpMaskState = []
    # print(getTargetGrpMaskName(IDNum))
    IsThereTargetGrpMaskColorIDSelSet = False
    for item in ListGrpMaskColorID:
        scn.select(item)
        for mask in scn.selectedByType('mask'):
            # print(mask.name)
            if mask.name == (getTargetGrpMaskName(IDNum) + " " + "(Material)"):
                IsThereTargetGrpMaskColorIDSelSet = True
                ListTargetGrpMaskState.append(IsThereTargetGrpMaskColorIDSelSet)
        lx.eval('smo.GC.DeselectAll')
    for item in ListTargetGrpMaskState:
        if item:
            GrpMaskAlreadyThere = True
            print('ColorID_%s Group Mask is already is the Shader Tree' % str(IDNum))
    if not GrpMaskAlreadyThere:
        print('No Group Mask called: %s' % ('ColorID_' + str(IDNum)))
        print('We need to create a new one')
    return GrpMaskAlreadyThere, IDNum


# print(IsThereTargetGrpMaskColorIDSelSet(ListGrpMaskColorIDSelSet(IDNum), IDNum))


# test if there is already MaxColorID in the "Base Shader" Render Item by checking the presence of the Channel "MatColorIDGlobalCount"
def ProcessGrp_ColorID(TargetGrpMask, IDNum, baseShad):
    scn = modo.scene.current()
    GrpPresence = False
    GrpTarget = []
    for item in scn.items(itype='mask', superType=True):
        # lx.out('Default Base Shader found:',item)
        if item.name == "Grp_ColorID":
            GrpPresence = True
            # print(item)
            GrpTarget.append(item.Ident())
            # print(GrpTarget[0])
    GrpColorIdent = []
    # print(GrpPresence)
    if not GrpPresence:
        GrpColorID = scn.addItem('mask', name='Grp_ColorID')
        # print(GrpColorID.Ident())
        GrpTarget.append(GrpColorID.Ident())
        GrpColorIdent = GrpColorID.Ident()
        lx.eval('texture.parent {%s} 99 item:{%s}' % (GrpColorIdent, TargetGrpMask))
    if GrpPresence:
        GrpColorIdent = GrpTarget[0]
        # scene.select(GrpTarget[0])
        lx.eval('texture.parent {%s} {%s} item:{%s}' % (GrpColorIdent, IDNum, TargetGrpMask))
    renderItem = scn.renderItem
    AllMasks = []
    for mGrp in renderItem.childrenByType("mask", 1):
        AllMasks.append(mGrp.index)
    # print(max(AllMasks))
    PosID = 0
    PosID = max(AllMasks)
    # print(PosID)
    # if not GrpPresence:
    #     lx.eval('texture.parent {%s} {%s} item:{%s}' % (baseShad, PosID, GrpColorIdent))
    scn.deselect(TargetGrpMask)
    return GrpColorIdent


def SetColorID_DiffuseColor_RGB(IDNum):
    TarCol = ""
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
        try:
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
        except RuntimeError:  # diffuse amount is zero.
            pass
    if IDNum > 16:
        from random import randrange
        r, g, b = [randrange(0, 255, 10) / 255.0 for i in range(3)]
    return TarCol


# print(SetColorID_DiffuseColor_RGB(IDNum))


def SetMaterial(GC_MatShadingModel, GC_OriginalModoMaterialOverride, ColorIDMatName, IDNum):
    GC_OriginalModoMaterialOverride = bool(lx.eval('user.value SMO_UseVal_GC_OriginalModoMaterialOverride ?'))
    GC_MatDefaultSmooAngle = lx.eval('user.value SMO_UseVal_GC_MatDefaultSmooAngle ?')
    GC_WeightByPolyArea = lx.eval('user.value SMO_UseVal_GC_WeightByPolyArea ?')
    scn = modo.scene.current()
    TarCol = SetColorID_DiffuseColor_RGB(IDNum)
    R = (TarCol.split(' ')[0])
    G = (TarCol.split(' ')[1])
    B = (TarCol.split(' ')[2])
    Modo_ver = int(lx.eval('query platformservice appversion ?'))
    # print('Modo Version:', Modo_ver)

    ###### Modo
    if GC_MatShadingModel < 4:
        if not GC_OriginalModoMaterialOverride:
            lx.eval('smo.GC.SetNewMaterialSmartRename 0 {%s} {%s %s %s}' % (ColorIDMatName, R, G, B))
        if GC_OriginalModoMaterialOverride:
            lx.eval('poly.setMaterial {%s} {%s %s %s} 0.8 0.04 true false type:default' % (ColorIDMatName, R, G, B))
            lx.eval('material.new {} true false'.format(ColorIDMatName))
        SetColorOnNode(IDNum)

    ###### Unreal
    if GC_MatShadingModel == 4:
        if not GC_OriginalModoMaterialOverride:
            lx.eval('smo.GC.SetNewMaterialSmartRename 0 {%s} {%s %s %s}' % (ColorIDMatName, R, G, B))
        if GC_OriginalModoMaterialOverride:
            lx.eval('poly.setMaterial {%s} {%s %s %s} 0.8 0.04 true false type:unreal' % (ColorIDMatName, R, G, B))
            lx.eval('material.new {} true false unreal'.format(ColorIDMatName))
        SetColorOnNode(IDNum)

    ###### Unity
    if GC_MatShadingModel == 5:
        if not GC_OriginalModoMaterialOverride:
            lx.eval('smo.GC.SetNewMaterialSmartRename 0 {%s} {%s %s %s}' % (ColorIDMatName, R, G, B))
        if GC_OriginalModoMaterialOverride:
            lx.eval('poly.setMaterial {%s} {%s %s %s} 0.8 0.04 true false false type:unity' % (ColorIDMatName, R, G, B))
            lx.eval('material.new {} true false unity'.format(ColorIDMatName))
        SetColorOnNode(IDNum)

    ###### glTF
    if GC_MatShadingModel == 6:
        if not GC_OriginalModoMaterialOverride:
            lx.eval('smo.GC.SetNewMaterialSmartRename 0 {%s} {%s %s %s}' % (ColorIDMatName, R, G, B))
        if GC_OriginalModoMaterialOverride:
            lx.eval('poly.setMaterial {%s} {%s %s %s} 0.8 0.04 true false false type:gltf' % (ColorIDMatName, R, G, B))
            lx.eval('material.new {} true false gltf'.format(ColorIDMatName))
        SetColorOnNode(IDNum)

    ###### AxF
    if GC_MatShadingModel == 7:
        if not GC_OriginalModoMaterialOverride:
            lx.eval('smo.GC.SetNewMaterialSmartRename 0 {%s} {%s %s %s}' % (ColorIDMatName, R, G, B))
        if GC_OriginalModoMaterialOverride:
            lx.eval('poly.setMaterial {%s} {%s %s %s} 0.8 0.04 true false type:axf' % (ColorIDMatName, R, G, B))
            lx.eval('material.new {} true false axf'.format(ColorIDMatName))
        SetColorOnNode(IDNum)

    ###### Modo Shader
    if GC_MatShadingModel < 4:
        for mask in scn.selectedByType('mask'):
            for child in mask.childrenByType('advancedMaterial'):
                child.name = ColorIDMatName.format(mask.name)
                scn.select(child)
                SetColorOnNode(IDNum)

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
            scn.deselect(Mat_ModelName)
        if GC_MatShadingModel == 4 and itemType != "unrealShader":
            scn.deselect(Mat_ModelName)
        if GC_MatShadingModel == 5 and itemType != "unityShader":
            scn.deselect(Mat_ModelName)
        if GC_MatShadingModel == 6 and itemType != "glTFShader":
            scn.deselect(Mat_ModelName)
        if GC_MatShadingModel == 7 and itemType != "AxFShader":
            scn.deselect(Mat_ModelName)


def ReorderMaskInGrp_ColorID():
    # List only "Grp_ColorID" MAIN GrpMask
    scn = modo.scene.current()
    GrpPresence = False
    GrpTarget = []
    #print(GrpTarget)
    for item in scn.items(itype='mask', superType=True):
        # lx.out('Default Base Shader found:',item)
        if item.name == "Grp_ColorID":
            GrpPresence = True
            # print(item)
            GrpTarget.append(item.Ident())
            # print(GrpTarget[0])
    GrpColorIdent = []
    GrpColorIdent = GrpTarget[0]
    scn.select(GrpTarget[0])
    AllColIDMasksName = []
    # print(AllColIDMasksName)
    AllColIDMasksIdent = []
    # print(AllColIDMasksIdent)

    # Get the Maximum Color ID in scurrent Scene
    MaxID = GetColorIDByNumberCheckSceneMaxColorID()
    #print('Maximum Color ID in scurrent Scene is: %s' % MaxID)

    # Get only "Base Shader" Shader Render Item
    Root = GetBaseShader()
    # print(Root)

    # List All and only "ColorID_" Childs GrpMask
    index = 0
    for item in xrange(0, int(GetColorIDByNumberCheckSceneMaxColorID())):
        # print(item)
        getTargetGrpMaskName(index)
        for mask in scn.items(itype='mask', superType=True):
            # print(mask.name)
            if mask.name == (getTargetGrpMaskName(index) + " " + "(Material)"):
                if mask.name.startswith('ColorID_'):
                    # print(mask.name)
                    AllColIDMasksName.append(mask.name)
                    AllColIDMasksIdent.append(mask.Ident())
        index += 1
    # print(AllColIDMasksName)
    # print(AllColIDMasksIdent)

    # scn.select(AllColIDMasksIdent[0])


    # Group all the ColorID GrpMAsk under a temp GrpMask Folder in order to reparrent those back into 'Grp_ColorID' GrpMask
    scn.select(Root[0])
    TEMP_GrpMask = []
    lx.eval('shader.create mask')
    lx.eval('item.name TEMP_GROUP mask')
    for mask in scn.items(itype='mask', superType=True):
        # print(mask.name)
        if mask.name.startswith('TEMP_GROUP'):
            # print(mask.Ident())
            TEMP_GrpMask.append(mask.Ident())
    scn.deselect(TEMP_GrpMask[0])

    # parent targeted ColorIDGrpMask in that TEMP_GROUP
    indexB = 0
    for maskitem in AllColIDMasksIdent:
        scn.select(maskitem)
        lx.eval('texture.parent {%s} {%s} item:{%s}' % (TEMP_GrpMask[0], indexB, maskitem))
        indexB += 1

    scn.select(GrpColorIdent)

    indexC = 0
    for maskitem in AllColIDMasksIdent:
        scn.select(maskitem)
        lx.eval('texture.parent {%s} {%s} item:{%s}' % (GrpColorIdent, indexC, maskitem))
        indexC += 1

    scn.select(TEMP_GrpMask[0])
    lx.eval('!delete')



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

    def basic_Enable(self, msg):
        return True

    def basic_Execute(self, msg, flags):
        scn = modo.scene.current()

        # ------------------------------ #
        # <----( DEFINE VARIABLES )----> #
        # ------------------------------ #
        # ---------  Check User Values  ------- #
        GC_OriginalModoMaterialOverride = bool(lx.eval('user.value SMO_UseVal_GC_OriginalModoMaterialOverride ?'))
        GC_MatDefaultSmooAngle = lx.eval('user.value SMO_UseVal_GC_MatDefaultSmooAngle ?')
        GC_WeightByPolyArea = lx.eval('user.value SMO_UseVal_GC_WeightByPolyArea ?')

        # Override for creating Modo Materials.
        # GC_MatShadingModel = lx.eval('user.value SMO_UseVal_GC_MatShadingModel ?')
        GC_MatShadingModel = 3

        # Check Current status of SMO SmartMaterial to turn it to TRUE if needed
        SMO_UseVal_GC_OriginalModoMaterialOverride = bool()
        SMO_UseVal_GC_OriginalModoMaterialOverride = lx.eval('user.value SMO_UseVal_GC_OriginalModoMaterialOverride ?')
        if SMO_UseVal_GC_OriginalModoMaterialOverride:
            lx.eval('user.value SMO_UseVal_GC_OriginalModoMaterialOverride false')
        SMO_UseVal_GC_MatNameSuffix = ""
        SMO_UseVal_GC_MatNameSuffix = lx.eval('user.value SMO_UseVal_GC_MatNameSuffix ?')
        if SMO_UseVal_GC_MatNameSuffix != "":
            lx.eval('user.value SMO_UseVal_GC_MatNameSuffix ""')

        ByItemMode = bool()

        if self.SelModeItem:
            lx.eval('smo.MASTER.ForceSelectMeshItemOnly')
            lx.eval('select.type polygon')
            lx.eval('select.all')
            ByItemMode = True

        if self.SelModePoly:
            lx.eval('smo.MASTER.ForceSelectMeshItemOnly')
            ByItemMode = False

        try:
            #####--- Define User Value for Count --- START ---#####
            #####
            # Create a user value that define the ID Number for the Command.
            lx.eval("user.defNew name:IDNumber type:integer life:momentary")
            # Set the title name for the dialog window
            lx.eval('user.def IDNumber dialogname "SMO QT - Color ID - IDNumber"')
            # Set the input field name for the value that the users will see
            lx.eval("user.def IDNumber username {Set the Color ID Number}")
            # The '?' before the user.value calls a popup to have the user set the value
            lx.eval("?user.value IDNumber")
            # Now that the user set the value, i can query it
            UserInput_IDNumber = lx.eval("user.value IDNumber ?")
            lx.out('User ID Number:', UserInput_IDNumber)
            IDNum = UserInput_IDNumber
        except:
            pass

        lx.out('MODE USER ACTIVATED: Set you own ID Number')

        # mesh = scene.selectedByType('mesh')[0]
        # CsPolys = len(mesh.geometry.polygons.selected)
        meshes = scn.selectedByType('mesh')
        lx.eval('query layerservice layer.id ? main')  # select main layer
        ItemUniqueName = lx.eval(
            'query layerservice layer.id ? main')  # store the Unique name of the current mesh layer
        # lx.out('Item Unique Name:', ItemUniqueName)

        print(getTargetGrpMaskName(IDNum))

        print('---')
        print(ListGrpMaskColorIDSelSet(IDNum))

        print('---')
        print(IsThereTargetGrpMaskColorIDSelSet(ListGrpMaskColorIDSelSet(IDNum), IDNum))

        # scn.select(meshes)

        print(SetColorIDByNumberCheckSceneMaxColorID(IDNum))
        print('ColorIDCount Channel already exist: %s' % SetColorIDByNumberCheckSceneMaxColorID(IDNum)[0])
        print('ColorIDCount Channel Value is: %s' % SetColorIDByNumberCheckSceneMaxColorID(IDNum)[1])
        print('Base Shader RenderItem call is: %s' % SetColorIDByNumberCheckSceneMaxColorID(IDNum)[2])
        # scn.select(SetColorIDByNumberCheckSceneMaxColorID(IDNum)[2])

        print('---')
        GrpMaskExist = IsThereTargetGrpMaskColorIDSelSet(ListGrpMaskColorIDSelSet(IDNum), IDNum)[0]
        # print(GrpMaskExist)

        scn.select(meshes)

        if not GrpMaskExist:
            SetColorID_DiffuseColor_RGB(IDNum)
            SetMaterial(GC_MatShadingModel, GC_OriginalModoMaterialOverride, getTargetGrpMaskName(IDNum), IDNum)
            for item in scn.items(itype='mask', superType=True):
                if item.name.startswith(str(getTargetGrpMaskName(IDNum))):
                    scn.select(item)
                    TargetGrpMask = ItemIdent()
                    # print(TargetGrpMask)
            ProcessGrp_ColorID(TargetGrpMask, IDNum, GetBaseShader())

        if GrpMaskExist:
            lx.eval('poly.setMaterial name:%s' % str(getTargetGrpMaskName(IDNum)))

        scn.select(meshes)

        if not GrpMaskExist:
            ReorderMaskInGrp_ColorID()

        scn.select(meshes)
        lx.eval('select.type polygon')
        lx.eval('select.drop polygon')

        # SetBack to user preferences the SMO SmartMaterial back to normal.
        if SMO_UseVal_GC_MatNameSuffix != "":
            lx.eval('user.value SMO_UseVal_GC_MatNameSuffix {%s}' % SMO_UseVal_GC_MatNameSuffix)
        if SMO_UseVal_GC_OriginalModoMaterialOverride:
            lx.eval(
                'user.value SMO_UseVal_GC_OriginalModoMaterialOverride %s' % SMO_UseVal_GC_OriginalModoMaterialOverride)
        ###
        scn.select(meshes)

        if self.SelModePoly:
            lx.eval('select.type polygon')

        if ByItemMode:
            lx.eval('select.type item')


lx.bless(SMO_GC_SetMatColorID_ByUser_Cmd, Cmd_Name)

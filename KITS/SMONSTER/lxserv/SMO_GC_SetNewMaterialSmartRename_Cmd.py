# python
# ---------------------------------------
# Name:         SMO_GC_SetNewMaterialSmartRename_Cmd.py
# Version:      1.0
#
# Purpose:      This script is designed to
#               Create a New Material Tag, rename the Material Layer in Shader tree according to Group Material name with a "_Mat" Suffix and show up Color Picker for setting Diffuse Color Channel.
#               It replace default command: "poly.setMaterial"
#
#
# Author:       Franck ELISABETH
# Website:      http://www.smoluck.com
#
# Created:      11/10/2021
# Copyright:    (c) Franck Elisabeth 2017-2022
# ---------------------------------------

import lx, lxu, modo

Command_Name = "smo.GC.SetNewMaterialSmartRename"
# smo.GC.SetNewMaterialSmartRename {MetalRust} {0.1 0.5 1.0}

def SetMatNameDialog():
    lx.eval('!user.defNew MatNameStr string momentary')
    lx.eval('user.def MatNameStr username "Set New Material Name"')
    lx.eval('user.def MatNameStr dialogname "Set New Material Name"')
    try:
        lx.eval('user.value MatNameStr')
        return lx.eval('user.value MatNameStr ?')
    except:
        return ''


class SMO_GC_SetNewMaterialSmartRename_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
        self.dyna_Add("Material Name", lx.symbol.sTYPE_STRING)      # this define the Name of the new Material.
        self.basic_SetFlags(0, lx.symbol.fCMDARG_OPTIONAL)          # here the (0) define the argument index.
        self.dyna_Add("Fill Color", lx.symbol.sTYPE_COLOR)          # this define the color of the diffuse color.
        self.basic_SetFlags(1, lx.symbol.fCMDARG_OPTIONAL)

    def cmd_Flags(self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO

    def cmd_Interact(self):
        pass

    def cmd_UserName(self):
        return 'SMO GC SetNewMaterialSmartRename'

    def cmd_Desc(self):
        return 'Create a New Material Tag, rename the Material Layer in Shader tree according to Group Material name with a "_Mat" Suffix and show up Color Picker for setting Diffuse Color Channel.'

    def cmd_Tooltip(self):
        return 'Create a New Material Tag, rename the Material Layer in Shader tree according to Group Material name with a "_Mat" Suffix and show up Color Picker for setting Diffuse Color Channel.'

    def cmd_Help(self):
        return 'https://twitter.com/sm0luck'

    def basic_ButtonName(self):
        return 'SMO GC SetNewMaterialSmartRename'

    def cmd_Flags(self):
        return lx.symbol.fCMD_UNDO

    def basic_Enable(self, msg):
        return True

    def basic_Execute(self, msg, flags):
        Modo_ver = int(lx.eval('query platformservice appversion ?'))
        lx.out('Modo Version:', Modo_ver)
        scene = modo.Scene()

        ###########  Check User Values  ###########
        GC_OriginalModoMaterialOverride =  bool(lx.eval('user.value SMO_UseVal_GC_OriginalModoMaterialOverride ?'))
        GC_MatDefaultSmooAngle = lx.eval('user.value SMO_UseVal_GC_MatDefaultSmooAngle ?')
        GC_WeightByPolyArea = lx.eval('user.value SMO_UseVal_GC_WeightByPolyArea ?')
        GC_MatShadingModel = lx.eval('user.value SMO_UseVal_GC_MatShadingModel ?')
        GC_ConstantColorOverride = bool(lx.eval('user.value SMO_UseVal_GC_ConstantColorOverride ?'))
        GC_MatNameSuffix = lx.eval('user.value SMO_UseVal_GC_MatNameSuffix ?')
        # print(GC_MatNameSuffix)
        Const_Suffix = "Constant"
        r = float()
        g = float()
        b = float()

        if self.dyna_String(0):
            material_name = self.dyna_String(0)
        if self.dyna_String(1):
            material_name = self.dyna_String(0)
        if self.dyna_String(1) and self.dyna_String(0):
            GC_OriginalModoMaterialOverride = False


        if GC_OriginalModoMaterialOverride == True:
            lx.eval('poly.setMaterial')

        if GC_OriginalModoMaterialOverride == False:

            if self.dyna_String(0) and self.dyna_String(1):
                if self.dyna_String(0):
                    print(self.dyna_String(0))
                    material_name = self.dyna_String(0)
                if self.dyna_String(1):
                    print(self.dyna_String(1))
                    TarCol = self.dyna_String(1)
                    print('Target Color is: %s' % TarCol)
                    r = TarCol.split(' ')[0]
                    g = TarCol.split(' ')[1]
                    b = TarCol.split(' ')[2]

            elif not self.dyna_String(0):
                material_name = SetMatNameDialog()

            print('----------')
            print('Target Material Name is : %s'% material_name)
            print('Target Color: R: %s , G: %s , B: %s' % (r, g, b))
            print('----------')

            Separator = lx.eval('pref.value application.indexStyle ?')
            if Separator == "none":
                Sep = ""
                Text = GC_MatNameSuffix + material_name
            if Separator == "sp":
                Sep = " "
                Text = GC_MatNameSuffix + Sep + material_name
            if Separator == "uscore":
                Sep = "_"
                Text = GC_MatNameSuffix + Sep + material_name
            if Separator == "brak":
                SepA = "("
                SepB = ")"
                Text = GC_MatNameSuffix + SepA + material_name + SepB
            if Separator == "brak-sp":
                SepA = " ("
                SepB = ") "
                Text = GC_MatNameSuffix + SepA + material_name + SepB
            # print(Text)

            if material_name != '' and material_name != None:
                ###### Modo
                if GC_MatShadingModel < 4:
                    if self.dyna_String(0) and self.dyna_String(1):
                        lx.eval('poly.setMaterial {%s} {%s %s %s} 0.8 0.04 true false type:default' % (material_name, r, g, b))
                    else:
                        lx.eval('poly.setMaterial {%s} {0.6 0.6 0.6} 0.8 0.04 true false type:default' % material_name)
                        lx.eval('material.new {} true false'.format(material_name))
                ###### Unreal
                if GC_MatShadingModel == 4:
                    if self.dyna_String(0) and self.dyna_String(1):
                        lx.eval('poly.setMaterial {%s} {%s %s %s} 0.8 0.04 true false type:unreal' % (material_name, r, g, b))
                    else:
                        lx.eval('poly.setMaterial {%s} {0.6 0.6 0.6} 0.8 0.04 true false type:unreal' % material_name)
                        lx.eval('material.new {} true false unreal'.format(material_name))
                ###### Unity
                if GC_MatShadingModel == 5:
                    if self.dyna_String(0) and self.dyna_String(1):
                        lx.eval('poly.setMaterial {%s} {%s %s %s} 0.8 0.04 true false false type:unity' % (material_name, r, g, b))
                    else:
                        lx.eval('poly.setMaterial {%s} {1.0 1.0 1.0} 0.8 0.04 true false false type:unity' % material_name)
                        lx.eval('material.new {} true false unity'.format(material_name))
                ###### glTF
                if GC_MatShadingModel == 6:
                    if self.dyna_String(0) and self.dyna_String(1):
                        lx.eval('poly.setMaterial {%s} {%s %s %s} 0.8 0.04 true false false type:gltf' % (material_name, r, g, b))
                    else:
                        lx.eval('poly.setMaterial {%s} {0.6 0.6 0.6} 0.8 0.04 true false false type:gltf' % material_name)
                        lx.eval('material.new {} true false gltf'.format(material_name))
                ###### AxF
                if GC_MatShadingModel == 7:
                    if self.dyna_String(0) and self.dyna_String(1):
                        lx.eval('poly.setMaterial {%s} {%s %s %s} 0.8 0.04 true false false type:gltf' % (material_name, r, g, b))
                    else:
                        lx.eval('poly.setMaterial {%s} {0.6 0.6 0.6} 0.8 0.04 true false type:axf' % material_name)
                        lx.eval('material.new {} true false axf'.format(material_name))

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



                        lx.eval('select.color "item.channel advancedMaterial$diffCol ?"')
                        if not self.dyna_String(1):
                            lx.eval('layout.window ColorPickerPopover true')

            ###### Unreal Unity glTF AxF
            if GC_MatShadingModel >= 4:
                for mask in scene.selectedByType('mask'):
                    #######################################################
                    if GC_MatShadingModel == 4:
                        for child in mask.childrenByType('unrealShader'):
                            child.name = Text.format(mask.name)
                            lx.eval('select.color "item.channel unrealShader$base ?"')
                    if GC_MatShadingModel == 5:
                        for child in mask.childrenByType('unityShader'):
                            child.name = Text.format(mask.name)
                            lx.eval('select.color "item.channel unityShader$albedo ?"')
                    if GC_MatShadingModel == 6:
                        for child in mask.childrenByType('glTFShader'):
                            child.name = Text.format(mask.name)
                            lx.eval('select.color "item.channel glTFShader$baseColor ?"')
                    if GC_MatShadingModel == 7:
                        for child in mask.childrenByType('AxFShader'):
                            child.name = Text.format(mask.name)
                    #######################################################

                SelItem = lxu.select.ItemSelection().current()
                print(SelItem)

                for item in SelItem:
                    itemType = modo.Item(item).type
                    print (itemType)
                    Mat_Model = lx.object.Item(item)
                    print (Mat_Model)
                    Mat_ModelName = Mat_Model.UniqueName()
                    print (Mat_ModelName)
                    Mat_ModelID = Mat_Model.Ident()
                    print (Mat_ModelID)
                    #######################################################
                    if GC_MatShadingModel == 4 and itemType != "unrealShader":
                        scene.deselect(Mat_ModelName)
                    if GC_MatShadingModel == 5 and itemType != "unityShader":
                        scene.deselect(Mat_ModelName)
                    if GC_MatShadingModel == 6 and itemType != "glTFShader":
                        scene.deselect(Mat_ModelName)
                    if GC_MatShadingModel == 7 and itemType != "AxFShader":
                        scene.deselect(Mat_ModelName)

                MaterialItemLX = lxu.select.ItemSelection().current()
                for item in MaterialItemLX:
                    # itemType = modo.Item(item).type
                    # print (itemType)
                    MaterialItem = lx.object.Item(item)
                    print (MaterialItem)
                    MaterialItemName = MaterialItem.UniqueName()
                    print (MaterialItemName)
                    MaterialItemID = MaterialItem.Ident()
                    print (MaterialItemID)

                lx.eval('smo.GC.DeselectAll')
                # scene.select(MaterialItemName)
                scene.select(SelItem)

                ###### Unreal
                if GC_MatShadingModel == 4:
                    for item in SelItem:
                        itemType = modo.Item(item).type
                        print (itemType)
                        Mat_Model = lx.object.Item(item)
                        print (Mat_Model)
                        Mat_ModelName = Mat_Model.UniqueName()
                        print (Mat_ModelName)
                        Mat_ModelID = Mat_Model.Ident()
                        print (Mat_ModelID)
                        if itemType != "unrealShader":
                            scene.deselect(Mat_ModelName)
                        if itemType == "unrealShader":
                            # lx.eval('smo.GC.DeselectAll')
                            lx.eval('select.channel {%s:base.R} set' % Mat_ModelID)
                            r = lx.eval('channel.value ? channel:{%s:base.R}' % Mat_ModelID)
                            print (r)
                            lx.eval('select.channel {%s:base.G} set' % Mat_ModelID)
                            g = lx.eval('channel.value ? channel:{%s:base.G}' % Mat_ModelID)
                            print (g)
                            lx.eval('select.channel {%s:base.B} set' % Mat_ModelID)
                            b = lx.eval('channel.value ? channel:{%s:base.B}' % Mat_ModelID)
                            print (b)

                ###### Unity
                if GC_MatShadingModel == 5:
                    for item in SelItem:
                        itemType = modo.Item(item).type
                        print (itemType)
                        Mat_Model = lx.object.Item(item)
                        print (Mat_Model)
                        Mat_ModelName = Mat_Model.UniqueName()
                        print (Mat_ModelName)
                        Mat_ModelID = Mat_Model.Ident()
                        print (Mat_ModelID)
                    if itemType != "unityShader":
                        scene.deselect(Mat_ModelName)
                    if itemType == "unityShader":
                        # lx.eval('smo.GC.DeselectAll')
                        lx.eval('select.channel {%s:base.R} set' % Mat_ModelID)
                        r = lx.eval('channel.value ? channel:{%s:albedo.R}' % Mat_ModelID)
                        print (r)
                        lx.eval('select.channel {%s:base.G} set' % Mat_ModelID)
                        g = lx.eval('channel.value ? channel:{%s:albedo.G}' % Mat_ModelID)
                        print (g)
                        lx.eval('select.channel {%s:base.B} set' % Mat_ModelID)
                        b = lx.eval('channel.value ? channel:{%s:albedo.B}' % Mat_ModelID)
                        print (b)

                ###### glTF
                if GC_MatShadingModel == 6:
                    for item in SelItem:
                        itemType = modo.Item(item).type
                        print (itemType)
                        Mat_Model = lx.object.Item(item)
                        print (Mat_Model)
                        Mat_ModelName = Mat_Model.UniqueName()
                        print (Mat_ModelName)
                        Mat_ModelID = Mat_Model.Ident()
                        print (Mat_ModelID)
                    if itemType != "glTFShader":
                        scene.deselect(Mat_ModelName)
                    if itemType == "glTFShader":
                        # lx.eval('smo.GC.DeselectAll')
                        lx.eval('select.channel {%s:baseColor.R} set' % Mat_ModelID)
                        r = lx.eval('channel.value ? channel:{%s:baseColor.R}' % Mat_ModelID)
                        print (r)
                        lx.eval('select.channel {%s:baseColor.G} set' % Mat_ModelID)
                        g = lx.eval('channel.value ? channel:{%s:baseColor.G}' % Mat_ModelID)
                        print (g)
                        lx.eval('select.channel {%s:baseColor.B} set' % Mat_ModelID)
                        b = lx.eval('channel.value ? channel:{%s:baseColor.B}' % Mat_ModelID)
                        print (b)

                ###### AxF
                if GC_MatShadingModel == 7:
                    for item in SelItem:
                        itemType = modo.Item(item).type
                        print (itemType)
                        Mat_Model = lx.object.Item(item)
                        print (Mat_Model)
                        Mat_ModelName = Mat_Model.UniqueName()
                        print (Mat_ModelName)
                        Mat_ModelID = Mat_Model.Ident()
                        print (Mat_ModelID)
                    if itemType != "AxFShader":
                        scene.deselect(Mat_ModelName)

                        #   from random import randrange
                        #   r, g, b = [randrange(0, 255, 10) / 255.0 for i in range(3)]

                if GC_MatShadingModel >= 4 and GC_ConstantColorOverride == True:
                    lx.eval('shader.create constant')
                    Const_item = lxu.select.ItemSelection().current()
                    for item in Const_item:
                        Const_item = lx.object.Item(item)
                        Const_Name = Const_item.UniqueName()
                        print (Const_Name)
                        Const_ID = Const_item.Ident()
                        print (Const_ID)
                    try:
                        ColorIDConstantName = ("%s_%s" % (Const_Suffix, material_name))
                        lx.eval('item.name %s constant' % ColorIDConstantName)
                    except RuntimeError:  # diffuse amount is zero.
                        pass
                        #        from random import randrange
                        #        r, g, b = [randrange(0, 255, 10) / 255.0 for i in range(3)]

                lx.eval('smo.GC.DeselectAll')

                ###### Unreal
                if GC_MatShadingModel == 4:
                    scene.select(MaterialItemName)
                    lx.eval('select.channel {%s:base.R} set' % MaterialItemName)
                    lx.eval('select.subItem %s add' % Const_ID)
                    lx.eval('select.channel {%s:color.R} add' % Const_ID)
                    lx.eval('channel.link toggle')
                    lx.eval('smo.GC.DeselectAll')

                    scene.select(MaterialItemName)
                    lx.eval('select.channel {%s:base.G} set' % MaterialItemName)
                    lx.eval('select.subItem %s add' % Const_ID)
                    lx.eval('select.channel {%s:color.G} add' % Const_ID)
                    lx.eval('channel.link toggle')
                    lx.eval('smo.GC.DeselectAll')

                    scene.select(MaterialItemName)
                    lx.eval('select.channel {%s:base.B} set' % MaterialItemName)
                    lx.eval('select.subItem %s add' % Const_ID)
                    lx.eval('select.channel {%s:color.B} add' % Const_ID)
                    lx.eval('channel.link toggle')
                    lx.eval('smo.GC.DeselectAll')

                    scene.select(MaterialItemName)
                    lx.eval('select.color "item.channel unrealShader$base ?"')
                    if not self.dyna_String(1):
                        lx.eval('layout.window ColorPickerPopover true')

                ###### Unity
                if GC_MatShadingModel == 5:
                    scene.select(MaterialItemName)
                    lx.eval('select.channel {%s:albedo.R} set' % MaterialItemName)
                    lx.eval('select.subItem %s add' % Const_ID)
                    lx.eval('select.channel {%s:color.R} add' % Const_ID)
                    lx.eval('channel.link toggle')
                    lx.eval('smo.GC.DeselectAll')

                    scene.select(MaterialItemName)
                    lx.eval('select.channel {%s:albedo.G} set' % MaterialItemName)
                    lx.eval('select.subItem %s add' % Const_ID)
                    lx.eval('select.channel {%s:color.G} add' % Const_ID)
                    lx.eval('channel.link toggle')
                    lx.eval('smo.GC.DeselectAll')

                    scene.select(MaterialItemName)
                    lx.eval('select.channel {%s:albedo.B} set' % MaterialItemName)
                    lx.eval('select.subItem %s add' % Const_ID)
                    lx.eval('select.channel {%s:color.B} add' % Const_ID)
                    lx.eval('channel.link toggle')
                    lx.eval('smo.GC.DeselectAll')

                    scene.select(MaterialItemName)
                    lx.eval('select.color "item.channel unityShader$albedo ?"')
                    if not self.dyna_String(1):
                        lx.eval('layout.window ColorPickerPopover true')

                ###### glTF
                if GC_MatShadingModel == 6:
                    scene.select(MaterialItemName)
                    lx.eval('select.channel {%s:baseColor.R} set' % MaterialItemName)
                    lx.eval('select.subItem %s add' % Const_ID)
                    lx.eval('select.channel {%s:color.R} add' % Const_ID)
                    lx.eval('channel.link toggle')
                    lx.eval('smo.GC.DeselectAll')

                    scene.select(MaterialItemName)
                    lx.eval('select.channel {%s:baseColor.G} set' % MaterialItemName)
                    lx.eval('select.subItem %s add' % Const_ID)
                    lx.eval('select.channel {%s:color.G} add' % Const_ID)
                    lx.eval('channel.link toggle')
                    lx.eval('smo.GC.DeselectAll')

                    scene.select(MaterialItemName)
                    lx.eval('select.channel {%s:baseColor.B} set' % MaterialItemName)
                    lx.eval('select.subItem %s add' % Const_ID)
                    lx.eval('select.channel {%s:color.B} add' % Const_ID)
                    lx.eval('channel.link toggle')
                    lx.eval('smo.GC.DeselectAll')

                    scene.select(MaterialItemName)
                    lx.eval('select.color "item.channel glTFShader$baseColor ?"')
                    if not self.dyna_String(1):
                        lx.eval('layout.window ColorPickerPopover true')

                ###### AxF
                if GC_MatShadingModel == 7:
                    scene.select(MaterialItemName)
                    lx.eval('select.channel {%s:baseColor.R} set' % MaterialItemName)
                    lx.eval('select.subItem %s add' % Const_ID)
                    lx.eval('select.channel {%s:color.R} add' % Const_ID)
                    lx.eval('channel.link toggle')
                    lx.eval('smo.GC.DeselectAll')

                    scene.select(MaterialItemName)
                    lx.eval('select.channel {%s:baseColor.G} set' % MaterialItemName)
                    lx.eval('select.subItem %s add' % Const_ID)
                    lx.eval('select.channel {%s:color.G} add' % Const_ID)
                    lx.eval('channel.link toggle')
                    lx.eval('smo.GC.DeselectAll')

                    scene.select(MaterialItemName)
                    lx.eval('select.channel {%s:baseColor.B} set' % MaterialItemName)
                    lx.eval('select.subItem %s add' % Const_ID)
                    lx.eval('select.channel {%s:color.B} add' % Const_ID)
                    lx.eval('channel.link toggle')
                    lx.eval('smo.GC.DeselectAll')

                    scene.select(MaterialItemName)
                    lx.eval('select.color "item.channel AxFShader$baseColor ?"')
                    if not self.dyna_String(1):
                        lx.eval('layout.window ColorPickerPopover true')

                ###### AxF as No Color Input except Texture Input

                scene.select(MaterialItemName)

        del (r, g, b, GC_OriginalModoMaterialOverride, GC_MatDefaultSmooAngle, GC_WeightByPolyArea, GC_MatShadingModel, GC_ConstantColorOverride, GC_MatNameSuffix, Const_Suffix)

lx.bless(SMO_GC_SetNewMaterialSmartRename_Cmd, Command_Name)
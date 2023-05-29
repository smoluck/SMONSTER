#python
"""
Name:               SMO_AutoImporter_V3.py

Purpose:            This Script is designed to:
                    Load LowPoly/Cage/HighPoly Meshes from current Modo scene,
                    and create ready to use Bake Project in Marmoset.

Author:             Franck ELISABETH
Website:            https://www.smoluck.com
Created:            15/11/2020
Copyright:          (c) Franck Elisabeth 2017-2022
"""

import json as j
import mset
import os
import tempfile

print('------------SMO_AutoImporter_V3-----------')
# ------------- DEFINE VARIABLES
PathSeparator = "/"
# ---------------------------- #


# PART A ########################## Initialization ########################
###########################################################################
print('LiveLink ------------ Initialization')
# def Get_LL_Data():
########### GET CURRENT Marmoset Toolbag Temporary path folder
with tempfile.TemporaryDirectory() as MarmoTempDir:
    print('Marmoset current Temp path:', MarmoTempDir)
    print(os.path.exists(MarmoTempDir))

# if (os.path.exists(MarmoTempDir)) == True :
########### Build up the Absolute OS Temp path back.
AbsTempDir, MarmoTempFolder = os.path.split(MarmoTempDir)
print(AbsTempDir, MarmoTempFolder, sep="\n")
print('Absolute Temp Path: ', AbsTempDir)

DataExchangeFileName = "SMO_Marmoset_LL_VarData.json"
DataExchangeFilePath = (os.path.join(AbsTempDir + "\\" + DataExchangeFileName))
print('Store Variable Data to File Path:    ', DataExchangeFilePath)
###########################################################################


print('-----------------------------------------------')

# PART B ###################### Read Data from Modo #######################
###########################################################################
# JsonData = open(DataExchangeFilePath, 'rb')
with open(DataExchangeFilePath, 'rb') as JsonData:
    # JsonData = open(DataExchangeFilePath, 'rb')
    # load variables from filename
    DataFromModo = j.load(JsonData)
    print(DataFromModo)
    # print(DataFromModo['DataExchangeFileName'])

print('-----------------------------------------------')
print('LiveLink ----------------------------- Data')
print('Store Variable Data File Name   :   ', (DataFromModo['DataExchangeFileName']))
print('Store Variable Data File Path   :   ', (DataFromModo['DataExchangeFilePath']))
print('-------------------------------------- Details')
print('Modo Scene Name                 :   ', (DataFromModo['SceneName']))
print('Bake Resolution                 :   ', (DataFromModo['MapSize']))
print('Output Bake Image File Format   :   ', (DataFromModo['ImgFileFrmt']))
print('Separator String (Underscore)   :   ', (DataFromModo['SeparatorStr']))
print('Data Output Folder Path         :   ', (DataFromModo['OutputFolder']))

print('LiveLink ----------------------------- Modes')
print('AutoSave Marmoset Scene File    :   ', (DataFromModo['AutoSaveMarmoSceneFile']))
print('AutoBake At Load                :   ', (DataFromModo['AutoBakeAtLoad']))
print('AutoClose Marmoset after bake   :   ', (DataFromModo['AutoCloseMarmo']))

print('LiveLink ------------------------- Mesh Tag Prefix')
print('Mesh Tag Prefix for LowPoly :   ', (DataFromModo['Lowpoly NameTag']))
print('Mesh Tag Prefix for Cage    :   ', (DataFromModo['Cage NameTag']))
print('Mesh Tag Prefix for HighPoly:   ', (DataFromModo['Highpoly NameTag']))

print('LiveLink ------------------------- FBX FileName List')
print('FBX FileName for LowPoly    :   ', (DataFromModo['Lowpoly FBX Filename']))
print('FBX FileName for Cage       :   ', (DataFromModo['Cage FBX Filename']))
print('FBX FileName for HighPoly   :   ', (DataFromModo['Highpoly FBX Filename']))

print('LiveLink ------------------------- FBX FileName List')
print('FBX FilePath for LowPoly    :   ', (DataFromModo['Lowpoly FBX FilePath']))
print('FBX FilePath for Cage       :   ', (DataFromModo['Cage FBX FilePath']))
print('FBX FilePath for HighPoly   :   ', (DataFromModo['Highpoly FBX FilePath']))

print('LiveLink ----------------------------------------- Normal Maps Modes')
print('Flip X - Flip Red channel                 State:', (DataFromModo['NRM_FlipX']))
print('Flip Y - Flip Green channel               State:', (DataFromModo['NRM_FlipY']))
print('Flip Z - Flip Blue channel                State:', (DataFromModo['NRM_FlipZ']))

print('LiveLink ------------------------------------- Maps Bake State List')
print('AO      - Ambient Occlusion          Bake State: ', (DataFromModo['AO State']))
print('AOF     - Ambient Occlusion (Floor)  Bake State: ', (DataFromModo['AOF State']))
print('TSNRM   - Tangent Space Normal       Bake State: ', (DataFromModo['TSNRM State']))
print('OSNRM   - Object Space Normal        Bake State: ', (DataFromModo['OSNRM State']))
print('POS     - Position                   Bake State: ', (DataFromModo['POS State']))
print('CUR     - Curvature                  Bake State: ', (DataFromModo['CUR State']))
print('OBJID   - Object ID                  Bake State: ', (DataFromModo['OBJID State']))
print('THI     - Thickness                  Bake State: ', (DataFromModo['THI State']))
print('MATID   - Material ID                Bake State: ', (DataFromModo['MATID State']))
print('ALBEDO  - Albedo                     Bake State: ', (DataFromModo['ALBEDO State']))
print('UVID    - UV Island ID               Bake State: ', (DataFromModo['UVID State']))

print('LiveLink ----------------------------------------- Maps Name Tag Prefix')
print('AO      - Ambient Occlusion         Name Prefix:', (DataFromModo['AO NameTag']))
print('AOF     - Ambient Occlusion (Floor) Name Prefix:', (DataFromModo['AOF NameTag']))
print('TSNRM   - Tangent Space Normal Map  Name Prefix:', (DataFromModo['TSNRM NameTag']))
print('OSNRM   - Object Space Normal Map   Name Prefix:', (DataFromModo['OSNRM NameTag']))
print('POS     - Position                  Name Prefix:', (DataFromModo['POS NameTag']))
print('CUR     - Curvature                 Name Prefix:', (DataFromModo['CUR NameTag']))
print('OBJID   - Object ID                 Name Prefix:', (DataFromModo['OBJID NameTag']))
print('THI     - Thickness                 Name Prefix:', (DataFromModo['THI NameTag']))
print('MATID   - Material ID               Name Prefix:', (DataFromModo['MATID NameTag']))
print('ALBEDO  - Albedo                    Name Prefix:', (DataFromModo['ALBEDO NameTag']))
print('UVID    - UV Island ID              Name Prefix:', (DataFromModo['UVID NameTag']))

print('LiveLink ----------------------------------------- Maps FileName')
print('               Bake to Scene Subfolder State:   ', (DataFromModo['ScenePathSubfolder']))
print('                          Base Bake FileName:   ', (DataFromModo['BaseBakeFileName']))
print('AO      - Ambient Occlusion         FileName:   ', (DataFromModo['AO Filename']))
print('AOF     - Ambient Occlusion (Floor) FileName:   ', (DataFromModo['AOF Filename']))
print('TSNRM   - Tangent Space Normal Map  FileName:   ', (DataFromModo['TSNRM Filename']))
print('OSNRM   - Object Space Normal Map   FileName:   ', (DataFromModo['OSNRM Filename']))
print('POS     - Position                  FileName:   ', (DataFromModo['POS Filename']))
print('CUR     - Curvature                 FileName:   ', (DataFromModo['CUR Filename']))
print('OBJID   - Object ID                 FileName:   ', (DataFromModo['OBJID Filename']))
print('THI     - Thickness                 FileName:   ', (DataFromModo['THI Filename']))
print('MATID   - Material ID               FileName:   ', (DataFromModo['MATID Filename']))
print('ALBEDO  - Albedo                    FileName:   ', (DataFromModo['ALBEDO Filename']))
print('UVID    - UV Island ID              FileName:   ', (DataFromModo['UVID Filename']))

print('LiveLink ----------------------------------------- Maps FilePath')
print('                          Base Bake FilePath:   ', (DataFromModo['BaseBakeFilePath']))
print('AO      - Ambient Occlusion         FilePath:   ', (DataFromModo['AO FilePath']))
print('AOF     - Ambient Occlusion (Floor) FilePath:   ', (DataFromModo['AOF FilePath']))
print('TSNRM   - Tangent Space Normal Map  FilePath:   ', (DataFromModo['TSNRM FilePath']))
print('OSNRM   - Object Space Normal Map   FilePath:   ', (DataFromModo['OSNRM FilePath']))
print('POS     - Position                  FilePath:   ', (DataFromModo['POS FilePath']))
print('CUR     - Curvature                 FilePath:   ', (DataFromModo['CUR FilePath']))
print('OBJID   - Object ID                 FilePath:   ', (DataFromModo['OBJID FilePath']))
print('THI     - Thickness                 FilePath:   ', (DataFromModo['THI FilePath']))
print('MATID   - Material ID               FilePath:   ', (DataFromModo['MATID FilePath']))
print('ALBEDO  - Albedo                    FilePath:   ', (DataFromModo['ALBEDO FilePath']))
print('UVID    - UV Island ID              FilePath:   ', (DataFromModo['UVID FilePath']))

print('LiveLink ----------------------------------------- Samples Settings')
print('Per Pixel Sample count                    State:', (DataFromModo['PerPixelSample']))
print('Baking AO-Thickness Rays Sample Count     State:', (DataFromModo['RaysSampleCount']))

# JsonData.close()
###########################################################################


print('-----------------------------------------------')


# PART C ###################### Organize Paths ############################
###########################################################################
# Build and join the Subfolder and FBX files back to the OS Temp path
DataFilePath = os.path.join((DataFromModo['OutputFolder']), "MARMO_BAKES")
print (DataFilePath)
# Build and join the Subfolder to save the output Marmoset Scene file
MarmoSceneFilePath = os.path.join((DataFromModo['OutputFolder']), (DataFromModo['SceneName']))
print (MarmoSceneFilePath)

Low_DataFilePath = (DataFromModo['Lowpoly FBX FilePath'])
Cage_DataFilePath = (DataFromModo['Cage FBX FilePath'])
High_DataFilePath = (DataFromModo['Highpoly FBX FilePath'])


OutputBakeName = (DataFromModo['SceneName'])
print('Baked Image Name: ', OutputBakeName)
ImageBakeDataFilePath = os.path.join(DataFilePath, OutputBakeName)
print('Baked Image Path: ', ImageBakeDataFilePath)


# Convert String path to Absolute Path using OS formating
Low_DataFile_AbsPath = os.path.abspath(Low_DataFilePath)
print('LowPoly Absolute Path: ', Low_DataFile_AbsPath)
# lx.out ('LowPoly File Absolute Path: %s' % Low_DataFile_AbsPath)

Cage_DataFile_AbsPath = os.path.abspath(Cage_DataFilePath)
print('Cage Absolute Path: ', Cage_DataFile_AbsPath)
# lx.out ('LowPoly File Absolute Path: %s' % Cage_DataFile_AbsPath)

High_DataFile_AbsPath = os.path.abspath(High_DataFilePath)
print('HighPoly Absolute Path: ', High_DataFile_AbsPath)
# lx.out ('LowPoly File Absolute Path: %s' % High_DataFile_AbsPath)

ImageBakeDataFile_AbsPath = os.path.abspath(ImageBakeDataFilePath)
print('Baked Image Absolute Path: ', ImageBakeDataFile_AbsPath)
# lx.out ('Baked Image Absolute Path: %s' % ImageBakeDataFile_AbsPath)

# Create the Output Base File PSD and save it.
with open((DataFromModo['BaseBakeFilePath']), 'wb') as f:
    print((DataFromModo['BaseBakeFilePath']))
    # b = open((DataFromModo['BaseBakeFilePath']), 'wb')
    # b.close()

# mset.groupObjects(Item_Low, Item_Cage, Item_High)
# Get_LL_Data()
###########################################################################


print('-----------------------------------------------')


# PART B ##################################################################
###########################################################################
# def LoadAndBake():
baker = mset.BakerObject()

###### Find a baker:
for obj in mset.getAllObjects():
    if isinstance(obj, mset.BakerObject):
        baker = obj

# Bake:
if baker != None:
    ###### Load FBX Files via the QuickLoader
    baker.importModel(Low_DataFilePath)
    baker.importModel(Cage_DataFilePath)
    baker.importModel(High_DataFilePath)

    ###### Setting up the baker
    # baker.outputPath = OutputBakeName
    # baker.outputPath = (DataFromModo['BaseBakeFilePath'])
    baker.outputPath = (DataFromModo['BaseBakeFilePath']).replace(os.sep, '/')
    baker.outputBits = 8
    baker.outputSamples = (DataFromModo['PerPixelSample'])

    ###### These settings only apply if texture sets aren't enabled:
    baker.outputWidth = (DataFromModo['MapSize'])
    baker.outputHeight = (DataFromModo['MapSize'])
    baker.edgePadding = "Custom"
    if (DataFromModo['MapSize']) == 256:
        baker.edgePaddingSize = 2
    if (DataFromModo['MapSize']) == 512:
        baker.edgePaddingSize = 4
    if (DataFromModo['MapSize']) == 1024:
        baker.edgePaddingSize = 8
    if (DataFromModo['MapSize']) == 2048:
        baker.edgePaddingSize = 16
    if (DataFromModo['MapSize']) == 4096:
        baker.edgePaddingSize = 32
    if (DataFromModo['MapSize']) == 8192:
        baker.edgePaddingSize = 64

    baker.outputSoften = 0
    baker.useHiddenMeshes = True
    baker.ignoreTransforms = False
    baker.smoothCage = True
    baker.ignoreBackfaces = True
    baker.multipleTextureSets = False

    # If Texture Sets are enabled, then you can set them up as follows:
    # baker.setTextureSetWidth("My Texture Set Name", 256)
    # Or...
    # baker.setTextureSetWidth(0, 256)

    ###### Loading the Base Preset

    baker.loadPreset("SMO_MARMOSET_MODO_LL") # Not Necessary with 4.03 as we set ourselves the maps
    # baker.loadPreset("All")

    # the same file should be available in C:\Users\USER_NAME\AppData\Local\Marmoset Toolbag 4\baker folder. File name must be SMO_MARMOSET_MODO_LL.tbbake
    # Strangely loading the Preset doesn't populate all the slot available in  the UI

    # baker.savePreset("SMO_MARMOSET_MODO_LL")

    ###### Trying to refresh the Bake Maps list.
    baker.getAllMaps()

    ###### Settings up the Maps settings

    AO_Map = baker.getMap("Ambient Occlusion")
    print('Ambient Occlusion Bake State:', (DataFromModo['AO State']))
    if (DataFromModo['AO State']) == 1:
        AO_Map.enabled = True
        AO_Map.resetSuffix()
        AO_Map.suffix = (DataFromModo['AO NameTag'])
        AO_Map.rayCount = (DataFromModo['RaysSampleCount'])
        AO_Map.floorOcclusion = False
    if (DataFromModo['AO State']) == 0:
        AO_Map.enabled = False

    # Bug in 3.08 in API
    # AOF_Map = baker.getMap("Ambient Occlusion (2)")
    # print('AO Floor Bake State:', (DataFromModo['AOF State']))
    # if (DataFromModo['AOF State']) == 1:
    #     AOF_Map.enabled = True
    #     AOF_Map.resetSuffix()
    #     AOF_Map.suffix = "AOF"
    #     AOF_Map.rayCount = (DataFromModo['RaysSampleCount'])
    #     AOF_Map.floorOcclusion = True
    #     AOF_Map.floor = 0.7
    # if (DataFromModo['AOF State']) == 0:
    #     AOF_Map.enabled = False

    TSNRM_Map = baker.getMap("Normals")
    print('Tangent Space Normal Bake State:', (DataFromModo['TSNRM State']))
    if (DataFromModo['TSNRM State']) == 1:
        TSNRM_Map.enabled = True
        TSNRM_Map.resetSuffix()
        TSNRM_Map.suffix = (DataFromModo['TSNRM NameTag'])
        if not (DataFromModo['NRM_FlipX']):
            TSNRM_Map.flipX = False
        if not (DataFromModo['NRM_FlipY']):
            TSNRM_Map.flipY = False
        if not (DataFromModo['NRM_FlipZ']):
            TSNRM_Map.flipZ = False
        if (DataFromModo['NRM_FlipX']):
            TSNRM_Map.flipX = True
        if (DataFromModo['NRM_FlipY']):
            TSNRM_Map.flipY = True
        if (DataFromModo['NRM_FlipZ']):
            TSNRM_Map.flipZ = True
    if (DataFromModo['TSNRM State']) == 0:
        TSNRM_Map.enabled = False

    OSNRM_Map = baker.getMap("Normals (Object)")
    print('Object Space Normal Bake State:', (DataFromModo['OSNRM State']))
    if (DataFromModo['OSNRM State']) == 1:
        OSNRM_Map.enabled = True
        OSNRM_Map.resetSuffix()
        OSNRM_Map.suffix = (DataFromModo['OSNRM NameTag'])
        if not (DataFromModo['NRM_FlipX']):
            OSNRM_Map.flipX = False
        if not (DataFromModo['NRM_FlipY']):
            OSNRM_Map.flipY = False
        if not (DataFromModo['NRM_FlipZ']):
            OSNRM_Map.flipZ = False
        if (DataFromModo['NRM_FlipX']):
            OSNRM_Map.flipX = True
        if (DataFromModo['NRM_FlipY']):
            OSNRM_Map.flipY = True
        if (DataFromModo['NRM_FlipZ']):
            OSNRM_Map.flipZ = True
    if (DataFromModo['OSNRM State']) == 0:
        OSNRM_Map.enabled = False

    POS_Map = baker.getMap("Position")
    print('Position Bake State:', (DataFromModo['POS State']))
    if (DataFromModo['POS State']) == 1:
        POS_Map.enabled = True
        POS_Map.resetSuffix()
        POS_Map.suffix = (DataFromModo['POS NameTag'])
        POS_Map.normalization = "Bounding Sphere"
    if (DataFromModo['POS State']) == 0:
        POS_Map.enabled = False

    CUR_Map = baker.getMap("Curvature")
    print('Curvature Bake State:', (DataFromModo['CUR State']))
    if (DataFromModo['CUR State']) == 1:
        CUR_Map.enabled = True
        CUR_Map.resetSuffix()
        CUR_Map.suffix = (DataFromModo['CUR NameTag'])
        CUR_Map.strength = 1.0
        CUR_Map.dither = True
    if (DataFromModo['CUR State']) == 0:
        CUR_Map.enabled = False

    OBJID_Map = baker.getMap("Object ID")
    print('Object ID Bake State:', (DataFromModo['OBJID State']))
    if (DataFromModo['OBJID State']) == 1:
        OBJID_Map.enabled = True
        OBJID_Map.resetSuffix()
        OBJID_Map.suffix = (DataFromModo['OBJID NameTag'])
    if (DataFromModo['OBJID State']) == 0:
        OBJID_Map.enabled = False

    THI_Map = baker.getMap("Thickness")
    print('Thickness Bake State:', (DataFromModo['THI State']))
    if (DataFromModo['THI State']) == 1:
        THI_Map.enabled = True
        THI_Map.resetSuffix()
        THI_Map.suffix = (DataFromModo['THI NameTag'])
        THI_Map.rayCount = (DataFromModo['RaysSampleCount'])
        THI_Map.dither = True
    if (DataFromModo['THI State']) == 0:
        THI_Map.enabled = False

    MATID_Map = baker.getMap("Material ID")
    print('MATID Bake State:', (DataFromModo['MATID State']))
    if (DataFromModo['MATID State']) == 1:
        MATID_Map.enabled = True
        MATID_Map.resetSuffix()
        MATID_Map.suffix = "MATID"
    if (DataFromModo['MATID State']) == 0:
        MATID_Map.enabled = False

    ALBEDO_Map = baker.getMap("Albedo")
    print('ALBEDO Bake State:', (DataFromModo['ALBEDO State']))
    if (DataFromModo['ALBEDO State']) == 1:
        ALBEDO_Map.enabled = True
        ALBEDO_Map.resetSuffix()
        ALBEDO_Map.suffix = "ALBEDO"
    if (DataFromModo['ALBEDO State']) == 0:
        ALBEDO_Map.enabled = False

    UVID_Map = baker.getMap("UV Island")
    print('UV Island Bake State:', (DataFromModo['UVID State']))
    if (DataFromModo['UVID State']) == 1:
        UVID_Map.enabled = True
        UVID_Map.resetSuffix()
        UVID_Map.suffix = "UVID"
    if (DataFromModo['UVID State']) == 0:
        UVID_Map.enabled = False

    if (DataFromModo['AutoBakeAtLoad']) == 1:
        print("AutoBake: Enabled")
        baker.bake()
    elif (DataFromModo['AutoBakeAtLoad']) == 0:
        print("AutoBake: Disabled")

else:
    print("Could not find baker!")
# LoadAndBake()

###########################################################################
################################################################## PART B #
###########################################################################
print('-----------------------------------------------')

if (DataFromModo['AutoSaveMarmoSceneFile']) == 1:
    print("AutoSave Marmoset Scene: Enabled")
    mset.saveScene(MarmoSceneFilePath)
elif (DataFromModo['AutoSaveMarmoSceneFile']) == 0:
    print("AutoSave Marmoset Scene: Disabled")

if (DataFromModo['AutoCloseMarmo']) == 1:
    print("AutoClose: Enabled")
    quit()
elif (DataFromModo['AutoCloseMarmo']) == 0:
    print("AutoClose: Disabled")
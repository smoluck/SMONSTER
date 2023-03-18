# python
"""
Name:         SMO_LL_MARMOSET_AutoSegmentedExport_Cmd.py

Purpose:      This Command is designed to :
              Export LowPoly/Cage/HighPoly Meshes from current scene,
              based on MTyp Tag, as FBX to MarmosetToolbag temp Folder.
              Create a Texture to store the TSNM.
              Resolution defined by User value in Prefs (in pixel).

Author:       Franck ELISABETH
Website:      https://www.smoluck.com
Modified:     09/07/2020
Copyright:    (c) Franck Elisabeth 2017-2022
"""

import json as j
import sys
import lx
import lxu.command
import lxu.select
import modo
import os
import subprocess
import traceback


python_majorver = sys.version_info.major
# print('the Highest version number 2 for 2.7 release / 3 for 3.7 release')
# print(python_majorver)


Cmd_Name = "smo.LL.MARMOSET.AutoSegmentedExport"


class SMO_MARMOSET_LIVELINK_AutoSegmentedExport_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
        # self.dyna_Add("Map Size", lx.symbol.sTYPE_INTEGER)
        # self.basic_SetFlags (0, lx.symbol.fCMDARG_OPTIONAL)             # here the (0) define the argument index.
        # self.dyna_Add("Explode Pre Pass", lx.symbol.sTYPE_INTEGER)
        # self.basic_SetFlags (1, lx.symbol.fCMDARG_OPTIONAL)
        # self.dyna_Add("Explode Distance By Prefs", lx.symbol.sTYPE_INTEGER)
        # self.basic_SetFlags (2, lx.symbol.fCMDARG_OPTIONAL)

        self.scrp_svc = lx.service.ScriptSys()
        self.sel_svc = lx.service.Selection()
        self.modo_ver = int(lx.eval('query platformservice appversion ?'))

    def cmd_Interact(self):
        pass

    def cmd_UserName(self):
        return 'SMO LL MARMOSET - Export Automatic Segmented FBX'

    def cmd_Desc(self):
        return 'Export LowPoly/Cage/HighPoly Meshes from current scene, based on MTyp Tag, as FBX to MarmosetToolbag temp Folder. Create a Texture to store the TSNM. Resolution defined by Argument in pixel.'

    def cmd_Tooltip(self):
        return 'Export LowPoly/Cage/HighPoly Meshes from current scene, based on MTyp Tag, as FBX to MarmosetToolbag temp Folder. Create a Texture to store the TSNM. Resolution defined by Argument in pixel.'

    def cmd_Help(self):
        return 'https://twitter.com/sm0luck'

    def basic_ButtonName(self):
        return 'SMO LL MARMOSET - Export Automatic Segmented FBX'

    def cmd_Flags(self):
        return lx.symbol.fCMD_UNDO

    def basic_Enable(self, msg):
        return True

    #######################################################################
    ################   MarmosetToolbag Executable   #######################

    # Validate the path to MarmosetToolbag is good.
    def valid_MarmosetToolbagExePath(self, marmosettoolbag_exe_path):
        return ((marmosettoolbag_exe_path != None) and os.path.lexists(marmosettoolbag_exe_path) and (
                    os.path.splitext(marmosettoolbag_exe_path)[1].lower() == '.exe'))

    # Set the path to MarmosetToolbag in a user variable.
    def set_MarmosetToolbagExePath(self, marmosettoolbag_exe_path):
        if self.valid_MarmosetToolbagExePath(marmosettoolbag_exe_path):
            # try:
            # lx.eval ('!!user.defNew name:Smo_MarmosetToolbagExePath type:string life:config')
            # except:
            # pass

            try:
                lx.eval('!!user.value SMO_UseVal_MARMOSET_ExePath {%s}' % marmosettoolbag_exe_path)
            except:
                pass

            return lx.eval1('user.value SMO_UseVal_MARMOSET_ExePath ?') == marmosettoolbag_exe_path
        return False

    # Ask the user for the path to MarmosetToolbag.
    def find_MarmosetToolbagExePath(self):
        default_exe_path = 'C:\Program Files\Marmoset\Toolbag 3\\toolbag.exe'
        if self.set_MarmosetToolbagExePath(default_exe_path):
            return True
        else:
            try:
                lx.eval('dialog.setup fileOpen')
                lx.eval('dialog.title "Select Marmoset Toolbag 3.X or 4.x executable file"')
                lx.eval('dialog.fileTypeCustom format:exe username:{EXE} loadPattern:{*.exe} saveExtension:exe')
                if self.modo_ver == 801:
                    lx.eval('+dialog.open')
                else:
                    lx.eval('dialog.open')
                marmosettoolbag_exe_path = lx.eval1('dialog.result ?')
            except:
                pass
            else:
                if self.set_MarmosetToolbagExePath(marmosettoolbag_exe_path):
                    return True

        lx.out('Failed to define path to MarmosetToolbag executable.')
        return False

    ################   MarmosetToolbag Executable   #######################
    #######################################################################

    # ###########################################################################
    # ################   MarmosetToolbag Scene Template   #######################

    # Validate the path to MarmosetToolbag Scene Template is good.
    # def valid_MarmosetTemplateScenePath (self, marmoset_tbscene_Path):
    # return ((marmoset_tbscene_Path != None) and os.path.lexists (marmoset_tbscene_Path) and (os.path.splitext (marmoset_tbscene_Path)[1].lower () == '.tbscene'))

    # Set the path to MarmosetToolbag in a user variable.
    # def set_MarmosetTemplateScenePath (self, marmoset_tbscene_Path):
    # if self.valid_MarmosetTemplateScenePath (marmoset_tbscene_Path):
    # try:
    # lx.eval ('!!user.defNew name:SMO_UseVal_MARMOSET_ExePath type:string life:config')
    # except:
    # pass

    # try:
    # lx.eval ('!!user.value SMO_UseVal_MARMOSET_TemplateScenePath {%s}' % marmoset_tbscene_Path)
    # except:
    # pass

    # return (lx.eval1 ('user.value SMO_UseVal_MARMOSET_TemplateScenePath ?') == marmoset_tbscene_Path)
    # return False

    # Ask the user for the path to MarmosetToolbag.
    # def find_MarmosetTemplateScenePath (self):
    # HardCoded_TBScene_Path = lx.eval('query platformservice alias ? {kit_SMO_MARMOSET_LIVELINK:Kits/SMO_MARMOSET_LIVELINK/MarmosetToolbag_Scene_Template/MarmosetToolbag_v4_Scene_Template.tbscene}')
    # print (HardCoded_TBScene_Path)
    # default_tbscene_path = HardCoded_TBScene_Path
    # if self.set_MarmosetTemplateScenePath (default_tbscene_path):
    # return True
    # else:
    # try:
    # lx.eval ('dialog.setup fileOpen')
    # lx.eval ('dialog.title "Select MarmosetToolbag Template Scene file"')
    # lx.eval ('dialog.fileTypeCustom format:tbscene username:{tbscene} loadPattern:{*.tbscene} saveExtension:tbscene')
    # if self.modo_ver == 801:
    # lx.eval ('+dialog.open')
    # else:
    # lx.eval ('dialog.open')
    # marmoset_tbscene_Path = lx.eval1 ('dialog.result ?')
    # except:
    # pass
    # else:
    # if self.set_MarmosetTemplateScenePath (marmoset_tbscene_Path):
    # return True

    # lx.out ('Failed to define path to Marmoset Scene Template.')
    # return False
    # ################   MarmosetToolbag Scene Template   #######################
    # ###########################################################################

    # #########################################################################
    # ###################   MarmosetToolbag Python Script   ###################

    # Validate the path to MarmosetToolbag Python Script is good.
    # def valid_MarmosetScriptPath (self, marmoset_python_path):
    # return ((marmoset_python_path != None) and os.path.lexists (marmoset_python_path) and (os.path.splitext (marmoset_python_path)[1].lower () == '.py'))

    # Set the path to Marmoset Python Script in a user variable.
    # def set_MarmosetScriptPath (self, marmoset_python_path):
    # if self.valid_MarmosetScriptPath (marmoset_python_path):

    # try:
    # lx.eval ('!!user.value SMO_UseVal_MARMOSET_ScriptPath {%s}' % marmoset_python_path)
    # except:
    # pass

    # return (lx.eval1 ('user.value SMO_UseVal_MARMOSET_ScriptPath ?') == marmoset_python_path)
    # return False

    # Ask the user for the path to Marmoset Python Script.
    # def find_MarmosetScriptPath (self):
    # default_script_path = lx.eval('query platformservice alias ? {kit_SMO_MARMOSET_LIVELINK:Kits/SMO_MARMOSET_LIVELINK/Marmoset_Script/autoimporter_backup.py}')
    # if self.set_MarmosetScriptPath (default_script_path):
    # return True
    # else:
    # try:
    # lx.eval ('dialog.setup fileOpen')
    # lx.eval ('dialog.title "Select Marmoset Python Script file"')
    # lx.eval ('dialog.fileTypeCustom format:py username:{py} loadPattern:{*.py} saveExtension:py')
    # if self.modo_ver == 801:
    # lx.eval ('+dialog.open')
    # else:
    # lx.eval ('dialog.open')
    # marmoset_python_path = lx.eval1 ('dialog.result ?')
    # except:
    # pass
    # else:
    # if self.set_MarmosetScriptPath (marmoset_python_path):
    # return True

    # lx.out ('Failed to define path to Marmoset Python Script file.')
    # return False
    # ###################   MarmosetToolbag Python Script   ###################
    # #########################################################################

    def recurseToFindFBXMeshes(self, fbx_item, fbx_meshes, mesh_items):
        fbx_item_child_count = fbx_item.SubCount()
        for child_index in range(fbx_item_child_count):
            child = fbx_item.SubByIndex(child_index)
            for x, mesh_item in enumerate(mesh_items):
                if child.Name() == mesh_item.UniqueName():
                    fbx_meshes[x] = child
            self.recurseToFindFBXMeshes(child, fbx_meshes, mesh_items)

    def getUserValue(self, name):
        try:
            valueObj = self.scrp_svc.UserValueLookup(name)
        except:
            return None

        itype = valueObj.Type()
        if itype == lx.symbol.i_TYPE_INTEGER:
            return valueObj.GetInt()
        elif itype == lx.symbol.i_TYPE_STRING:
            return valueObj.GetString()
        elif itype == lx.symbol.i_TYPE_FLOAT:
            return valueObj.GetFlt()

    def storeFBXSettings(self):
        FBX_USERVALUE_PREFIX = 'sceneio.fbx.save.'
        FBX_USERVALUE_COMMAND = 'user.value ' + FBX_USERVALUE_PREFIX
        fbxSettings = {}
        uValCount = self.scrp_svc.UserValueCount()
        for x in range(uValCount):
            try:
                uval = self.scrp_svc.UserValueByIndex(x)
            except IndexError:
                print("Invalid User Value Index: %s (%s total user values)" % (x, uValCount))
            else:
                name = uval.Name()
                if name.startswith('sceneio.fbx.save.'):
                    fbxSettings[name] = self.getUserValue(name)
        return fbxSettings

    def restoreFBXSettings(self, fbxSettings):
        for name, value in fbxSettings.items():
            lx.eval('user.value %s %s' % (name, value))

    def basic_Execute(self, msg, flags):
        ###################################################################
        ###########  Setup Data Management for Marmoset Export  ###########
        # get OS temp dir in order to store Variable Data to be used in Marmoset
        LocalTempFolder = lx.eval('query platformservice path.path ? temp')
        lx.out('Local Temp Path:    ', LocalTempFolder)

        DataExchangeFileName = "SMO_Marmoset_LL_VarData.smo"
        DataExchangeFilePath = (os.path.join(LocalTempFolder + "\\" + DataExchangeFileName))
        lx.out('Store Variable Data to File Path:    ', DataExchangeFilePath)

        # DataExchangeFile_AbsPath = os.path.abspath(DataExchangeFilePath)
        # print('Store Variable Data to File Absolute Path: ', DataExchangeFile_AbsPath)

        # create the file in temp folder
        f = open(DataExchangeFilePath, 'wb')
        ###################################################################

        # ------------------------------------- #
        # ---------  Check User Values  ------- #
        Str_OutBakeFileFrmt = lx.eval1('user.value SMO_UseVal_MARMOSET_OutBakeFileFrmt ?')
        # lx.out ('Output bake file format is set to:    ', Str_OutBakeFileFrmt)
        # name our temp file
        ImgFileFrmt = Str_OutBakeFileFrmt
        SeparatorStr = "_"

        TagImg_AO = lx.eval1('user.value SMO_UseVal_MARMOSET_TagString_AO ?')
        TagImg_AOF = lx.eval1('user.value SMO_UseVal_MARMOSET_TagString_AOF ?')
        TagImg_TSNRM = lx.eval1('user.value SMO_UseVal_MARMOSET_TagString_TSNRM ?')
        TagImg_OSNRM = lx.eval1('user.value SMO_UseVal_MARMOSET_TagString_OSNRM ?')
        TagImg_POS = lx.eval1('user.value SMO_UseVal_MARMOSET_TagString_POS ?')
        TagImg_CUR = lx.eval1('user.value SMO_UseVal_MARMOSET_TagString_CUR ?')
        TagImg_OBJID = lx.eval1('user.value SMO_UseVal_MARMOSET_TagString_OBJID ?')
        TagImg_THI = lx.eval1('user.value SMO_UseVal_MARMOSET_TagString_THI ?')
        TagImg_MATID = lx.eval1('user.value SMO_UseVal_MARMOSET_TagString_MATID ?')
        TagImg_ALBEDO = lx.eval1('user.value SMO_UseVal_MARMOSET_TagString_ALBEDO ?')
        TagImg_UVID = lx.eval1('user.value SMO_UseVal_MARMOSET_TagString_UVID ?')

        # if Smo_Marmoset_ScenePathSubfolder == 1 :
        # SMO_Marmoset_LL_FolderName = "MARMO_BAKES"
        # if Smo_Marmoset_ScenePathSubfolder == 0 :
        SMO_Marmoset_LL_FolderName = "MARMO_BAKES"
        FBXSubFolder = "MARMO_BAKES"

        NameTagLP = lx.eval1('user.value SMO_UseVal_MARMOSET_NameTagString_low ?')
        # lx.out ('Nametag for Lowpoly:    ', NameTagLP)
        NameTagCage = lx.eval1('user.value SMO_UseVal_MARMOSET_NameTagString_cage ?')
        # lx.out ('Nametag for Cage:    ', NameTagCage)
        NameTagHP = lx.eval1('user.value SMO_UseVal_MARMOSET_NameTagString_high ?')
        # lx.out ('Nametag for HighPoly:    ', NameTagHP)

        Bool_AutoSave = lx.eval1('user.value SMO_UseVal_MARMOSET_AutoSaveSceneBeforeProcess ?')
        # lx.out ('AutoSave Scene before Export:    ', Bool_AutoSave)

        Bool_AutoSaveMarmoSceneFile = lx.eval1('user.value SMO_UseVal_MARMOSET_AutoSaveMarmoSceneFile ?')
        # lx.out ('AutoSave Marmoset Scene after Bake:    ', Bool_AutoSaveMarmoSceneFile)

        Bool_AutoBakeAtLoad = lx.eval1('user.value SMO_UseVal_MARMOSET_AutoBakeAtLoad ?')
        # lx.out ('Automatically bake in Marmoset:    ', Bool_AutoBakeAtLoad)

        Bool_AutoCloseMarmo = lx.eval1('user.value SMO_UseVal_MARMOSET_AutoCloseMarmo ?')
        # lx.out ('Automatically Close Marmoset after Autobake:    ', Bool_AutoCloseMarmo)

        # Automatically Create and Set Mikk Tanget Space maps
        Bool_NRMMikkTspace = lx.eval1('user.value SMO_UseVal_MARMOSET_SetMikkTSpace ?')
        # NormalMap channel settings
        Bool_NRMFlipX = lx.eval1('user.value SMO_UseVal_MARMOSET_NRMFlipX ?')
        Bool_NRMFlipY = lx.eval1('user.value SMO_UseVal_MARMOSET_NRMFlipY ?')
        Bool_NRMFlipZ = lx.eval1('user.value SMO_UseVal_MARMOSET_NRMFlipZ ?')

        PerPxSampleCount = lx.eval('user.value SMO_UseVal_MARMOSET_BakingPerPixelSampleCount ?')
        RaysSampleCount = lx.eval('user.value SMO_UseVal_MARMOSET_BakingRaysSampleCount ?')

        # the Freeze Subdivided Poly on High in Preferences. Incremental Save in this Mode
        Smo_Marmoset_FreezeHPSubdiv = lx.eval1('user.value SMO_UseVal_MARMOSET_FreezeHPSubdiv ?')
        # If FBX export are stored Locally in Scene Path Subfolder
        Smo_Marmoset_ScenePathSubfolder = lx.eval1('user.value SMO_UseVal_MARMOSET_ScenePathSubfolder ?')

        SceneName = lx.eval('smo.GC.GetSceneDetail 5 ?')
        # lx.out('Scene File Name:    ', SceneName)

        CurrentScenePath = lx.eval('smo.GC.GetSceneDetail 0 ?')
        # lx.out('Current Scene Full Path:    ', CurrentScenePath)

        if Smo_Marmoset_ScenePathSubfolder == 1:
            SceneFolderPath = lx.eval('smo.GC.GetSceneDetail 4 ?')
            # lx.out('Scene Folder Path (Path Without File and Extension):    ',SceneFolderPath)

        # name our temp file and folder
        OutputMeshFileFrmt = ".fbx"
        KIT = "SMO_Marmoset_LL"
        FileTagKit = "_BAKE"

        image_load_time = 0

        image_export_path_AO = ""
        image_file_name_AO = ""
        image_load_time_AO = 0
        image_save_time_AO = 0

        image_export_path_AOF = ""
        image_file_name_AOF = ""
        image_load_time_AOF = 0
        image_save_time_AOF = 0

        image_export_path_TSNRM = ""
        image_file_name_TSNRM = ""
        image_load_time_TSNRM = 0
        image_save_time_TSNRM = 0

        image_export_path_OSNRM = ""
        image_file_name_OSNRM = ""
        image_load_time_OSNRM = 0
        image_save_time_OSNRM = 0

        image_export_path_POS = ""
        image_file_name_POS = ""
        image_load_time_POS = 0
        image_save_time_POS = 0

        image_export_path_CUR = ""
        image_file_name_CUR = ""
        image_load_time_CUR = 0
        image_save_time_CUR = 0

        image_export_path_OBJID = ""
        image_file_name_OBJID = ""
        image_load_time_OBJID = 0
        image_save_time_OBJID = 0

        image_export_path_THI = ""
        image_file_name_THI = ""
        image_load_time_THI = 0
        image_save_time_THI = 0

        image_export_path_MATID = ""
        image_file_name_MATID = ""
        image_load_time_MATID = 0
        image_save_time_MATID = 0

        image_export_path_ALBEDO = ""
        image_file_name_ALBEDO = ""
        image_load_time_ALBEDO = 0
        image_save_time_ALBEDO = 0

        image_export_path_UVID = ""
        image_file_name_UVID = ""
        image_load_time_UVID = 0
        image_save_time_UVID = 0

        # ------------------------------------- #

        ############  Export FBX DATA  ############
        lx.eval('smo.LL.MARMOSET.ExportFBXBakes')
        # ------------------------------------- #

        scene = modo.scene.current()
        # ------------- ARGUMENTS ------------- #
        MapSize = lx.eval('user.value SMO_UseVal_MARMOSET_OutputBakeRes ?')
        # ExplodePrePass = self.dyna_Int (1)
        # ExplodeDistanceByPrefs = self.dyna_Int (2)
        # ------------------------------------- #

        # if ExplodeDistanceByPrefs == 1 and ExplodePrePass == 1 :
        # lx.eval('smo.GC.DupAndExplodeByDist 1')

        # if ExplodeDistanceByPrefs == 0 and ExplodePrePass == 1 :
        # lx.eval('smo.GC.DupAndExplodeByDist 0')

        Smo_MarmosetToolbagVersion = lx.eval1('user.value SMO_UseVal_MARMOSET_Version ?')

        # fbxSettings = self.storeFBXSettings ()
        # print (fbxSettings)

        # MODO version checks. Different versions have different FBX options.
        if self.modo_ver < 1300:
            lx.out('Requires Modo 13.0 or newer.')
            return

        # Get the selected UV names.
        # selected_uv_names = self.getUVSelection ()
        # if len (selected_uv_names) == 0:
        # lx.out ('No UV maps selected.')
        # return

        if Bool_NRMMikkTspace:
            lx.eval('smo.LL.MARMOSET.CreateMikkTangentBasis')

        # Create Selection Set from Tags to temporary select Lowpoly, Cage or HighPoly meshes to export them.
        lx.eval('smo.GC.CreateDeleteSelSetFromMTypTag 1')

        # Select target LowPoly Meshes via MTyp Tags
        lx.eval('smo.GC.SelectMTypMesh 0')

        # Grab the active layer.
        layer_svc = lx.service.Layer()
        layer_scan = lx.object.LayerScan(layer_svc.ScanAllocate(lx.symbol.f_LAYERSCAN_ACTIVE))
        if not layer_scan.test():
            lx.out('Layerscan failed.')
            return

        # Early out if there are no active layers.
        layer_count = layer_scan.Count()
        if layer_count <= 0:
            lx.out('No active layers.')
            return

        # Grab the relevant meshes and UV maps.
        mesh_items = []
        mesh_uvs = []
        for layer_idx in range(layer_count):
            mesh_item = lx.object.Item(layer_scan.MeshItem(layer_idx))
            if not mesh_item.test():
                lx.out('Failed to get mesh item of layer %s.' % layer_idx)
                continue

            mesh_name = mesh_item.UniqueName()

            mesh = lx.object.Mesh(layer_scan.MeshBase(layer_idx))
            if not mesh.test():
                lx.out('Failed to get mesh of %s.' % mesh_name)
                continue

            # Get the selected UV maps that exist on this model.
            meshmap = lx.object.MeshMap(mesh.MeshMapAccessor())
            if not meshmap.test():
                lx.out('Failed to get meshmap accessor of %s.' % mesh_name)
                continue

            # selected_uv_names_mesh = []
            # for uv_map in selected_uv_names:
            # try:
            # meshmap.SelectByName (lx.symbol.i_VMAP_TEXTUREUV, uv_map)
            # except:
            # pass
            # else:
            # selected_uv_names_mesh.append (uv_map)

            # if len (selected_uv_names_mesh) == 0:
            # lx.out ('%s does not have any of the selected UV maps on it.' % mesh_name)
            # continue

            mesh_items.append(mesh_item)
            # mesh_uvs.append (selected_uv_names_mesh)

        layer_scan.Apply()

        # Select the meshes.
        for x, mesh_item in enumerate(mesh_items):
            if x == 0:
                lx.eval('select.subItem %s set mesh 0 0' % mesh_item.Ident())
            else:
                lx.eval('select.subItem %s add mesh 0 0' % mesh_item.Ident())

        #############################   CHECK   #############################
        ################   MarmosetToolbag Executable Path   ################
        # Smo_MarmosetToolbagExePath = lx.eval1 ('!!user.value SMO_UseVal_MARMOSET_ExePath ?')
        # print (Smo_MarmosetToolbagExePath)

        Smo_MarmosetToolbagExePath = None
        try:
            Smo_MarmosetToolbagExePath = lx.eval1('!!user.value SMO_UseVal_MARMOSET_ExePath ?')
        except:
            if not self.findMarmosetToolbagPath():
                return
        else:
            if not self.valid_MarmosetToolbagExePath(Smo_MarmosetToolbagExePath):
                if not self.findMarmosetToolbagPath():
                    return
                else:
                    Smo_MarmosetToolbagExePath = lx.eval1('!!user.value SMO_UseVal_MARMOSET_ExePath ?')

        if Smo_MarmosetToolbagExePath is None:
            lx.out('Invalid MarmosetToolbag path.')
            return

        # Convert String path to Absolute Path using OS formating
        Smo_MarmosetToolbagExe_AbsPath = os.path.abspath(Smo_MarmosetToolbagExePath)
        # print Smo_MarmosetToolbagExe_AbsPath
        # lx.out ('EXE Absolute Path: %s' % Smo_MarmosetToolbagExe_AbsPath)
        # Smo_MarmosetToolbagExe_AbsPath = Smo_MarmosetToolbagExe_AbsPath.replace('\\', '/')
        # print Smo_MarmosetToolbagExe_AbsPath
        ################   MarmosetToolbag Executable Path   ###############
        ####################################################################

        #############################   CHECK   ############################
        ####################################################################
        ################   MarmosetToolbag Scene Template   ################
        if Smo_MarmosetToolbagVersion == 0:
            HardCoded_TBScene_Path = lx.eval(
                'query platformservice alias ? {kit_SMO_MARMOSET_LIVELINK:MarmosetToolbag_Scene_Template/MarmosetToolbag_v3_Scene_Template.tbscene}')
            # print HardCoded_TBScene_Path
        if Smo_MarmosetToolbagVersion == 1:
            HardCoded_TBScene_Path = lx.eval(
                'query platformservice alias ? {kit_SMO_MARMOSET_LIVELINK:MarmosetToolbag_Scene_Template/MarmosetToolbag_v4_Scene_Template.tbscene}')
            # print HardCoded_TBScene_Path

        lx.eval('user.value SMO_UseVal_MARMOSET_TemplateScenePath {%s}' % HardCoded_TBScene_Path)
        Smo_MarmosetToolbagTemplateScenePath = HardCoded_TBScene_Path

        # Convert String path to Absolute Path using OS formating
        Smo_MarmosetToolbagTemplateScene_AbsPath = os.path.abspath(Smo_MarmosetToolbagTemplateScenePath)
        # print Smo_MarmosetToolbagTemplateScene_AbsPath
        # lx.out ('TBSCENE Absolute Path: %s' % Smo_MarmosetToolbagTemplateScene_AbsPath)
        # Smo_MarmosetToolbagTemplateScene_AbsPath = Smo_MarmosetToolbagTemplateScene_AbsPath.replace('\\', '/')
        # print Smo_MarmosetToolbagTemplateScene_AbsPath

        # Smo_MarmosetToolbagTemplateScenePath = None
        # try:
        # Smo_MarmosetToolbagTemplateScenePath = lx.eval('query platformservice alias ? {kit_SMO_MARMOSET_LIVELINK:MarmosetToolbag_Scene_Template/MarmosetToolbag_v4_Scene_Template.tbscene}')
        # lx.eval('user.value Smo_MarmosetToolbagTemplateScenePath {%s}' % Smo_MarmosetToolbagTemplateScenePath)
        # except:
        # if not self.find_MarmosetTemplateScenePath ():
        # return
        # else:
        # if not self.valid_MarmosetTemplateScenePath (Smo_MarmosetToolbagTemplateScenePath):
        # if not self.find_MarmosetTemplateScenePath ():
        # return
        # else:
        # Smo_MarmosetToolbagTemplateScenePath = lx.eval1 ('!!user.value SMO_UseVal_MARMOSET_TemplateScenePath ?')

        # if Smo_MarmosetToolbagTemplateScenePath is None:
        # lx.out ('Invalid MarmosetToolbagModoKit path.')
        # return
        ################   MarmosetToolbag Scene Template   ################
        ####################################################################

        #############################   CHECK   ############################
        ####################################################################
        ################   MarmosetToolbag Python Script   #################
        if Smo_MarmosetToolbagVersion == 0:
            HardCoded_Script_Path = lx.eval(
                'query platformservice alias ? {kit_SMO_MARMOSET_LIVELINK:Marmoset_Script/SMO_AutoImporter_V3.py}')
            # print HardCoded_Script_Path
        if Smo_MarmosetToolbagVersion == 1:
            HardCoded_Script_Path = lx.eval(
                'query platformservice alias ? {kit_SMO_MARMOSET_LIVELINK:Marmoset_Script/SMO_AutoImporter_V4.py}')
            # print HardCoded_Script_Path

        lx.eval('user.value SMO_UseVal_MARMOSET_ScriptPath {%s}' % HardCoded_Script_Path)
        Smo_MarmosetToolbagScriptPath = HardCoded_Script_Path

        # Convert String path to Absolute Path using OS formating
        Smo_MarmosetToolbagScript_AbsPath = os.path.abspath(Smo_MarmosetToolbagScriptPath)
        # print Smo_MarmosetToolbagScript_AbsPath
        # lx.out ('PY SCRIPT Absolute Path: %s' % Smo_MarmosetToolbagScript_AbsPath)
        # Smo_MarmosetToolbagScript_AbsPath = Smo_MarmosetToolbagScript_AbsPath.replace('\\', '/')
        # print Smo_MarmosetToolbagScript_AbsPath

        # Smo_MarmosetToolbagScriptPath = None
        # try:
        # Smo_MarmosetToolbagScriptPath = lx.eval('query platformservice alias ? {kit_SMO_MARMOSET_LIVELINK:Marmoset_Script/SMO_AutoImporter_V3.py}')
        # lx.eval('user.value Smo_MarmosetToolbagScriptPath {%s}' % Smo_MarmosetToolbagScriptPath)
        # except:
        # if not self.find_MarmosetScriptPath ():
        # return
        # else:
        # if not self.valid_MarmosetScriptPath (Smo_MarmosetToolbagScriptPath):
        # if not self.find_MarmosetScriptPath ():
        # return
        # else:
        # Smo_MarmosetToolbagScriptPath = lx.eval1 ('!!user.value SMO_UseVal_MARMOSET_ScriptPath ?')

        # if Smo_MarmosetToolbagScriptPath is None:
        # lx.out ('Invalid MarmosetScript path.')
        # return
        ################   MarmosetToolbag Python Script   ################
        ###################################################################

        ############################ Export FBX Data #############################

        # Store user's FBX preferences for restoring later.
        # fbxSettings = self.storeFBXSettings ()

        # get modo's temp dir
        OutputFolder = lx.eval('query platformservice path.path ? temp')

        # build up the path for the OutputFolder using the User value to guide wich solution is used.
        if Smo_Marmoset_ScenePathSubfolder == 1:
            OutputFolder = SceneFolderPath
            # OutputFolder = (os.path.join(SceneFolderPath + "\\" + KIT ))
            # lx.out ('Output Folder path:    ', OutputFolder)

        if Smo_Marmoset_ScenePathSubfolder == 0:
            OutputFolder = (os.path.join(LocalTempFolder + "\\" + KIT + "\\" + SceneName))
            # lx.out ('Output Folder path:    ', OutputFolder)

        # name our LowPoly / Cage / HighPoly files
        fbx_file_name_LP = (SceneName + FileTagKit + NameTagLP + OutputMeshFileFrmt)
        # lx.out ('Filename for Lowpoly:    ', fbx_file_name_LP)
        fbx_file_name_Cage = (SceneName + FileTagKit + NameTagCage + OutputMeshFileFrmt)
        # lx.out ('Filename for Cage:    ', fbx_file_name_Cage)
        fbx_file_name_HP = (SceneName + FileTagKit + NameTagHP + OutputMeshFileFrmt)
        # lx.out ('Filename for Cage:    ', fbx_file_name_HP)

        if Smo_Marmoset_ScenePathSubfolder == 0:
            # builds the complete path out of the temp dir/or/ Scene subfolder and the bakes file name
            fbx_export_path_LP = os.path.join(OutputFolder, fbx_file_name_LP)
            lx.out('Lowpoly File Path:    ', fbx_export_path_LP)
            fbx_export_path_Cage = os.path.join(OutputFolder, fbx_file_name_Cage)
            lx.out('Cage File Path:    ', fbx_export_path_Cage)
            fbx_export_path_HP = os.path.join(OutputFolder, fbx_file_name_HP)
            lx.out('Highpoly File Path:    ', fbx_export_path_HP)
        if Smo_Marmoset_ScenePathSubfolder == 1:
            fbx_export_path_LP = os.path.join(OutputFolder, FBXSubFolder, fbx_file_name_LP)
            lx.out('Lowpoly File Path:    ', fbx_export_path_LP)
            fbx_export_path_Cage = os.path.join(OutputFolder, FBXSubFolder, fbx_file_name_Cage)
            lx.out('Cage File Path:    ', fbx_export_path_Cage)
            fbx_export_path_HP = os.path.join(OutputFolder, FBXSubFolder, fbx_file_name_HP)
            lx.out('Highpoly File Path:    ', fbx_export_path_HP)

        #########################################################################################
        ############################# GET User Pref Variable and Mesh Materials if needed #######

        # Selection Lowpoly Meshes
        lx.eval('smo.GC.SelectMTypMesh 0')

        # Get materials Name on current LowPoly Meshes
        MatsOnTargetMesh = lx.eval('smo.GC.GetMaterialListOnMesh ?')
        # lx.out('The Materials on the LowPoly Meshes are:',MatsOnTargetMesh)

        Smo_MarmosetToolbag_AO = lx.eval1('!!user.value SMO_UseVal_MARMOSET_AO ?')
        Smo_MarmosetToolbag_AOF = lx.eval1('!!user.value SMO_UseVal_MARMOSET_AOF ?')
        Smo_MarmosetToolbag_TSNRM = lx.eval1('!!user.value SMO_UseVal_MARMOSET_TSNRM ?')
        Smo_MarmosetToolbag_OSNRM = lx.eval1('!!user.value SMO_UseVal_MARMOSET_OSNRM ?')
        Smo_MarmosetToolbag_POS = lx.eval1('!!user.value SMO_UseVal_MARMOSET_POS ?')
        Smo_MarmosetToolbag_CUR = lx.eval1('!!user.value SMO_UseVal_MARMOSET_CUR ?')
        Smo_MarmosetToolbag_OBJID = lx.eval1('!!user.value SMO_UseVal_MARMOSET_OBJID ?')
        Smo_MarmosetToolbag_THI = lx.eval1('!!user.value SMO_UseVal_MARMOSET_THI ?')
        Smo_MarmosetToolbag_MATID = lx.eval1('!!user.value SMO_UseVal_MARMOSET_MATID ?')
        Smo_MarmosetToolbag_ALBEDO = lx.eval1('!!user.value SMO_UseVal_MARMOSET_ALBEDO ?')
        Smo_MarmosetToolbag_UVID = lx.eval1('!!user.value SMO_UseVal_MARMOSET_UVID ?')

        DefaultTextureName = lx.eval1('!!user.value SMO_UseVal_MARMOSET_DefaultTextureName ?')
        # lx.out('Default Output Marmoset Bake name is: ',DefaultTextureName)
        UseMeshMaterialName = lx.eval1('!!user.value SMO_UseVal_MARMOSET_USE_MeshMaterialName ?')
        # lx.out('Use Material name from Mesh state:',UseMeshMaterialName)

        if DefaultTextureName == "":
            DefaultTextureName = SceneName

        if UseMeshMaterialName == 1:
            TargetMaterialName = MatsOnTargetMesh
            # lx.out('Use Material name from Mesh.')

        if UseMeshMaterialName == 0:
            TargetMaterialName = SceneName
            # lx.out('Use Default Output name.')

        # lx.out('Material Name for Livelink is:',TargetMaterialName)

        # Drop LowPoly meshes
        lx.eval('select.drop item')
        #########################################################################################

        ##
        #####
        ########
        #########################################################
        # Externalized to the First part the FBX Export Procedure

        # For more info look line 332
        #########################################################
        ########
        #####
        ##

        ########################## GET Info of SHADER TREE #############################
        # Drop current item selection Scene wise
        lx.eval('select.clear item')
        lx.eval('select.drop schmNode')
        lx.eval('select.drop channel')
        lx.eval('select.drop link')

        PolyRender = lx.eval('smo.GC.SelectPolyRenderItem ?')
        # lx.out('Render item Identity name is :',PolyRender)
        ShaderItem = lx.eval('smo.GC.SelectShaderItem ?')
        # lx.out('Shader item Identity name is :',ShaderItem)

        ShaderItem_ST_Pos = lx.eval('smo.GC.GetShaderItemPosIndex ?')
        # lx.out('Position Index of the Shader Item (in the Shader Tree) is :',ShaderItem_ST_Pos)
        Texture_ST_Pos = (ShaderItem_ST_Pos - 1)

        lx.eval('select.clear item')
        lx.eval('select.drop schmNode')
        lx.eval('select.drop channel')
        lx.eval('select.drop link')
        ########################## GET Info of SHADER TREE #############################

        image_file_name_AO = TargetMaterialName + SeparatorStr + TagImg_AO + ImgFileFrmt
        image_file_name_AOF = TargetMaterialName + SeparatorStr + TagImg_AOF + ImgFileFrmt
        image_file_name_TSNRM = TargetMaterialName + SeparatorStr + TagImg_TSNRM + ImgFileFrmt
        image_file_name_OSNRM = TargetMaterialName + SeparatorStr + TagImg_OSNRM + ImgFileFrmt
        image_file_name_POS = TargetMaterialName + SeparatorStr + TagImg_POS + ImgFileFrmt
        image_file_name_CUR = TargetMaterialName + SeparatorStr + TagImg_CUR + ImgFileFrmt
        image_file_name_OBJID = TargetMaterialName + SeparatorStr + TagImg_OBJID + ImgFileFrmt
        image_file_name_THI = TargetMaterialName + SeparatorStr + TagImg_THI + ImgFileFrmt
        image_file_name_MATID = TargetMaterialName + SeparatorStr + TagImg_MATID + ImgFileFrmt
        image_file_name_ALBEDO = TargetMaterialName + SeparatorStr + TagImg_ALBEDO + ImgFileFrmt
        image_file_name_UVID = TargetMaterialName + SeparatorStr + TagImg_UVID + ImgFileFrmt

        ImageNameAO = TargetMaterialName + SeparatorStr + TagImg_AO + ':videoStill001'
        ImageNameAOF = TargetMaterialName + SeparatorStr + TagImg_AOF + ':videoStill001'
        ImageNameTSNRM = TargetMaterialName + SeparatorStr + TagImg_TSNRM + ':videoStill001'
        ImageNameOSNRM = TargetMaterialName + SeparatorStr + TagImg_OSNRM + ':videoStill001'
        ImageNamePOS = TargetMaterialName + SeparatorStr + TagImg_POS + ':videoStill001'
        ImageNameCUR = TargetMaterialName + SeparatorStr + TagImg_CUR + ':videoStill001'
        ImageNameOBJID = TargetMaterialName + SeparatorStr + TagImg_OBJID + ':videoStill001'
        ImageNameTHI = TargetMaterialName + SeparatorStr + TagImg_THI + ':videoStill001'
        ImageNameMATID = TargetMaterialName + SeparatorStr + TagImg_MATID + ':videoStill001'
        ImageNameALBEDO = TargetMaterialName + SeparatorStr + TagImg_ALBEDO + ':videoStill001'
        ImageNameUVID = TargetMaterialName + SeparatorStr + TagImg_UVID + ':videoStill001'

        BaseBakeFileName = SceneName + ImgFileFrmt
        if Smo_Marmoset_ScenePathSubfolder == 1:
            BaseBakeFilePath = os.path.join(OutputFolder, SMO_Marmoset_LL_FolderName, BaseBakeFileName)
        if Smo_Marmoset_ScenePathSubfolder == 0:
            BaseBakeFilePath = os.path.join(OutputFolder, BaseBakeFileName)

        ############################ Create AO MAP Image Data #############################
        if Smo_MarmosetToolbag_AO == 1:
            # Select Lowpoly Meshes in order to be sure that the UV Map is set in Texture locator when the image are created.
            lx.eval('smo.GC.SelectMTypMesh 0')
            lx.eval('smo.GC.ClearSelectionVmap 1 0')

            if Smo_Marmoset_ScenePathSubfolder == 1:
                # builds the complete path out of the SceneFolder
                image_export_path_AO = os.path.join(OutputFolder, SMO_Marmoset_LL_FolderName, image_file_name_AO)
            if Smo_Marmoset_ScenePathSubfolder == 0:
                # builds the complete path out of the temp dir and the temp file name
                image_export_path_AO = os.path.join(OutputFolder, image_file_name_AO)

            if not os.path.exists(os.path.dirname(image_export_path_AO)):
                # try to create the directory.
                try:
                    os.makedirs(os.path.dirname(image_export_path_AO))
                except:
                    # if that fails for any reason print out the error
                    print(traceback.format_exc())
            else:
                if image_export_path_AO == None:
                    lx.out('Didn\'t save AO Map Image for MarmosetToolbag.')
                    return
                else:
                    image_export_path_AO = os.path.splitext(image_export_path_AO)[0] + ImgFileFrmt
                    image_file_name_AO = os.path.splitext(os.path.basename(image_export_path_AO))[0]

            # lx.eval('clip.new')
            if MapSize == 512:
                lx.eval('clip.newStill "{}" x512 RGBA false false format:PSD colorspace:(none)'.format(
                    image_export_path_AO))
            if MapSize == 1024:
                lx.eval('clip.newStill "{}" x1024 RGBA false false format:PSD colorspace:(none)'.format(
                    image_export_path_AO))
            if MapSize == 2048:
                lx.eval('clip.newStill "{}" x2048 RGBA false false format:PSD colorspace:(none)'.format(
                    image_export_path_AO))
            if MapSize == 4096:
                lx.eval('clip.newStill "{}" x4096 RGBA false false format:PSD colorspace:(none)'.format(
                    image_export_path_AO))
            lx.eval('clip.addStill "{}"'.format(image_export_path_AO))
            lx.eval('clip.save')

            lx.eval('select.subItem {%s} set textureLayer;mediaClip' % ImageNameAO)
            lx.eval('select.item {%s} add' % ImageNameAO)
            lx.eval('select.type item')
            lx.eval('select.subItem {%s} set mediaClip' % ImageNameAO)
            lx.eval('select.subItem %s set textureLayer;light;render;environment' % PolyRender)
            lx.eval('texture.new clip:{%s}' % ImageNameAO)

            # Parent to Render item to add the texture layer to the ShaderTree
            lx.eval('texture.parent %s %i' % (PolyRender, ShaderItem_ST_Pos))
            # Deselect the Render Item
            lx.eval(
                'select.subItem %s remove ;render;environment;mediaClip;scene;camera;light;locator;bake;textureLayer' % PolyRender)

            # Set Blend Mode / Effect and Opacity
            lx.eval('shader.setEffect diffColor')
            lx.eval('item.channel textureLayer$blend multiply')
            lx.eval('item.channel textureLayer$opacity 0.8')

            # lx.command("select.subItem", item={ImageNameAO}, mode="set")
            image_save_time_AO = os.path.getmtime(image_export_path_AO)

            if Smo_MarmosetToolbag_AO:
                lx.eval('item.channel textureLayer$enable true')
            if not Smo_MarmosetToolbag_AO:
                lx.eval('item.channel textureLayer$enable false')
        # -------------------------------------------- #

        ############################ Create AO MAP Floor Image Data #############################
        if Smo_MarmosetToolbag_AOF == 1:
            # Select Lowpoly Meshes in order to be sure that the UV Map is set in Texture locator when the image are created.
            lx.eval('smo.GC.SelectMTypMesh 0')
            lx.eval('smo.GC.ClearSelectionVmap 1 0')

            if Smo_Marmoset_ScenePathSubfolder == 1:
                # builds the complete path out of the SceneFolder
                image_export_path_AOF = os.path.join(OutputFolder, SMO_Marmoset_LL_FolderName, image_file_name_AOF)
            if Smo_Marmoset_ScenePathSubfolder == 0:
                # builds the complete path out of the temp dir and the temp file name
                image_export_path_AOF = os.path.join(OutputFolder, image_file_name_AOF)

            if not os.path.exists(os.path.dirname(image_export_path_AOF)):
                # try to create the directory.
                try:
                    os.makedirs(os.path.dirname(image_export_path_AOF))
                except:
                    # if that fails for any reason print out the error
                    print(traceback.format_exc())
            else:
                if image_export_path_AOF == None:
                    lx.out('Didn\'t save AO Map (Floor) Image for MarmosetToolbag.')
                    return
                else:
                    image_export_path_AOF = os.path.splitext(image_export_path_AOF)[0] + ImgFileFrmt
                    image_file_name_AOF = os.path.splitext(os.path.basename(image_export_path_AOF))[0]

            # lx.eval('clip.new')
            if MapSize == 512:
                lx.eval(
                    'clip.newStill "{}" x512 RGBA false false format:PSD colorspace:(none)'.format(
                        image_export_path_AOF))
            if MapSize == 1024:
                lx.eval(
                    'clip.newStill "{}" x1024 RGBA false false format:PSD colorspace:(none)'.format(
                        image_export_path_AOF))
            if MapSize == 2048:
                lx.eval(
                    'clip.newStill "{}" x2048 RGBA false false format:PSD colorspace:(none)'.format(
                        image_export_path_AOF))
            if MapSize == 4096:
                lx.eval(
                    'clip.newStill "{}" x4096 RGBA false false format:PSD colorspace:(none)'.format(
                        image_export_path_AOF))
            lx.eval('clip.addStill "{}"'.format(image_export_path_AOF))
            lx.eval('clip.save')

            lx.eval('select.subItem {%s} set textureLayer;mediaClip' % ImageNameAOF)
            lx.eval('select.item {%s} add' % ImageNameAOF)
            lx.eval('select.type item')
            lx.eval('select.subItem {%s} set mediaClip' % ImageNameAOF)
            lx.eval('select.subItem %s set textureLayer;light;render;environment' % PolyRender)
            lx.eval('texture.new clip:{%s}' % ImageNameAOF)

            # Parent to Render item to add the texture layer to the ShaderTree
            lx.eval('texture.parent %s %i' % (PolyRender, ShaderItem_ST_Pos))
            # Deselect the Render Item
            lx.eval(
                'select.subItem %s remove ;render;environment;mediaClip;scene;camera;light;locator;bake;textureLayer' % PolyRender)

            # Set Blend Mode / Effect and Opacity
            lx.eval('shader.setEffect diffColor')
            lx.eval('item.channel textureLayer$blend multiply')
            lx.eval('item.channel textureLayer$opacity 0.8')

            # lx.command("select.subItem", item={ImageNameAOF}, mode="set")
            image_save_time_AOF = os.path.getmtime(image_export_path_AOF)

            if Smo_MarmosetToolbag_AOF:
                lx.eval('item.channel textureLayer$enable true')
            if not Smo_MarmosetToolbag_AOF:
                lx.eval('item.channel textureLayer$enable false')
        # -------------------------------------------- #

        ############################ Create TANGENT SPACE NORMAL MAP Image Data #############################
        if Smo_MarmosetToolbag_TSNRM == 1:
            # Select Lowpoly Meshes in order to be sure that the UV Map is set in Texture locator when the image are created.
            lx.eval('smo.GC.SelectMTypMesh 0')
            lx.eval('smo.GC.ClearSelectionVmap 1 0')

            if Smo_Marmoset_ScenePathSubfolder == 1:
                # builds the complete path out of the SceneFolder
                image_export_path_TSNRM = os.path.join(OutputFolder, SMO_Marmoset_LL_FolderName, image_file_name_TSNRM)
            if Smo_Marmoset_ScenePathSubfolder == 0:
                # builds the complete path out of the temp dir and the temp file name
                image_export_path_TSNRM = os.path.join(OutputFolder, image_file_name_TSNRM)

            if not os.path.exists(os.path.dirname(image_export_path_TSNRM)):
                # try to create the directory.
                try:
                    os.makedirs(os.path.dirname(image_export_path_TSNRM))
                except:
                    # if that fails for any reason print out the error
                    print(traceback.format_exc())
            else:
                if image_export_path_TSNRM == None:
                    lx.out('Didn\'t save Tangent Space Normal Map Image for MarmosetToolbag.')
                    return
                else:
                    image_export_path_TSNRM = os.path.splitext(image_export_path_TSNRM)[0] + ImgFileFrmt
                    image_file_name_TSNRM = os.path.splitext(os.path.basename(image_export_path_TSNRM))[0]

            # lx.eval('clip.new')
            if MapSize == 512:
                lx.eval('clip.newStill "{}" x512 RGBA false false format:PSD colorspace:(none)'.format(
                    image_export_path_TSNRM))
            if MapSize == 1024:
                lx.eval('clip.newStill "{}" x1024 RGBA false false format:PSD colorspace:(none)'.format(
                    image_export_path_TSNRM))
            if MapSize == 2048:
                lx.eval('clip.newStill "{}" x2048 RGBA false false format:PSD colorspace:(none)'.format(
                    image_export_path_TSNRM))
            if MapSize == 4096:
                lx.eval('clip.newStill "{}" x4096 RGBA false false format:PSD colorspace:(none)'.format(
                    image_export_path_TSNRM))
            lx.eval('clip.addStill "{}"'.format(image_export_path_TSNRM))
            lx.eval('clip.save')

            lx.eval('select.subItem {%s} set textureLayer;mediaClip' % ImageNameTSNRM)
            lx.eval('select.item {%s} add' % ImageNameTSNRM)
            lx.eval('select.type item')
            lx.eval('select.subItem {%s} set mediaClip' % ImageNameTSNRM)
            lx.eval('select.subItem %s set textureLayer;light;render;environment' % PolyRender)
            lx.eval('texture.new clip:{%s}' % ImageNameTSNRM)

            # Parent to Render item to add the texture layer to the ShaderTree
            lx.eval('texture.parent %s %i' % (PolyRender, ShaderItem_ST_Pos))
            # Deselect the Render Item
            lx.eval(
                'select.subItem %s remove ;render;environment;mediaClip;scene;camera;light;locator;bake;textureLayer' % PolyRender)

            # Set Blend Mode / Effect and Opacity
            lx.eval('shader.setEffect normal')

            # lx.command("select.subItem", item={ImageNameAO}, mode="set")
            image_save_time_TSNRM = os.path.getmtime(image_export_path_TSNRM)

            if Smo_MarmosetToolbag_TSNRM:
                lx.eval('item.channel textureLayer$enable true')
            if not Smo_MarmosetToolbag_TSNRM:
                lx.eval('item.channel textureLayer$enable false')
        # -------------------------------------------- #

        ############################ Create OBJECT SPACE NORMAL MAP Image Data #############################
        if Smo_MarmosetToolbag_OSNRM == 1:
            # Select Lowpoly Meshes in order to be sure that the UV Map is set in Texture locator when the image are created.
            lx.eval('smo.GC.SelectMTypMesh 0')
            lx.eval('smo.GC.ClearSelectionVmap 1 0')

            if Smo_Marmoset_ScenePathSubfolder == 1:
                # builds the complete path out of the SceneFolder
                image_export_path_OSNRM = os.path.join(OutputFolder, SMO_Marmoset_LL_FolderName, image_file_name_OSNRM)
            if Smo_Marmoset_ScenePathSubfolder == 0:
                # builds the complete path out of the temp dir and the temp file name
                image_export_path_OSNRM = os.path.join(OutputFolder, image_file_name_OSNRM)

            if not os.path.exists(os.path.dirname(image_export_path_OSNRM)):
                # try to create the directory.
                try:
                    os.makedirs(os.path.dirname(image_export_path_OSNRM))
                except:
                    # if that fails for any reason print out the error
                    print(traceback.format_exc())
            else:
                if image_export_path_OSNRM == None:
                    lx.out('Didn\'t save Object Space Normal Map Image for MarmosetToolbag.')
                    return
                else:
                    image_export_path_OSNRM = os.path.splitext(image_export_path_OSNRM)[0] + ImgFileFrmt
                    image_file_name_OSNRM = os.path.splitext(os.path.basename(image_export_path_OSNRM))[0]

            # lx.eval('clip.new')
            if MapSize == 512:
                lx.eval('clip.newStill "{}" x512 RGBA false false format:PSD colorspace:(none)'.format(
                    image_export_path_OSNRM))
            if MapSize == 1024:
                lx.eval('clip.newStill "{}" x1024 RGBA false false format:PSD colorspace:(none)'.format(
                    image_export_path_OSNRM))
            if MapSize == 2048:
                lx.eval('clip.newStill "{}" x2048 RGBA false false format:PSD colorspace:(none)'.format(
                    image_export_path_OSNRM))
            if MapSize == 4096:
                lx.eval('clip.newStill "{}" x4096 RGBA false false format:PSD colorspace:(none)'.format(
                    image_export_path_OSNRM))
            lx.eval('clip.addStill "{}"'.format(image_export_path_OSNRM))
            lx.eval('clip.save')

            lx.eval('select.subItem {%s} set textureLayer;mediaClip' % ImageNameOSNRM)
            lx.eval('select.item {%s} add' % ImageNameOSNRM)
            lx.eval('select.type item')
            lx.eval('select.subItem {%s} set mediaClip' % ImageNameOSNRM)
            lx.eval('select.subItem %s set textureLayer;light;render;environment' % PolyRender)
            lx.eval('texture.new clip:{%s}' % ImageNameOSNRM)

            # Parent to Render item to add the texture layer to the ShaderTree
            lx.eval('texture.parent %s %i' % (PolyRender, ShaderItem_ST_Pos))
            # Deselect the Render Item
            lx.eval(
                'select.subItem %s remove ;render;environment;mediaClip;scene;camera;light;locator;bake;textureLayer' % PolyRender)

            # Set Blend Mode / Effect and Opacity
            lx.eval('shader.setEffect diffColor')
            lx.eval('item.channel textureLayer$blend normal')
            lx.eval('item.channel textureLayer$opacity 1.0')

            # lx.command("select.subItem", item={ImageNameAO}, mode="set")
            image_save_time_OSNRM = os.path.getmtime(image_export_path_OSNRM)

            if Smo_MarmosetToolbag_OSNRM:
                lx.eval('item.channel textureLayer$enable true')
            if not Smo_MarmosetToolbag_OSNRM:
                lx.eval('item.channel textureLayer$enable false')
        # -------------------------------------------- #

        ############################ Create POSITION MAP Image Data #############################
        if Smo_MarmosetToolbag_POS == 1:
            # Select Lowpoly Meshes in order to be sure that the UV Map is set in Texture locator when the image are created.
            lx.eval('smo.GC.SelectMTypMesh 0')
            lx.eval('smo.GC.ClearSelectionVmap 1 0')

            if Smo_Marmoset_ScenePathSubfolder == 1:
                # builds the complete path out of the SceneFolder
                image_export_path_POS = os.path.join(OutputFolder, SMO_Marmoset_LL_FolderName, image_file_name_POS)
            if Smo_Marmoset_ScenePathSubfolder == 0:
                # builds the complete path out of the temp dir and the temp file name
                image_export_path_POS = os.path.join(OutputFolder, image_file_name_POS)

            if not os.path.exists(os.path.dirname(image_export_path_POS)):
                # try to create the directory.
                try:
                    os.makedirs(os.path.dirname(image_export_path_POS))
                except:
                    # if that fails for any reason print out the error
                    print(traceback.format_exc())
            else:
                if image_export_path_POS == None:
                    lx.out('Didn\'t save Position Map Image for MarmosetToolbag.')
                    return
                else:
                    image_export_path_POS = os.path.splitext(image_export_path_POS)[0] + ImgFileFrmt
                    image_file_name_POS = os.path.splitext(os.path.basename(image_export_path_POS))[0]

            # lx.eval('clip.new')
            if MapSize == 512:
                lx.eval('clip.newStill "{}" x512 RGBA false false format:PSD colorspace:(none)'.format(
                    image_export_path_POS))
            if MapSize == 1024:
                lx.eval('clip.newStill "{}" x1024 RGBA false false format:PSD colorspace:(none)'.format(
                    image_export_path_POS))
            if MapSize == 2048:
                lx.eval('clip.newStill "{}" x2048 RGBA false false format:PSD colorspace:(none)'.format(
                    image_export_path_POS))
            if MapSize == 4096:
                lx.eval('clip.newStill "{}" x4096 RGBA false false format:PSD colorspace:(none)'.format(
                    image_export_path_POS))
            lx.eval('clip.addStill "{}"'.format(image_export_path_POS))
            lx.eval('clip.save')

            lx.eval('select.subItem {%s} set textureLayer;mediaClip' % ImageNamePOS)
            lx.eval('select.item {%s} add' % ImageNameOSNRM)
            lx.eval('select.type item')
            lx.eval('select.subItem {%s} set mediaClip' % ImageNamePOS)
            lx.eval('select.subItem %s set textureLayer;light;render;environment' % PolyRender)
            lx.eval('texture.new clip:{%s}' % ImageNamePOS)

            # Parent to Render item to add the texture layer to the ShaderTree
            lx.eval('texture.parent %s %i' % (PolyRender, ShaderItem_ST_Pos))
            # Deselect the Render Item
            lx.eval(
                'select.subItem %s remove ;render;environment;mediaClip;scene;camera;light;locator;bake;textureLayer' % PolyRender)

            # Set Blend Mode / Effect and Opacity
            lx.eval('shader.setEffect diffColor')
            lx.eval('item.channel textureLayer$blend normal')
            lx.eval('item.channel textureLayer$opacity 1.0')

            # lx.command("select.subItem", item={ImageNameAO}, mode="set")
            image_save_time_POS = os.path.getmtime(image_export_path_POS)

            if Smo_MarmosetToolbag_POS:
                lx.eval('item.channel textureLayer$enable true')
            if not Smo_MarmosetToolbag_POS:
                lx.eval('item.channel textureLayer$enable false')
        # -------------------------------------------- #

        ############################ Create CURVATURE MAP Image Data #############################
        if Smo_MarmosetToolbag_CUR == 1:
            # Select Lowpoly Meshes in order to be sure that the UV Map is set in Texture locator when the image are created.
            lx.eval('smo.GC.SelectMTypMesh 0')
            lx.eval('smo.GC.ClearSelectionVmap 1 0')

            if Smo_Marmoset_ScenePathSubfolder == 1:
                # builds the complete path out of the SceneFolder
                image_export_path_CUR = os.path.join(OutputFolder, SMO_Marmoset_LL_FolderName, image_file_name_CUR)
            if Smo_Marmoset_ScenePathSubfolder == 0:
                # builds the complete path out of the temp dir and the temp file name
                image_export_path_CUR = os.path.join(OutputFolder, image_file_name_CUR)

            if not os.path.exists(os.path.dirname(image_export_path_CUR)):
                # try to create the directory.
                try:
                    os.makedirs(os.path.dirname(image_export_path_CUR))
                except:
                    # if that fails for any reason print out the error
                    print(traceback.format_exc())
            else:
                if image_export_path_CUR == None:
                    lx.out('Didn\'t save Curvature Map Image for MarmosetToolbag.')
                    return
                else:
                    image_export_path_CUR = os.path.splitext(image_export_path_CUR)[0] + ImgFileFrmt
                    image_file_name_CUR = os.path.splitext(os.path.basename(image_export_path_CUR))[0]

            # lx.eval('clip.new')
            if MapSize == 512:
                lx.eval('clip.newStill "{}" x512 RGBA false false format:PSD colorspace:(none)'.format(
                    image_export_path_CUR))
            if MapSize == 1024:
                lx.eval('clip.newStill "{}" x1024 RGBA false false format:PSD colorspace:(none)'.format(
                    image_export_path_CUR))
            if MapSize == 2048:
                lx.eval('clip.newStill "{}" x2048 RGBA false false format:PSD colorspace:(none)'.format(
                    image_export_path_CUR))
            if MapSize == 4096:
                lx.eval('clip.newStill "{}" x4096 RGBA false false format:PSD colorspace:(none)'.format(
                    image_export_path_CUR))
            lx.eval('clip.addStill "{}"'.format(image_export_path_CUR))
            lx.eval('clip.save')

            lx.eval('select.subItem {%s} set textureLayer;mediaClip' % ImageNameCUR)
            lx.eval('select.item {%s} add' % ImageNameCUR)
            lx.eval('select.type item')
            lx.eval('select.subItem {%s} set mediaClip' % ImageNameCUR)
            lx.eval('select.subItem %s set textureLayer;light;render;environment' % PolyRender)
            lx.eval('texture.new clip:{%s}' % ImageNameCUR)

            # Parent to Render item to add the texture layer to the ShaderTree
            lx.eval('texture.parent %s %i' % (PolyRender, ShaderItem_ST_Pos))
            # Deselect the Render Item
            lx.eval(
                'select.subItem %s remove ;render;environment;mediaClip;scene;camera;light;locator;bake;textureLayer' % PolyRender)

            # Set Blend Mode / Effect and Opacity
            lx.eval('shader.setEffect diffColor')
            lx.eval('item.channel textureLayer$blend normal')
            lx.eval('item.channel textureLayer$opacity 1.0')

            # lx.command("select.subItem", item={ImageNameAO}, mode="set")
            image_save_time_CUR = os.path.getmtime(image_export_path_CUR)

            if Smo_MarmosetToolbag_CUR:
                lx.eval('item.channel textureLayer$enable true')
            if not Smo_MarmosetToolbag_CUR:
                lx.eval('item.channel textureLayer$enable false')
        # -------------------------------------------- #

        ############################ Create OBJECT ID MAP Image Data #############################
        if Smo_MarmosetToolbag_OBJID == 1:
            # Select Lowpoly Meshes in order to be sure that the UV Map is set in Texture locator when the image are created.
            lx.eval('smo.GC.SelectMTypMesh 0')
            lx.eval('smo.GC.ClearSelectionVmap 1 0')

            if Smo_Marmoset_ScenePathSubfolder == 1:
                # builds the complete path out of the SceneFolder
                image_export_path_OBJID = os.path.join(OutputFolder, SMO_Marmoset_LL_FolderName, image_file_name_OBJID)
            if Smo_Marmoset_ScenePathSubfolder == 0:
                # builds the complete path out of the temp dir and the temp file name
                image_export_path_OBJID = os.path.join(OutputFolder, image_file_name_OBJID)

            if not os.path.exists(os.path.dirname(image_export_path_OBJID)):
                # try to create the directory.
                try:
                    os.makedirs(os.path.dirname(image_export_path_OBJID))
                except:
                    # if that fails for any reason print out the error
                    print(traceback.format_exc())
            else:
                if image_export_path_OBJID == None:
                    lx.out('Didn\'t save Object ID Map Image for MarmosetToolbag.')
                    return
                else:
                    image_export_path_OBJID = os.path.splitext(image_export_path_OBJID)[0] + ImgFileFrmt
                    image_file_name_OBJID = os.path.splitext(os.path.basename(image_export_path_OBJID))[0]

            # lx.eval('clip.new')
            if MapSize == 512:
                lx.eval('clip.newStill "{}" x512 RGBA false false format:PSD colorspace:(none)'.format(
                    image_export_path_OBJID))
            if MapSize == 1024:
                lx.eval('clip.newStill "{}" x1024 RGBA false false format:PSD colorspace:(none)'.format(
                    image_export_path_OBJID))
            if MapSize == 2048:
                lx.eval('clip.newStill "{}" x2048 RGBA false false format:PSD colorspace:(none)'.format(
                    image_export_path_OBJID))
            if MapSize == 4096:
                lx.eval('clip.newStill "{}" x4096 RGBA false false format:PSD colorspace:(none)'.format(
                    image_export_path_OBJID))
            lx.eval('clip.addStill "{}"'.format(image_export_path_OBJID))
            lx.eval('clip.save')

            lx.eval('select.subItem {%s} set textureLayer;mediaClip' % ImageNameOBJID)
            lx.eval('select.item {%s} add' % ImageNameOBJID)
            lx.eval('select.type item')
            lx.eval('select.subItem {%s} set mediaClip' % ImageNameOBJID)
            lx.eval('select.subItem %s set textureLayer;light;render;environment' % PolyRender)
            lx.eval('texture.new clip:{%s}' % ImageNameOBJID)

            # Parent to Render item to add the texture layer to the ShaderTree
            lx.eval('texture.parent %s %i' % (PolyRender, ShaderItem_ST_Pos))
            # Deselect the Render Item
            lx.eval(
                'select.subItem %s remove ;render;environment;mediaClip;scene;camera;light;locator;bake;textureLayer' % PolyRender)

            # Set Blend Mode / Effect and Opacity
            lx.eval('shader.setEffect diffColor')
            lx.eval('item.channel textureLayer$blend normal')
            lx.eval('item.channel textureLayer$opacity 1.0')

            # lx.command("select.subItem", item={ImageNameAO}, mode="set")
            image_save_time_OBJID = os.path.getmtime(image_export_path_OBJID)

            if Smo_MarmosetToolbag_OBJID:
                lx.eval('item.channel textureLayer$enable true')
            if not Smo_MarmosetToolbag_OBJID:
                lx.eval('item.channel textureLayer$enable false')
        # -------------------------------------------- #

        ############################ Create THICKNESS MAP Image Data #############################
        if Smo_MarmosetToolbag_THI == 1:
            # Select Lowpoly Meshes in order to be sure that the UV Map is set in Texture locator when the image are created.
            lx.eval('smo.GC.SelectMTypMesh 0')
            lx.eval('smo.GC.ClearSelectionVmap 1 0')

            if Smo_Marmoset_ScenePathSubfolder == 1:
                # builds the complete path out of the SceneFolder
                image_export_path_THI = os.path.join(OutputFolder, SMO_Marmoset_LL_FolderName, image_file_name_THI)
            if Smo_Marmoset_ScenePathSubfolder == 0:
                # builds the complete path out of the temp dir and the temp file name
                image_export_path_THI = os.path.join(OutputFolder, image_file_name_THI)

            if not os.path.exists(os.path.dirname(image_export_path_THI)):
                # try to create the directory.
                try:
                    os.makedirs(os.path.dirname(image_export_path_THI))
                except:
                    # if that fails for any reason print out the error
                    print(traceback.format_exc())
            else:
                if image_export_path_THI == None:
                    lx.out('Didn\'t save Thickness Map Image for MarmosetToolbag.')
                    return
                else:
                    image_export_path_THI = os.path.splitext(image_export_path_THI)[0] + ImgFileFrmt
                    image_file_name_THI = os.path.splitext(os.path.basename(image_export_path_THI))[0]

            # lx.eval('clip.new')
            if MapSize == 512:
                lx.eval('clip.newStill "{}" x512 RGBA false false format:PSD colorspace:(none)'.format(
                    image_export_path_THI))
            if MapSize == 1024:
                lx.eval('clip.newStill "{}" x1024 RGBA false false format:PSD colorspace:(none)'.format(
                    image_export_path_THI))
            if MapSize == 2048:
                lx.eval('clip.newStill "{}" x2048 RGBA false false format:PSD colorspace:(none)'.format(
                    image_export_path_THI))
            if MapSize == 4096:
                lx.eval('clip.newStill "{}" x4096 RGBA false false format:PSD colorspace:(none)'.format(
                    image_export_path_THI))
            lx.eval('clip.addStill "{}"'.format(image_export_path_THI))
            lx.eval('clip.save')

            lx.eval('select.subItem {%s} set textureLayer;mediaClip' % ImageNameTHI)
            lx.eval('select.item {%s} add' % ImageNameTHI)
            lx.eval('select.type item')
            lx.eval('select.subItem {%s} set mediaClip' % ImageNameTHI)
            lx.eval('select.subItem %s set textureLayer;light;render;environment' % PolyRender)
            lx.eval('texture.new clip:{%s}' % ImageNameTHI)

            # Parent to Render item to add the texture layer to the ShaderTree
            lx.eval('texture.parent %s %i' % (PolyRender, ShaderItem_ST_Pos))
            # Deselect the Render Item
            lx.eval(
                'select.subItem %s remove ;render;environment;mediaClip;scene;camera;light;locator;bake;textureLayer' % PolyRender)

            # Set Blend Mode / Effect and Opacity
            lx.eval('shader.setEffect diffColor')
            lx.eval('item.channel textureLayer$blend normal')
            lx.eval('item.channel textureLayer$opacity 1.0')

            # lx.command("select.subItem", item={ImageNameAO}, mode="set")
            image_save_time_THI = os.path.getmtime(image_export_path_THI)

            if Smo_MarmosetToolbag_THI:
                lx.eval('item.channel textureLayer$enable true')
            if not Smo_MarmosetToolbag_THI:
                lx.eval('item.channel textureLayer$enable false')
        # -------------------------------------------- #

        ############################ Create MATERIAL ID MAP Image Data #############################
        if Smo_MarmosetToolbag_MATID == 1:
            # Select Lowpoly Meshes in order to be sure that the UV Map is set in Texture locator when the image are created.
            lx.eval('smo.GC.SelectMTypMesh 0')
            lx.eval('smo.GC.ClearSelectionVmap 1 0')

            if Smo_Marmoset_ScenePathSubfolder == 1:
                # builds the complete path out of the SceneFolder
                image_export_path_MATID = os.path.join(OutputFolder, SMO_Marmoset_LL_FolderName, image_file_name_MATID)
            if Smo_Marmoset_ScenePathSubfolder == 0:
                # builds the complete path out of the temp dir and the temp file name
                image_export_path_MATID = os.path.join(OutputFolder, image_file_name_MATID)

            if not os.path.exists(os.path.dirname(image_export_path_MATID)):
                # try to create the directory.
                try:
                    os.makedirs(os.path.dirname(image_export_path_MATID))
                except:
                    # if that fails for any reason print out the error
                    print(traceback.format_exc())
            else:
                if image_export_path_MATID == None:
                    lx.out('Didn\'t save Thickness Map Image for MarmosetToolbag.')
                    return
                else:
                    image_export_path_MATID = os.path.splitext(image_export_path_MATID)[0] + ImgFileFrmt
                    image_file_name_MATID = os.path.splitext(os.path.basename(image_export_path_MATID))[0]

            # lx.eval('clip.new')
            if MapSize == 512:
                lx.eval(
                    'clip.newStill "{}" x512 RGBA false false format:PSD colorspace:(none)'.format(
                        image_export_path_MATID))
            if MapSize == 1024:
                lx.eval(
                    'clip.newStill "{}" x1024 RGBA false false format:PSD colorspace:(none)'.format(
                        image_export_path_MATID))
            if MapSize == 2048:
                lx.eval(
                    'clip.newStill "{}" x2048 RGBA false false format:PSD colorspace:(none)'.format(
                        image_export_path_MATID))
            if MapSize == 4096:
                lx.eval(
                    'clip.newStill "{}" x4096 RGBA false false format:PSD colorspace:(none)'.format(
                        image_export_path_MATID))
            lx.eval('clip.addStill "{}"'.format(image_export_path_MATID))
            lx.eval('clip.save')

            lx.eval('select.subItem {%s} set textureLayer;mediaClip' % ImageNameMATID)
            lx.eval('select.item {%s} add' % ImageNameMATID)
            lx.eval('select.type item')
            lx.eval('select.subItem {%s} set mediaClip' % ImageNameMATID)
            lx.eval('select.subItem %s set textureLayer;light;render;environment' % PolyRender)
            lx.eval('texture.new clip:{%s}' % ImageNameMATID)

            # Parent to Render item to add the texture layer to the ShaderTree
            lx.eval('texture.parent %s %i' % (PolyRender, ShaderItem_ST_Pos))
            # Deselect the Render Item
            lx.eval(
                'select.subItem %s remove ;render;environment;mediaClip;scene;camera;light;locator;bake;textureLayer' % PolyRender)

            # Set Blend Mode / Effect and Opacity
            lx.eval('shader.setEffect diffColor')
            lx.eval('item.channel textureLayer$blend normal')
            lx.eval('item.channel textureLayer$opacity 1.0')

            # lx.command("select.subItem", item={ImageNameAO}, mode="set")
            image_save_time_MATID = os.path.getmtime(image_export_path_MATID)

            if Smo_MarmosetToolbag_MATID:
                lx.eval('item.channel textureLayer$enable true')
            if not Smo_MarmosetToolbag_MATID:
                lx.eval('item.channel textureLayer$enable false')
        # -------------------------------------------- #

        ############################ Create ALBEDO MAP Image Data #############################
        if Smo_MarmosetToolbag_ALBEDO == 1:
            # Select Lowpoly Meshes in order to be sure that the UV Map is set in Texture locator when the image are created.
            lx.eval('smo.GC.SelectMTypMesh 0')
            lx.eval('smo.GC.ClearSelectionVmap 1 0')

            if Smo_Marmoset_ScenePathSubfolder == 1:
                # builds the complete path out of the SceneFolder
                image_export_path_ALBEDO = os.path.join(OutputFolder, SMO_Marmoset_LL_FolderName,
                                                        image_file_name_ALBEDO)
            if Smo_Marmoset_ScenePathSubfolder == 0:
                # builds the complete path out of the temp dir and the temp file name
                image_export_path_ALBEDO = os.path.join(OutputFolder, image_file_name_ALBEDO)

            if not os.path.exists(os.path.dirname(image_export_path_ALBEDO)):
                # try to create the directory.
                try:
                    os.makedirs(os.path.dirname(image_export_path_ALBEDO))
                except:
                    # if that fails for any reason print out the error
                    print(traceback.format_exc())
            else:
                if image_export_path_ALBEDO == None:
                    lx.out('Didn\'t save Thickness Map Image for MarmosetToolbag.')
                    return
                else:
                    image_export_path_ALBEDO = os.path.splitext(image_export_path_ALBEDO)[0] + ImgFileFrmt
                    image_file_name_ALBEDO = os.path.splitext(os.path.basename(image_export_path_ALBEDO))[0]

            # lx.eval('clip.new')
            if MapSize == 512:
                lx.eval(
                    'clip.newStill "{}" x512 RGBA false false format:PSD colorspace:(none)'.format(
                        image_export_path_ALBEDO))
            if MapSize == 1024:
                lx.eval(
                    'clip.newStill "{}" x1024 RGBA false false format:PSD colorspace:(none)'.format(
                        image_export_path_ALBEDO))
            if MapSize == 2048:
                lx.eval(
                    'clip.newStill "{}" x2048 RGBA false false format:PSD colorspace:(none)'.format(
                        image_export_path_ALBEDO))
            if MapSize == 4096:
                lx.eval(
                    'clip.newStill "{}" x4096 RGBA false false format:PSD colorspace:(none)'.format(
                        image_export_path_ALBEDO))
            lx.eval('clip.addStill "{}"'.format(image_export_path_ALBEDO))
            lx.eval('clip.save')

            lx.eval('select.subItem {%s} set textureLayer;mediaClip' % ImageNameALBEDO)
            lx.eval('select.item {%s} add' % ImageNameALBEDO)
            lx.eval('select.type item')
            lx.eval('select.subItem {%s} set mediaClip' % ImageNameALBEDO)
            lx.eval('select.subItem %s set textureLayer;light;render;environment' % PolyRender)
            lx.eval('texture.new clip:{%s}' % ImageNameALBEDO)

            # Parent to Render item to add the texture layer to the ShaderTree
            lx.eval('texture.parent %s %i' % (PolyRender, ShaderItem_ST_Pos))
            # Deselect the Render Item
            lx.eval(
                'select.subItem %s remove ;render;environment;mediaClip;scene;camera;light;locator;bake;textureLayer' % PolyRender)

            # Set Blend Mode / Effect and Opacity
            lx.eval('shader.setEffect diffColor')
            lx.eval('item.channel textureLayer$blend normal')
            lx.eval('item.channel textureLayer$opacity 1.0')

            # lx.command("select.subItem", item={ImageNameAO}, mode="set")
            image_save_time_ALBEDO = os.path.getmtime(image_export_path_ALBEDO)

            if Smo_MarmosetToolbag_ALBEDO:
                lx.eval('item.channel textureLayer$enable true')
            if not Smo_MarmosetToolbag_ALBEDO:
                lx.eval('item.channel textureLayer$enable false')
        # -------------------------------------------- #

        ############################ Create UV Island ID MAP Image Data #############################
        if Smo_MarmosetToolbag_UVID == 1:
            # Select Lowpoly Meshes in order to be sure that the UV Map is set in Texture locator when the image are created.
            lx.eval('smo.GC.SelectMTypMesh 0')
            lx.eval('smo.GC.ClearSelectionVmap 1 0')

            if Smo_Marmoset_ScenePathSubfolder == 1:
                # builds the complete path out of the SceneFolder
                image_export_path_UVID = os.path.join(OutputFolder, SMO_Marmoset_LL_FolderName, image_file_name_UVID)
            if Smo_Marmoset_ScenePathSubfolder == 0:
                # builds the complete path out of the temp dir and the temp file name
                image_export_path_UVID = os.path.join(OutputFolder, image_file_name_UVID)

            if not os.path.exists(os.path.dirname(image_export_path_UVID)):
                # try to create the directory.
                try:
                    os.makedirs(os.path.dirname(image_export_path_UVID))
                except:
                    # if that fails for any reason print out the error
                    print(traceback.format_exc())
            else:
                if image_export_path_UVID == None:
                    lx.out('Didn\'t save Thickness Map Image for MarmosetToolbag.')
                    return
                else:
                    image_export_path_UVID = os.path.splitext(image_export_path_UVID)[0] + ImgFileFrmt
                    image_file_name_UVID = os.path.splitext(os.path.basename(image_export_path_UVID))[0]

            # lx.eval('clip.new')
            if MapSize == 512:
                lx.eval(
                    'clip.newStill "{}" x512 RGBA false false format:PSD colorspace:(none)'.format(
                        image_export_path_UVID))
            if MapSize == 1024:
                lx.eval(
                    'clip.newStill "{}" x1024 RGBA false false format:PSD colorspace:(none)'.format(
                        image_export_path_UVID))
            if MapSize == 2048:
                lx.eval(
                    'clip.newStill "{}" x2048 RGBA false false format:PSD colorspace:(none)'.format(
                        image_export_path_UVID))
            if MapSize == 4096:
                lx.eval(
                    'clip.newStill "{}" x4096 RGBA false false format:PSD colorspace:(none)'.format(
                        image_export_path_UVID))
            lx.eval('clip.addStill "{}"'.format(image_export_path_UVID))
            lx.eval('clip.save')

            lx.eval('select.subItem {%s} set textureLayer;mediaClip' % ImageNameUVID)
            lx.eval('select.item {%s} add' % ImageNameUVID)
            lx.eval('select.type item')
            lx.eval('select.subItem {%s} set mediaClip' % ImageNameUVID)
            lx.eval('select.subItem %s set textureLayer;light;render;environment' % PolyRender)
            lx.eval('texture.new clip:{%s}' % ImageNameUVID)

            # Parent to Render item to add the texture layer to the ShaderTree
            lx.eval('texture.parent %s %i' % (PolyRender, ShaderItem_ST_Pos))
            # Deselect the Render Item
            lx.eval(
                'select.subItem %s remove ;render;environment;mediaClip;scene;camera;light;locator;bake;textureLayer' % PolyRender)

            # Set Blend Mode / Effect and Opacity
            lx.eval('shader.setEffect diffColor')
            lx.eval('item.channel textureLayer$blend normal')
            lx.eval('item.channel textureLayer$opacity 1.0')

            # lx.command("select.subItem", item={ImageNameAO}, mode="set")
            image_save_time_UVID = os.path.getmtime(image_export_path_UVID)

            if Smo_MarmosetToolbag_UVID:
                lx.eval('item.channel textureLayer$enable true')
            if not Smo_MarmosetToolbag_UVID:
                lx.eval('item.channel textureLayer$enable false')
        # -------------------------------------------- #

        # Marmo_Launch_viaTbscene_Cmd = (Smo_MarmosetToolbagExe_AbsPath + " " + Smo_MarmosetToolbagTemplateScene_AbsPath)
        # print Marmo_Launch_viaTbscene_Cmd
        # lx.out('Marmoset Load Data via Tbscene: ', Marmo_Launch_viaTbscene_Cmd)

        # Marmo_Launch_viaPython_Cmd = (Smo_MarmosetToolbagExe_AbsPath + " " + Smo_MarmosetToolbagScript_AbsPath)
        # print Marmo_Launch_viaPython_Cmd
        # lx.out('Marmoset Load Data via Python Script: ', Marmo_Launch_viaPython_Cmd)

        # Call MarmosetToolbag.
        # proc = subprocess.Popen([Smo_MarmosetToolbagExe_AbsPath, " ", Smo_MarmosetToolbagScript_AbsPath], executable=Smo_MarmosetToolbagExe_AbsPath, stdout=subprocess.PIPE)
        # stdout, stderr = proc.communicate()
        # rc = proc.returncode

        ################## Save ##################
        ################## Data ##################
        if python_majorver < 3:
            # print("do something for 2.X code")
            # "f" is the FileName where we store the Variable Data for Marmoset Pipe.
            f = open(DataExchangeFilePath, 'wb')
        elif python_majorver >= 3:
            # print("do something for 3.X code")
            f = open(DataExchangeFilePath, 'wt')


        # Create a dictionary of pairs "key: value"
        # Data = {'String name': StringA, 'Valeur': StringB}
        Data = {'ScenePathSubfolder': Smo_Marmoset_ScenePathSubfolder, 'BaseBakeFilePath': BaseBakeFilePath,
                'BaseBakeFileName': BaseBakeFileName, 'SceneName': SceneName,
                'DataExchangeFileName': DataExchangeFileName, 'DataExchangeFilePath': DataExchangeFilePath,
                'MapSize': MapSize, 'ImgFileFrmt': ImgFileFrmt, 'SeparatorStr': SeparatorStr,
                'OutputFolder': OutputFolder, 'Lowpoly NameTag': NameTagLP, 'Cage NameTag': NameTagCage,
                'Highpoly NameTag': NameTagHP, 'Lowpoly FBX Filename': fbx_file_name_LP,
                'Cage FBX Filename': fbx_file_name_Cage, 'Highpoly FBX Filename': fbx_file_name_HP,
                'Lowpoly FBX FilePath': fbx_export_path_LP, 'Cage FBX FilePath': fbx_export_path_Cage,
                'Highpoly FBX FilePath': fbx_export_path_HP, 'AO State': Smo_MarmosetToolbag_AO,
                'AOF State': Smo_MarmosetToolbag_AOF, 'TSNRM State': Smo_MarmosetToolbag_TSNRM,
                'OSNRM State': Smo_MarmosetToolbag_OSNRM, 'POS State': Smo_MarmosetToolbag_POS,
                'CUR State': Smo_MarmosetToolbag_CUR, 'OBJID State': Smo_MarmosetToolbag_OBJID,
                'THI State': Smo_MarmosetToolbag_THI, 'MATID State': Smo_MarmosetToolbag_MATID,
                'ALBEDO State': Smo_MarmosetToolbag_ALBEDO, 'UVID State': Smo_MarmosetToolbag_UVID,
                'AO NameTag': TagImg_AO, 'AOF NameTag': TagImg_AOF, 'TSNRM NameTag': TagImg_TSNRM,
                'OSNRM NameTag': TagImg_OSNRM, 'POS NameTag': TagImg_POS, 'CUR NameTag': TagImg_CUR,
                'OBJID NameTag': TagImg_OBJID, 'THI NameTag': TagImg_THI, 'MATID NameTag': TagImg_MATID,
                'ALBEDO NameTag': TagImg_ALBEDO, 'UVID NameTag': TagImg_UVID, 'AO Filename': image_file_name_AO,
                'AOF Filename': image_file_name_AOF, 'TSNRM Filename': image_file_name_TSNRM,
                'OSNRM Filename': image_file_name_OSNRM, 'POS Filename': image_file_name_POS,
                'CUR Filename': image_file_name_CUR, 'OBJID Filename': image_file_name_OBJID,
                'THI Filename': image_file_name_THI, 'MATID Filename': image_file_name_MATID,
                'ALBEDO Filename': image_file_name_ALBEDO, 'UVID Filename': image_file_name_UVID,
                'AO FilePath': image_export_path_AO, 'AOF FilePath': image_export_path_AOF,
                'TSNRM FilePath': image_export_path_TSNRM, 'OSNRM FilePath': image_export_path_OSNRM,
                'POS FilePath': image_export_path_POS, 'CUR FilePath': image_export_path_CUR,
                'OBJID FilePath': image_export_path_OBJID, 'THI FilePath': image_export_path_THI,
                'MATID FilePath': image_export_path_MATID, 'ALBEDO FilePath': image_export_path_ALBEDO,
                'UVID FilePath': image_export_path_UVID, 'AutoSaveMarmoSceneFile': Bool_AutoSaveMarmoSceneFile,
                'AutoBakeAtLoad': Bool_AutoBakeAtLoad, 'AutoCloseMarmo': Bool_AutoCloseMarmo,
                'NRM_FlipX': Bool_NRMFlipX, 'NRM_FlipY': Bool_NRMFlipY, 'NRM_FlipZ': Bool_NRMFlipZ,
                'PerPixelSample': PerPxSampleCount, 'RaysSampleCount': RaysSampleCount}

        # Data = [BaseBakeFilePath, BaseBakeFileName, SceneName, DataExchangeFileName, DataExchangeFilePath, MapSize, ImgFileFrmt, SeparatorStr, OutputFolder, NameTagLP, NameTagCage, NameTagHP, fbx_file_name_LP, fbx_file_name_Cage, fbx_file_name_HP, fbx_export_path_LP, fbx_export_path_Cage, fbx_export_path_HP, Smo_MarmosetToolbag_AO, Smo_MarmosetToolbag_TSNRM, Smo_MarmosetToolbag_OSNRM, Smo_MarmosetToolbag_POS, Smo_MarmosetToolbag_CUR, Smo_MarmosetToolbag_OBJID, Smo_MarmosetToolbag_THI, TagImg_AO, TagImg_TSNRM, TagImg_OSNRM, TagImg_POS, TagImg_CUR, TagImg_OBJID, TagImg_THI, image_file_name_AO, image_file_name_TSNRM, image_file_name_OSNRM, image_file_name_POS, image_file_name_CUR, image_file_name_OBJID, image_file_name_THI, image_export_path_AO, image_export_path_TSNRM, image_export_path_OSNRM, image_export_path_POS, image_export_path_CUR, image_export_path_OBJID, image_export_path_THI]

        # write variables to filename [Data] and close it.
        if python_majorver < 3:
            # print("do something for 2.X code")
            j.dump(Data, f)
        elif python_majorver >= 3:
            # print("do something for 3.X code")
            j.dump(Data, f, ensure_ascii=False)
        f.close()
        # ------------------------------------------ #

        # ------------------------------ #    To set the AutoLoad Method
        LoadViaPythonMode = bool(lx.eval('user.value SMO_UseVal_MARMOSET_LoadViaPythonMode ?'))
        # print LoadViaPythonMode

        # Call MarmosetToolbag.
        if not LoadViaPythonMode:
            proc = subprocess.Popen([Smo_MarmosetToolbagExe_AbsPath, " ", Smo_MarmosetToolbagTemplateScene_AbsPath],
                                    executable=Smo_MarmosetToolbagExe_AbsPath, stdout=subprocess.PIPE)
            stdout, stderr = proc.communicate()
            rc = proc.returncode

        if LoadViaPythonMode:
            proc = subprocess.Popen([Smo_MarmosetToolbagExe_AbsPath, " ", Smo_MarmosetToolbagScript_AbsPath],
                                    executable=Smo_MarmosetToolbagExe_AbsPath, stdout=subprocess.PIPE)
            stdout, stderr = proc.communicate()
            rc = proc.returncode

        if rc != 0 and Bool_AutoCloseMarmo == 0:
            # MarmosetToolbag crashed or threw an error.
            lx.out('MarmosetToolbag crashed.')
            lx.out('Standard Output: %s' % stdout)
            lx.out('Error Output: %s' % stderr)

        if rc != 0 and Bool_AutoCloseMarmo == 1:
            # Get the modified time of the export file.
            #
            # if Smo_MarmosetToolbag_AO == True:
            #     if os.path.lexists (image_export_path_AO):
            #         image_load_time_AO = os.path.getmtime (image_export_path_AO)
            # if Smo_MarmosetToolbag_AOF == True:
            #     if os.path.lexists(image_export_path_AOF):
            #         image_load_time_AOF = os.path.getmtime(image_export_path_AOF)
            # if Smo_MarmosetToolbag_TSNRM == True:
            #     if os.path.lexists (image_export_path_TSNRM):
            #         image_load_time_TSNRM = os.path.getmtime (image_export_path_TSNRM)
            # if Smo_MarmosetToolbag_OSNRM == True:
            #     if os.path.lexists (image_export_path_OSNRM):
            #         image_load_time_OSNRM = os.path.getmtime (image_export_path_OSNRM)
            # if Smo_MarmosetToolbag_POS == True:
            #     if os.path.lexists (image_export_path_POS):
            #         image_load_time_POS = os.path.getmtime (image_export_path_POS)
            # if Smo_MarmosetToolbag_CUR == True:
            #     if os.path.lexists (image_export_path_CUR):
            #         image_load_time_CUR = os.path.getmtime (image_export_path_CUR)
            # if Smo_MarmosetToolbag_OBJID == True:
            #     if os.path.lexists (image_export_path_OBJID):
            #         image_load_time_OBJID = os.path.getmtime (image_export_path_OBJID)
            # if Smo_MarmosetToolbag_THI == True:
            #     if os.path.lexists (image_export_path_THI):
            #         image_load_time_THI = os.path.getmtime (image_export_path_THI)
            # if Smo_MarmosetToolbag_MATID == True:
            #     if os.path.lexists (image_export_path_MATID):
            #         image_load_time_MATID = os.path.getmtime (image_export_path_MATID)
            # if Smo_MarmosetToolbag_ALBEDO == True:
            #     if os.path.lexists (image_export_path_ALBEDO):
            #         image_load_time_ALBEDO = os.path.getmtime (image_export_path_ALBEDO)
            # if Smo_MarmosetToolbag_UVID == True:
            #     if os.path.lexists (image_export_path_UVID):
            #         image_load_time_UVID = os.path.getmtime (image_export_path_UVID)
            #
            #
            # if Smo_MarmosetToolbag_AO == True :
            #     # User has likely saved over the old file.
            #     if image_load_time_AO > image_save_time_AO :
            #         lx.out ('MarmosetToolbag Bake: AO updated')
            #
            # if Smo_MarmosetToolbag_AOF == True :
            #     # User has likely saved over the old file.
            #     if image_load_time_AOF > image_save_time_AOF :
            #         lx.out ('MarmosetToolbag Bake: AO (Floor) updated')
            #
            # if Smo_MarmosetToolbag_TSNRM == True :
            #     # User has likely saved over the old file.
            #     if image_load_time_TSNRM > image_save_time_TSNRM :
            #         lx.out ('MarmosetToolbag Bake: Tangent Space Normal Map updated')
            #
            # if Smo_MarmosetToolbag_OSNRM == True :
            #     # User has likely saved over the old file.
            #     if image_load_time_OSNRM > image_save_time_OSNRM :
            #         lx.out ('MarmosetToolbag Bake: Object Space Normal Map updated')
            #
            # if Smo_MarmosetToolbag_POS == True :
            #     # User has likely saved over the old file.
            #     if image_load_time_POS > image_save_time_POS :
            #         lx.out ('MarmosetToolbag Bake: Position Map updated')
            #
            # if Smo_MarmosetToolbag_CUR == True :
            #     # User has likely saved over the old file.
            #     if image_load_time_CUR > image_save_time_CUR :
            #         lx.out ('MarmosetToolbag Bake: Curvature Map updated')
            #
            # if Smo_MarmosetToolbag_OBJID == True :
            #     # User has likely saved over the old file.
            #     if image_load_time_OBJID > image_save_time_OBJID :
            #         lx.out ('MarmosetToolbag Bake: Object ID Map updated')
            #
            # if Smo_MarmosetToolbag_THI == True :
            #     # User has likely saved over the old file.
            #     if image_load_time_THI > image_save_time_THI :
            #         lx.out ('MarmosetToolbag Bake: Thickness Map updated')
            #
            # if Smo_MarmosetToolbag_MATID == True :
            #     # User has likely saved over the old file.
            #     if image_load_time_MATID > image_save_time_MATID :
            #         lx.out ('MarmosetToolbag Bake: MaterialID Map updated')
            #
            # if Smo_MarmosetToolbag_ALBEDO == True:
            #     # User has likely saved over the old file.
            #     if image_load_time_ALBEDO > image_save_time_ALBEDO:
            #         lx.out('MarmosetToolbag Bake: Albedo Map updated')
            #
            # if Smo_MarmosetToolbag_UVID == True:
            #     # User has likely saved over the old file.
            #     if image_load_time_UVID > image_save_time_UVID:
            #         lx.out('MarmosetToolbag Bake: UV ID Map updated')

            lx.eval('select.drop item')
            lx.eval('select.clear item')
            lx.eval('select.drop schmNode')
            lx.eval('select.drop channel')
            lx.eval('select.drop link')

            # -------- CREATE A NEW SET OF STILL IMAGE
            # if Smo_MarmosetToolbag_AO == True :
            # lx.eval('smo.GC.SelectImageMaps 0')
            # if Smo_MarmosetToolbag_TSNRM == True :
            # lx.eval('smo.GC.SelectImageMaps 1')
            # if Smo_MarmosetToolbag_OSNRM == True :
            # lx.eval('smo.GC.SelectImageMaps 2')
            # if Smo_MarmosetToolbag_POS == True :
            # lx.eval('smo.GC.SelectImageMaps 3')
            # if Smo_MarmosetToolbag_CUR == True :
            # lx.eval('smo.GC.SelectImageMaps 4')
            # if Smo_MarmosetToolbag_OBJID == True :
            # lx.eval('smo.GC.SelectImageMaps 5')
            # if Smo_MarmosetToolbag_THI == True :
            # lx.eval('smo.GC.SelectImageMaps 6')

            if Smo_MarmosetToolbag_AO:
                if image_load_time_AO > image_save_time_AO:
                    lx.eval('select.subItem {%s} set textureLayer;mediaClip' % ImageNameAO)
                    lx.eval('!clip.reload')
                    lx.eval('select.drop item')
                    lx.eval('select.clear item')
                    lx.eval('select.drop schmNode')
                    lx.eval('select.drop channel')
                    lx.eval('select.drop link')

            if Smo_MarmosetToolbag_AOF:
                if image_load_time_AOF > image_save_time_AOF:
                    lx.eval('select.subItem {%s} set textureLayer;mediaClip' % ImageNameAOF)
                    lx.eval('!clip.reload')
                    lx.eval('select.drop item')
                    lx.eval('select.clear item')
                    lx.eval('select.drop schmNode')
                    lx.eval('select.drop channel')
                    lx.eval('select.drop link')

            if Smo_MarmosetToolbag_TSNRM:
                if image_load_time_TSNRM > image_save_time_TSNRM:
                    lx.eval('select.subItem {%s} set textureLayer;mediaClip' % ImageNameTSNRM)
                    lx.eval('!clip.reload')
                    lx.eval('select.drop item')
                    lx.eval('select.clear item')
                    lx.eval('select.drop schmNode')
                    lx.eval('select.drop channel')
                    lx.eval('select.drop link')

            if Smo_MarmosetToolbag_OSNRM:
                if image_load_time_OSNRM > image_save_time_OSNRM:
                    lx.eval('select.subItem {%s} set textureLayer;mediaClip' % ImageNameOSNRM)
                    lx.eval('!clip.reload')
                    lx.eval('select.drop item')
                    lx.eval('select.clear item')
                    lx.eval('select.drop schmNode')
                    lx.eval('select.drop channel')
                    lx.eval('select.drop link')

            if Smo_MarmosetToolbag_POS:
                if image_load_time_POS > image_save_time_POS:
                    lx.eval('select.subItem {%s} set textureLayer;mediaClip' % ImageNamePOS)
                    lx.eval('!clip.reload')
                    lx.eval('select.drop item')
                    lx.eval('select.clear item')
                    lx.eval('select.drop schmNode')
                    lx.eval('select.drop channel')
                    lx.eval('select.drop link')

            if Smo_MarmosetToolbag_CUR:
                if image_load_time_CUR > image_save_time_CUR:
                    lx.eval('select.subItem {%s} set textureLayer;mediaClip' % ImageNameCUR)
                    lx.eval('!clip.reload')
                    lx.eval('select.drop item')
                    lx.eval('select.clear item')
                    lx.eval('select.drop schmNode')
                    lx.eval('select.drop channel')
                    lx.eval('select.drop link')

            if Smo_MarmosetToolbag_OBJID:
                if image_load_time_OBJID > image_save_time_OBJID:
                    lx.eval('select.subItem {%s} set textureLayer;mediaClip' % ImageNameOBJID)
                    lx.eval('!clip.reload')
                    lx.eval('select.drop item')
                    lx.eval('select.clear item')
                    lx.eval('select.drop schmNode')
                    lx.eval('select.drop channel')

            if Smo_MarmosetToolbag_THI:
                if image_load_time_THI > image_save_time_THI:
                    lx.eval('select.subItem {%s} set textureLayer;mediaClip' % ImageNameTHI)
                    lx.eval('!clip.reload')
                    lx.eval('select.drop item')
                    lx.eval('select.clear item')
                    lx.eval('select.drop schmNode')
                    lx.eval('select.drop channel')
                    lx.eval('select.drop link')

            if Smo_MarmosetToolbag_MATID:
                if image_load_time_MATID > image_save_time_MATID:
                    lx.eval('select.subItem {%s} set textureLayer;mediaClip' % ImageNameMATID)
                    lx.eval('!clip.reload')
                    lx.eval('select.drop item')
                    lx.eval('select.clear item')
                    lx.eval('select.drop schmNode')
                    lx.eval('select.drop channel')
                    lx.eval('select.drop link')

            if Smo_MarmosetToolbag_ALBEDO:
                if image_load_time_ALBEDO > image_save_time_ALBEDO:
                    lx.eval('select.subItem {%s} set textureLayer;mediaClip' % ImageNameALBEDO)
                    lx.eval('!clip.reload')
                    lx.eval('select.drop item')
                    lx.eval('select.clear item')
                    lx.eval('select.drop schmNode')
                    lx.eval('select.drop channel')

            if Smo_MarmosetToolbag_UVID:
                if image_load_time_UVID > image_save_time_UVID:
                    lx.eval('select.subItem {%s} set textureLayer;mediaClip' % ImageNameUVID)
                    lx.eval('!clip.reload')
                    lx.eval('select.drop item')
                    lx.eval('select.clear item')
                    lx.eval('select.drop schmNode')
                    lx.eval('select.drop channel')
                    lx.eval('select.drop link')

        else:
            # Get the modified time of the export file.

            lx.eval('select.drop item')
            lx.eval('select.clear item')
            lx.eval('select.drop schmNode')
            lx.eval('select.drop channel')
            lx.eval('select.drop link')

            if Smo_MarmosetToolbag_AO:
                if image_load_time_AO > image_save_time_AO:
                    lx.eval('select.subItem {%s} set textureLayer;mediaClip' % ImageNameAO)
                    lx.eval('!clip.reload')
                    lx.eval('select.drop item')
                    lx.eval('select.clear item')
                    lx.eval('select.drop schmNode')
                    lx.eval('select.drop channel')
                    lx.eval('select.drop link')

            if Smo_MarmosetToolbag_AOF:
                if image_load_time_AOF > image_save_time_AOF:
                    lx.eval('select.subItem {%s} set textureLayer;mediaClip' % ImageNameAOF)
                    lx.eval('!clip.reload')
                    lx.eval('select.drop item')
                    lx.eval('select.clear item')
                    lx.eval('select.drop schmNode')
                    lx.eval('select.drop channel')
                    lx.eval('select.drop link')

            if Smo_MarmosetToolbag_TSNRM:
                if image_load_time_TSNRM > image_save_time_TSNRM:
                    lx.eval('select.subItem {%s} set textureLayer;mediaClip' % ImageNameTSNRM)
                    lx.eval('!clip.reload')
                    lx.eval('select.drop item')
                    lx.eval('select.clear item')
                    lx.eval('select.drop schmNode')
                    lx.eval('select.drop channel')
                    lx.eval('select.drop link')

            if Smo_MarmosetToolbag_OSNRM:
                if image_load_time_OSNRM > image_save_time_OSNRM:
                    lx.eval('select.subItem {%s} set textureLayer;mediaClip' % ImageNameOSNRM)
                    lx.eval('!clip.reload')
                    lx.eval('select.drop item')
                    lx.eval('select.clear item')
                    lx.eval('select.drop schmNode')
                    lx.eval('select.drop channel')
                    lx.eval('select.drop link')

            if Smo_MarmosetToolbag_POS:
                if image_load_time_POS > image_save_time_POS:
                    lx.eval('select.subItem {%s} set textureLayer;mediaClip' % ImageNamePOS)
                    lx.eval('!clip.reload')
                    lx.eval('select.drop item')
                    lx.eval('select.clear item')
                    lx.eval('select.drop schmNode')
                    lx.eval('select.drop channel')
                    lx.eval('select.drop link')

            if Smo_MarmosetToolbag_CUR:
                if image_load_time_CUR > image_save_time_CUR:
                    lx.eval('select.subItem {%s} set textureLayer;mediaClip' % ImageNameCUR)
                    lx.eval('!clip.reload')
                    lx.eval('select.drop item')
                    lx.eval('select.clear item')
                    lx.eval('select.drop schmNode')
                    lx.eval('select.drop channel')
                    lx.eval('select.drop link')

            if Smo_MarmosetToolbag_OBJID:
                if image_load_time_OBJID > image_save_time_OBJID:
                    lx.eval('select.subItem {%s} set textureLayer;mediaClip' % ImageNameOBJID)
                    lx.eval('!clip.reload')
                    lx.eval('select.drop item')
                    lx.eval('select.clear item')
                    lx.eval('select.drop schmNode')
                    lx.eval('select.drop channel')

            if Smo_MarmosetToolbag_THI:
                if image_load_time_THI > image_save_time_THI:
                    lx.eval('select.subItem {%s} set textureLayer;mediaClip' % ImageNameTHI)
                    lx.eval('!clip.reload')
                    lx.eval('select.drop item')
                    lx.eval('select.clear item')
                    lx.eval('select.drop schmNode')
                    lx.eval('select.drop channel')
                    lx.eval('select.drop link')

            if Smo_MarmosetToolbag_MATID:
                if image_load_time_MATID > image_save_time_MATID:
                    lx.eval('select.subItem {%s} set textureLayer;mediaClip' % ImageNameMATID)
                    lx.eval('!clip.reload')
                    lx.eval('select.drop item')
                    lx.eval('select.clear item')
                    lx.eval('select.drop schmNode')
                    lx.eval('select.drop channel')
                    lx.eval('select.drop link')

            if Smo_MarmosetToolbag_ALBEDO:
                if image_load_time_ALBEDO > image_save_time_ALBEDO:
                    lx.eval('select.subItem {%s} set textureLayer;mediaClip' % ImageNameALBEDO)
                    lx.eval('!clip.reload')
                    lx.eval('select.drop item')
                    lx.eval('select.clear item')
                    lx.eval('select.drop schmNode')
                    lx.eval('select.drop channel')

            if Smo_MarmosetToolbag_UVID:
                if image_load_time_UVID > image_save_time_UVID:
                    lx.eval('select.subItem {%s} set textureLayer;mediaClip' % ImageNameUVID)
                    lx.eval('!clip.reload')
                    lx.eval('select.drop item')
                    lx.eval('select.clear item')
                    lx.eval('select.drop schmNode')
                    lx.eval('select.drop channel')
                    lx.eval('select.drop link')

            # if ExplodePrePass == 1 :
            # Get the Unique name of the current Exploded Meshlayer and save it in User Values
            # TempExplodedMeshMarmosetToolbag = lx.eval ('!!user.value SMO_UseVal_MARMOSET_TempExplodedMesh ?')
            # lx.eval('select.subItem {%s} set mesh;replicator;meshInst;camera;light;txtrLocator;backdrop;groupLocator;replicator;surfGen;locator;falloff;deform;locdeform;weightContainer;morphContainer;deformGroup;deformMDD2;ABCStreamingDeformer;morphDeform;itemInfluence;genInfluence;deform.push;deform.wrap;softLag;ABCCurvesDeform.sample;ABCdeform.sample;force.root;baseVolume;chanModify;itemModify;meshoperation;chanEffect;defaultShader;defaultShader 0 0' % TempExplodedMeshMarmosetToolbag)
            # lx.eval('!delete')

            # if ExplodePrePass == 0 :
            # Get the Unique name of the current Exploded Meshlayer and save it in User Values
            # TempExplodedMeshMarmosetToolbag = lx.eval ('!!user.value SMO_UseVal_MARMOSET_TempExplodedMesh ?')
            # lx.eval('select.subItem {%s} set mesh;replicator;meshInst;camera;light;txtrLocator;backdrop;groupLocator;replicator;surfGen;locator;falloff;deform;locdeform;weightContainer;morphContainer;deformGroup;deformMDD2;ABCStreamingDeformer;morphDeform;itemInfluence;genInfluence;deform.push;deform.wrap;softLag;ABCCurvesDeform.sample;ABCdeform.sample;force.root;baseVolume;chanModify;itemModify;meshoperation;chanEffect;defaultShader;defaultShader 0 0' % TempExplodedMeshMarmosetToolbag)
            # lx.eval('item.channel locator$visible off')

            # Get the Unique name of the current Target Meshlayer and save it in User Values
            # TargetMeshMarmosetToolbag = lx.eval ('!!user.value SMO_UseVal_MARMOSET_TargetMesh ?')
            # lx.eval('select.subItem {%s} set mesh;replicator;meshInst;camera;light;txtrLocator;backdrop;groupLocator;replicator;surfGen;locator;falloff;deform;locdeform;weightContainer;morphContainer;deformGroup;deformMDD2;ABCStreamingDeformer;morphDeform;itemInfluence;genInfluence;deform.push;deform.wrap;softLag;ABCCurvesDeform.sample;ABCdeform.sample;force.root;baseVolume;chanModify;itemModify;meshoperation;chanEffect;defaultShader;defaultShader 0 0' % TargetMeshMarmosetToolbag)

        # CLEANUP scene for Viewing the data back from Marmoset
        # Hide the HighPoly
        lx.eval('smo.GC.DeselectAll')
        lx.eval('smo.GC.CreateDeleteSelSetFromMTypTag 1')
        # Hide HighPoly
        lx.eval('smo.GC.SelectMTypMesh 2')
        lx.eval('hide.sel')
        lx.eval('select.drop item')
        # Delete Temporary Selection Set (from Tags) of Lowpoly, Cage or HighPoly meshes
        lx.eval('smo.GC.CreateDeleteSelSetFromMTypTag 0')
        lx.eval('smo.GC.DeselectAll')


lx.bless(SMO_MARMOSET_LIVELINK_AutoSegmentedExport_Cmd, Cmd_Name)

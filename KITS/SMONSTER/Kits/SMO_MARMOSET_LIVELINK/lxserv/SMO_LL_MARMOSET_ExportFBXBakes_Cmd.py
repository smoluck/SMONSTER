#python
#---------------------------------------
# Name:         SMO_LL_MARMOSET_ExportFBXBakes_Cmd.py
# Version:      1.20
#
# Purpose:      This Command is designed to :
#               Export LowPoly/Cage/HighPoly Meshes from current scene,
#               based on MTyp Tag, as FBX to MarmosetToolbag temp Folder.
#               Create a Texture to store the TSNM.
#               Resolution defined by Argument in pixel.
#
# Author:       Franck ELISABETH
# Website:      http://www.smoluck.com
#
# Modified:     09/07/2020
# Copyright:    (c) Franck Elisabeth 2017-2022
#---------------------------------------

import modo, lx, lxifc, lxu.command, lxu.select, subprocess, os

Cmd_Name = "smo.LL.MARMOSET.ExportFBXBakes"

class SMO_MARMOSET_LIVELINK_ExportFBXBakes_Cmd (lxu.command.BasicCommand):
    def __init__ (self):
        lxu.command.BasicCommand.__init__(self)
        self.dyna_Add("Explode Pre Pass", lx.symbol.sTYPE_INTEGER)
        self.basic_SetFlags (0, lx.symbol.fCMDARG_OPTIONAL)
        self.dyna_Add("Explode Distance By Prefs", lx.symbol.sTYPE_INTEGER)
        self.basic_SetFlags (1, lx.symbol.fCMDARG_OPTIONAL)
        
        self.scrp_svc = lx.service.ScriptSys ()
        self.sel_svc = lx.service.Selection ()
    
    def cmd_Interact (self):
        pass
    
    def cmd_UserName (self):
        return 'SMO LL MARMOSET - Export Game Ready FBX For Bakes'
    
    def cmd_Desc (self):
        return 'Export LowPoly/Cage/HighPoly Meshes from current scene, based on MTyp Tag, as FBX to Temp Scene Path SubFolder.'
    
    def cmd_Tooltip (self):
        return 'Export LowPoly/Cage/HighPoly Meshes from current scene, based on MTyp Tag, as FBX to Temp Scene Path SubFolder.'
    
    def cmd_Help (self):
        return 'https://twitter.com/sm0luck'
    
    def basic_ButtonName (self):
        return 'SMO LL MARMOSET - Export Game Ready FBX For Bakes'
    
    def cmd_Flags (self):
        return lx.symbol.fCMD_UNDO
    
    def basic_Enable (self, msg):
        return True
    
    def recurseToFindFBXMeshes (self, fbx_item, fbx_meshes, mesh_items):
        fbx_item_child_count = fbx_item.SubCount ()
        for child_index in range(fbx_item_child_count):
            child = fbx_item.SubByIndex (child_index)
            for x, mesh_item in enumerate (mesh_items):
                if child.Name () == mesh_item.UniqueName ():
                    fbx_meshes[x] = child
            self.recurseToFindFBXMeshes (child, fbx_meshes, mesh_items)
    
    
    
    def getUserValue (self, name):
        try:
            valueObj = self.scrp_svc.UserValueLookup (name)
        except:
            return None
        
        itype = valueObj.Type ()
        if itype == lx.symbol.i_TYPE_INTEGER:
            return valueObj.GetInt ()
        elif itype == lx.symbol.i_TYPE_STRING:
            return valueObj.GetString ()
        elif itype == lx.symbol.i_TYPE_FLOAT:
            return valueObj.GetFlt ()
    
    
    
    def storeFBXSettings (self):
        FBX_USERVALUE_PREFIX    = 'sceneio.fbx.save.'
        FBX_USERVALUE_COMMAND   = 'user.value ' + FBX_USERVALUE_PREFIX
        fbxSettings = {}
        uValCount = self.scrp_svc.UserValueCount ()
        for x in range(uValCount):
            try:
                uval = self.scrp_svc.UserValueByIndex (x)
            except IndexError:
                print("Invalid User Value Index: %s (%s total user values)" % (x, uValCount))
            else:
                name = uval.Name ()
                if name.startswith ('sceneio.fbx.save.'):
                    fbxSettings[name] = self.getUserValue (name)
        return fbxSettings
    
    
    
    def restoreFBXSettings (self, fbxSettings):
        for name, value in fbxSettings.items():
            lx.eval ('user.value %s %s' % (name, value))
    
    
    
    def basic_Execute (self, msg, flags):
        # get modo's temp dir
        LocalTempFolder = lx.eval('query platformservice path.path ? temp')
        # lx.out ('Local Temp Path:    ', LocalTempFolder)
        
        ###########  Check User Values  ###########
        NameTag_LP = lx.eval1 ('user.value SMO_UseVal_MARMOSET_NameTagString_low ?')
        # lx.out ('Nametag for Lowpoly:    ', NameTag_LP)
        NameTag_Cage = lx.eval1 ('user.value SMO_UseVal_MARMOSET_NameTagString_cage ?')
        # lx.out ('Nametag for Cage:    ', NameTag_Cage)
        NameTag_HP = lx.eval1 ('user.value SMO_UseVal_MARMOSET_NameTagString_high ?')
        # lx.out ('Nametag for HighPoly:    ', NameTag_HP)
        
        
        AutoSave = lx.eval1 ('user.value SMO_UseVal_MARMOSET_AutoSaveSceneBeforeProcess ?')
        # lx.out ('AutoSave Scene before Export:    ', AutoSave)
        
        
        # the Freeze Subdivided Poly on High in Preferences. Incremental Save in this Mode
        Smo_Marmoset_FreezeHPSubdiv = lx.eval1 ('user.value SMO_UseVal_MARMOSET_FreezeHPSubdiv ?')
        # If FBX export are stored Locally in Scene Path Subfolder
        Smo_Marmoset_ScenePathSubfolder = lx.eval1 ('user.value SMO_UseVal_MARMOSET_ScenePathSubfolder ?')
        
        
        SceneName = lx.eval('smo.GC.GetSceneDetail 5 ?')
        # lx.out('Scene File Name:    ', SceneName)
        
        CurrentScenePath = lx.eval('smo.GC.GetSceneDetail 0 ?')
        # lx.out('Current Scene Full Path:    ', CurrentScenePath)
        
        if Smo_Marmoset_ScenePathSubfolder == 1 :
            SceneFolderPath = lx.eval('smo.GC.GetSceneDetail 4 ?')
            # lx.out('Scene Folder Path (Path Without File and Extension):    ',SceneFolderPath)
        
        
        if AutoSave == 1 :
            lx.eval('item.create sunLight')
            lx.eval('!!delete')
            lx.eval('scene.saveAs {%s} $LXOB false' % CurrentScenePath)
        
        
        if Smo_Marmoset_FreezeHPSubdiv == 1 :
            lx.eval('smo.GC.FreezeHighSubdivPoly')
        
        
        # name our temp file
        OutputMeshFileFrmt = ".fbx"
        FBXSubFolder = "MARMO_BAKES"
        KIT = "SMO_Marmoset_LL"
        FileTagKit = "_BAKE"
        ###########################################
        
        
        
        scene = modo.scene.current()
        ############### 1 ARGUMENTS ###############
        # ExplodePrePass = self.dyna_Int (0)
        # ExplodeDistanceByPrefs = self.dyna_Int (1)
        ###########################################
        
        
        fbxSettings = self.storeFBXSettings ()
        # print fbxSettings
        
        # MODO version checks. Different versions have different FBX options.
        self.modo_ver = int(lx.eval ('query platformservice appversion ?'))
        if self.modo_ver < 1300:
            lx.out ('Requires Modo 13.0 or newer.')
            return
        
        
        # Create Selection Set from Tags to temporary select Lowpoly, Cage or HighPoly meshes to export them.
        lx.eval('smo.GC.CreateDeleteSelSetFromMTypTag 1')
        
        # Select target LowPoly Meshes via MTyp Tags
        lx.eval('smo.GC.SelectMTypMesh 0')
        
        # create Cage meshes
        lx.eval('smo.GC.CreateCloneCAGEData')
        
        # Select Back the LowPoly Meshes via MTyp Tags
        lx.eval('smo.GC.SelectMTypMesh 0')
        





        # Grab the active layer.
        layer_svc = lx.service.Layer ()
        layer_scan = lx.object.LayerScan (layer_svc.ScanAllocate (lx.symbol.f_LAYERSCAN_ACTIVE))
        if not layer_scan.test ():
            lx.out ('Layerscan failed.')
            return
        
        
        
        # Early out if there are no active layers.
        layer_count = layer_scan.Count ()
        if layer_count <= 0:
            lx.out ('No active layers.')
            return
        
        
        
        # Grab the relevant meshes and UV maps.
        mesh_items = []
        mesh_uvs = []
        for layer_idx in range(layer_count):
            mesh_item = lx.object.Item (layer_scan.MeshItem (layer_idx))
            if not mesh_item.test ():
                lx.out ('Failed to get mesh item of layer %s.' % layer_idx)
                continue
            
            mesh_name = mesh_item.UniqueName ()
            
            mesh = lx.object.Mesh (layer_scan.MeshBase (layer_idx))
            if not mesh.test ():
                lx.out ('Failed to get mesh of %s.' % mesh_name)
                continue
            
            # Get the selected UV maps that exist on this model.
            meshmap = lx.object.MeshMap (mesh.MeshMapAccessor ())
            if not meshmap.test ():
                lx.out ('Failed to get meshmap accessor of %s.' % mesh_name)
                continue
            
                
            mesh_items.append (mesh_item)
            # mesh_uvs.append (selected_uv_names_mesh)
        
        layer_scan.Apply ()
        
        # Select the meshes.
        for x, mesh_item in enumerate(mesh_items):
            if x == 0:
                lx.eval ('select.subItem %s set mesh 0 0' % mesh_item.Ident ())
            else:
                lx.eval ('select.subItem %s add mesh 0 0' % mesh_item.Ident ())
        
        
        
        
        
        
        ############################ Export FBX Data #############################
        
        # Store user's FBX preferences for restoring later.
        fbxSettings = self.storeFBXSettings ()
        
        
        # build up the path for the OutputFolder using the User value to guide wich solution is used.
        if Smo_Marmoset_ScenePathSubfolder == 1 :
            OutputFolder = SceneFolderPath
            # OutputFolder = (os.path.join(SceneFolderPath + "\\" + KIT ))
            # lx.out ('Output Folder path:    ', OutputFolder)
        
        if Smo_Marmoset_ScenePathSubfolder == 0 :
            OutputFolder = (os.path.join(LocalTempFolder + "\\" + KIT + "\\" + SceneName))
            # lx.out ('Output Folder path:    ', OutputFolder)
        
        
        # name our LowPoly / Cage / HighPoly files
        fbx_file_name_LP = (SceneName + FileTagKit + NameTag_LP + OutputMeshFileFrmt)
        # lx.out ('Filename for Lowpoly:    ', fbx_file_name_LP)
        fbx_file_name_Cage = (SceneName + FileTagKit + NameTag_Cage + OutputMeshFileFrmt)
        # lx.out ('Filename for Cage:    ', fbx_file_name_Cage)
        fbx_file_name_HP = (SceneName + FileTagKit + NameTag_HP + OutputMeshFileFrmt)
        # lx.out ('Filename for Cage:    ', fbx_file_name_HP)
        
        
        if Smo_Marmoset_ScenePathSubfolder == 0 :
            # builds the complete path out of the temp dir/or/ Scene subfolder and the bakes file name
            fbx_export_path_LP = os.path.join(OutputFolder, fbx_file_name_LP)
            lx.out ('Lowpoly File Path:    ', fbx_export_path_LP)
            fbx_export_path_Cage = os.path.join(OutputFolder, fbx_file_name_Cage)
            lx.out ('Cage File Path:    ', fbx_export_path_Cage)
            fbx_export_path_HP = os.path.join(OutputFolder, fbx_file_name_HP)
            lx.out ('Highpoly File Path:    ', fbx_export_path_HP)
        if Smo_Marmoset_ScenePathSubfolder == 1 :
            # builds the complete path out of the temp dir/or/ Scene subfolder and the bakes file name
            fbx_export_path_LP = os.path.join(OutputFolder, FBXSubFolder, fbx_file_name_LP)
            lx.out ('Lowpoly File Path:    ', fbx_export_path_LP)
            fbx_export_path_Cage = os.path.join(OutputFolder, FBXSubFolder, fbx_file_name_Cage)
            lx.out ('Cage File Path:    ', fbx_export_path_Cage)
            fbx_export_path_HP = os.path.join(OutputFolder, FBXSubFolder, fbx_file_name_HP)
            lx.out ('Highpoly File Path:    ', fbx_export_path_HP)
        
        
        ############################ Export FBX Data ########## LowPoly ##########
        # ------------------------------------------------------------------------
        
        # Apply FBX settings we want to use for Export.
        
        ###############          Settings for LowPoly Mesh         ###############
        
        # Essentially disabling everything except geometry and setting export to selection.
        # Also picking FBX2013, just because that should ensure things export smoothly.
        lx.eval ('user.value sceneio.fbx.save.format 2')
        lx.eval ('user.value sceneio.fbx.save.exportType 1')
        lx.eval ('user.value sceneio.fbx.save.geometry 1')
        lx.eval ('user.value sceneio.fbx.save.exportToASCII 0')
        lx.eval ('user.value sceneio.fbx.save.animationOnly 0')
        lx.eval ('user.value sceneio.fbx.save.cameras 0')
        lx.eval ('user.value sceneio.fbx.save.lights 0')
        lx.eval ('user.value sceneio.fbx.save.materials 0')
        lx.eval ('user.value sceneio.fbx.save.polygonParts 0')
        lx.eval ('user.value sceneio.fbx.save.selectionSets 0')
        lx.eval ('user.value sceneio.fbx.save.smoothingGroups 1')
        lx.eval ('user.value sceneio.fbx.save.morphMaps 0')
        lx.eval ('user.value sceneio.fbx.save.animation 0')
        lx.eval ('user.value sceneio.fbx.save.sampleAnimation 0')
        
        if self.modo_ver >= 1300 and self.modo_ver <= 1399:
            try:
                lx.eval ('user.value sceneio.fbx.save.surfaceRefining FBXExportTriangles')
                lx.eval ('user.value sceneio.fbx.save.format FBX2018')
            except RuntimeError:
                pass
        if self.modo_ver >= 1400 and self.modo_ver <= 1499:
            try:
                # lx.eval ('user.value sceneio.fbx.save.surfaceRefining FBXExportSubDiv')
                lx.eval ('user.value sceneio.fbx.save.surfaceRefining FBXExportTriangles')
                lx.eval ('user.value sceneio.fbx.save.format FBX2018')
            except RuntimeError:
                pass
        
        
        # Selection Lowpoly Meshes
        lx.eval('smo.GC.SelectMTypMesh 0')
        
        
        # make sure the Lowpoly Path directory exists, if not create it
        if not os.path.exists(os.path.dirname(fbx_export_path_LP)):
            # try to create the directory. 
            try:
                os.makedirs(os.path.dirname(fbx_export_path_LP))
            except:
                # if that fails for any reason print out the error
                print(traceback.format_exc())
        else:
            if fbx_export_path_LP == None:
                lx.out ('Didn\'t save FBX for MarmosetToolbag.')
                return
            else:
                fbx_export_path_LP = os.path.splitext (fbx_export_path_LP)[0] + '.fbx'
                fbx_file_name_LP = os.path.splitext (os.path.basename (fbx_export_path_LP))[0]
        
        
        lx.eval('scene.saveAs filename:"{}" format:"fbx" export:true'.format(fbx_export_path_LP))
        fbx_save_time_LP = os.path.getmtime (fbx_export_path_LP)
        lx.eval('select.drop item')
        #########################################################
        
        
        
        
        
        
        
        ############################ Export FBX Data ########## Cage ##########
        # ------------------------------------------------------------------------
        
        # Apply FBX settings we want to use for Export.
        
        ###############          Settings for Cage Mesh         ###############
        
        # Essentially disabling everything except geometry and setting export to selection.
        # Also picking FBX2013, just because that should ensure things export smoothly.
        lx.eval ('user.value sceneio.fbx.save.format 2')
        lx.eval ('user.value sceneio.fbx.save.exportType 1')
        lx.eval ('user.value sceneio.fbx.save.geometry 1')
        lx.eval ('user.value sceneio.fbx.save.exportToASCII 0')
        lx.eval ('user.value sceneio.fbx.save.animationOnly 0')
        lx.eval ('user.value sceneio.fbx.save.cameras 0')
        lx.eval ('user.value sceneio.fbx.save.lights 0')
        lx.eval ('user.value sceneio.fbx.save.materials 0')                 # No material save for Cage
        lx.eval ('user.value sceneio.fbx.save.polygonParts 0')
        lx.eval ('user.value sceneio.fbx.save.selectionSets 0')
        lx.eval ('user.value sceneio.fbx.save.smoothingGroups 1')
        lx.eval ('user.value sceneio.fbx.save.morphMaps 0')
        lx.eval ('user.value sceneio.fbx.save.animation 0')
        lx.eval ('user.value sceneio.fbx.save.sampleAnimation 0')
        
        if self.modo_ver >= 1300 and self.modo_ver <= 1399:
            try:
                lx.eval ('user.value sceneio.fbx.save.surfaceRefining FBXExportTriangles')
                lx.eval ('user.value sceneio.fbx.save.format FBX2018')
            except RuntimeError:
                pass
        if self.modo_ver >= 1400 and self.modo_ver <= 1499:
            try:
                # lx.eval ('user.value sceneio.fbx.save.surfaceRefining FBXExportSubDiv')
                lx.eval ('user.value sceneio.fbx.save.surfaceRefining FBXExportTriangles')
                lx.eval ('user.value sceneio.fbx.save.format FBX2018')
            except RuntimeError:
                pass
        
        
        # Selection Cage Meshes
        lx.eval('smo.GC.SelectMTypMesh 1')
        
        
        # make sure the Cage Path directory exists, if not create it
        if not os.path.exists(os.path.dirname(fbx_export_path_Cage)):
            # try to create the directory. 
            try:
                os.makedirs(os.path.dirname(fbx_export_path_Cage))
            except:
                # if that fails for any reason print out the error
                print(traceback.format_exc())
        else:
            if fbx_export_path_Cage == None:
                lx.out ('Didn\'t save FBX for MarmosetToolbag.')
                return
            else:
                fbx_export_path_Cage = os.path.splitext (fbx_export_path_Cage)[0] + '.fbx'
                fbx_file_name_Cage = os.path.splitext (os.path.basename (fbx_export_path_Cage))[0]
        
        
        lx.eval('scene.saveAs filename:"{}" format:"fbx" export:true'.format(fbx_export_path_Cage))
        fbx_save_time_Cage = os.path.getmtime (fbx_export_path_Cage)
        lx.eval('select.drop item')
        
        # IMPORTANT
        # Selection Cage Group and Meshes and delete them as they are temporary data.
        lx.eval('smo.GC.SelectMTypMesh 1')
        lx.eval('!delete')
        #########################################################
        
        
        
        
        
        ############################ Export FBX Data ########## HighPoly ##########
        # ------------------------------------------------------------------------
        
        # Apply FBX settings we want to use for Export.
        
        ###############          Settings for HighPoly Mesh         ###############
        
        # Essentially disabling everything except geometry and setting export to selection.
        # Also picking FBX2013, just because that should ensure things export smoothly.
        lx.eval ('user.value sceneio.fbx.save.format 2')
        lx.eval ('user.value sceneio.fbx.save.exportType 1')
        lx.eval ('user.value sceneio.fbx.save.geometry 1')
        lx.eval ('user.value sceneio.fbx.save.exportToASCII 0')
        lx.eval ('user.value sceneio.fbx.save.animationOnly 0')
        lx.eval ('user.value sceneio.fbx.save.cameras 0')
        lx.eval ('user.value sceneio.fbx.save.lights 0')
        lx.eval ('user.value sceneio.fbx.save.materials 1')
        lx.eval ('user.value sceneio.fbx.save.polygonParts 0')
        lx.eval ('user.value sceneio.fbx.save.selectionSets 0')
        lx.eval ('user.value sceneio.fbx.save.smoothingGroups 1')
        lx.eval ('user.value sceneio.fbx.save.morphMaps 0')
        lx.eval ('user.value sceneio.fbx.save.animation 0')
        lx.eval ('user.value sceneio.fbx.save.sampleAnimation 0')
        
        if self.modo_ver >= 1300 and self.modo_ver <= 1399:
            try:
                lx.eval ('user.value sceneio.fbx.save.surfaceRefining FBXExportTriangles')
                lx.eval ('user.value sceneio.fbx.save.format FBX2018')
            except RuntimeError:
                pass
        if self.modo_ver >= 1400 and self.modo_ver <= 1499:
            try:
                # lx.eval ('user.value sceneio.fbx.save.surfaceRefining FBXExportSubDiv')
                lx.eval ('user.value sceneio.fbx.save.surfaceRefining FBXExportTriangles')
                lx.eval ('user.value sceneio.fbx.save.format FBX2018')
            except RuntimeError:
                pass
        
        
        # Selection HighPoly Meshes
        lx.eval('smo.GC.SelectMTypMesh 2')
        
        
        # make sure the HighPoly Path directory exists, if not create it
        if not os.path.exists(os.path.dirname(fbx_export_path_HP)):
            # try to create the directory. 
            try:
                os.makedirs(os.path.dirname(fbx_export_path_HP))
            except:
                # if that fails for any reason print out the error
                print(traceback.format_exc())
        else:
            if fbx_export_path_HP == None:
                lx.out ('Didn\'t save FBX for MarmosetToolbag.')
                return
            else:
                fbx_export_path_HP = os.path.splitext (fbx_export_path_HP)[0] + '.fbx'
                fbx_file_name_HP = os.path.splitext (os.path.basename (fbx_export_path_HP))[0]
        
        
        lx.eval('!scene.saveAs filename:"{}" format:"fbx" export:true'.format(fbx_export_path_HP))
        fbx_save_time_HP = os.path.getmtime (fbx_export_path_HP)
        lx.eval('select.drop item')
        #########################################################
        
        
        
        
        
        # Restore the FBX preferences.
        self.restoreFBXSettings (fbxSettings)
        
        
        # CLEANUP scene
        # Delete Temporary Selection Set (from Tags) of Lowpoly, Cage or HighPoly meshes
        lx.eval('smo.GC.CreateDeleteSelSetFromMTypTag 0')
        
        lx.eval('!scene.revert')


lx.bless (SMO_MARMOSET_LIVELINK_ExportFBXBakes_Cmd, Cmd_Name)

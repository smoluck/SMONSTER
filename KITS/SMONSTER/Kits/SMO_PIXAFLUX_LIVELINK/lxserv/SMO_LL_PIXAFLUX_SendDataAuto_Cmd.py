# python
"""
Name:             SMO_LL_PIXAFLUX_SendDataAuto_Cmd.py

Purpose:      This Command is designed to:
              Export the Current Mesh as FBX to PixaFlux temp Folder.
              Create a Texture to store the TSNM.
              Resolution defined by Argument in pixel.

Author:       Franck ELISABETH
Website:      https://www.smoluck.com
Modified:     09/07/2020
Copyright:    (c) Franck Elisabeth 2017-2022
"""

# !/usr/bin/env python

import lx
import lxu.command
import lxu.select
import os
import subprocess
import traceback

Cmd_Name = "smo.LL.PIXAFLUX.SendDataAuto"
# smo.LL.PIXAFLUX.SendDataAuto 1 0 2048


class SMO_LL_PIXAFLUX_SendData_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
        self.modo_ver = int(lx.eval('query platformservice appversion ?'))
        self.dyna_Add("Map Size", lx.symbol.sTYPE_INTEGER)
        self.basic_SetFlags(0, lx.symbol.fCMDARG_OPTIONAL)  # here the (0) define the argument index.
        self.dyna_Add("Explode Pre Pass", lx.symbol.sTYPE_INTEGER)
        self.basic_SetFlags(1, lx.symbol.fCMDARG_OPTIONAL)
        self.dyna_Add("Explode Distance By Prefs", lx.symbol.sTYPE_INTEGER)
        self.basic_SetFlags(2, lx.symbol.fCMDARG_OPTIONAL)

        self.scrp_svc = lx.service.ScriptSys()
        self.sel_svc = lx.service.Selection()

    def cmd_Interact(self):
        pass

    def cmd_UserName(self):
        return 'SMO LL PIXAFLUX - Send Data Auto'

    def cmd_Desc(self):
        return 'Export the Current Mesh as FBX to PixaFlux temp Folder. Create a Texture to store the TSNM. Resolution defined by Argument in pixel.'

    def cmd_Tooltip(self):
        return 'Export the Current Mesh as FBX to PixaFlux temp Folder. Create a Texture to store the TSNM. Resolution defined by Argument in pixel.'

    def cmd_Help(self):
        return 'https://twitter.com/sm0luck'

    def basic_ButtonName(self):
        return 'SMO LL PIXAFLUX - Send Data Auto'

    def cmd_Flags(self):
        return lx.symbol.fCMD_UNDO

    def basic_Enable(self, msg):
        return True

    # Validate the path to PixaFlux is good.
    def validPixaFluxPath(self, pixaflux_exe_path):
        return ((pixaflux_exe_path != None) and os.path.lexists(pixaflux_exe_path) and (
                    os.path.splitext(pixaflux_exe_path)[1].lower() == '.exe'))

    # def getUVSelection (self):
    # uv_selection = []
    # vmap_pkt_trans = lx.object.VMapPacketTranslation (self.sel_svc.Allocate (lx.symbol.sSELTYP_VERTEXMAP))
    # sel_type_vmap = self.sel_svc.LookupType (lx.symbol.sSELTYP_VERTEXMAP)

    # for i in range(self.sel_svc.Count (sel_type_vmap)):
    # pkt = self.sel_svc.ByIndex (sel_type_vmap, i)
    # if vmap_pkt_trans.Type (pkt) == lx.symbol.i_VMAP_TEXTUREUV:
    # uv_selection.append (vmap_pkt_trans.Name (pkt))
    # return uv_selection

    # Set the path to PixaFlux in a user variable.
    def setPixaFluxPath(self, pixaflux_exe_path):
        if self.validPixaFluxPath(pixaflux_exe_path):
            # try:
            # lx.eval ('!!user.defNew name:Smo_PixaFluxPath type:string life:config')
            # except:
            # pass

            try:
                lx.eval('!!user.value Smo_PixaFluxPath {%s}' % pixaflux_exe_path)
            except:
                pass

            return lx.eval1('user.value Smo_PixaFluxPath ?') == pixaflux_exe_path
        return False

    # Ask the user for the path to PixaFlux.
    def findPixaFluxPath(self):
        default_path = 'C:\Program Files\PixaFlux\\PixaFlux.exe'
        if self.setPixaFluxPath(default_path):
            return True
        else:
            try:
                lx.eval('dialog.setup fileOpen')
                lx.eval('dialog.title "Select PixaFlux executable file"')
                lx.eval('dialog.fileTypeCustom format:exe username:{EXE} loadPattern:{*.exe} saveExtension:exe')
                if self.modo_ver == 801:
                    lx.eval('+dialog.open')
                else:
                    lx.eval('dialog.open')
                pixaflux_exe_path = lx.eval1('dialog.result ?')
            except:
                pass
            else:
                if self.setPixaFluxPath(pixaflux_exe_path):
                    return True

        lx.out('Failed to define path to PixaFlux.')
        return False

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
        # ------------- ARGUMENTS ------------- #
        MapSize = self.dyna_Int(0)
        ExplodePrePass = self.dyna_Int(1)
        ExplodeDistanceByPrefs = self.dyna_Int(2)
        # ------------------------------------- #

        if ExplodeDistanceByPrefs == 1 and ExplodePrePass == 1:
            lx.eval('smo.LL.PIXAFLUX.DupAndExplodeByDist 1')

        if ExplodeDistanceByPrefs == 0 and ExplodePrePass == 1:
            lx.eval('smo.LL.PIXAFLUX.DupAndExplodeByDist 0')

        fbxSettings = self.storeFBXSettings()
        print(fbxSettings)

        # MODO version checks. Different versions have different FBX options.
        if self.modo_ver < 901:
            lx.out('Requires Modo 901 or newer.')
            return

        # Get the selected UV names.
        # selected_uv_names = self.getUVSelection ()
        # if len (selected_uv_names) == 0:
        # lx.out ('No UV maps selected.')
        # return

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

        # Get PixaFlux executable path.
        Smo_PixaFluxPath = None
        try:
            Smo_PixaFluxPath = lx.eval1('!!user.value Smo_PixaFluxPath ?')
        except:
            if not self.findPixaFluxPath():
                return
        else:
            if not self.validPixaFluxPath(Smo_PixaFluxPath):
                if not self.findPixaFluxPath():
                    return
                else:
                    Smo_PixaFluxPath = lx.eval1('!!user.value Smo_PixaFluxPath ?')

        if Smo_PixaFluxPath is None:
            lx.out('Invalid PixaFlux path.')
            return

        # Store user's FBX preferences for restoring later.
        fbxSettings = self.storeFBXSettings()

        # Apply FBX settings we want to use for PixaFlux.
        # Essentially disabling everything except geometry and setting export to selection.
        # Also picking FBX2013, just because that should ensure things export smoothly.
        lx.eval('user.value sceneio.fbx.save.format 2')
        lx.eval('user.value sceneio.fbx.save.exportType 1')
        lx.eval('user.value sceneio.fbx.save.geometry 1')
        lx.eval('user.value sceneio.fbx.save.exportToASCII 0')
        lx.eval('user.value sceneio.fbx.save.animationOnly 0')
        lx.eval('user.value sceneio.fbx.save.cameras 0')
        lx.eval('user.value sceneio.fbx.save.lights 0')
        lx.eval('user.value sceneio.fbx.save.materials 1')
        lx.eval('user.value sceneio.fbx.save.polygonParts 0')
        lx.eval('user.value sceneio.fbx.save.selectionSets 0')
        lx.eval('user.value sceneio.fbx.save.smoothingGroups 1')
        lx.eval('user.value sceneio.fbx.save.morphMaps 0')
        lx.eval('user.value sceneio.fbx.save.animation 0')
        lx.eval('user.value sceneio.fbx.save.sampleAnimation 0')

        if self.modo_ver > 900:
            try:
                lx.eval1('user.value sceneio.fbx.save.tangentsBitangents 0')
            except RuntimeError:
                pass
        if 1000 < self.modo_ver <= 1011:
            try:
                lx.eval('user.value sceneio.fbx.save.triangulate 1')
                lx.eval('user.value sceneio.fbx.save.meshSmoothing 1')
            except RuntimeError:
                pass
        if 1012 <= self.modo_ver <= 1099:
            try:
                lx.eval('user.value sceneio.fbx.save.surfaceRefining FBXExportTriangles')
            except RuntimeError:
                pass
        if 1100 <= self.modo_ver <= 1199:
            try:
                lx.eval('user.value sceneio.fbx.save.surfaceRefining FBXExportTriangles')
                lx.eval('user.value sceneio.fbx.save.format 4')
            except RuntimeError:
                pass
        if 1200 <= self.modo_ver <= 1299:
            try:
                lx.eval('user.value sceneio.fbx.save.surfaceRefining FBXExportTriangles')
                lx.eval('user.value sceneio.fbx.save.format 4')
            except RuntimeError:
                pass
        if 1300 <= self.modo_ver <= 1399:
            try:
                lx.eval('user.value sceneio.fbx.save.surfaceRefining FBXExportTriangles')
                lx.eval('user.value sceneio.fbx.save.format 4')
            except RuntimeError:
                pass
        if 1400 <= self.modo_ver <= 1499:
            try:
                # lx.eval ('user.value sceneio.fbx.save.surfaceRefining FBXExportSubDiv')
                lx.eval('user.value sceneio.fbx.save.surfaceRefining FBXExportTriangles')
                lx.eval('user.value sceneio.fbx.save.format 4')
            except RuntimeError:
                pass
        if 1500 <= self.modo_ver <= 1599:
            try:
                lx.eval ('user.value sceneio.fbx.save.surfaceRefining FBXExportSubDiv')
                lx.eval ('user.value sceneio.fbx.save.format FBX2013')
            except RuntimeError:
                pass



        ############################ Export FBX Data #############################
        # get modo's temp dir
        temp_dir = lx.eval('query platformservice path.path ? temp')
        # name our temp file
        fbx_file_name = "PixaFlux_DATA.fbx"
        # builds the complete path out of the temp dir and the temp file name
        fbx_export_path = os.path.join(temp_dir, "SMO_PixaFluxLiveLink", fbx_file_name)

        # make sure the SMO_PixaFluxLiveLink directory exists, if not create it
        if not os.path.exists(os.path.dirname(fbx_export_path)):
            # try to create the directory.
            try:
                os.makedirs(os.path.dirname(fbx_export_path))
            except:
                # if that fails for any reason print out the error
                print(traceback.format_exc())
        else:
            if fbx_export_path == None:
                lx.out('Didn\'t save FBX for PixaFlux.')
                return
            else:
                fbx_export_path = os.path.splitext(fbx_export_path)[0] + '.fbx'
                fbx_file_name = os.path.splitext(os.path.basename(fbx_export_path))[0]

        lx.eval('scene.saveAs filename:"{}" format:"fbx" export:true'.format(fbx_export_path))
        fbx_save_time = os.path.getmtime(fbx_export_path)

        #########################################################

        PolyRender = lx.eval('smo.GC.SelectPolyRenderItem ?')
        # lx.out('Render item Identity name is :',PolyRender)
        ShaderItem = lx.eval('smo.GC.SelectShaderItem ?')
        # lx.out('Shader item Identity name is :',ShaderItem)

        ShaderItem_ST_Pos = lx.eval('smo.GC.GetShaderItemPosIndex ?')
        # lx.out('Position Index of the Shader Item (in the Shader Tree) is :',ShaderItem_ST_Pos)
        Texture_ST_Pos = (ShaderItem_ST_Pos - 1)

        ############################ Create Image Data #############################
        # name our temp file
        ImageNameTSNRM = "PixaFlux_NM.png"
        # builds the complete path out of the temp dir and the temp file name
        image_export_path = os.path.join(temp_dir, "SMO_PixaFluxLiveLink", ImageNameTSNRM)

        if not os.path.exists(os.path.dirname(image_export_path)):
            # try to create the directory.
            try:
                os.makedirs(os.path.dirname(image_export_path))
            except:
                # if that fails for any reason print out the error
                print(traceback.format_exc())
        else:
            if image_export_path == None:
                lx.out('Didn\'t save Normal Map Image for PixaFlux.')
                return
            else:
                image_export_path = os.path.splitext(image_export_path)[0] + '.png'
                ImageNameTSNRM = os.path.splitext(os.path.basename(image_export_path))[0]

        # lx.eval('clip.new')
        if MapSize == 512:
            lx.eval('clip.newStill "{}" x512 RGBA false false format:PNG colorspace:(none)'.format(image_export_path))
        if MapSize == 1024:
            lx.eval('clip.newStill "{}" x1024 RGBA false false format:PNG colorspace:(none)'.format(image_export_path))
        if MapSize == 2048:
            lx.eval('clip.newStill "{}" x2048 RGBA false false format:PNG colorspace:(none)'.format(image_export_path))
        if MapSize == 4096:
            lx.eval('clip.newStill "{}" x4096 RGBA false false format:PNG colorspace:(none)'.format(image_export_path))
        lx.eval('clip.addStill "{}"'.format(image_export_path))
        # lx.eval('select.subItem {PIXAFLUX_NM:videoStill001} set mediaClip')
        # lx.command("select.subItem", item=ImageNameTSNRM, mode="set")

        # lx.eval('clip.save')

        # lx.eval('select.subItem {%s} set textureLayer;mediaClip' % ImageNameTSNRM)
        # lx.eval('select.item {%s} add' % ImageNameTSNRM)
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

        image_save_time = os.path.getmtime(image_export_path)
        # -------------------------------------------- #

        # Restore the FBX preferences.
        self.restoreFBXSettings(fbxSettings)

        # Call PixaFlux.
        proc = subprocess.Popen([Smo_PixaFluxPath, fbx_export_path], stdout=subprocess.PIPE)
        stdout, stderr = proc.communicate()
        rc = proc.returncode

        if rc != 0:
            # PixaFlux crashed or threw an error.
            lx.out('PixaFlux crashed.')
            lx.out('Standard Output: %s' % stdout)
            lx.out('Error Output: %s' % stderr)
        else:
            # Get the modified time of the export file.
            image_load_time = 0
            if os.path.lexists(image_export_path):
                image_load_time = os.path.getmtime(image_export_path)

            # User has likely saved over the old file.
            if image_load_time > image_save_time:
                lx.out('PixaFlux image updated.')

                lx.eval('select.drop item')
                lx.eval('select.clear item')
                lx.eval('select.drop schmNode')
                lx.eval('select.drop channel')
                lx.eval('select.drop link')

                # lx.eval('smo.GC.LoadStillImageInShaderTree')

                if ExplodePrePass == 1:
                    # Get the Unique name of the current Exploded Meshlayer and save it in User Values
                    TempExplodedMeshPixaFlux = lx.eval('!!user.value Smo_PixaFluxTempExplodedMesh ?')
                    lx.eval(
                        'select.subItem {%s} set mesh;replicator;meshInst;camera;light;txtrLocator;backdrop;groupLocator;replicator;surfGen;locator;falloff;deform;locdeform;weightContainer;morphContainer;deformGroup;deformMDD2;ABCStreamingDeformer;morphDeform;itemInfluence;genInfluence;deform.push;deform.wrap;softLag;ABCCurvesDeform.sample;ABCdeform.sample;force.root;baseVolume;chanModify;itemModify;meshoperation;chanEffect;defaultShader;defaultShader 0 0' % TempExplodedMeshPixaFlux)
                    lx.eval('!delete')

                # if ExplodePrePass == 0 :
                # Get the Unique name of the current Exploded Meshlayer and save it in User Values
                # TempExplodedMeshPixaFlux = lx.eval ('!!user.value Smo_PixaFluxTempExplodedMesh ?')
                # lx.eval('select.subItem {%s} set mesh;replicator;meshInst;camera;light;txtrLocator;backdrop;groupLocator;replicator;surfGen;locator;falloff;deform;locdeform;weightContainer;morphContainer;deformGroup;deformMDD2;ABCStreamingDeformer;morphDeform;itemInfluence;genInfluence;deform.push;deform.wrap;softLag;ABCCurvesDeform.sample;ABCdeform.sample;force.root;baseVolume;chanModify;itemModify;meshoperation;chanEffect;defaultShader;defaultShader 0 0' % TempExplodedMeshPixaFlux)
                # lx.eval('item.channel locator$visible off')

                # Get the Unique name of the current Target Meshlayer and save it in User Values
                # TargetMeshPixaFlux = lx.eval ('!!user.value Smo_PixaFluxTargetMesh ?')
                # lx.eval('select.subItem {%s} set mesh;replicator;meshInst;camera;light;txtrLocator;backdrop;groupLocator;replicator;surfGen;locator;falloff;deform;locdeform;weightContainer;morphContainer;deformGroup;deformMDD2;ABCStreamingDeformer;morphDeform;itemInfluence;genInfluence;deform.push;deform.wrap;softLag;ABCCurvesDeform.sample;ABCdeform.sample;force.root;baseVolume;chanModify;itemModify;meshoperation;chanEffect;defaultShader;defaultShader 0 0' % TargetMeshPixaFlux)


lx.bless(SMO_LL_PIXAFLUX_SendData_Cmd, Cmd_Name)

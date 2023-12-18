# python
"""
Name:           SMO_LL_RIZOMUV_Task_Repack_Cmd.py

Purpose:        This Command is designed to:
                SmartPack the current Model using a texture map resolution and optimization
                on given range of distorted UVIsland and get the updated data back in Modo.

Author:         Franck ELISABETH
Website:        https://www.linkedin.com/in/smoluck/
Created:        23/04/2023
Copyright:      (c) Franck Elisabeth 2017-2022
"""

# !/usr/bin/env python

import lx
import lxu.command
import lxu.select
import subprocess
import traceback
import os
import sys

Cmd_Name = "smo.LL.RIZOMUV.Task.SmartPack"


###############################################################################################
py_majorver = sys.version_info.major
py_minorver = sys.version_info.minor
print("-------------------------")
print("Python version is:\n", py_majorver, py_minorver)
print("-------------------------")
# Get Modo Preferences User Values for the Packing options
RUVL_UserVal_PackMapRes = int(lx.eval("!user.value SMO_UseVal_RUVL_Task_PackingMapRes ?"))
RUVL_UserVal_PackIteration = int(lx.eval("!user.value SMO_UseVal_RUVL_Task_PackingIteration ?"))

RUVL_UserVal_PackOpti = bool(lx.eval("!user.value SMO_UseVal_RUVL_Task_PackingOptimizeDistorted ?"))
RUVL_UserVal_PackOptiIter = int(lx.eval("!user.value SMO_UseVal_RUVL_Task_PackingOptiIteration ?"))
RUVL_UserVal_PackOptiDistRange = float(lx.eval("!user.value SMO_UseVal_RUVL_Task_PackingOptiDistRange ?"))
#####################################################
############# IMPORT RIZOMUVLINK MODULE #############
#####################################################


def get_ruvpath():
    """ 
    Returns the path to the most recent version
    of the RizomUV installation directory on the system using
    the windows registry.
    
    Try versions from 2029.10 to 2022.2 included
    """
    import os
    import winreg

    for i in range(9, 1, -1):
        for j in range(10, -1, -1):
            if i == 2 and j < 2:
                continue
            path = "SOFTWARE\\Rizom Lab\\RizomUV VS RS 202" + str(i) + "." + str(j)
            try:
                key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, path)
                exePath = winreg.QueryValue(key, "rizomuv.exe")
                return os.path.dirname(exePath)
            except FileNotFoundError:
                pass

    return None
# print(RizomUVWinRegisterInstallPath())
#################


#################
def ruvl_module_path(ruvl_path):
    riz_module_path = ruvl_path + "\\" + "RizomUVLink"  # + "\\" + "RizomUVLink.py"
    # print(riz_module_path)
    try:
        return riz_module_path
    except ValueError:
        return None


print("RizomUV 2022.2 Livelink Python Module is located in:\n", ruvl_module_path(get_ruvpath()))
#################


# For current Plugin i should use the function RizomUVWinRegisterInstallPath()
# in order to retrieve the installation path of RizomUV >= 2022.2

# No need of going up in the path  structure. removed "/../"
# # tar_path = ((ruvl_module_path(get_ruvpath())) + "/../")
# tar_path = (ruvl_module_path(get_ruvpath()))
# print(os.path.abspath(tar_path))

sys.path.append(ruvl_module_path(get_ruvpath()))

# import all RizomUVLink module items.
# the correct .pyc binary library for the current Python version should magically be loaded.
from RizomUVLink import *
#####################################################
############# IMPORT RIZOMUVLINK MODULE##############
#################### DONE ###########################


###############################################
###############################################
def RUVL_Mod_LaunchLink(export_path):
    """
    import ruvl module, start rizomuv, load a mesh, unfold it, pack it, then save it
    """
    # import sys
    import tempfile
    from os.path import dirname
    # # Load module via hardcoded path
    # sys.path.append("C:\Program Files\Rizom Lab\RizomUV 2022.2\RizomUVLink")
    # from RizomUVLink import *



    # create a rizomuvlink object instance
    link = CRizomUVLink()
    print("RizomUVLink " + link.Version() + " instance has been created")

    # Run rizomuv standalone and connect the link to it.
    # The returned port is a free TCP port used to communicate with the two entities.
    # Installed RizomUV Standalone must be version >= 2022.2
    port = link.RunRizomUV()
    print("RizomUV " + link.RizomUVVersion() + " is now listening command on TCP port: " + str(port))

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    #
    # "link" is now associated to the current RizomUV standalone instance and
    # ready to send commands to it
    #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    #
    # The link object instance is meant to be persistant along with the
    # standalone instance. This permits to load new meshes and send new commands
    # without the need to run RizomUV again and wait for its initialisation.
    # So if you can, keep the link instance somewhere and use it as long as
    # possible along with the RizomUV standalone instance.
    #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    #
    # In very special cases, several RizomUV instance can be ran simultaneously.
    # To do that simply create a new link instance and run a new RizomUV instance.
    # The following link1 and link2 object can perfectly live simultaneously and
    # independently
    #
    # link1 = CRizomUVLink()
    # link2 = CRizomUVLink()
    #
    # link1.RunRizomUV()
    # link2.RunRizomUV()
    #
    # link1.Load(...)
    # link2.Load(...)
    # link1.Unfold()
    # link2.Unfold()
    #
    #       .
    #       .
    #       .
    #
    #  link1.Quit()
    #
    #  link2.Pack()
    #  link2.Quit()
    #
    # WARNING: While the previous lines are perfectly legal, each RizomUV instance
    # take 1 token on floating license configuration. This is not a problem
    # in case of nodelocked licenses however, but in case of floating license
    # you could running out of license token.
    #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    def RUVL_Mod_Task_SmartPack(mapres, packiter, OptiDistort, Opti_iter, Dist_Range):
        """
        SmartPack the current Model using a texture map resolution and optimization on given range of distorted UVIsland.

        :param mapres:          SmartPack the current Model using a target preset texture map resolution / level like the one for LOD.
                                Map size in pixel: 4096 / 2048 / 1024 / 512 / 256 / 128
        :param packiter:        Iteration count for the Pack
        :param OptiDistort:     FixDistortion by applying a UV Optimize on a range of UV Island that are outside of a specified Distortion Range
        :param Opti_iter:       Distortion Optimize iteration count
        :param Dist_Range:      Distortion Range span around ideal 1.0 value to select Distorted UV Islands
        :return:
        """

        floor_packiter = int(packiter)
        if 0 <= packiter <= 1:
            floor_packiter = 1
        if 1 < packiter <= 2:
            floor_packiter = 2
        if 2 < packiter <= 4:
            floor_packiter = 4
        if 4 < packiter <= 8:
            floor_packiter = 8
        if 8 < packiter <= 16:
            floor_packiter = 16
        if 16 < packiter <= 32:
            floor_packiter = 32
        if 32 < packiter <= 64:
            floor_packiter = 64
        print("Packing iteration set to %s" % floor_packiter)
        link.IslandGroups({'Mode': "SetGroupsProperties", 'WorkingSet': "Visible", 'GroupPaths': ["RootGroup"], 'Properties': {'Pack': {'MaxMutations': floor_packiter}}})

        dist_range_min = 1.0 - (Dist_Range / 2)
        dist_range_min = float(format(dist_range_min, ".4f"))
        dist_range_max = 1.0 + (Dist_Range / 2)
        dist_range_max = float(format(dist_range_max, ".4f"))

        # Disable RemoteControl File system
        link.Set({'Path': "Prefs.RemoteControlFileMonitoringOn", 'Value': False})

        link.IslandGroups({'Mode': "SetGroupsProperties", 'WorkingSet': "Visible", 'GroupPath': "RootGroup",
                           'Properties': {'Pack': {'MapResolution': mapres}}})

        # link.Set({'Path': "Lib.Scene.Settings.TexelDensityDisplayUnit", 'Value': "tx/m", 'UndoAble': True})
        # link.Set({'Path': "Lib.Scene.Settings.TexelDensityDisplayUnit", 'Value': "tx/cm", 'UndoAble': True})
        # link.Set({'Path': "Lib.Scene.Settings.Unit", 'Value': "m", 'UndoAble': True})
        # link.Set({'Path': "Lib.Scene.Settings.Unit", 'Value': "cm", 'UndoAble': True})

        # if SaveToInputFile:
        #     # Get the FBX FilePath
        #     filepath = link.Get("LIB.File.Path." + item)
        #     print(filepath)
        #
        #     # filepath = link.Save({'File':{'Path': ?})
        #     # print(filepath)

        # Get current selection Mode: 0=Vertex 1=Edge 2=Polygon 3=Island
        selmode = str(link.Get("Vars.EditMode.ElementMode"))
        # print(selmode)

        # switch to Island Selection Mode
        link.Set({'Path': "Vars.EditMode.ElementMode", 'Value': 3})
        link.Select(
            {'PrimType': "Island", 'WorkingSet': "Visible", 'IslandGroupMode': "Group", 'Select': True, 'All': True})

        # List current Islands IDs
        IslandID_s_List = link.ItemNames("Lib.Mesh.Islands")
        print("All Island IDs:")
        print(IslandID_s_List)
        # print(IslandID_s_List[7])

        IslandID_i_List = []
        for item in IslandID_s_List:
            IslandID_i_List.append(int(item))

        # # query ID for each selected Islands
        # # it prints a lot of data on each link.Get
        # SelIsland = []
        # for item in IslandID_s_List:
        # isSelected = link.Get("Lib.Mesh.Islands." + item + ".Properties.Selected")
        # # print(isSelected)
        # if isSelected:
        # # print("Islands ID " + item + " is selected")
        # SelIsland.append(int(item))
        # print(SelIsland)

        # if len(SelIsland) >= 1:
        # for m in SelIsland:
        # # Set Initial Orientation to Off and Optimization to 90 degree
        # link.IslandProperties({'IslandIDs':[m], 'Properties':{'Pack':{'Rotate':{'Mode':0}}}})
        # link.IslandProperties({'IslandIDs':[m], 'Properties':{'Pack':{'Rotate':{'Step':90}}}})

        link.IslandProperties({'IslandIDs': IslandID_i_List, 'Properties': {'Pack': {'Rotate': {'Mode': 0}}}})
        link.IslandProperties({'IslandIDs': IslandID_i_List, 'Properties': {'Pack': {'Rotate': {'Step': 90}}}})

        # Disable Labels  from Initial Orienatation and Optimization
        link.Set({'Path': "Vars.UI.Display.PackingProperties.RotateStep", 'Value': False})
        link.Set({'Path': "Vars.UI.Display.PackingProperties.RotateMode", 'Value': False})

        link.Select(
            {'PrimType': "Island", 'WorkingSet': "Visible", 'IslandGroupMode': "Group", 'DeSelect': True, 'All': True})

        link.Select(
            {'PrimType': "Island", 'WorkingSet': "Visible", 'IslandGroupMode': "Group", 'Select': True, 'All': True})
        link.Deform({'WorkingSet': "Visible&UnLocked", 'PrimType': "Island", 'CenterMode': "MultiBBox",
                     'ResetIslandScale': True, 'Transform': [0.00779263, 0, 0, 0, 0.00779263, 0, 0, 0, 1],
                     'IDs': IslandID_i_List})

        # Pack Islands
        link.IslandGroups({'Mode': "SetGroupsProperties", 'WorkingSet': "Visible", 'GroupPaths': ["RootGroup"],
                           'Properties': {'Pack': {'MaxMutations': 1}}})
        link.Pack({'RootGroup': "RootGroup", 'WorkingSet': "Visible&Selected", 'ProcessTileSelection': False,
                   'RecursionDepth': 1, 'Translate': True, 'AuxGroup': "RootGroup", 'LayoutScalingMode': 0})

        ####################
        ind_distort = 0
        if OptiDistort:
            # Optimize all Islands that are too much Distorted
            # link.Set({'Path': "Vars.EditMode.ElementMode", 'Value': 3})
            link.Set({'Path': "Prefs.Optimize.AngleDistanceMix", 'Value': 1})
            link.Select({'PrimType': "Island", 'WorkingSet': "Visible", 'IslandGroupMode': "Group", 'Select': True,
                         'ResetBefore': True, 'Range': {'Min': 0.0, 'Max': dist_range_min, 'Mode': "Distortion"}})

            # Distort a certain amount of time (number of Optimize Iteration)
            ind_distort = 0
            while ind_distort <= Opti_iter:
                link.Optimize(
                    {'PrimType': "Island", 'WorkingSet': "Visible&Selected&UnLocked", 'Mix': 1, 'AngleDistanceMix': 1,
                     'RoomSpace': 0, 'MinAngle': 1e-05, 'PinMapName': "Pin"})
                ind_distort += 1

            link.Deform({'WorkingSet': "Visible&Selected&UnLocked", 'PrimType': "Island", 'Rotation': 0,
                         'Geometrical': "AlignIslandToSelection"})
            link.Select({'PrimType': "Island", 'WorkingSet': "Visible", 'IslandGroupMode': "Group", 'DeSelect': True,
                         'All': True})

            link.Select({'PrimType': "Island", 'WorkingSet': "Visible", 'IslandGroupMode': "Group", 'Select': True,
                         'ResetBefore': True, 'Range': {'Min': dist_range_max, 'Max': 2.0, 'Mode': "Distortion"}})

            # Distort a certain amount of time (number of Optimize Iteration)
            ind_distort = 0
            while ind_distort <= Opti_iter:
                link.Optimize(
                    {'PrimType': "Island", 'WorkingSet': "Visible&Selected&UnLocked", 'Mix': 1, 'AngleDistanceMix': 1,
                     'RoomSpace': 0, 'MinAngle': 1e-05, 'PinMapName': "Pin"})
                ind_distort += 1

            link.Deform({'WorkingSet': "Visible&Selected&UnLocked", 'PrimType': "Island", 'Rotation': 0,
                         'Geometrical': "AlignIslandToSelection"})
            link.Select({'PrimType': "Island", 'WorkingSet': "Visible", 'IslandGroupMode': "Group", 'DeSelect': True,
                         'All': True})

        ####################
        # SmartPack Islands for correcting all Undistorted Islands
        # Set the Packing IterationCount
        link.IslandGroups({'Mode': "SetGroupsProperties", 'WorkingSet': "Visible", 'GroupPaths': ["RootGroup"],
                           'Properties': {'Pack': {'MaxMutations': floor_packiter}}})
        link.Select(
            {'PrimType': "Island", 'WorkingSet': "Visible", 'IslandGroupMode': "Group", 'Select': True, 'All': True})
        link.Pack({'RootGroup': "RootGroup", 'WorkingSet': "Visible&Selected", 'ProcessTileSelection': False,
                   'RecursionDepth': 1, 'Translate': True, 'AuxGroup': "RootGroup", 'LayoutScalingMode': 0})

        # Deselect all Islands
        link.Select(
            {'PrimType': "Island", 'WorkingSet': "Visible", 'IslandGroupMode': "Group", 'DeSelect': True, 'All': True})

        # if SaveToInputFile:
        #     # Save the data back to input file
        #     App.Save({'File':{'FBX':{'Compatibilty':"FBX201300"}, 'Path':filepath, 'UVWProps':True}})
        #
        # if AppQuit:
        #     # Close RizomUV standalone instance
        #     App.Quit({})

    try:
        # mesh path inpt & output from the example directory
        meshInputPath = export_path
        meshOutputPath = export_path

        params = {
            "File.Path": meshInputPath,
            "File.XYZUVW": True,  # 3D + UV data loaded (use File.XYZ instead to load 3D data only)
            "File.UVWProps": True,
            # UVs properties such as pinning, texel density settings etc... will be loaded
            "File.ImportGroups": True,  # Island group hierarchy will be loaded
            "__Focus": True,  # Focus viewports on the loaded mesh
        }
        link.Load(params)

        # Pack full mesh with specific parameters
        RUVL_Mod_Task_SmartPack(RUVL_UserVal_PackMapRes, RUVL_UserVal_PackIteration, RUVL_UserVal_PackOpti, RUVL_UserVal_PackOptiIter, RUVL_UserVal_PackOptiDistRange)



        # Save the mesh with default parameters
        link.Save({"File.Path": meshOutputPath})

        # Close RizomUV standalone instance associated to link
        link.Quit({})

        # link.Load(...) # obviously won't work here as the rizomUV instance
        # is closed so a new call to link.RunRizomUV() would be necessary
        
    except CZEx as ex:
        print(str(ex))
        
    print("Done")
###############################################################################################


class SMO_LL_RIZOMUV_Task_SmartPack_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)

        self.modo_ver = int(lx.eval("query platformservice appversion ?"))
        self.scrp_svc = lx.service.ScriptSys()
        self.sel_svc = lx.service.Selection()

    def cmd_Interact(self):
        pass

    def cmd_UserName(self):
        return "SMO LL RIZOMUV 2022.2 - Task - SmartPack"

    def cmd_Desc(self):
        return "SmartPack the current Model using a texture map resolution and optimization on given range of distorted UVIsland and get the updated data back in Modo."

    def cmd_Tooltip(self):
        return "SmartPack the current Model using a texture map resolution and optimization on given range of distorted UVIsland and get the updated data back in Modo."

    def cmd_Help(self):
        return "https://twitter.com/sm0luck"

    def basic_ButtonName(self):
        return "SMO LL RIZOMUV 2022.2 - Task - SmartPack"

    def cmd_Flags(self):
        return lx.symbol.fCMD_UNDO

    def basic_Enable(self, msg):
        return True

    # Validate the path to RizomUV is good.
    def validRizomUVPath(self, rizomuv_exe_path):
        return ((rizomuv_exe_path != None) and os.path.lexists(rizomuv_exe_path) and (
                os.path.splitext(rizomuv_exe_path)[1].lower() == ".exe"))

    def getUVSelection(self):
        uv_selection = []
        vmap_pkt_trans = lx.object.VMapPacketTranslation(self.sel_svc.Allocate(lx.symbol.sSELTYP_VERTEXMAP))
        sel_type_vmap = self.sel_svc.LookupType(lx.symbol.sSELTYP_VERTEXMAP)

        for i in range(self.sel_svc.Count(sel_type_vmap)):
            pkt = self.sel_svc.ByIndex(sel_type_vmap, i)
            if vmap_pkt_trans.Type(pkt) == lx.symbol.i_VMAP_TEXTUREUV:
                uv_selection.append(vmap_pkt_trans.Name(pkt))
        return uv_selection

    # Set the path to RizomUV in a user variable.
    def setRizomUVPath(self, rizomuv_exe_path):
        if self.validRizomUVPath(rizomuv_exe_path):
            # try:
            # lx.eval ("!!user.defNew name:Smo_RizomUVPath type:string life:config")
            # except:
            # pass

            try:
                lx.eval("!!user.value Smo_RizomUVPath {%s}" % rizomuv_exe_path)
            except:
                pass

            return lx.eval1("user.value Smo_RizomUVPath ?") == rizomuv_exe_path
        return False

    # Ask the user for the path to RizomUV.
    def findRizomUVPath(self):
        # default_path = r"C:\Program Files\Rizom Lab\RizomUV 2018\rizomuv.exe"
        # default_path = r"C:\Program Files\Rizom Lab\RizomUV 2019\rizomuv.exe"
        # default_path = r"C:\Program Files\Rizom Lab\RizomUV 2020\rizomuv.exe"
        # default_path = r"C:\Program Files\Rizom Lab\RizomUV 2021\rizomuv.exe"
        default_path = r"C:\Program Files\Rizom Lab\RizomUV 2022\rizomuv.exe"
        if self.setRizomUVPath(default_path):
            return True
        else:
            try:
                lx.eval("dialog.setup fileOpen")
                lx.eval("dialog.title {Select RizomUV 2018.X to 2022.X executable file}")
                lx.eval("dialog.fileTypeCustom format:exe username:{EXE} loadPattern:{*.exe} saveExtension:exe")
                if self.modo_ver == 801:
                    lx.eval("+dialog.open")
                else:
                    lx.eval("dialog.open")
                rizomuv_exe_path = lx.eval1("dialog.result ?")
            except:
                pass
            else:
                if self.setRizomUVPath(rizomuv_exe_path):
                    return True

        lx.out("Failed to define path to RizomUV.")
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
        FBX_USERVALUE_PREFIX = "sceneio.fbx.save."
        FBX_USERVALUE_COMMAND = "user.value " + FBX_USERVALUE_PREFIX
        fbxSettings = {}
        uValCount = self.scrp_svc.UserValueCount()
        for x in range(uValCount):
            try:
                uval = self.scrp_svc.UserValueByIndex(x)
            except IndexError:
                print("Invalid User Value Index: %s (%s total user values)" % (x, uValCount))
            else:
                name = uval.Name()
                if name.startswith("sceneio.fbx.save."):
                    fbxSettings[name] = self.getUserValue(name)
        return fbxSettings


    def restoreFBXSettings(self, fbxSettings):
        for name, value in fbxSettings.items():
            lx.eval("user.value %s %s" % (name, value))


    def basic_Execute(self, msg, flags):

        fbxSettings = self.storeFBXSettings()
        print(fbxSettings)

        # MODO version checks. Different versions have different FBX options.
        if self.modo_ver < 901:
            lx.out("Requires Modo 901 or newer.")
            return

        # Automatically Select UV Maps on the meshs selected
        # lx.eval("smo.GC.ClearSelectionVmap 1 0")

        # Get the selected UV names.
        selected_uv_names = self.getUVSelection()
        if len(selected_uv_names) == 0:
            lx.out("No UV maps selected.")
            return

        # Grab the active layer.
        layer_svc = lx.service.Layer()
        layer_scan = lx.object.LayerScan(layer_svc.ScanAllocate(lx.symbol.f_LAYERSCAN_ACTIVE))
        if not layer_scan.test():
            lx.out("Layerscan failed.")
            return

        # Early out if there are no active layers.
        layer_count = layer_scan.Count()
        if layer_count <= 0:
            lx.out("No active layers.")
            return

        # Grab the relevant meshes and UV maps.
        mesh_items = []
        mesh_uvs = []
        for layer_idx in range(layer_count):
            mesh_item = lx.object.Item(layer_scan.MeshItem(layer_idx))
            if not mesh_item.test():
                lx.out("Failed to get mesh item of layer %s." % layer_idx)
                continue

            mesh_name = mesh_item.UniqueName()

            mesh = lx.object.Mesh(layer_scan.MeshBase(layer_idx))
            if not mesh.test():
                lx.out("Failed to get mesh of %s." % mesh_name)
                continue

            # Get the selected UV maps that exist on this model.
            meshmap = lx.object.MeshMap(mesh.MeshMapAccessor())
            if not meshmap.test():
                lx.out("Failed to get meshmap accessor of %s." % mesh_name)
                continue

            selected_uv_names_mesh = []
            for uv_map in selected_uv_names:
                try:
                    meshmap.SelectByName(lx.symbol.i_VMAP_TEXTUREUV, uv_map)
                except:
                    pass
                else:
                    selected_uv_names_mesh.append(uv_map)

            if len(selected_uv_names_mesh) == 0:
                lx.out("%s does not have any of the selected UV maps on it." % mesh_name)
                continue

            mesh_items.append(mesh_item)
            mesh_uvs.append(selected_uv_names_mesh)

        layer_scan.Apply()

        # Select the meshes.
        for x, mesh_item in enumerate(mesh_items):
            if x == 0:
                lx.eval("select.subItem %s set mesh 0 0" % mesh_item.Ident())
            else:
                lx.eval("select.subItem %s add mesh 0 0" % mesh_item.Ident())

        # Get RizomUV executable path.
        Smo_RizomUVPath = None
        try:
            Smo_RizomUVPath = lx.eval1("!!user.value Smo_RizomUVPath ?")
        except:
            if not self.findRizomUVPath():
                return
        else:
            if not self.validRizomUVPath(Smo_RizomUVPath):
                if not self.findRizomUVPath():
                    return
                else:
                    Smo_RizomUVPath = lx.eval1("!!user.value Smo_RizomUVPath ?")

        if Smo_RizomUVPath is None:
            lx.out("Invalid RizomUV path.")
            return
        # Store user's FBX preferences for restoring later.
        fbxSettings = self.storeFBXSettings()

        # Apply FBX settings we want to use for RizomUV.
        # Essentially disabling everything except geometry and setting export to selection.
        # Also picking FBX2013, just because that should ensure things export smoothly.
        lx.eval("user.value sceneio.fbx.save.format 2")
        lx.eval("user.value sceneio.fbx.save.exportType 1")
        lx.eval("user.value sceneio.fbx.save.geometry 1")
        lx.eval("user.value sceneio.fbx.save.exportToASCII 0")
        lx.eval("user.value sceneio.fbx.save.animationOnly 0")
        lx.eval("user.value sceneio.fbx.save.cameras 0")
        lx.eval("user.value sceneio.fbx.save.lights 0")
        lx.eval("user.value sceneio.fbx.save.materials 1")  # Save Materials as RizomUV can now pack by Materials
        lx.eval("user.value sceneio.fbx.save.polygonParts 1")
        lx.eval("user.value sceneio.fbx.save.selectionSets 1")
        lx.eval("user.value sceneio.fbx.save.smoothingGroups 1")
        lx.eval("user.value sceneio.fbx.save.morphMaps 0")
        lx.eval("user.value sceneio.fbx.save.animation 0")
        lx.eval("user.value sceneio.fbx.save.sampleAnimation 0")

        if self.modo_ver > 900:
            try:
                lx.eval1("user.value sceneio.fbx.save.tangentsBitangents 0")
            except RuntimeError:
                pass
            
        if 1000 < self.modo_ver <= 1011:
            try:
                lx.eval("user.value sceneio.fbx.save.triangulate 0")
                lx.eval("user.value sceneio.fbx.save.meshSmoothing 1")
            except RuntimeError:
                pass
            
        if 1012 <= self.modo_ver <= 1099:
            try:
                lx.eval("user.value sceneio.fbx.save.surfaceRefining FBXExportSubDiv")
            except RuntimeError:
                pass
            
        if 1100 <= self.modo_ver <= 1499:
            try:
                lx.eval("user.value sceneio.fbx.save.surfaceRefining FBXExportSubDiv")
                lx.eval("user.value sceneio.fbx.save.format 4")
            except RuntimeError:
                pass
            
        if 1500 <= self.modo_ver <= 1699:
            try:
                lx.eval("user.value sceneio.fbx.save.surfaceRefining FBXExportSubDiv")
                lx.eval("user.value sceneio.fbx.save.format FBX2013")
            except RuntimeError:
                pass
            
        if 1510 <= self.modo_ver <= 1699:
            try:
                lx.eval("user.value sceneio.fbx.save.embedMedia false")
            except RuntimeError:
                pass

        # get modo's temp dir
        temp_dir = lx.eval("query platformservice path.path ? temp")
        # name our temp file
        fbx_file_name = "RizomUV_DATA.fbx"
        # builds the complete path out of the temp dir and the temp file name
        fbx_export_path = os.path.join(temp_dir, "SMO_RizomUVLiveLink", fbx_file_name)

        # make sure the SMO_RizomUVLiveLink directory exists, if not create it
        if not os.path.exists(os.path.dirname(fbx_export_path)):
            # try to create the directory.
            try:
                os.makedirs(os.path.dirname(fbx_export_path))
            except:
                # if that fails for any reason print out the error
                print(traceback.format_exc())
        else:
            if fbx_export_path == None:
                lx.out('Didn\'t save FBX for RizomUV.')
                return
            else:
                fbx_export_path = os.path.splitext(fbx_export_path)[0] + '.fbx'
                fbx_file_name = os.path.splitext(os.path.basename(fbx_export_path))[0]

        lx.eval('!scene.saveAs filename:"{}" format:"fbx" export:true'.format(fbx_export_path))
        fbx_save_time = os.path.getmtime(fbx_export_path)

        # Restore the FBX preferences.
        self.restoreFBXSettings(fbxSettings)

        ###############################################################################################
        print("Smart Packing Options:")
        print("Map Resolution in pixel:", RUVL_UserVal_PackMapRes)
        print("Packing Iteration Count:", RUVL_UserVal_PackIteration)
        print("Optimize Distorted UVisland:", RUVL_UserVal_PackOpti)
        print("-------------------------")
        RUVL_Mod_LaunchLink(fbx_export_path)
        ###############################################################################################

        # Call RizomUV.
        # proc = subprocess.Popen([Smo_RizomUVPath, fbx_export_path], stdout=subprocess.PIPE)
        # stdout, stderr = proc.communicate()
        # rc = proc.returncode
        # print("Return Code", rc)
        # if rc != 0:
        #     # RizomUV crashed or threw an error.
        #     lx.out('RizomUV crashed.')
        #     lx.out('Standard Output: %s' % stdout)
        #     lx.out('Error Output: %s' % stderr)
        # else:
        # Get the modified time of the export file.
        fbx_load_time = 0
        if os.path.lexists(fbx_export_path):
            fbx_load_time = os.path.getmtime(fbx_export_path)

        # User has likely saved over the old file.
        if fbx_load_time > fbx_save_time:
            if self.modo_ver > 1000:
                lx.eval(
                    '!!loaderOptions.fbx mergeWithExistingItems:false loadGeometry:true loadNormals:true loadMeshSmoothing:false loadBlendShapes:false loadPolygonParts:false loadSelectionSets:false loadMaterials:false invertMatTranAmt:false useMatTranColAsTranAmt:false changeTextureEffect:false loadCameras:false loadLights:false loadAnimation:false loadSampleAnimation:false loadSampleAnimationRate:0 globalScalingFactor:1.0 importUnits:0')
            else:
                lx.eval(
                    '!!loaderOptions.fbx mergeWithExistingItems:false loadGeometry:true loadNormals:true loadMeshSmoothing:false loadBlendShapes:false loadPolygonParts:false loadSelectionSets:false loadMaterials:false invertMatTranAmt:false useMatTranColAsTranAmt:false loadCameras:false loadLights:false loadAnimation:false loadSampleAnimation:false loadSampleAnimationRate:0')
            lx.eval('!!scene.open "%s" import' % fbx_export_path)
        else:
            try:
                lx.eval('dialog.setup fileOpen')
                lx.eval('dialog.title "Load FBX file from RizomUV"')
                lx.eval('dialog.fileType scene2')
                if self.modo_ver == 801:
                    lx.eval('+dialog.open')
                else:
                    lx.eval('dialog.open')
                fbx_import_path = lx.eval1('dialog.result ?')
            except:
                lx.out('Failed to load scene with new UVs.')
                return
            else:
                if fbx_import_path == None:
                    return
                else:
                    fbx_file_name = os.path.splitext(os.path.basename(fbx_import_path))[0]
                    if self.modo_ver > 1000:
                        lx.eval(
                            '!!loaderOptions.fbx mergeWithExistingItems:false loadGeometry:true loadNormals:true loadMeshSmoothing:false loadBlendShapes:false loadPolygonParts:false loadSelectionSets:false loadMaterials:false invertMatTranAmt:false useMatTranColAsTranAmt:false changeTextureEffect:false loadCameras:false loadLights:false loadAnimation:false loadSampleAnimation:false loadSampleAnimationRate:0 globalScalingFactor:1.0 importUnits:0')
                    else:
                        lx.eval(
                            '!!loaderOptions.fbx mergeWithExistingItems:false loadGeometry:true loadNormals:true loadMeshSmoothing:false loadBlendShapes:false loadPolygonParts:false loadSelectionSets:false loadMaterials:false invertMatTranAmt:false useMatTranColAsTranAmt:false loadCameras:false loadLights:false loadAnimation:false loadSampleAnimation:false loadSampleAnimationRate:0')
                    lx.eval('!scene.open "%s" import' % fbx_import_path)

        scene = lxu.select.SceneSelection().current()
        scn_svc = lx.service.Scene()
        group_type = scn_svc.ItemTypeLookup(lx.symbol.sITYPE_GROUPLOCATOR)

        fbx_group_index = -2
        fbx_group = None
        group_ident = None
        item_ident = None

        # Find the newly imported FBX scene.
        group_count = scene.ItemCount(group_type)
        for i in reversed(range(group_count)):
            group = scene.ItemByIndex(group_type, i)
            if group.Name() == fbx_file_name:
                group_index = group.UniqueIndex()
                if group_index > fbx_group_index:
                    fbx_group_index = group_index
                    fbx_group = group

        if fbx_group is not None:

            # Find the newly imported FBX versions of our original meshes.
            fbx_meshes = [None] * len(mesh_items)
            self.recurseToFindFBXMeshes(fbx_group, fbx_meshes, mesh_items)

            # Copy over the UVs.
            for fbx_mesh, mesh_item, mesh_uv in zip(fbx_meshes, mesh_items, mesh_uvs):
                if fbx_mesh is not None:
                    fbx_ident = fbx_mesh.Ident()
                    mesh_ident = mesh_item.Ident()
                    for uv_map in mesh_uv:
                        lx.eval('select.subItem %s set mesh 0 0' % fbx_ident)

                        try:
                            lx.eval('select.vertexMap %s txuv replace' % uv_map)
                        except:
                            continue
                        else:
                            try:
                                lx.eval('select.type polygon')
                                lx.eval('select.all')
                                lx.eval('uv.copy')

                                lx.eval('select.subItem %s set mesh 0 0' % mesh_ident)
                                lx.eval('select.vertexMap %s txuv replace' % uv_map)
                            except:
                                continue
                            else:
                                try:
                                    lx.eval('select.type polygon')
                                    lx.eval('select.all')

                                    if self.modo_ver > 801:
                                        lx.eval('uv.paste selection')
                                    else:
                                        lx.eval('uv.paste')
                                except:
                                    continue

            # Delete the imported FBX scene.
            if self.modo_ver > 1009:
                lx.eval('!!item.delete child:1 item:%s' % fbx_group.Ident())
            else:
                lx.eval('select.subItem %s set groupLocator 0 0' % fbx_group.Ident())
                lx.eval('!!item.delete mask:groupLocator child:1')

            # Reselect the original mesh and UVs.
            for mesh_item in mesh_items:
                lx.eval('select.subItem %s add mesh 0 0' % mesh_item.Ident())
            for idx, uv_map in enumerate(selected_uv_names_mesh):
                if idx == 0:
                    lx.eval('select.vertexMap %s txuv replace' % uv_map)
                else:
                    lx.eval('select.vertexMap %s txuv add' % uv_map)
            lx.eval('select.drop polygon')

            del mesh_items
            del mesh_uvs


lx.bless(SMO_LL_RIZOMUV_Task_SmartPack_Cmd, Cmd_Name)


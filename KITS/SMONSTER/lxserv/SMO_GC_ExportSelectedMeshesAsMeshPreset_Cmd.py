# python
# ---------------------------------------
# Name:         SMO_GC_ExportSelectedMeshesAsMeshPreset_Cmd.py
# Version:      1.0
#
# Purpose:      This script is designed to:
#               Export Selected Meshes As MeshPreset LXL file into Target Path.
#               (optional: Define Path destination as argument)
#
#
# Author:       Franck ELISABETH
# Website:      http://www.smoluck.com
#
# Created:      12/05/2022
# Copyright:    (c) Franck Elisabeth 2017-2022
# ---------------------------------------

import lx, lxu, modo

Command_Name = "smo.GC.ExportSelectedMeshesAsMeshPreset"
# smo.GC.ExportSelectedMeshesAsMeshPreset {C:\TEMP\Target}

class SMO_GC_ExportSelectedMeshesAsMeshPreset_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
        self.dyna_Add("Directory Path", lx.symbol.sTYPE_STRING)
        self.basic_SetFlags(0, lx.symbol.fCMDARG_OPTIONAL)  # here the (0) define the argument index.

    def cmd_Flags(self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO

    def cmd_Interact(self):
        pass

    def cmd_UserName(self):
        return 'SMO GC Export Selected Meshes as MeshPreset LXL files'

    def cmd_Desc(self):
        return 'Export Selected Meshes As MeshPreset LXL file into Target Path. (optional: Define Path destination as argument)'

    def cmd_Tooltip(self):
        return 'Export Selected Meshes As MeshPreset LXL file into Target Path. (optional: Define Path destination as argument)'

    def cmd_Help(self):
        return 'https://twitter.com/sm0luck'

    def basic_ButtonName(self):
        return 'SMO GC Export Selected Meshes as MeshPreset LXL files'

    def basic_Enable(self, msg):
        return True

    def basic_Execute(self, msg, flags):
        # In case a Path is defined directly with the path argument we overwrite the path
        TargetDirPath = ""

        if self.dyna_IsSet(0):
            TargetDirPath = self.dyna_String(0)
            # print('Destination Path is set by Argument')

        scene = modo.scene.current()
        meshes_list = scene.selectedByType(lx.symbol.sITYPE_MESH)
        # print(meshes_list)

        if self.dyna_IsSet(0):
            for mesh in meshes_list:
                mesh.select(True)
                lx.eval('smo.GC.ExportMeshAsMeshPreset {%s}' % TargetDirPath)

        if not self.dyna_IsSet(0):
            for mesh in meshes_list:
                mesh.select(True)
                lx.eval('smo.GC.ExportMeshAsMeshPreset')

        lx.eval('smo.GC.DeselectAll')

lx.bless(SMO_GC_ExportSelectedMeshesAsMeshPreset_Cmd, Command_Name)

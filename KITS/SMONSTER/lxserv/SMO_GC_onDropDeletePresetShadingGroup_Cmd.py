# python
"""
# Name:         SMO_GC_onDropDeletePresetShadingGroup_Cmd.py
# Version:      1.0
#
# Purpose:      This script is designed to:
#               Automatically Remove the Shading Group "meshPresetName.lxl" created by Modo when we drop a meshpreset in the scene.
#               It also setup the Transform tool ON, with Background MeshConstraint, and Action Center to Local mode, for easy adjustment.
#               (Attach SMO_GC_onDrop_RotateTool.py script to the selected MeshPreset file via PB_View and smo.GC.AttachScriptToPreset command.)
#
# Author:       Franck ELISABETH
# Website:      https://www.smoluck.com
#
# Created:      01/10/2020
# Copyright:    (c) Franck Elisabeth 2017-2022
"""

import lx
import lxu.select
import modo

Cmd_Name = "smo.GC.OnDropDeletePresetShadingGroup"


class SMO_GC_onDropDeletePresetShadingGroup_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)

    def cmd_Flags(self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO

    def cmd_Interact(self):
        pass

    def cmd_UserName(self):
        return 'SMO GC - OnDrop Delete Preset Shading Group'

    def cmd_Desc(self):
        return 'Automatically Remove the Shading Group "meshPresetName.lxl" created by Modo when we drop a meshpreset in the scene. It also setup the Transform tool ON, with Background MeshConstraint, and Action Center to Local mode, for easy adjustment. (Attach SMO_GC_onDrop_RotateTool.py script to the selected MeshPreset file via PB_View and smo.GC.AttachScriptToPreset command.)'

    def cmd_Tooltip(self):
        return 'Automatically Remove the Shading Group "meshPresetName.lxl" created by Modo when we drop a meshpreset in the scene. It also setup the Transform tool ON, with Background MeshConstraint, and Action Center to Local mode, for easy adjustment. (Attach SMO_GC_onDrop_RotateTool.py script to the selected MeshPreset file via PB_View and smo.GC.AttachScriptToPreset command.)'

    def cmd_Help(self):
        return 'https://twitter.com/sm0luck'

    def basic_ButtonName(self):
        return 'SMO GC - OnDrop Delete Preset Shading Group'

    def basic_Enable(self, msg):
        return True

    def basic_Execute(self, msg, flags):
        scene = modo.scene.current()
        scnSrv = lx.service.Scene()
        scn = lxu.select.SceneSelection().current()

         # Lookup our Internal ID of the mask type
        maskType = scnSrv.ItemTypeLookup('mask')
        meshType = scnSrv.ItemTypeLookup('mesh')

        # get a List of How many masks are in the scene.
        # in theory the last one (dropped) should belong to our newly added preset
        maskCount = scn.ItemCount(maskType)
        presetMask = scn.ItemByIndex(maskType, maskCount - 1)

        # get a List of How many meshes are in the scene.
        # in theory the last one (dropped) should belong to our newly added preset
        meshCount = scn.ItemCount(meshType)
        presetMesh = scn.ItemByIndex(meshType, meshCount - 1)

        # drop all the items.
        lx.eval('select.drop item')

        # select the Shading Group "meshPresetName.lxl" that is automatically created on drop and Delete it.
        lx.eval('select.item {%s} set' % presetMask.Ident())
        lx.eval('!delete')

        # select back the dropped MeshItem and rename it to get rid of the "".lxl" tag.
        lx.eval('select.type item')
        lx.eval('select.drop item')
        lx.eval('select.item {%s} set' % presetMesh.Ident())

        # store the Unique name of the current mesh layer (Mesh item (Preset) that we just dropped on scene)
        MeshUName = lx.eval('query layerservice layer.id ? fg')
        # lx.out('Item Unique Name:', MeshUName)
        # scene.select(MeshUName)

        Mesh_Name = lx.eval('item.name ? xfrmcore')
        # lx.out('current item name is ', Mesh_Name)
        lxlNameTag = Mesh_Name.split(".lxl")
        # lx.out('current item name is ', lxlNameTag)
        lx.eval('item.name %s xfrmcore' % lxlNameTag[0])

        lx.eval('tool.set const.bg on')
        lx.eval('tool.set "Transform" "on"')
        lx.eval('tool.set actr.local on')


lx.bless(SMO_GC_onDropDeletePresetShadingGroup_Cmd, Cmd_Name)

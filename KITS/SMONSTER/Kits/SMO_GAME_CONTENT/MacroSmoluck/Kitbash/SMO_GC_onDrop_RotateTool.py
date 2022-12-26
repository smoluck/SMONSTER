# python
"""
# Name:         SMO_GC_onDrop_RotateTool_Cmd.py
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
import lxu
import modo

scene = modo.scene.current()
scnSrv = lx.service.Scene()
scn = lxu.select.SceneSelection().current()
evt = lx.args()[0]

###===
###=== Executed before the preset is added to the scene, allows us to
###=== abort the preset application if we need to.
###===
# if evt == 'beforeCreate':
#    pass

###===
###=== Executed after the preset is added to the scene
###===
# elif evt == 'onDo':
#    pass

# 'onCreate' and 'onDrop' events are special cases.
# 'onCreate' is called if the assembly preset has an 'onCreate' script defined as part of the assembly.
# elif evt == 'onCreate':
#    pass

# 'onDrop' is called of the preset is darg/dropped into a viewport
# elif evt == 'onDrop':
#    pass

# if evt == "onDo":
#     lx.eval('smo.GC.onDropTransformTool')
    # scene = modo.scene.current()
    # scnSrv = lx.service.Scene()
    # scn = lxu.select.SceneSelection().current()
    # # select back the dropped MeshItem and rename it to get rid of the "".lxl" tag.
    # lx.eval('select.type item')
    # # store the Unique name of the current mesh layer (Mesh item (Preset) that we just dropped on scene)
    # MeshUName = lx.eval('query layerservice layer.id ? fg')
    # lx.out('Item Unique Name:', MeshUName)
    # scene.select(MeshUName)
    #
    # Mesh_Name = lx.eval('item.name ? xfrmcore')
    # lx.out('current item name is ', Mesh_Name)
    # lxlNameTag = Mesh_Name.split(".lxl")
    # lx.out('current item name is ', lxlNameTag)
    # lx.eval('item.name %s xfrmcore' % lxlNameTag[0])


if evt == "onDrop":
    lx.eval('smo.GC.OnDropDeletePresetShadingGroup')
    # lx.eval('tool.set const.bg on')
    # lx.eval('tool.set "Transform" "on"')
    # lx.eval('tool.set actr.local on')




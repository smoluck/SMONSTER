# python
# ---------------------------------------
# Name:         SMO_GC_RenderThumbPreset_Cmd.py
# Version:      1.0
#
# Purpose:      This script is designed to:
#               Replace the current Preset Thumbnail by SMO ThumbnailMaker_Template scene Render.
#
# Author:       Franck ELISABETH
# Website:      http://www.smoluck.com
#
# Created:      03/02/2021
# Copyright:    (c) Franck Elisabeth 2017-2022
# ---------------------------------------

import lx, lxu, modo, time, sys

Command_Name = "smo.GC.RenderThumbPreset"


class SMO_GC_RenderThumbPreset_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)

    def cmd_Flags(self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO

    def cmd_Interact(self):
        pass

    def cmd_UserName(self):
        return 'SMO GC RenderThumbPreset'

    def cmd_Desc(self):
        return 'Replace the current Preset Thumbnail by SMO ThumbnailMaker_Template scene Render.)'

    def cmd_Tooltip(self):
        return 'Replace the current Preset Thumbnail by SMO ThumbnailMaker_Template scene Render.)'

    def cmd_Help(self):
        return 'https://twitter.com/sm0luck'

    def basic_ButtonName(self):
        return 'SMO GC RenderThumbPreset'

    def basic_Enable(self, msg):
        return True

    def basic_Execute(self, msg, flags):
        # scene = modo.scene.current()
        OriginalViewState = lx.eval('view3d.projection ?')
        print(OriginalViewState)
        try:
            SelPrstPBPath = lxu.select.PresetPathSelection().current()[-1][0]
        except:
            lx.eval('dialog.setup info')
            lx.eval('dialog.title SMO KitBash')
            lx.eval('dialog.msg {You need to select a Polystein Preset in the Preset Browser}')
            lx.eval('dialog.open')
            sys.exit()
        # lx.out(SelPrstPBPath)

        kitpath = lx.eval(
            "query platformservice alias ? {kit_SMO_GAME_CONTENT:Scenes/ThumbnailMaker_Template_ColoredBG.lxo}")
        lx.eval('scene.open {%s} normal' % kitpath)

        BGColor = modo.Vector3(0.0, 0.0, 0.0)
        BGColor = lx.eval('user.value SMO_UseVal_ThumbBG_Color ?')
        # print (BGColor)
        lx.eval('select.subItem constant001 set textureLayer;render;environment;light;camera;scene;replicator;bake;mediaClip;txtrLocator')
        lx.eval('item.channel constant$color {%s}' % BGColor)
        lx.eval('smo.GC.DeselectAll')

        lx.eval('select.preset {%s} add' % SelPrstPBPath)
        lx.eval('select.filepath {%s} add' % SelPrstPBPath)
        lx.eval('preset.do')
        MeshPreset_Name = modo.Item().name
        lx.out('MeshPreset name', MeshPreset_Name)
        MeshPreset_ID = modo.Item().id
        lx.out('MeshPreset ID', MeshPreset_ID)

        # Move Center Position to Center of Available Polygons.
        lx.eval('select.type polygon')
        lx.eval('select.all')
        lx.eval('smo.GC.Setup.MoveRotateCenterToSelection 1 0')
        lx.eval('select.drop polygon')
        lx.eval('select.type item')
        lx.eval('!transform.channel pos.X 0.0')
        lx.eval('!transform.channel pos.Y 0.0')
        lx.eval('!transform.channel pos.Z 0.0')

        lx.eval('view3d.projection cam')
        lx.eval('view3d.renderCamera')
        lx.eval('camera.fit true false')
        lx.eval('view3d.projection psp')

        lx.eval('group.create TARGET std selItems')
        SelGroup_Name = modo.Item().name
        lx.out('Target Group name', SelGroup_Name)
        SelGroup_ID = modo.Item().id
        lx.out('Target Group ID', SelGroup_ID)

        lx.eval('select.drop item')
        lx.eval('select.clear item')
        lx.eval('select.drop schmNode')
        lx.eval('select.drop channel')
        lx.eval('select.drop link')

        lx.eval('item.link pmodel.meshmerge.graph {%s} pmodel.meshmerge028 posT:65535 replace:false' % SelGroup_ID)

        lx.eval('select.drop item')
        lx.eval('select.clear item')
        lx.eval('select.drop schmNode')
        lx.eval('select.drop channel')
        lx.eval('select.drop link')

        lx.eval('select.subItem camera002 set')
        # lx.eval('camera.autofocus')

        lx.eval('render')
        time.sleep(0.5)
        lx.eval('preset.thumbReplace image:render')
        lx.eval('!render.clearAll')
        lx.eval('renderWindow.close')

        lx.eval('!scene.close')
        lx.eval('view3d.projection %s' % OriginalViewState)

lx.bless(SMO_GC_RenderThumbPreset_Cmd, Command_Name)
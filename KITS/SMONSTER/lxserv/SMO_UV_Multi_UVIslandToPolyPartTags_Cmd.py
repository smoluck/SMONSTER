# python
"""
Name:         SMO_UV_Multi_UVIslandToPolyPartTags_Cmd.py

Purpose:      This script is designed to
              MULTI - Create polygon part tags that are related to their UVIsland by connectivity.

Author:       Franck ELISABETH
Website:      https://www.linkedin.com/in/smoluck/
Created:      29/06/2025
Copyright:    (c) Franck Elisabeth 2017-2022
"""

import lx
import lxu
import modo

Cmd_Name = "smo.UV.Multi.UVIslandToPolyPartTags"

class SMO_UV_Multi_UVIslandToPolyPartTags_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
        scenedata = modo.scene.current()
        CheckGrpSelItems = lxu.select.ItemSelection().current()
        for item in CheckGrpSelItems:
            itemType = modo.Item(item).type
            item = lx.object.Item(item)
            item_name = item.UniqueName()
            # print(item_name)
            if itemType != "mesh":
                scenedata.deselect(item_name)

    def cmd_Flags(self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO

    def cmd_Interact(self):
        pass

    def cmd_UserName(self):
        return 'SMO UV - (Multi) UVIsland to Polygon Part Tags'

    def cmd_Desc(self):
        return 'MULTI - Create polygon part tags that are related to their UVIsland by connectivity'

    def cmd_Tooltip(self):
        return 'MULTI - Create polygon part tags that are related to their UVIsland by connectivity'

    def cmd_Help(self):
        return 'https://twitter.com/sm0luck'

    def basic_ButtonName(self):
        return 'SMO UV - (Multi) UVIsland to Polygon Part Tags'

    def basic_Enable(self, msg):
        return True

    def basic_Execute(self, msg, flags):
        scene = modo.scene.current()
        items = modo.Scene().selected

        selmesh = scene.selectedByType(lx.symbol.sITYPE_MESH)
        lx.eval('select.drop item')

        for mesh in selmesh:
            mesh.select(True)
            lx.eval('tool.viewType uv')
            lx.eval('smo.UV.UVIslandToPolyPartTags')
            lx.eval('select.drop item')
        lx.eval('smo.GC.DeselectAll')
        scene.select(selmesh)


lx.bless(SMO_UV_Multi_UVIslandToPolyPartTags_Cmd, Cmd_Name)

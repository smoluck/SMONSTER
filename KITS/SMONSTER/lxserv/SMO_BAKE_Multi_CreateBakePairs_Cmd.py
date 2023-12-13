# python
"""
Name:       SMO_BAKE_Multi_CreatePairsFromMesh_Cmd.py

Purpose:    This script is designed to:
            (for Multiple items)
            Create a New Bake Pairs from a Single High Poly mesh and
            Enter into Polygon Editing To Reduce the Mesh Detail


Author:     Franck ELISABETH
Website:    https://www.smoluck.com
Created:    02/04/2021
Copyright:  (c) Franck Elisabeth 2017-2022
"""

import lx
import lxu
import modo

Cmd_Name = "smo.BAKE.Multi.CreatePairsFromMesh"
# smo.BAKE.Multi.CreatePairsFromMesh


class SMO_BAKE_Multi_CreatePairsFromMesh_Cmd(lxu.command.BasicCommand):
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
        return 'SMO BAKE - (Multi) Create Bake Pairs from HighPoly'

    def cmd_Desc(self):
        return 'Create a New Bake Pairs from a Single High Poly mesh and Enter into Polygon Editing To Reduce the Mesh Detail.'

    def cmd_Tooltip(self):
        return 'Create a New Bake Pairs from a Single High Poly mesh and Enter into Polygon Editing To Reduce the Mesh Detail.'

    def cmd_Help(self):
        return 'https://twitter.com/sm0luck'

    def basic_ButtonName(self):
        return 'SMO BAKE - (Multi) Create Bake Pairs from HighPoly'

    def basic_Enable(self, msg):
        return True

    def basic_Execute(self, msg, flags):
        scene = modo.scene.current()
        items = modo.Scene().selected

        selmeshessssa = scene.selectedByType(lx.symbol.sITYPE_MESH)
        lx.eval('select.drop item')
        MeshesList = []

        for mesh in selmeshessssa:
            mesh.select(True)
            lx.eval('smo.BAKE.CreatePairsFromMesh')
            # lx.eval('select.drop item')
            MeshesList.append(scene.selectedByType(lx.symbol.sITYPE_MESH))

        lx.eval('select.drop item')
        for item in MeshesList:
            scene.select(item, True)


lx.bless(SMO_BAKE_Multi_CreatePairsFromMesh_Cmd, Cmd_Name)

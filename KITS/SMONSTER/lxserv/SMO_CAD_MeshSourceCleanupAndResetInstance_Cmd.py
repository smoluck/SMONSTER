# python
"""
Name:         SMO_CAD_MeshSourceCleanupAndResetInstance_Cmd.py

Purpose:      This script is designed to
              Select the Source mesh of a given Instanced Mesh,
              instance it in place, and move it back to Origin
              with zero transforms.

Author:       Franck ELISABETH (with the help of Pavel Efimov)
Website:      https://www.linkedin.com/in/smoluck/
Created:      26/03/2021
Copyright:    (c) Franck Elisabeth 2017-2022
"""

import lx
import lxu
import modo

Cmd_Name = "smo.CAD.MeshSourceCleanupAndResetInstance"
# smo.CAD.MeshSourceCleanupAndResetInstance


class SMO_CAD_MeshSourceCleanupAndResetInstance_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)

    def cmd_Flags(self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO

    def cmd_Interact(self):
        pass

    def cmd_UserName(self):
        return 'SMO CAD - Isolate Instances Source Mesh / Reset Pos / Move To Group'

    def cmd_Desc(self):
        return 'Select the Source mesh of a given Instanced Mesh, instance it in place and move it back to Origin with zero transforms.'

    def cmd_Tooltip(self):
        return 'Select the Source mesh of a given Instanced Mesh, instance it in place and move it back to Origin with zero transforms.'

    def cmd_Help(self):
        return 'https://twitter.com/sm0luck'

    def basic_ButtonName(self):
        return 'SMO CAD - Isolate Instances Source Mesh / Reset Pos / Move To Group'

    def basic_Enable(self, msg):
        return True

    def basic_Execute(self, msg, flags):
        scene = modo.scene.current()
        lx.eval('select.itemSourceSelected')
        Source = modo.Scene().selected[0]

        lx.eval('item.duplicate true locator false false')
        NewInstance = modo.Scene().selected[0]
        lx.eval('smo.GC.ClearTransformLink')

        lx.eval('smo.GC.DeselectAll')

        Source.select()
        lx.eval('smo.CLEANUP.UnparentInPlace')

        Source.select()
        lx.eval('transform.channel pos.X 0.0')
        lx.eval('transform.channel pos.Y 0.0')
        lx.eval('transform.channel pos.Z 0.0')

        Source.select()
        SourceName = lx.eval('item.name ? xfrmcore')
        lx.eval('select.itemInstances')
        lx.eval('select.item %s add' % SourceName)


        lx.eval('item.parent parent:{} inPlace:1')
        lx.eval('layer.groupSelected')
        lx.eval('smo.CB.ItemColor 10 0')

        Source.select()
        lx.eval('smo.CB.ItemColor 8 0')
        lx.eval('select.itemInstances')
        lx.eval('item.editorColor magenta')
        lx.eval('select.itemHierarchy')

        Source.select()
        lx.eval('select.itemInstances')
        lx.eval('select.item %s add' % SourceName)
        lx.eval('hide.unsel')

        lx.eval('smo.GC.DeselectAll')

        Source.select()
        InstancesList = []
        lx.eval('select.itemInstances')
        InstancesItem = scene.selected[0]
        InstancesList = lx.eval('query sceneservice selection ? locator')

        if InstancesItem:  # checking selected item relationships for instance moving
            if InstancesItem.isAnInstance:
                for i in InstancesList:
                    lx.eval('smo.GC.ClearTransformLink')

        lx.eval('smo.GC.DeselectAll')

        Source.select()
        lx.eval('transform.channel pos.X 0.0')
        lx.eval('transform.channel pos.Y 0.0')
        lx.eval('transform.channel pos.Z 0.0')
        lx.eval('transform.channel rot.X 0.0')
        lx.eval('transform.channel rot.Y 0.0')
        lx.eval('transform.channel rot.Z 0.0')
        lx.eval('item.setType.mesh')


lx.bless(SMO_CAD_MeshSourceCleanupAndResetInstance_Cmd, Cmd_Name)

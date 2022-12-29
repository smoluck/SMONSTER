# python
"""
Name:         SMO_GC_ReplaceTargetByInstance_Cmd.py

Purpose:      This script is designed to:
              From selected targets, create a copy or an instance of the last
              selected Mesh, without or with a Guide Mesh creation.

Author:       Franck ELISABETH (based on William Vaughan Script)
Website:      https://www.smoluck.com
Created:      19/06/2020
Copyright:    (c) Franck Elisabeth 2017-2022
"""

import lx
import lxu
import modo
import sys

Cmd_Name = "smo.GC.ReplaceTargetByInstance"
# smo.GC.ReplaceTargetByInstance 1 # copy in instance mode


class SMO_GC_ReplaceTargetByInstance_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
        self.dyna_Add("Item Type", lx.symbol.sTYPE_INTEGER)
        self.basic_SetFlags(0, lx.symbol.fCMDARG_OPTIONAL)             # here the (0) define the argument index.
        self.dyna_Add("Create a Guide Mesh from Target", lx.symbol.sTYPE_INTEGER)
        self.basic_SetFlags(1, lx.symbol.fCMDARG_OPTIONAL)

    def cmd_Flags(self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO
    
    def cmd_Interact (self):
        pass
    
    def cmd_UserName (self):
        return 'SMO GC - Replace By Instance'
    
    def cmd_Desc (self):
        return 'From selected targets, create a copy or an instance of the last selected Mesh, without or with a Guide Mesh creation.'
    
    def cmd_Tooltip (self):
        return 'From selected targets, create a copy or an instance of the last selected Mesh, without or with a Guide Mesh creation.'
    
    def cmd_Help (self):
        return 'https://twitter.com/sm0luck'
    
    def basic_ButtonName (self):
        return 'SMO GC - Replace By Instance'
    
    def basic_Enable (self, msg):
        return True
    
    def basic_Execute(self, msg, flags):
        scene = modo.Scene()
        item_type = self.dyna_Int(0)
        guide_mode = self.dyna_Int(1)

        if item_type == 0:
            lx.out('Regular Clone Mode')
        elif item_type == 1:
            lx.out('Instance Clone Mode')

        SelectedItemsCount = len(lx.evalN("query sceneservice selection ? locator"))

        if SelectedItemsCount < 2:
            lx.eval('dialog.setup info')
            lx.eval('dialog.title {Replace Target By Instance:}')
            lx.eval('dialog.msg {"You must have at least 2 items selected to run this script.}')
            lx.eval('+dialog.open')
            sys.exit()

        if SelectedItemsCount >= 2:
            SelectedItemsCount = (SelectedItemsCount - 1)
            lx.out('Selected Target Count:', SelectedItemsCount)

            selMeshes = lx.eval('query sceneservice selection ? mesh')
            lx.out('selMeshes', selMeshes)
            TargetMeshes = scene.selected

            sourceMesh = selMeshes[-1]
            lx.out(sourceMesh)

            meshnum = 0

            # deselect items
            lx.eval('smo.GC.DeselectAll')

            if guide_mode == 1:
                lx.eval("layer.new")
                GuideMesh = scene.selected
                lx.eval("item.name Guide mesh")
                lx.eval("smo.CB.ItemColor 8 1")
                lx.eval("item.channel locator$select off")
                lx.eval('smo.GC.DeselectAll')
                scene.select(TargetMeshes)
                lx.eval("select.type polygon")
                lx.eval("select.all")
                lx.eval("copy")
                scene.select(GuideMesh)
                lx.eval("paste")
                lx.eval("select.drop polygon")
                lx.eval("select.type item")
                lx.eval('smo.GC.DeselectAll')

            lx.eval('select.item {%s} set' % sourceMesh)
            lx.eval("smo.CB.ItemColor 3 0")
            lx.eval('smo.GC.DeselectAll')

            for r in range(SelectedItemsCount):
                lx.eval('select.item {%s} set' % selMeshes[meshnum])
                m = lx.eval('query sceneservice selection ? mesh')
                # print(m)

                # Get item Position, Scale and Rotation
                m_pos = lx.eval('query sceneservice item.Pos ? %s' % m)  # Queries the current item XYZ position
                m_rot = lx.eval('query sceneservice item.Rot ? %s' % m)  # Queries the current item Rotation XYZ value
                m_scl = lx.eval('query sceneservice item.Scale ? %s' % m)  # Queries the current item Scale XYZ value
                lx.out(m_pos)
                lx.out(m_rot)
                lx.out(m_scl)

                m_rot_x = ((m_rot[0] * 180) / 3.14)
                m_rot_y = ((m_rot[1] * 180) / 3.14)
                m_rot_z = ((m_rot[2] * 180) / 3.14)
                # print(m_rot_x)
                # print(m_rot_y)
                # print(m_rot_z)

                # delete
                lx.eval('!delete')

                lx.eval('select.item {%s} set' % sourceMesh)
                if item_type == 0:
                    lx.eval('item.duplicate')
                elif item_type == 1:
                    lx.eval('item.duplicate true locator false true')

                # Move the new item
                lx.eval('transform.channel pos.X %s' % m_pos[0])
                lx.eval('transform.channel pos.Y %s' % m_pos[1])
                lx.eval('transform.channel pos.Z %s' % m_pos[2])

                # Rotate the new item
                lx.eval('transform.channel rot.X %s' % m_rot_x)
                lx.eval('transform.channel rot.Y %s' % m_rot_y)
                lx.eval('transform.channel rot.Z %s' % m_rot_z)

                # Scale the new item
                lx.eval('transform.channel scl.X %s' % m_scl[0])
                lx.eval('transform.channel scl.Y %s' % m_scl[1])
                lx.eval('transform.channel scl.Z %s' % m_scl[2])

                # deselect items
                lx.eval('select.drop item')

                meshnum += 1

            del selMeshes
            del TargetMeshes
        
    
lx.bless(SMO_GC_ReplaceTargetByInstance_Cmd, Cmd_Name)

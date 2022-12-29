# python
"""
Name:         SMO_GC_ClearTransformLink_Cmd.py

Purpose:      This script is designed to
              Remove any link between Sources and Instances Transform / Order

Author:       Franck ELISABETH (with the help of Pavel Efimov)
Website:      https://www.smoluck.com
Created:      26/03/2021
Copyright:    (c) Franck Elisabeth 2017-2022
"""

import lx
import lxu
import modo

Cmd_Name = "smo.GC.ClearTransformLink"
# smo.GC.ClearTransformLink


class SMO_GC_ClearTransformLink_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)

    def cmd_Flags(self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO

    def cmd_Interact(self):
        pass

    def cmd_UserName(self):
        return 'SMO GC - Clear Transform Link'

    def cmd_Desc(self):
        return 'Remove any link between Sources and Instances Transform / Order.'

    def cmd_Tooltip(self):
        return 'Remove any link between Sources and Instances Transform / Order.'

    def cmd_Help(self):
        return 'https://twitter.com/sm0luck'

    def basic_ButtonName(self):
        return 'SMO GC - Clear Transform Link'

    def basic_Enable(self, msg):
        return True

    def basic_Execute(self, msg, flags):
        scene = modo.scene.current()
        Instance = modo.Scene().selected[0]
        # We can access item transform graph, it contains all translation, rotation and scale channels
        # The graph is useful for retrieving the channel IDs that are unique per item
        trfrm_channels = Instance.itemGraph('xfrmCore').reverse()
        # Go through all channels that the instance contains
        # NOTE: The instance item will only contain channels that were changed in the source item. So if the source item was only moved, but not rotated, the instance will only contain translation channel
        for trfrm_pos in trfrm_channels:
            # Cache the transform id
            transformTrans_id = trfrm_pos.id
            # This is the hacky part, I only filter for translation channels
            if 'translation' in transformTrans_id:
                # Now we simply query the current translation values on XYZ axes
                pos_x_value = lx.eval('channel.value ? channel:{%s:pos.X}' % transformTrans_id)
                pos_y_value = lx.eval('channel.value ? channel:{%s:pos.Y}' % transformTrans_id)
                pos_z_value = lx.eval('channel.value ? channel:{%s:pos.Z}' % transformTrans_id)

                lx.eval('channel.key mode:add channel:{%s:pos.X}' % transformTrans_id)
                lx.eval('channel.key mode:remove channel:{%s:pos.X}' % transformTrans_id)
                lx.eval('channel.key mode:add channel:{%s:pos.Y}' % transformTrans_id)
                lx.eval('channel.key mode:remove channel:{%s:pos.Y}' % transformTrans_id)
                lx.eval('channel.key mode:add channel:{%s:pos.Z}' % transformTrans_id)
                lx.eval('channel.key mode:remove channel:{%s:pos.Z}' % transformTrans_id)

                # And then set them again, forcing the channel value to go into 'edit' state and not inherit translation data from the source item anymore
                # lx.eval('channel.value %s channel:{%s:pos.X}' % (pos_x_value, transform_id))
                # lx.eval('channel.value %s channel:{%s:pos.Y}' % (pos_y_value, transform_id))
                # lx.eval('channel.value %s channel:{%s:pos.Z}' % (pos_z_value, transform_id))

        for trfrm_rot in trfrm_channels:
            # Cache the transform id
            transformRot_id = trfrm_rot.id
            # This is the hacky part, I only filter for translation channels
            if 'rotation' in transformRot_id:
                # Now we simply query the current rotation values on XYZ axes
                rot_x_value = lx.eval('channel.value ? channel:{%s:rot.X}' % transformRot_id)
                rot_y_value = lx.eval('channel.value ? channel:{%s:rot.Y}' % transformRot_id)
                rot_z_value = lx.eval('channel.value ? channel:{%s:rot.Z}' % transformRot_id)

                lx.eval('channel.key mode:add channel:{%s:rot.X}' % transformRot_id)
                lx.eval('channel.key mode:remove channel:{%s:rot.X}' % transformRot_id)
                lx.eval('channel.key mode:add channel:{%s:rot.Y}' % transformRot_id)
                lx.eval('channel.key mode:remove channel:{%s:rot.Y}' % transformRot_id)
                lx.eval('channel.key mode:add channel:{%s:rot.Z}' % transformRot_id)
                lx.eval('channel.key mode:remove channel:{%s:rot.Z}' % transformRot_id)

                # And then set them again, forcing the channel value to go into 'edit' state and not inherit translation data from the source item anymore
                # lx.eval('channel.value %s channel:{%s:rot.X}' % (rot_x_value, transform_id))
                # lx.eval('channel.value %s channel:{%s:rot.Y}' % (rot_y_value, transform_id))
                # lx.eval('channel.value %s channel:{%s:rot.Z}' % (rot_z_value, transform_id))

                # Now we simply query the current translation values on XYZ axes
                order_value = lx.eval('channel.value ? channel:{%s:rot.X}' % transformRot_id)

                lx.eval('channel.key mode:add channel:{%s:order}' % transformRot_id)
                lx.eval('channel.key mode:remove channel:{%s:order}' % transformRot_id)
                # And then set them again, forcing the channel value to go into 'edit' state and not inherit translation data from the source item anymore
                # lx.eval('channel.value %s channel:{%s:order}' % transformRot_id)


lx.bless(SMO_GC_ClearTransformLink_Cmd, Cmd_Name)

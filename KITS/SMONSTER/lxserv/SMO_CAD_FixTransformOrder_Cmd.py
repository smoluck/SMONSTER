# python
"""
Name:         SMO_CAD_FixTransformOrder_Cmd.py

Purpose:      This script is designed to:
              Change the Transform Order of current selected item to XYZ Order.

Author:       Franck ELISABETH
Website:      https://www.linkedin.com/in/smoluck/
Created:      07/05/2021
Copyright:    (c) Franck Elisabeth 2017-2022
"""

import lx
import lxu
import modo

Cmd_Name = "smo.CAD.FixTransformOrder"


class SMO_CAD_FixTransformOrder_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
        # Use ModoStandard because Unity FBX loader use XYZ
        # self.dyna_Add("Mode", lx.symbol.sTYPE_BOOLEAN)      # XYZ by default
        self.SelModeItem = bool(lx.eval1("select.typeFrom typelist:item;polygon;vertex;edge ?"))

    def cmd_Flags(self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO

    def cmd_Interact(self):
        pass

    def cmd_UserName(self):
        return 'SMO CAD - Fix Transform Order'

    def cmd_Desc(self):
        return 'Change the Transform Order of current selected item to XYZ Order.'

    def cmd_Tooltip(self):
        return 'Change the Transform Order of current selected item to XYZ Order.'

    def cmd_Help(self):
        return 'https://twitter.com/sm0luck'

    def basic_ButtonName(self):
        return 'SMO CAD - Fix Transform Order'

    def basic_Enable(self, msg):
        return True

    def basic_Execute(self, msg, flags):
        scene = modo.scene.current()
        if self.SelModeItem:


            # BugFix to preserve the state of the RefSystem (item at origin in viewport)
            # This query only works when an item is selected.
            RefSystemActive = bool()
            CurrentRefSystemItem = lx.eval('item.refSystem ?')
            # print(CurrentRefSystemItem)
            if len(CurrentRefSystemItem) != 0:
                RefSystemActive = True
            else:
                RefSystemActive = False
            # print(RefSystemActive)


            Item_Source = scene.selected[0]
            Item_Source_ID = Item_Source.Ident()
            # print('Source Mesh:', Item_Source_ID)


            # Check if the item have Transform Rotation set
            Item_Source = modo.Scene().selected[0]
            # We can access item transform graph, it contains all translation, rotation and scale channels
            # The graph is useful for retrieving the channel IDs that are unique per item
            trfrm_channels = Item_Source.itemGraph('xfrmCore').reverse()
            # Go through all channels that the instance contains
            # NOTE: The instance item will only contain channels that were changed in the source item. So if the source item was only moved, but not rotated, the instance will only contain translation channel

            ItemHaveRotationTransform = False
            rot_x_value = 0.0
            rot_y_value = 0.0
            rot_z_value = 0.0
            for trfrm_rot in trfrm_channels:
                # Cache the transform id
                transformRot_id = trfrm_rot.id
                # This is the hacky part, I only filter for translation channels
                if 'rotation' in transformRot_id:
                    ItemHaveRotationTransform = True
                    # Now we simply query the current rotation values on XYZ axes
                    rot_x_value = lx.eval('channel.value ? channel:{%s:rot.X}' % transformRot_id)
                    rot_y_value = lx.eval('channel.value ? channel:{%s:rot.Y}' % transformRot_id)
                    rot_z_value = lx.eval('channel.value ? channel:{%s:rot.Z}' % transformRot_id)
                    # print(rot_x_value)
                    # print(rot_y_value)
                    # print(rot_z_value)

            # when the Transform Rotation is set then we have to do the Transform Order Fix via Locator to get it back in line.
            if ItemHaveRotationTransform:
                if rot_x_value != 0.0 or rot_y_value != 0.0 or rot_z_value != 0.0 or rot_x_value != -0.0 or rot_y_value != -0.0 or rot_z_value != -0.0:
                    lx.eval('item.create locator')
                    Loc_Child = scene.selectedByType('locator')[0]
                    Loc_Child_ID = Loc_Child.Ident()
                    # print('Child Locator:', Loc_Child_ID)

                    lx.eval('select.subItem {%s} add mesh 0 0' % Item_Source_ID)
                    lx.eval('item.parent')
                    lx.eval('smo.GC.DeselectAll')

                    scene.select(Loc_Child_ID)
                    lx.eval('item.parent parent:{} inPlace:1')

                    scene.select(Item_Source)
                    lx.eval('transform.channel order xyz')

                    lx.eval('select.subItem {%s} add mesh 0 0' % Loc_Child_ID)
                    # lx.eval('item.match item pos average:false item:{%s} itemTo:{%s}' % (Item_Source_ID, Loc_Child_ID))
                    lx.eval('item.match item rot average:false item:{%s} itemTo:{%s}' % (Item_Source_ID, Loc_Child_ID))
                    # lx.eval('item.match item scl average:false item:{%s} itemTo:{%s}' % (Item_Source_ID, Loc_Child_ID))
                    scene.select(Loc_Child_ID)
                    lx.eval('!delete')
                    scene.select(Item_Source)


                    trfrm_channels = Item_Source.itemGraph('xfrmCore').reverse()
                    # Save current Rotation as Setup Rest Value
                    for trfrm_rot in trfrm_channels:
                        # Cache the transform id
                        transformRot_id = trfrm_rot.id
                        # This is the hacky part, I only filter for translation channels
                        if 'rotation' in transformRot_id:
                            # Now we simply query the current rotation values on XYZ axes
                            rot_x_value = lx.eval('channel.value ? channel:{%s:rot.X}' % transformRot_id)
                            rot_y_value = lx.eval('channel.value ? channel:{%s:rot.Y}' % transformRot_id)
                            rot_z_value = lx.eval('channel.value ? channel:{%s:rot.Z}' % transformRot_id)
                            lx.eval('channel.toSetup channel:{%s:rot.X} restore:false' % transformRot_id)
                            lx.eval('channel.toSetup channel:{%s:rot.Y} restore:false' % transformRot_id)
                            lx.eval('channel.toSetup channel:{%s:rot.Z} restore:false' % transformRot_id)


                    lx.eval('smo.GC.DeselectAll')
                    scene.select(Item_Source)


                if rot_x_value == 0.0 and rot_y_value == 0.0 and rot_z_value == 0.0:
                    scene.select(Item_Source)
                    lx.eval('transform.channel order xyz')


            if not RefSystemActive:
                lx.eval('item.refSystem {}')
            if RefSystemActive:
                lx.eval('item.refSystem %s' % CurrentRefSystemItem)


    def cmd_Query(self, index, vaQuery):
        lx.notimpl()


lx.bless(SMO_CAD_FixTransformOrder_Cmd, Cmd_Name)

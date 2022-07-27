# python
# ---------------------------------------
# Name:         SMO_GC_Setup_OffsetCenterPosPreserveInstancesPos_Cmd
# Version:      1.0
#
# Purpose:      This script is designed to:
#               Offset Center Position on selected Mesh Item, but preserve the Instances Positions in Worldspace.
#
#
# Author:       Franck ELISABETH
# Website:      http://www.smoluck.com
#
# Created:      19/04/2021
# Copyright:    (c) Franck Elisabeth 2017-2022
# ---------------------------------------

import lx, lxu, modo

Cmd_Name = "smo.GC.Setup.OffsetCenterPosPreserveInstancesPos"

class SMO_GC_Setup_OffsetCenterPosPreserveInstancesPos_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
    
    def cmd_Flags(self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO
    
    def cmd_Interact (self):
        pass
    
    def cmd_UserName (self):
        return 'SMO GC - Setup - Offset Center Position and Preserve Instances Position'
    
    def cmd_Desc (self):
        return 'Offset Center Position on selected Mesh Item, but preserve the Instances Positions in Worldspace.'
    
    def cmd_Tooltip (self):
        return 'Offset Center Position on selected Mesh Item, but preserve the Instances Positions in Worldspace.'
    
    def cmd_Help (self):
        return 'https://twitter.com/sm0luck'
    
    def basic_ButtonName (self):
        return 'SMO GC - Setup - Offset Center Position and Preserve Instances Position'
    
    def basic_Enable (self, msg):
        return True
    
    def basic_Execute(self, msg, flags):
        def rad(a):
            return a * 57.2957795130

        scene = modo.scene.current()
        selected_Items = lxu.select.ItemSelection().current()
        print(selected_Items)

        ###############COPY/PASTE Check Procedure#################
        ## create variables
        lx.eval("user.defNew name:User_Pref_CopyDeselectChangedState type:boolean life:momentary")
        lx.eval("user.defNew name:User_Pref_PasteSelectionChangedState type:boolean life:momentary")
        lx.eval("user.defNew name:User_Pref_PasteDeselectChangedState type:boolean life:momentary")

        lx.eval("user.defNew name:User_Pref_CopyDeselect type:boolean life:momentary")
        lx.eval("user.defNew name:User_Pref_PasteSelection type:boolean life:momentary")
        lx.eval("user.defNew name:User_Pref_PasteDeselect type:boolean life:momentary")
        ###################

        # Look at current Copy / Paste user Preferences:
        User_Pref_CopyDeselect = lx.eval('pref.value application.copyDeSelection ?')
        lx.out('User Pref: Deselect Elements after Copying', User_Pref_CopyDeselect)
        User_Pref_PasteSelection = lx.eval('pref.value application.pasteSelection ?')
        lx.out('User Pref: Select Pasted Elements', User_Pref_PasteSelection)
        User_Pref_PasteDeselect = lx.eval('pref.value application.pasteDeSelection ?')
        lx.out('User Pref: Deselect Elements Before Pasting', User_Pref_PasteDeselect)
        # Is Copy Deselect False ?
        if User_Pref_CopyDeselect == 0:
            lx.eval('pref.value application.copyDeSelection true')
            User_Pref_CopyDeselectChangedState = 1

        # Is Paste Selection False ?
        if User_Pref_PasteSelection == 0:
            lx.eval('pref.value application.pasteSelection true')
            User_Pref_PasteSelectionChangedState = 1

        # Is Paste Deselect False ?
        if User_Pref_PasteDeselect == 0:
            lx.eval('pref.value application.pasteDeSelection true')
            User_Pref_PasteDeselectChangedState = 1

        # Is Copy Deselect True ?
        if User_Pref_CopyDeselect == 1:
            User_Pref_CopyDeselectChangedState = 0

        # Is Paste Selection True ?
        if User_Pref_PasteSelection == 1:
            User_Pref_PasteSelectionChangedState = 0

        # Is Paste Deselect True ?
        if User_Pref_PasteDeselect == 1:
            User_Pref_PasteDeselectChangedState = 0
        ################################################

        ### 1 ######################################################################################
        ################ Calculate the Offset needed ###############################################
        TargetList = []
        TotalInstancesList = []
        HaveInstance = False

        if lx.eval('workPlane.state ?') == True:
            lx.eval('workPlane.state false')
        RefSystemActive = bool()
        CurrentRefSystemItem = lx.eval('item.refSystem ?')
        print(CurrentRefSystemItem)
        if CurrentRefSystemItem is not None:
            lx.eval('item.refSystem {}')

        for item in selected_Items:
            item = lx.object.Item(item)
            TargetID = item.Ident()
            TargetList.append(TargetID)
        print(TargetList)

        lx.eval('select.type polygon')
        lx.eval('workPlane.fitGeometry')
        lx.eval('workPlane.fitSelect')
        WorldTargetCenterX = lx.eval('workplane.edit ? 0 0 0 0 0')
        WorldTargetCenterY = lx.eval('workplane.edit 0 ? 0 0 0 0')
        WorldTargetCenterZ = lx.eval('workplane.edit 0 0 ? 0 0 0')
        lx.eval('workPlane.state false')
        lx.out('Workplane posX:', WorldTargetCenterX)
        lx.out('Workplane posY:', WorldTargetCenterY)
        lx.out('Workplane posZ:', WorldTargetCenterZ)
        lx.eval('workPlane.edit cenX:%f cenY:%f cenZ:%f rotX:0 rotY:0 rotZ:0' % (
        WorldTargetCenterX, WorldTargetCenterY, WorldTargetCenterZ))

        # Get the Offset position from the Item Relative Position
        scene.select(selected_Items)
        print(len(selected_Items))
        # if (len(selected_Items)) == 1 :
        selected_mesh = scene.selected[0]  # gets the current selected object (throws an error if nothing is selected)
        Tar_WorldPos = selected_mesh.transforms.position.get()
        lx.out(Tar_WorldPos)
        Tar_WorldRot = selected_mesh.transforms.rotation.get()
        lx.out(Tar_WorldRot)
        lx.eval('item.refSystem %s' % TargetList[0])

        lx.eval('select.type polygon')
        lx.eval('workPlane.fitGeometry')
        lx.eval('workPlane.fitSelect')
        RelativeOffsetX = lx.eval('workplane.edit ? 0 0 0 0 0')
        RelativeOffsetY = lx.eval('workplane.edit 0 ? 0 0 0 0')
        RelativeOffsetZ = lx.eval('workplane.edit 0 0 ? 0 0 0')
        lx.eval('workPlane.state false')
        lx.out('Center Offset posX:', RelativeOffsetX)
        lx.out('Center Offset posY:', RelativeOffsetY)
        lx.out('Center Offset posZ:', RelativeOffsetZ)
        # lx.eval('workPlane.edit cenX:%f cenY:%f cenZ:%f rotX:0 rotY:0 rotZ:0' % (RelativeOffsetX, RelativeOffsetY, RelativeOffsetZ))

        RelativeOffsetPos = [float(), float(), float()]
        RelativeOffsetPos = [RelativeOffsetX, RelativeOffsetY, RelativeOffsetZ]
        print(RelativeOffsetPos)

        NewPosX = (Tar_WorldPos[0] + RelativeOffsetPos[0])
        NewPosY = (Tar_WorldPos[1] + RelativeOffsetPos[1])
        NewPosZ = (Tar_WorldPos[2] + RelativeOffsetPos[2])
        print([NewPosX, NewPosY, NewPosZ])

        lx.eval('workPlane.edit cenX:%f cenY:%f cenZ:%f rotX:0 rotY:0 rotZ:0' % (
        WorldTargetCenterX, WorldTargetCenterY, WorldTargetCenterZ))
        ### 1 #####################################################################################

        ### 2 #####################################################################################
        ################ Copy the Mesh Polygon Data and paste it back at the correct location #####
        lx.eval('item.refSystem {}')
        lx.eval('workPlane.state false')

        scene.select(selected_Items)
        lx.eval('select.type polygon')
        lx.eval('select.all')
        lx.eval('cut')

        # Get the Transform of the current selected Item.
        TargetItem = lx.eval1("query sceneservice selection ? locator")
        TargetXfrm = lx.eval1("query sceneservice item.xfrmPos ? " + TargetItem)
        print(TargetXfrm)

        lx.eval('select.channel {%s:pos.X} set' % TargetXfrm)
        lx.eval('channel.value {%s} channel:{%s:pos.X}' % (NewPosX, TargetXfrm))
        lx.eval('select.channel {%s:pos.X} set' % TargetXfrm)
        lx.eval('channel.value {%s} channel:{%s:pos.Y}' % (NewPosY, TargetXfrm))
        lx.eval('select.channel {%s:pos.X} set' % TargetXfrm)
        lx.eval('channel.value {%s} channel:{%s:pos.Z}' % (NewPosZ, TargetXfrm))

        lx.eval('select.type polygon')
        lx.eval('paste')
        lx.eval('select.drop polygon')
        ### 2 #####################################################################################

        ### 3 ############################################################################################################################
        #####Select the instances back and offset them individualy and localy to get them back at the right Position in World space. #####
        lx.eval('select.type item')
        lx.eval('workPlane.reset')

        Source_PosX = RelativeOffsetX
        Source_PosY = RelativeOffsetY
        Source_PosZ = RelativeOffsetZ

        print (Source_PosX)
        print (Source_PosY)
        print (Source_PosZ)

        # Drop channels selected.
        lx.eval('select.drop channel')

        lx.eval('select.itemInstances')

        scene = modo.scene.current()
        SelItem = lxu.select.ItemSelection().current()
        print (SelItem)

        ToProcessList = []
        # for item in TargetIDList:
        for item in SelItem:
            scene.select(item)
            item_name = item.UniqueName()
            ToProcessList.append(item_name)
        print(ToProcessList)

        lx.eval('smo.GC.DeselectAll')
        for item in ToProcessList:
            scene.select(item)
            TargetItem = lx.eval1("query sceneservice selection ? locator")
            print(TargetItem)
            chanRotX = lx.eval('transform.channel rot.X ?')
            print(chanRotX)
            chanRotY = lx.eval('transform.channel rot.Y ?')
            print(chanRotY)
            chanRotZ = lx.eval('transform.channel rot.Z ?')
            print(chanRotZ)

            lx.eval('item.parent parent:{} inPlace:1')
            lx.eval('item.create locator applyDefaultPreset:true')
            LocItem = lx.eval1("query sceneservice selection ? locator")
            print(LocItem)
            lx.eval('smo.GC.DeselectAll')

            # Parent Loc To Target
            scene.select(LocItem)
            lx.eval('select.item {%s} add' % TargetItem)
            lx.eval('item.parent')
            lx.eval('smo.GC.DeselectAll')

            # Unparent in place the Locator
            scene.select(LocItem)
            lx.eval('item.parent parent:{} inPlace:1')
            lx.eval('smo.GC.DeselectAll')

            # Parent Target back to Loc Position
            scene.select(TargetItem)
            TargetXfrm = lx.eval1("query sceneservice item.xfrmPos ? " + TargetItem)
            print(TargetXfrm)

            ######################
            lx.eval('channel.value {%s} channel:{%s:pos.X}' % (Source_PosX, TargetXfrm))
            lx.eval('channel.value {%s} channel:{%s:pos.Y}' % (Source_PosY, TargetXfrm))
            lx.eval('channel.value {%s} channel:{%s:pos.Z}' % (Source_PosZ, TargetXfrm))

            lx.eval('smo.GC.DeselectAll')
            scene.select(TargetItem)
            lx.eval('select.item {%s} add' % LocItem)
            lx.eval('item.parent')
            lx.eval('smo.GC.DeselectAll')

            scene.select(TargetItem)
            lx.eval('item.parent parent:{} inPlace:1')
            lx.eval('transform.channel rot.X %s' % rad(chanRotX))
            lx.eval('transform.channel rot.Y %s' % rad(chanRotY))
            lx.eval('transform.channel rot.Z %s' % rad(chanRotZ))
            scene.select(LocItem)
            lx.eval('!delete')

        del (ToProcessList[:])
        # lx.eval('smo.GC.DeselectAll')
        # scene.select(selected_Items)
        # for i in range(len(selected_Items)) :
        #     scene.select(selected_Items[i])
        #     try:
        #         lx.eval('!select.itemInstances')
        #         Instances = lxu.select.ItemSelection().current()
        #         for item in Instances:
        #             item = lx.object.Item(item)
        #             InstancesID = item.Ident()
        #             TotalInstancesList.append(InstancesID)
        #     except:
        #         pass
        # print(TotalInstancesList)
        # # del TotalInstancesList [:]  # Delete A List , Used at the end of a script to be sure it's cleared.
        # lx.eval('smo.GC.DeselectAll')
        # for i in range(len(TotalInstancesList)) :
        #     scene.select(TotalInstancesList[i])
        #     # Get the Transform of the current selected Item.
        #     InstanceItem = lx.eval1( "query sceneservice selection ? locator" )
        #     InstanceXfrm = lx.eval1( "query sceneservice item.xfrmPos ? " + InstanceItem )
        #     print(InstanceXfrm)
        #     lx.eval('select.channel {%s:pos.X} set' % TargetXfrm)
        #     InstancePosX = lx.eval('channel.value ? channel:{%s:pos.X}' % InstanceXfrm)
        #     lx.eval('select.channel {%s:pos.Y} set' % TargetXfrm)
        #     InstancePosY = lx.eval('channel.value ? channel:{%s:pos.Y}' % InstanceXfrm)
        #     lx.eval('select.channel {%s:pos.Z} set' % TargetXfrm)
        #     InstancePosZ = lx.eval('channel.value ? channel:{%s:pos.Z}' % InstanceXfrm)
        #     InstancePos = [float(), float(),float()]
        #     InstancePos = [InstancePosX, InstancePosY, InstancePosZ]
        #
        #     NewInstaPosX = (InstancePos[0] + RelativeOffsetPos[0])
        #     NewInstaPosY = (InstancePos[1] + RelativeOffsetPos[1])
        #     NewInstaPosZ = (InstancePos[2] + RelativeOffsetPos[2])
        #     InstanceOffsetPos = [float(), float(),float()]
        #     InstanceOffsetPos = [InstancePosX, InstancePosY, InstancePosZ]
        #     print(InstanceOffsetPos)
        #
        #
        #     # Position Transform Channel Solution --> Not working if Rotation different from 0 0 0
        #     lx.eval('channel.value {%s} channel:{%s:pos.X}' % (NewInstaPosX, InstanceXfrm))
        #     lx.eval('select.channel {%s:pos.X} set' % TargetXfrm)
        #     lx.eval('channel.value {%s} channel:{%s:pos.Y}' % (NewInstaPosY, InstanceXfrm))
        #     lx.eval('select.channel {%s:pos.X} set' % TargetXfrm)
        #     lx.eval('channel.value {%s} channel:{%s:pos.Z}' % (NewInstaPosZ, InstanceXfrm))
        #
        #
        #     # # Transform Move Tool Solution --> Not working actually
        #     # lx.eval('tool.set actr.localAxis on')
        #     # lx.eval('tool.set TransformMove on')
        #     # lx.eval('tool.viewType type:xyz')
        #     # lx.eval('@kit_SMO_GAME_CONTENT:MacroSmoluck/Basic/SMO_BAS_TransformMoveSetValueXYZ.LXM {%f} {%f} {%f}' % (NewInstaPosX, NewInstaPosY, NewInstaPosZ))
        #     # lx.eval('@kit_SMO_GAME_CONTENT:MacroSmoluck/Basic/SMO_BAS_TransformMoveSetValueXYZ.py {%s} {%s} {%s}' % (NewInstaPosX, NewInstaPosY, NewInstaPosZ))
        #     # #lx.eval('tool.set actr.local on')
        #     # #lx.eval('tool.attr xfrm.transform TX %s' % NewInstaPosX)
        #     # #lx.eval('tool.attr xfrm.transform TY %s' % NewInstaPosY)
        #     # #lx.eval('tool.attr xfrm.transform TZ %s' % NewInstaPosZ)
        #     # lx.eval('tool.doApply')
        #     # lx.eval('tool.set TransformMove off')
        #     # lx.eval('tool.set actr.localAxis off')
        #     # lx.eval('actionCenter.state false')
        #
        # del InstancePos[:]
        # del InstanceOffsetPos[:]

        lx.eval('smo.GC.DeselectAll')
        scene.select(selected_Items)
        lx.eval('select.type polygon')

        ###############COPY/PASTE END Procedure#################
        # Restore user Preferences:
        if User_Pref_CopyDeselectChangedState == 1:
            lx.eval('pref.value application.copyDeSelection false')
            lx.out('"Deselect Elements after Copying" have been Restored')
        if User_Pref_PasteSelectionChangedState == 1:
            lx.eval('pref.value application.pasteSelection false')
            lx.out('"Select Pasted Elements" have been Restored')
        if User_Pref_PasteDeselectChangedState == 1:
            lx.eval('pref.value application.pasteDeSelection false')
            lx.out('"Deselect Elements Before Pasting" have been Restored')
        ########################################################


lx.bless(SMO_GC_Setup_OffsetCenterPosPreserveInstancesPos_Cmd, Cmd_Name)

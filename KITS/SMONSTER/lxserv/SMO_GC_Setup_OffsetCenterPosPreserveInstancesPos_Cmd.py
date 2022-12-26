# python
"""
# Name:         SMO_GC_Setup_OffsetCenterPosPreserveInstancesPos_Cmd
# Version:      1.0
#
# Purpose:      This script is designed to:
#               Offset Center Position on selected Mesh Item,
#               but preserve the Instances Positions in Worldspace.
#
#
# Author:       Franck ELISABETH
# Website:      https://www.smoluck.com
#
# Created:      19/04/2021
# Copyright:    (c) Franck Elisabeth 2017-2022
"""

import lx
import lxu
import modo

Cmd_Name = "smo.GC.Setup.OffsetCenterPosPreserveInstancesPos"


class SMO_GC_Setup_OffsetCenterPosPreserveInstancesPos_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
        self.SelModeVert = bool(lx.eval1("select.typeFrom typelist:vertex;polygon;edge;item;ptag ?"))
        self.SelModeEdge = bool(lx.eval1("select.typeFrom typelist:edge;vertex;polygon;item ?"))
        self.SelModePoly = bool(lx.eval1("select.typeFrom typelist:polygon;vertex;edge;item ?"))
        self.SelModeItem = bool(lx.eval1("select.typeFrom typelist:item;pivot;center;edge;polygon;vertex;ptag ?"))
        # print(self.SelModeVert)
        # print(self.SelModeEdge)
        # print(self.SelModePoly)
        # print(self.SelModeItem)
        self.sel_mode = int()
        if self.SelModeVert:
            self.sel_mode = 1
        if self.SelModeEdge:
            self.sel_mode = 2
        if self.SelModePoly:
            self.sel_mode = 3
        if self.SelModeItem:
            self.sel_mode = 5
    
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
        # lx.out('User Pref: Deselect Elements after Copying', User_Pref_CopyDeselect)
        User_Pref_PasteSelection = lx.eval('pref.value application.pasteSelection ?')
        # lx.out('User Pref: Select Pasted Elements', User_Pref_PasteSelection)
        User_Pref_PasteDeselect = lx.eval('pref.value application.pasteDeSelection ?')
        # lx.out('User Pref: Deselect Elements Before Pasting', User_Pref_PasteDeselect)
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
        scene = modo.scene.current()
        selected_Items = lxu.select.ItemSelection().current()
        # print(selected_Items)

        Target_Meshes = scene.selected
        mi = modo.Item()  # selected item,
        name = mi.UniqueName()
        # print('Mesh Name is:', name)
        ident = mi.Ident()
        # print('Mesh ID is:', ident)
        p_name = []


        # Detect Instance Count on selected item.
        inst_ss = lxu.select.SceneSelection()
        inst_scene = inst_ss.current()
        # print(dir(inst_scene))
        inst_graph = lx.object.ItemGraph(inst_scene.GraphLookup(lx.symbol.sGRAPH_MESHINST))
        print('Number of instances on selected item: ', inst_graph.FwdCount(mi))
        InstanceCount = (inst_graph.FwdCount(mi))
        HaveInstance = bool()
        if InstanceCount > 0:
            HaveInstance = True
            print('Target have instances: ', HaveInstance)
        else:
            HaveInstance = False


        mesh = scene.selectedByType('mesh')
        ComponentTuple = []
        ComponentList = list()
        if self.sel_mode == 1:
            for item in mesh:
                # CsVertex = len(item.geometry.vertices.selected)
                # print('Total selected Vertex on this mesh layer', CsVertex)
                Vertex = item.geometry.vertices.selected
                # print('modo.Mesh list ',Vertex)
                ComponentTuple.append(Vertex)
            # print('Tuple (Vertex ID and Mesh ID): ---)', ComponentTuple)
            lx.eval('select.drop vertex')

        if self.sel_mode == 2:
            for item in mesh:
                # CsEdges = len(item.geometry.edges.selected)
                # print('Total selected Edges on this mesh layer', CsEdges)
                Edges = item.geometry.edges.selected
                # print('modo.Mesh list ',Edges)
                ComponentTuple.append(Edges)
            # print('Tuple (Edges ID and Mesh ID): ---)', ComponentTuple)
            lx.eval('select.drop edge')

        if self.sel_mode == 3:
            for item in mesh:
                # CsPolys = len(item.geometry.polygons.selected)
                # print('Total selected Polygons on this mesh layer', CsPolys)
                Polys = item.geometry.polygons.selected
                # print('modo.Mesh list ', Polys)
                ComponentTuple.append(Polys)
            # print('Tuple (Poly ID and Mesh ID): ---)', ComponentTuple)
            lx.eval('select.drop polygon')

        # if self.sel_mode == 5:
        #     for item in mesh:
        #         # CsPolys = len(item.geometry.polygons.selected)
        #         # print('Total selected Polygons on this mesh layer', CsPolys)
        #         Polys = item.geometry.polygons.selected
        #         # print('modo.Mesh list ', Polys)
        #         ComponentTuple.append(Polys)
        #     # print('Tuple (Poly ID and Mesh ID): ---)', ComponentTuple)
        #     lx.eval('select.drop polygon')

        ComponentList = list(ComponentTuple)
        # print('List (Vertex ID and Mesh ID): ---)', ComponentList)

        # Detect if current item have a Parent, then it's a child of a hierarchy
        HaveParent = bool()
        try:
            p = mi.Parent()
            p_name = p.UniqueName()
            p_ident = p.Ident()
            # print('Parent Name of %s  is : %s' % (name, p_name))
            # print(p_name)
            HaveParent = True
        except:
            HaveParent = False
            pass
        # print('Target Original Mesh have parent: ', HaveParent)

        instance_ident = []
        TargetList = []
        TotalInstancesList = []
        CurrentRefSystemItem = []
        ToProcessList = []
        Presence_W_Loc = bool()
        if HaveInstance:
            scene.select(ident)
            lx.eval('select.itemInstances')
            instance_ident = mi.Ident()


            # ------------------------------------- #
            # ------------------------------------- #
            # Create a list of parent for all instances
            InstID_List = []
            n = scene.selected
            # print(n)
            for item in n:
                ID = item.Ident()
                # print(ID)
                InstID_List.append(ID)
            # print(InstID_List)

            Inst_Parent_List = []
            State_InstanceParent = []
            InstHaveParent = bool()
            print('------------------------------------')
            for i in InstID_List:
                scene.select(i)
                test_mi_inst = modo.Item()
                # print(test_mi_inst)
                try :
                    test_inst_p = test_mi_inst.Parent()
                    # print(test_inst_p)
                    test_inst_p_ident = test_inst_p.Ident()
                    # print(test_inst_p_ident)
                    Inst_Parent_List.append(test_inst_p_ident)
                    InstHaveParent = True
                    print('current instance have parent: ', InstHaveParent)
                except:
                    test_inst_p_ident = "XXXXXXXXXXXXYYYYZZZZ"
                    Inst_Parent_List.append(test_inst_p_ident)
                    InstHaveParent = False
                    print('current instance have parent: ', InstHaveParent)
                State_InstanceParent.append(InstHaveParent)

            # print(Inst_Parent_List)
            # print(State_InstanceParent)
            # ------------------------------------- #
            # ------------------------------------- #


            if HaveParent:
                scene.select(ident)
                lx.eval('!item.parent parent:{} inPlace:1')
                lx.eval('smo.GC.DeselectAll')
                Presence_W_Loc = False

            if not HaveParent:
                # Need to create a World Locator to proceed the data.
                Presence_W_Loc = True
                lx.eval('smo.GC.DeselectAll')
                lx.eval('item.create locator applyDefaultPreset:true')
                lx.eval('item.name Wrld_Loc xfrmcore')
                world_item = modo.Item().Ident()
                scene.select(ident)
                scene.select(world_item, "add")
                lx.eval('item.parent inPlace:1')
                scene.select(ident)
                scene.select(instance_ident)
                scene.select(world_item, "add")
                lx.eval('item.parent inPlace:1')
                scene.select(ident)

            if lx.eval('workPlane.state ?'):
                lx.eval('workPlane.state false')
            RefSystemActive = bool()
            try:
                CurrentRefSystemItem = lx.eval('item.refSystem ?')
                # print(CurrentRefSystemItem)
            except:
                pass
            if CurrentRefSystemItem is not None:
                lx.eval('item.refSystem {}')

            for item in selected_Items:
                item = lx.object.Item(item)
                TargetID = item.Ident()
                TargetList.append(TargetID)
            # print(TargetList)

            scene.select(ident)
            selected_mesh = scene.selectedByType('mesh')[0]
            lx.eval('select.type polygon')
            for item in ComponentList:
                # print(item)
                if self.sel_mode == 1:
                    selected_mesh.geometry.vertices.select(item)
                if self.sel_mode == 2:
                    selected_mesh.geometry.edges.select(item)
                if self.sel_mode == 3:
                    selected_mesh.geometry.polygons.select(item)
            lx.eval('workPlane.fitGeometry')
            lx.eval('workPlane.fitSelect')
            WorldTargetCenterX = lx.eval('workplane.edit ? 0 0 0 0 0')
            WorldTargetCenterY = lx.eval('workplane.edit 0 ? 0 0 0 0')
            WorldTargetCenterZ = lx.eval('workplane.edit 0 0 ? 0 0 0')
            lx.eval('workPlane.state false')
            # lx.out('Workplane posX:', WorldTargetCenterX)
            # lx.out('Workplane posY:', WorldTargetCenterY)
            # lx.out('Workplane posZ:', WorldTargetCenterZ)
            lx.eval('workPlane.edit cenX:%f cenY:%f cenZ:%f rotX:0 rotY:0 rotZ:0' % (WorldTargetCenterX, WorldTargetCenterY, WorldTargetCenterZ))

            # Get the Offset position from the Item Relative Position
            scene.select(selected_Items)
            # print(len(selected_Items))
            # if (len(selected_Items)) == 1 :
            selected_mesh = scene.selected[0]  # gets the current selected object (throws an error if nothing is selected)
            Tar_WorldPos = selected_mesh.transforms.position.get()
            # lx.out(Tar_WorldPos)
            Tar_WorldRot = selected_mesh.transforms.rotation.get()
            # lx.out(Tar_WorldRot)
            lx.eval('item.refSystem %s' % TargetList[0])

            lx.eval('select.type polygon')
            lx.eval('workPlane.fitGeometry')
            lx.eval('workPlane.fitSelect')
            RelativeOffsetX = lx.eval('workplane.edit ? 0 0 0 0 0')
            RelativeOffsetY = lx.eval('workplane.edit 0 ? 0 0 0 0')
            RelativeOffsetZ = lx.eval('workplane.edit 0 0 ? 0 0 0')
            # lx.eval('workPlane.state false')
            # lx.out('Center Offset posX:', RelativeOffsetX)
            # lx.out('Center Offset posY:', RelativeOffsetY)
            # lx.out('Center Offset posZ:', RelativeOffsetZ)
            # lx.eval('workPlane.edit cenX:%f cenY:%f cenZ:%f rotX:0 rotY:0 rotZ:0' % (RelativeOffsetX, RelativeOffsetY, RelativeOffsetZ))

            RelativeOffsetPos = [float(), float(), float()]
            RelativeOffsetPos = [RelativeOffsetX, RelativeOffsetY, RelativeOffsetZ]
            # print(RelativeOffsetPos)

            NewPosX = (Tar_WorldPos[0] + RelativeOffsetPos[0])
            NewPosY = (Tar_WorldPos[1] + RelativeOffsetPos[1])
            NewPosZ = (Tar_WorldPos[2] + RelativeOffsetPos[2])
            # print([NewPosX, NewPosY, NewPosZ])

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
            # print(TargetXfrm)

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
            # print(Source_PosX)
            # print(Source_PosY)
            # print(Source_PosZ)

            # Drop channels selected.
            lx.eval('select.drop channel')

            lx.eval('select.itemInstances')

            SelItem = lxu.select.ItemSelection().current()
            # print(SelItem)

            # for item in TargetIDList:
            for item in SelItem:
                scene.select(item)
                item_name = item.UniqueName()
                ToProcessList.append(item_name)
            # print(ToProcessList)

            lx.eval('smo.GC.DeselectAll')

            iteration = -1
            for item in ToProcessList:
                iteration += 1
                scene.select(item)
                TargetItem = lx.eval1("query sceneservice selection ? locator")
                # print(TargetItem)
                chanRotX = lx.eval('transform.channel rot.X ?')
                # print(chanRotX)
                chanRotY = lx.eval('transform.channel rot.Y ?')
                # print(chanRotY)
                chanRotZ = lx.eval('transform.channel rot.Z ?')
                # print(chanRotZ)
                scene.select(item)

                if State_InstanceParent[iteration]:
                    lx.eval('!item.parent parent:{} inPlace:1')
                lx.eval('smo.GC.DeselectAll')

                lx.eval('item.create locator applyDefaultPreset:true')
                LocItem = lx.eval1("query sceneservice selection ? locator")
                # print(LocItem)
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
                # print(TargetXfrm)

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

            if HaveParent:
                scene.select(ident)
                scene.select(p_ident, "add")
                lx.eval('item.parent inPlace:1')
                lx.eval('smo.GC.DeselectAll')

                scene.select(ident)
                lx.eval('select.itemInstances')
                # scene.select(instance_ident)
                scene.select(p_ident, "add")
                lx.eval('item.parent inPlace:1')
                lx.eval('smo.GC.DeselectAll')

            if not HaveParent:
                scene.select(ident)
                # lx.eval('item.parent parent:{} inPlace:1')
                lx.eval('smo.GC.DeselectAll')

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

            if Presence_W_Loc:
                lx.eval('select.type item')
                scene.select(ident)
                lx.eval('!item.parent parent:{} inPlace:1')
                scene.select(world_item)
                lx.eval('!delete')


            ################################################
            ################################################
            # Parent instances back to their original parent
            # print(InstID_List)
            # print(Inst_Parent_List)
            # print(State_InstanceParent)
            inst_num = -1
            for i in InstID_List:
                inst_num += 1
                scene.select(i)
                # Check the state of Parent presence on original instances via "State_InstanceParent"
                if State_InstanceParent[inst_num]:
                    scene.select(Inst_Parent_List[inst_num], "add")
                    lx.eval('!item.parent inPlace:1')
            ################################################
            ################################################



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

        del instance_ident
        del TargetList
        del TotalInstancesList
        del CurrentRefSystemItem
        del (ToProcessList[:])
        del ComponentTuple
        del (ComponentList[:])
        del InstID_List
        del Inst_Parent_List
        del State_InstanceParent



lx.bless(SMO_GC_Setup_OffsetCenterPosPreserveInstancesPos_Cmd, Cmd_Name)

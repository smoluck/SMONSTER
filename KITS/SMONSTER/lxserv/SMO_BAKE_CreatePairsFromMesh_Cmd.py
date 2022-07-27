# python
# ---------------------------------------
# Name:         SMO_BAKE_CreatePairsFromMesh_Cmd.py
# Version:      1.0
#
# Purpose:      This script is designed to
#               Create a New Bake Pairs from a Single High Poly mesh and Enter into Polygon Editing To Reduce the Mesh Detail
#
#
# Author:       Franck ELISABETH (with the help of Tom Dymond for debug)
# Website:      http://www.smoluck.com
#
# Created:      02/04/2021
# Copyright:    (c) Franck Elisabeth 2017-2022
# ---------------------------------------

import lx, lxu, modo

Cmd_Name = "smo.BAKE.CreatePairsFromMesh"
# smo.BAKE.CreatePairsFromMesh

class SMO_BAKE_CreatePairsFromMesh_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)

    def cmd_Flags(self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO

    def cmd_Interact(self):
        pass

    def cmd_UserName(self):
        return 'SMO BAKE - Create Bake Pairs from Mesh'

    def cmd_Desc(self):
        return 'Create a New Bake Pairs from a Single High Poly mesh and Enter into Polygon Editing To Reduce the Mesh Detail.'

    def cmd_Tooltip(self):
        return 'Create a New Bake Pairs from a Single High Poly mesh and Enter into Polygon Editing To Reduce the Mesh Detail.'

    def cmd_Help(self):
        return 'https://twitter.com/sm0luck'

    def basic_ButtonName(self):
        return 'SMO BAKE - Create Bake Pairs from Mesh'

    def basic_Enable(self, msg):
        return True

    def basic_Execute(self, msg, flags):
        scene = modo.scene.current()
        LowItem = lxu.select.ItemSelection().current()
        TCount = len(LowItem)

        # Get the default Vertex Normal Map Name from User Preferences
        VNMapName = lx.eval('pref.value application.defaultVertexNormals ?')
        # print(VNMapName)

        CreateTransferVertexNormalMapOnLowWhenCreateBakePairsFromHigh = lx.eval('user.value SMO_UseVal_BAKE_CreateTransferVertexNormalMapOnLowWhenCreateBakePairsFromHigh ?')
        DeleteVertexNormalMapOnLowWhenCreateBakePairsFromHigh = lx.eval('user.value SMO_UseVal_BAKE_DeleteVertexNormalMapOnLowWhenCreateBakePairsFromHigh ?')
        RefSystemWhenCreateBakePairsFromHigh = lx.eval('user.value SMO_UseVal_BAKE_RefSystemWhenCreateBakePairsFromHigh ?')
        IsolateInViewportWhenCreateBakePairsFromHigh = lx.eval('user.value SMO_UseVal_BAKE_IsolateInViewportWhenCreateBakePairsFromHigh ?')
        AutoHide_Set_BakePairs = lx.eval('user.value SMO_UseVal_BAKE_AutoHideWhenSetBakePairs ?')

        TargetIDList = []
        TargetNameList = []
        VertNrnMapList = []
        LowVertNrnMapList = []

        # Loop through the selected items in the scene and get only meshes.
        for item in LowItem:
            itemType = modo.Item(item).type
            item = lx.object.Item(item)
            item_name = item.UniqueName()
            if itemType != "mesh":
                scene.deselect(item_name)

        TCount = len(lxu.select.ItemSelection().current())
        if TCount == 1:
            lx.eval('item.duplicate false all:true')
            HighItem = lxu.select.ItemSelection().current()
            for item in HighItem:
                HighItemID = item.Ident()
            for item in LowItem:
                LowItemID = item.Ident()
            scene.select(LowItem)

            if CreateTransferVertexNormalMapOnLowWhenCreateBakePairsFromHigh == True :
                # Vertex Nornmal Map (From CAD) Detection on HighPoly.
                meshUpdateVNMap = modo.Mesh()
                VMaps = meshUpdateVNMap.geometry.vmaps
                # print(VMaps)
                VMapCount = len(meshUpdateVNMap.geometry.vmaps)
                # print(VMapCount)
                if VMapCount > 0:
                    for map in VMaps:
                        mapObj = lx.object.MeshMap(map)
                        # print(mapObj.Name())
                        # print(mapObj.Type())
                        if mapObj.Type() == 1313821261:  # int id for Vertex Normal map
                            lx.eval("select.vertexMap {%s} norm mode:remove" % mapObj.Name())
                            lx.eval("select.vertexMap {%s} norm mode:add" % mapObj.Name())
                            CurrentVertexNormalMapName = mapObj.Name()
                            # print(CurrentVertexNormalMapName)
                            VertNrnMapList.append(CurrentVertexNormalMapName)

                            # Vertex Nornmal Map Detected. Delete it.
                            if CurrentVertexNormalMapName is not None:
                                if CurrentVertexNormalMapName != VNMapName:
                                    try:
                                        lx.eval('select.vertexMap "{%s}" norm replace' % CurrentVertexNormalMapName)
                                        lx.eval('vertMap.name {%s} norm active' % VNMapName)
                                        # lx.eval('!vertMap.delete norm')
                                        # lx.eval('vertMap.new name:"Vertex Normal" type:norm init:false')
                                    except:
                                        pass
                # # Create an empty VertexNormalMap if there is no Vertex Normals on Original HighPoly Mesh Source
                # if len(VertNrnMapList) == 0:
                #     lx.eval('vertMap.new name:{%s} type:norm init:false' % VNMapName)

            lx.eval('select.item %s add' % HighItemID)
            lx.eval('smo.BAKE.SetBakePairs')

            if AutoHide_Set_BakePairs == True :
                lx.eval('unhide')

            scene.select(LowItem)
            if DeleteVertexNormalMapOnLowWhenCreateBakePairsFromHigh == True:
                # Vertex Nornmal Map (From CAD) Detection on HighPoly.
                LowmeshUpdateVNMap = modo.Mesh()
                LowVMaps = LowmeshUpdateVNMap.geometry.vmaps
                print(LowVMaps)
                LowVMapCount = len(LowmeshUpdateVNMap.geometry.vmaps)
                print(LowVMapCount)
                if LowVMapCount > 0:
                    for map in LowVMaps:
                        mapObj = lx.object.MeshMap(map)
                        # print(mapObj.Name())
                        # print(mapObj.Type())
                        if mapObj.Type() == 1313821261:  # int id for Vertex Normal map
                            lx.eval("select.vertexMap {%s} norm mode:remove" % mapObj.Name())
                            lx.eval("select.vertexMap {%s} norm mode:add" % mapObj.Name())
                            LowVertexNormalMapName = mapObj.Name()
                            # print(LowVertexNormalMapName)
                            LowVertNrnMapList.append(LowVertexNormalMapName)
                            # Vertex Nornmal Map Detected. Delete it.
                            if LowVertexNormalMapName is not None:
                                try:
                                    lx.eval('select.vertexMap "{%s}" norm replace' % LowVertexNormalMapName)
                                    lx.eval('vertMap.name {%s} norm active' % VNMapName)
                                    lx.eval('!vertMap.delete norm')
                                except:
                                    pass

            if IsolateInViewportWhenCreateBakePairsFromHigh == True :
                lx.eval('hide.unsel')
            if RefSystemWhenCreateBakePairsFromHigh == True :
                lx.eval('item.refSystem %s' % LowItemID)
                lx.eval('select.type polygon')
                lx.eval('viewport.fitSelected')


lx.bless(SMO_BAKE_CreatePairsFromMesh_Cmd, Cmd_Name)

# python
# ---------------------------------------
# Name:         SMO_BAKE_CreateAndOrSelectCAGEMorph_Cmd.py
# Version:      1.0
#
# Purpose:      This Command is designed to :
#               Check if CAGE Map exist on current Mesh. If not, create a new MorphMap, then Select that CAGE Morph.
#
# Author:       Franck ELISABETH
# Website:      http://www.smoluck.com
#
# Modified:     07/04/2021
# Copyright:    (c) Franck Elisabeth 2017-2022
# ---------------------------------------

import modo, lx, lxu

Cmd_Name = "smo.BAKE.CreateAndOrSelectCAGEMorph"
# smo.BAKE.CreateAndOrSelectCAGEMorph

class SMO_BAKE_CreateAndOrSelectCAGEMorph_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)

    def cmd_Interact(self):
        pass

    def cmd_UserName(self):
        return 'SMO BAKE - Create CAGE Morph'

    def cmd_Desc(self):
        return 'Check if CAGE Map exist on current Mesh. If not, create a new MorphMap, then Select that CAGE Morph.'

    def cmd_Tooltip(self):
        return 'Check if CAGE Map exist on current Mesh. If not, create a new MorphMap, then Select that CAGE Morph.'

    def cmd_Help(self):
        return 'https://twitter.com/sm0luck'

    def basic_ButtonName(self):
        return 'SMO BAKE - Create CAGE Morph'

    def cmd_Flags(self):
        return lx.symbol.fCMD_UNDO

    def basic_Enable(self, msg):
        return True

    def basic_Execute(self, msg, flags):
        scene = modo.scene.current()
        lx.eval('smo.GC.DeselectAll')
        # Create Selection Set from Tags to temporary select Lowpoly, Cage or HighPoly meshes to export them.
        lx.eval('smo.GC.CreateDeleteSelSetFromMTypTag 1')
        # Select Cage meshes via Tags
        lx.eval('smo.GC.SelectMTypMesh 0')

        MeshItemList = list(scene.selectedByType("mesh"))
        # print(MeshItemList)
        # print(MeshItemCount)

        # Store the current Selected Mesh Items. As well as their ID and Names.
        MeshNameList = []
        MeshIDList = []
        MissingCAGEMeshList = []
        MissingCAGEMeshIDList = []
        MissingCAGEState = False
        for i in MeshItemList:
            MeshName = i.name
            MeshID = i.id
            # print(MeshName)
            # print(MeshID)
            MeshNameList.append(MeshName)
            MeshIDList.append(MeshID)
        # print(MeshNameList)
        # print(MeshIDList)

        # store all the current Morph Maps in a List.
        # MorphMapList = []
        # MorphMapName = []
        # for mesh in MeshItemList:
        #     mesh.select(True)
        #     lx.eval('smo.GC.ClearSelectionVmap 3 1')
        #     for map in mesh.geometry.vmaps:
        #         mapObj = lx.object.MeshMap(map)
        #         # print(mapObj.Name())
        #         # print(mapObj.Type())
        #         if mapObj.Type() == 1297044038:  # int id for Morph map
        #             MorphMapName = (mapObj.Name())
        #             MorphMapList.append(MorphMapName)
        # lx.eval('smo.GC.DeselectAll')
        # print(MorphMapList)
        # print(MorphMapName)

        # Test if a CAGE Morph map exist. If yes: select it. Else: Create it
        for mesh in MeshItemList:
            mesh.select(True)
            lx.eval('smo.GC.ClearSelectionVmap 3 1')
            for map in mesh.geometry.vmaps:
                mapObj = lx.object.MeshMap(map)
                if mapObj.Type() == 1297044038:  # int id for Morph map
                    MorphMapName = (mapObj.Name())
            if MorphMapName == 'CAGE':
                lx.eval('select.vertexMap CAGE morf replace')
            else:
                lx.eval('vertMap.new CAGE morf true {0.78 0.78 0.78} 1.0')
                lx.eval('smo.CB.ItemColor 2 2')
                MissingCAGEState = True
                MissingCAGEMesh = scene.selectedByType("mesh")[0]
                MissingCAGEMeshList.append(MissingCAGEMesh)
        lx.eval('smo.GC.DeselectAll')

        # CLear Selection Set based on Mesh MTyp Tags
        lx.eval('smo.GC.CreateDeleteSelSetFromMTypTag 0')

        if MissingCAGEState == False:
            scene.select(MeshItemList)
            # Old and Long Method to select Item by List
            # MeshItemCount = len(MeshItemList)
            # for i in range(MeshItemCount):
            #     lx.eval('select.subItem %s add mesh 0 0' % MeshIDList[i])

        if MissingCAGEState == True:
            # print(MissingCAGEMeshList)
            scene.select(MissingCAGEMeshList)


    def cmd_Query(self, index, vaQuery):
        lx.notimpl()


lx.bless(SMO_BAKE_CreateAndOrSelectCAGEMorph_Cmd, Cmd_Name)

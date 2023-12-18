# python
"""
Name:         SMO_BAKE_CheckAndFixCAGEMorphMapsPresence_Cmd.py

Purpose:      This Command is designed to:
              Check if CAGE Map exist on current Mesh. If not, create a new MorphMap, then Select that CAGE Morph.

Author:       Franck ELISABETH
Website:      https://www.linkedin.com/in/smoluck/
Modified:     07/04/2021
Copyright:    (c) Franck Elisabeth 2017-2022
"""

import lx
import lxu
import modo

Cmd_Name = "smo.BAKE.CheckAndFixCAGEMorphMapsPresence"

# OLD NAME OF THAT COMMAND: smo.BAKE.CreateAndOrSelectCAGEMorph
# smo.BAKE.CheckAndFixCAGEMorphMapsPresence


class SMO_BAKE_CheckAndFixCAGEMorphMapsPresence_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)

    def cmd_Interact(self):
        pass

    def cmd_UserName(self):
        return 'SMO BAKE - CheckAndFixCAGEMorphMapsPresence'

    def cmd_Desc(self):
        return 'Check if CAGE Map exist on current Mesh. If not, create that "Cage" MorphMap, then Select those meshes and that "CAGE" Morph.'

    def cmd_Tooltip(self):
        return 'Check if CAGE Map exist on current Mesh. If not, create that "Cage" MorphMap, then Select those meshes and that "CAGE" Morph.'

    def cmd_Help(self):
        return 'https://twitter.com/sm0luck'

    def basic_ButtonName(self):
        return 'SMO BAKE - CheckAndFixCAGEMorphMapsPresence'

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
        TroubleMeshList = []
        MissingCAGEMeshIDList = []
        MissingCAGEState = False
        for i in MeshItemList:
            MeshName = i.name
            MeshID = i.id
            # print(MeshName)
            # print(MeshID)
            MeshNameList.append(MeshName)
            MeshIDList.append(MeshID)
        # print("Selected Mesh Names:", MeshNameList)
        # print("Selected Mesh ID:", MeshIDList)

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

        MorphMapName = []
        MissingCAGEState = bool()
        MM_MatchCount = 0
        # Test if a CAGE Morph map exist. If yes: select it. Else: Create it
        for mesh in MeshItemList:
            mesh.select(True)
            lx.eval('smo.GC.ClearSelectionVmap 3 1')
            for map in mesh.geometry.vmaps:
                mapObj = lx.object.MeshMap(map)
                if mapObj.Type() == 1297044038:  # int id for Morph map
                    MorphMapName.append(mapObj.Name())
                    # print(MorphMapName)
            # print(MorphMapName)
            if len(MorphMapName) == 0:
                print('MophMap "CAGE" Missing')
                lx.eval('vertMap.new CAGE morf true {0.78 0.78 0.78} 1.0')
                lx.eval('smo.CB.ItemColor 1 0')
                print('MophMap "CAGE" Created')
                MissingCAGEState = True
                lx.eval('select.vertexMap CAGE morf replace')
                MorphMapName.append("CAGE")
                MissingCAGEMesh = scene.selectedByType("mesh")[0]
                TroubleMeshList.append(MissingCAGEMesh)
                MM_MatchCount += 1
                MissingCAGEState = True
                if MissingCAGEState:
                    # print(MissingCAGEMeshList)
                    scene.select(MissingCAGEMesh)
                    lx.eval('smo.CB.ItemColor 2 0')
                    lx.eval('select.vertexMap CAGE morf replace')
            else:
                print('MophMaps are present')
                for mm in MorphMapName:
                    if mm != 'CAGE':
                        # print('MophMap Present but not equal to "CAGE"')
                        MissingCAGEState = True
                    if mm == 'CAGE':
                        MissingCAGEState = False
                        MM_MatchCount += 1
                        # print('MophMap "CAGE" Present')
                if MM_MatchCount == 0:
                    print('MophMap "CAGE" Missing')
                    lx.eval('smo.CB.ItemColor 2 0')
                    print('MophMap "CAGE" Created')
                    MissingCAGEState = True
                    lx.eval('vertMap.new CAGE morf true {0.78 0.78 0.78} 1.0')
                    lx.eval('select.vertexMap CAGE morf replace')
                    # print('MophMap "CAGE" have been created and selected')
                    MissingCAGEMesh = scene.selectedByType("mesh")[0]
                    TroubleMeshList.append(MissingCAGEMesh)
                    MM_MatchCount += 1
                MM_MatchCount = 0
            del MorphMapName[:]

            # print('Matching "CAGE" Morph map count:', MM_MatchCount)
            if MM_MatchCount > 0 and not MissingCAGEState:
                lx.eval('smo.CB.ItemColor 8 0')
                MissingCAGEState = False
                print('MophMap "CAGE" Present')

        lx.eval('smo.GC.DeselectAll')
        # CLear Selection Set based on Mesh MTyp Tags
        lx.eval('smo.GC.CreateDeleteSelSetFromMTypTag 0')

        if len(TroubleMeshList) > 0:
            # print(MissingCAGEMeshList)
            print('MophMap "CAGE" have been created and selected')
            scene.select(TroubleMeshList)
            lx.eval('select.vertexMap CAGE morf replace')
            lx.eval('dialog.setup info')
            lx.eval('dialog.title {SMO BAKE - Check CAGE Morph:}')
            lx.eval('dialog.msg {"MophMap "CAGE" have been created on selected meshes. Modify and Update that new "CAGE" Morph to match requirements.}')
            lx.eval('+dialog.open')

        if len(TroubleMeshList) == 0:
            scene.select(MeshItemList)
            lx.eval('smo.CB.ItemColor 8 0')
            lx.eval('smo.GC.DeselectAll')

    def cmd_Query(self, index, vaQuery):
        lx.notimpl()


lx.bless(SMO_BAKE_CheckAndFixCAGEMorphMapsPresence_Cmd, Cmd_Name)

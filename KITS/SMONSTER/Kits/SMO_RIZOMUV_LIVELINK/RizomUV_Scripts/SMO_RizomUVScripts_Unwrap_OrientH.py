# python
"""
Name:           SMO_RizomUVScripts_Unwrap_OrientH.py

Purpose:        This Command is designed to:
                Cut Selection of Polygons and Unwrap them and Orient them horizontally,
                Assign Initial Orientation Horiz and Step Angle to 90 degree
                Then Hide those recently unwrapped polygons

Author:         Franck ELISABETH
Website:        https://www.linkedin.com/in/smoluck/
Created:        31/12/2022
Copyright:      (c) Franck Elisabeth 2017-2022
"""

from rizomuv import App as riz
for item in dir(riz):
    print(item)
print("-----------------")
for item in dir(riz.Get):
    print(item)


PolyIDLst = riz.Get({'PrimType':"Polygon", 'WorkingSet':"Visible", 'IslandGroupMode':"Group", 'ResetBefore':True, 'Select':True, 'XYZSpace':True, 'Path':"IDs", 'List':True})


# Get current selection Mode: 0=Vertex 1=Edge 2=Polygon 3=Island
selmode = (riz.Get("Vars.EditMode.ElementMode"))
# print(type(selmode))
# print(selmode)
if selmode == 2:
    print("Selection Mode: Polygon")
    AllPolyIDList = (riz.Get("Lib.Mesh.ObjectsPolyIDs"))


# Cut Selected Polygons, Unfold them, Set Step Angle, Pack all
if selmode == 2:
    riz.Cut({'PrimType': "Polygon", 'WorkingSet': "Visible&UnLocked"})
    riz.Unfold({'PrimType': "Polygon", 'WorkingSet': "Visible&UnLocked", 'Mix': 1, 'RoomSpace': 0, 'MinAngle': 1e-05, 'PreIterations': 5, 'StopIfOutOFDomain': False, 'PinMapName': "Pin"})
    riz.Deform({'WorkingSet': "Visible&UnLocked", 'PrimType': "Polygon", 'Rotation': 0, 'Geometrical': "AlignIslandToSelection"})
    riz.IslandGroups({'Mode': "SetGroupsProperties", 'WorkingSet': "Visible", 'GroupPaths': ["RootGroup"], 'Properties': {'Pack': {'Rotate': {'Mode': 0}}}})
    riz.IslandGroups({'Mode': "SetGroupsProperties", 'WorkingSet': "Visible", 'GroupPaths': ["RootGroup"], 'Properties': {'Pack': {'Rotate': {'Step': 90}}}})

    riz.Hide({'PrimType':"Polygon", 'Isolate':True, 'UseList':[], 'Deselect':False})







# Analyze all Islands on Mesh, then hide only Selected Islands
IslandIDList = riz.ItemNames("Lib.Mesh.Islands")
print(IslandIDList)
SelIsland = []

index = 0
for item in range(0, len(IslandIDList)):
    print(item)
for item in IslandIDList:
    isSelected = riz.Get("Lib.Mesh.Islands." + item + ".Properties.Selected")
    # print("Island ID:", item, "selected status:", isSelected)
    print(isSelected)
    if isSelected:
        print("Islands ID " + item + " is selected")
        SelIsland.append(item)
print("Current selected Islands ", SelIsland)
if len(SelIsland) >= 1:
    for m in SelIsland:
        riz.Hide({'PrimType': "Island", 'Hide': True, 'UseList': [m], 'Deselect': True})


riz.Pack({'RootGroup': "RootGroup", 'WorkingSet': "Visible", 'ProcessTileSelection': False, 'RecursionDepth': 1, 'Translate': True, 'AuxGroup': "RootGroup", 'LayoutScalingMode': 0})
















































# Get current selection Mode: 0=Vertex 1=Edge 2=Polygon 3=Island
selmode = (App.Get("Vars.EditMode.ElementMode"))
# print(type(selmode))
# print(selmode)
if selmode == 2:
    print("Selection Mode: Polygon")

# Cut Selected Polygons, Unfold them, Set Step Angle, Pack all
if selmode == 2:
    App.Cut({'PrimType': "Polygon", 'WorkingSet': "Visible&UnLocked"})
    App.Unfold({'PrimType': "Polygon", 'WorkingSet': "Visible&UnLocked", 'Mix': 1, 'RoomSpace': 0, 'MinAngle': 1e-05, 'PreIterations': 5, 'StopIfOutOFDomain': False, 'PinMapName': "Pin"})
    App.Deform({'WorkingSet': "Visible&UnLocked", 'PrimType': "Polygon", 'Rotation': 0, 'Geometrical': "AlignIslandToSelection"})
    App.IslandGroups({'Mode': "SetGroupsProperties", 'WorkingSet': "Visible", 'GroupPaths': ["RootGroup"], 'Properties': {'Pack': {'Rotate': {'Mode': 0}}}})
    App.IslandGroups({'Mode': "SetGroupsProperties", 'WorkingSet': "Visible", 'GroupPaths': ["RootGroup"], 'Properties': {'Pack': {'Rotate': {'Step': 90}}}})
    App.Pack({'RootGroup': "RootGroup", 'WorkingSet': "Visible", 'ProcessTileSelection': False, 'RecursionDepth': 1, 'Translate': True, 'AuxGroup': "RootGroup", 'LayoutScalingMode': 0})

App.Set({'Path': "Vars.EditMode.ElementMode", 'Value': 3})
App.Select({'PrimType': "Island", 'WorkingSet': "Visible", 'IslandGroupMode': "Group", 'Select': True, 'All': True})

IslandIDList = App.ItemNames("Lib.Mesh.Islands")
SelIsland = []
print(SelIsland)

PolyIDList = (App.Get("Lib.Mesh.PolygonVertIDs"))
print(PolyIDList)
AllPolyIDList = (App.Get("Lib.Mesh.ObjectsPolyIDs"))
PolyIDList = list(set(PolyIDList))
AllPolyIDListN = []
for i in AllPolyIDList:
    if i not in AllPolyIDListN:
        AllPolyIDList.append(i)
print(AllPolyIDListN)

print(type(AllPolyIDList))
print(type(AllPolyIDList[0]))
print("-----------")
for item in AllPolyIDList:
    print(item)
print(AllPolyIDList)
print("first polygon")
print(AllPolyIDList[0])


def SMO_SmartUnwrapOrient(Direction):
    # Get current selection Mode: 0=Vertex 1=Edge 2=Polygon 3=Island
    selmode = str(App.Get("Vars.EditMode.ElementMode"))
    print(selmode)

    # Cut Selected Polygons, Unfold them, Set Step Angle, Pack all
    if selmode == 2:
        App.Cut({'PrimType': "Polygon", 'WorkingSet': "Visible&UnLocked"})
        App.Unfold(
            {'PrimType': "Polygon", 'WorkingSet': "Visible&UnLocked", 'Mix': 1, 'RoomSpace': 0, 'MinAngle': 1e-05,
             'PreIterations': 5, 'StopIfOutOFDomain': False, 'PinMapName': "Pin", 'ProcessSelection': True})
        App.Deform({'WorkingSet': "Visible&UnLocked", 'PrimType': "Polygon", 'Rotation': 0,
                    'Geometrical': "AlignIslandToSelection"})
        App.IslandGroups({'Mode': "SetGroupsProperties", 'WorkingSet': "Visible", 'GroupPaths': ["RootGroup"],
                          'Properties': {'Pack': {'Rotate': {'Step': 90}}}})
        App.IslandGroups({'Mode': "SetGroupsProperties", 'WorkingSet': "Visible", 'GroupPaths': ["RootGroup"],
                          'Properties': {'Pack': {'Rotate': {'Mode': 1}}}})
        App.Pack({'RootGroup': "RootGroup", 'WorkingSet': "Visible", 'ProcessTileSelection': False, 'RecursionDepth': 1,
                  'Translate': True, 'AuxGroup': "RootGroup", 'LayoutScalingMode': 0})

    # Switch to Island Mode (Why do we loose current poly/island selection when changing selection mode ?)
    App.Set({'Path': "Vars.EditMode.ElementMode", 'Value': 3})

    # Analyze all Islands on Mesh, then hide only Selected Islands
    IslandIDList = App.ItemNames("Lib.Mesh.Islands")
    SelIsland = []

    for item in IslandIDList:
        isSelected = App.Get("Lib.Mesh.Islands." + item + ".Properties.Selected")
        # print(isSelected)
        if isSelected:
            print("Islands ID " + item + " is selected")
            SelIsland.append(item)
    print("Current selected Islands ", SelIsland)
    if len(SelIsland) >= 1:
        for m in SelIsland:
            App.Hide({'PrimType': "Island", 'Hide': True, 'UseList': [m], 'Deselect': True})

    """
    itemNames=App.ItemNames("Lib.Mesh.Islands")
    
    area3D = 0
    areaUV = 0
    
    for itemName in itemNames:
        isSelected = App.Get("Lib.Mesh.Islands." + itemName + ".Properties.Selected")
        print(isSelected)
        if isSelected:
            print("Island " + item + " is selected")
            areaUV = areaUV + App.Eval("Lib.Mesh.Islands." + itemName + ".GetAreaUVW")
            area3D = area3D + App.Eval("Lib.Mesh.Islands." + itemName + ".GetAreaXYZ")
    
    print("Total Selected 3D Area: " + str(area3D))
    print("Total Selected UV Area: " + str(areaUV))
    """

    """
    PolyIDList=App.ItemNames("Lib.Mesh.Islands")
    SelPoly = []
    
    for item in PolyIDList:
        isSelected = App.Get("Lib.Mesh.Islands." + item + ".Properties.Selected")
        # print(isSelected)
        if isSelected:
            print("Islands " + item + " is selected")
            SelPoly.append(item)
    print(SelPoly)
    """

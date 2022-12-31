# python
"""
Name:           SMO_RizomUVScripts_Unwrap_OrientH.py

Purpose:        This Command is designed to:
                Cut Selection of Polygons and Unwrap them and Orient them horizontaly,
                Assign Initial Orientation Horiz and Step Angle to 90 degree
                Then Hide those recently unwrapped polygons

Author:         Franck ELISABETH
Website:        https://www.smoluck.com
Created:        31/12/2022
Copyright:      (c) Franck Elisabeth 2017-2022
"""

# Get current selection Mode: 0=Vertex 1=Edge 2=Polygon 3=Island
selmode = str(App.Get("Vars.EditMode.ElementMode"))
print(selmode)

# Cut Selected Polygons, Unfold them, Set Step Angle, Pack all
if selmode == 2:
    App.Cut({'PrimType':"Polygon", 'WorkingSet':"Visible&UnLocked"})
    App.Unfold({'PrimType':"Polygon", 'WorkingSet':"Visible&UnLocked", 'Mix':1, 'RoomSpace':0, 'MinAngle':1e-05, 'PreIterations':5, 'StopIfOutOFDomain':False, 'PinMapName':"Pin", 'ProcessSelection':True})
    App.Deform({'WorkingSet':"Visible&UnLocked", 'PrimType':"Polygon", 'Rotation':0, 'Geometrical':"AlignIslandToSelection"})
    App.IslandGroups({'Mode':"SetGroupsProperties", 'WorkingSet':"Visible", 'GroupPaths':["RootGroup" ], 'Properties':{'Pack':{'Rotate':{'Step':90}}}})
    App.IslandGroups({'Mode':"SetGroupsProperties", 'WorkingSet':"Visible", 'GroupPaths':["RootGroup" ], 'Properties':{'Pack':{'Rotate':{'Mode':1}}}})
    App.Pack({'RootGroup':"RootGroup", 'WorkingSet':"Visible", 'ProcessTileSelection':False, 'RecursionDepth':1, 'Translate':True, 'AuxGroup':"RootGroup", 'LayoutScalingMode':0})

# Switch to Island Mode (Why do we loose current poly/island selection when changing selection mode ?)
App.Set({'Path':"Vars.EditMode.ElementMode", 'Value':3})


# Analyze all Islanf on Mesh to hide only Selected Islands
IslandIDList=App.ItemNames("Lib.Mesh.Islands")
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
        App.Hide({'PrimType':"Island", 'Hide':True, 'UseList':[m], 'Deselect':True})




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


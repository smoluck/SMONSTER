# python
# Switch to Vertex Selection Mode
# App.Set({'Path':"Vars.EditMode.ElementMode", 'Value':0})
# Switch to Edges Selection Mode
# App.Set({'Path':"Vars.EditMode.ElementMode", 'Value':1})

# Switch to Polygon Selection Mode
App.Set({'Path':"Vars.EditMode.ElementMode", 'Value':2})

# Enable the MagicWand
App.Set({'Path':"Prefs.PolygonMagicWand.MaxGlobalAngleEnable", 'Value':True})
App.Set({'Path':"Prefs.PolygonMagicWand.MaxGlobalAngle", 'Value':2})


App.Select({'PrimType':"Polygon", 'WorkingSet':"Visible", 'IslandGroupMode':"Group", 'ResetBefore':True, 'Select':True, 'XYZSpace':True, 'PolyArea':{'AbsoluteAngle':20, 'SmoothMix':0, 'SmoothIterations':2, 'MaxGapSize':0}, 'IDs':[1156], 'List':True})

# Cut selected Polygons
App.Cut({'PrimType':"Polygon", 'WorkingSet':"Visible&UnLocked"})

# Unfold selected
App.Unfold({'PrimType':"Polygon", 'WorkingSet':"Visible&UnLocked", 'Mix':1, 'RoomSpace':0, 'MinAngle':1e-05, 'PreIterations':5, 'StopIfOutOFDomain':False, 'PinMapName':"Pin", 'ProcessSelection':True})

# Orient Horizontaly
App.Deform({'WorkingSet':"Visible&UnLocked", 'PrimType':"Polygon", 'Rotation':0, 'Geometrical':"AlignIslandToSelection"})


App.Hide({'PrimType':"Polygon", 'Hide':True, 'UseList':[], 'Deselect':True})
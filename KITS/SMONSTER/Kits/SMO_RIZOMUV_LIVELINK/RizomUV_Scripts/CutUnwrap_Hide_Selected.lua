App.Cut({'PrimType':"Polygon", 'WorkingSet':"Visible&UnLocked"})
App.Unfold({'PrimType':"Polygon", 'WorkingSet':"Visible&UnLocked", 'StopIfZeroMix':False, 'Mix':1, 'RoomSpace':0, 'MinAngle':1e-05, 'PreIterations':5, 'StopIfOutOFDomain':False, 'PinMapName':"Pin", 'ProcessSelection':True, 'Iterations':1})
App.Deform({'WorkingSet':"Visible&UnLocked", 'PrimType':"Polygon", 'Rotation':0, 'Geometrical':"AlignIslandToSelection"})
App.Hide({'PrimType':"Island", 'Hide':True, 'UseList':[], 'Deselect':True})
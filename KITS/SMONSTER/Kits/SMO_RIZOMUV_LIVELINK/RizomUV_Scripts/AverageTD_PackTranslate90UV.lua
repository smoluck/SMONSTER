---
--- Created by Franck Elisabeth.
---

-- Set Packing Resolution to 4096 pixel
ZomSet({Path="Prefs.PackOptions.MapResolution", Value=4096})

ZomSet({Path="Prefs.UI.Display.IslandProperties", Value=true})

-- Set the Mutation count to 32
ZomIslandGroups({Mode="SetGroupsProperties", WorkingSet="Visible", MergingPolicyString="A_ADD|AIB_ADD_A_VALUE_B|B_CLONE", GroupPaths={ "RootGroup" }, Properties={Pack={MaxMutations=32}}})

-- Set The Pack Rotation angle to 90 degrees
ZomSet({Path="Vars.EditMode.ElementMode", Value=3})
ZomSelect({PrimType="Island", WorkingSet="Visible", IslandGroupMode="Group", Select=true, All=true})
ZomIslandProperties({MergingPolicyString="A_ADD|AIB_ADD_A_VALUE_B|B_CLONE", IslandIDs={ 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106}, Properties={Pack={Rotate={Step=90}}}})
ZomIslandGroups({Mode="SetGroupsProperties", WorkingSet="Visible", MergingPolicyString="A_ADD|AIB_ADD_A_VALUE_B|B_CLONE", GroupPaths={ }, Properties={Pack={Rotate={Step=90}}}})
ZomSelect({PrimType="Island", WorkingSet="Visible", IslandGroupMode="Group", DeSelect=true, All=true})

-- Launch the Packing Process
ZomPack({RootGroup="RootGroup", WorkingSet="Visible", ProcessTileSelection=false, RecursionDepth=1, Translate=true, AuxGroup="RootGroup", LayoutScalingMode=2, Rotate={Mode=0, Step=0, Min=0, Max=0}, Scaling={Mode=0, Steps=0}})

-- Save the FBX
ZomSave({File={Path="C:/TEMP/SMO_RizomUVLiveLink/RizomUV_DATA.fbx", UVWProps=true}})

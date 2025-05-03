# python

App.Uvset({'Mode': "SetCurrent", 'Name': "LM"})
App.Select({'PrimType': "Island", 'WorkingSet': "Visible", 'IslandGroupMode': "Group", 'ResetBefore': True, 'Select': True})
App.IslandGroups({'Mode': "SetGroupsProperties", 'WorkingSet': "Visible", 'GroupPath': "RootGroup", 'Properties': {'Pack': {'Scaling': {'TexelDensity': 200}}}})
App.Select({'PrimType': "Island", 'WorkingSet': "Visible", 'IslandGroupMode': "Group", 'Select': True, 'All': True})


def list_IslandID():
    ################# List All IDs
    IslandID_s_List = App.ItemNames("Lib.Mesh.Islands")
    print("All Island IDs:")
    print("-------------")
    print(IslandID_s_List)
    print(type(IslandID_s_List))
    print(type(IslandID_s_List[0]))
    print("---- this list should be integer but it's string -----")
    print("-------------")

    IslandID_i_List = []
    for item in IslandID_s_List:
        IslandID_i_List.append(int(item))
    print(IslandID_i_List)
    print(type(IslandID_i_List))
    print(type(IslandID_i_List[0]))
    #################

    ################# In All IDs List , check what is selected
    # query ID for each selected Islands
    # it print a lot of data on each App.Get
    SelIsland = []
    for item in IslandID_s_List:
        isSelected = App.Get("Lib.Mesh.Islands." + item + ".Properties.Selected")
        # print(isSelected)
        SelIsland.append(int(item))
    print("-------------")
    print(SelIsland)
    #################
    return SelIsland


list_IslandID()

uvlist = list_IslandID()
for i in (list_IslandID()):
    uvlist.append(i)

print(uvlist)

App.IslandProperties({'IslandIDs': (list_IslandID()), 'Properties': {'Pack': {'Rotate': {'Step': 90}}}})
App.IslandProperties({'IslandIDs': (list_IslandID()), 'Properties': {'Pack': {'Rotate': {'Mode': 1}}}})
App.Deform({'WorkingSet': "Visible&UnLocked", 'PrimType': "Island", 'ResetIslandScale': True, 'CenterMode': "MultiBBox", 'IDs': list_IslandID(), 'Transform': [0.000976562, 0, 0, 0, 0.000976562, 0, 0, 0, 1]})
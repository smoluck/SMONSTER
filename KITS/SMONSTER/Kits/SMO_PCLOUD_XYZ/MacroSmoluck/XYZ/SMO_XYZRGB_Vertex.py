# python
"""
Name:               SMO_XYZRGB_Vertex.py

Purpose:            This Script is designed to:
                    Open a txt file (Target) and create
                    Vertex at current position defined by the target File (3 first float value
                    (separated by a coma)) and set the vertex color value defined by 4th to 6th
                    float in line> Each line is a new Vertex

Author:             Franck ELISABETH
Website:            https://www.linkedin.com/in/smoluck/
Created:            29/11/2019
Copyright:          (c) Franck Elisabeth 2017-2022
"""

import lx
import lxu

# Get current scene
scene = lxu.select.SceneSelection().current()

# Create new mesh item
scene_service = lx.service.Scene()
mesh_type = scene_service.ItemTypeLookup(lx.symbol.sTYPE_MESH)
mesh_item = scene.ItemAdd(mesh_type)

# Get mesh object
chanWrite = lx.object.ChannelWrite(scene.Channels(lx.symbol.s_ACTIONLAYER_SETUP, 0))
write_mesh_obj = chanWrite.ValueObj(mesh_item, mesh_item.ChannelLookup(lx.symbol.sICHAN_MESH_MESH))
mesh = lx.object.Mesh(write_mesh_obj)

lx.eval('vertMap.new type:rgb')

PositionfloatList = []  # Define an array of floats
file_path = 'C:\Temp\TEST.xyz'  # Defines path of output text file
FileDATA = open(file_path, 'r')  # Opens and read file

with FileDATA as f:
    line = f.readline()
    pointAccessor = mesh.PointAccessor()  # Add a point using the PointAccessor interface

    for line in f:
        PositionfloatList = map(float, line.split(','))
        # print('\n'.join([str(x) for x in PositionfloatList]))
        newPointID = pointAccessor.New(PositionfloatList[0:3])
        # Update the mesh
        mesh.SetMeshEdits(lx.symbol.f_MESHEDIT_POINTS)
        VertColor_R = PositionfloatList[3]
        VertColor_G = PositionfloatList[4]
        VertColor_B = PositionfloatList[5]
        lx.eval('vertMap.setValue rgb 0 %f', VertColor_R)  # Set R Value
        lx.eval('vertMap.setValue rgb 1 %f', VertColor_G)  # Set G Value
        lx.eval('vertMap.setValue rgb 2 %f', VertColor_B)  # Set B Value
FileDATA.close()  # Closes the file

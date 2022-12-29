# python
"""
Name:           SMO_XYZ_Vertex.py

Purpose:		This script is designed to:
                Open a txt file (Target) and create Vertex at current position
                defined by the target File 3 float value (separated by a coma)
                Each line is a new Vertex

Author:         Franck ELISABETH
Website:        https://www.smoluck.com
Created:        29/11/2019
Copyright:      (c) Franck Elisabeth 2017-2022
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

Pi = 3.14159265358979323846
Radian = (180 / Pi)

PositionfloatList = []  # Define an array of floats
file_path = 'D:\EXTRIPLE\POSCO\CLOUDCOMP\ROOM_B\Cam_ROOM_B_000000.cam'  # Defines path of output text file
FileDATA = open(file_path, 'r')  # Opens and read file

with FileDATA as f:
    line = f.readline()

    for line in f:
        PositionfloatList = map(float, line.split(','))
        # print '\n'.join([str(x) for x in PositionfloatList])
        lx.eval('item.create camera')
        RotX = (PositionfloatList[0] * Radian)
        RotY = (PositionfloatList[1] * Radian)
        RotZ = (PositionfloatList[2] * Radian)
        PosX = (PositionfloatList[3])
        PosY = (PositionfloatList[4])
        PosZ = (PositionfloatList[5])
        lx.eval('transform.channel rot.X %s' % RotX)
        lx.eval('transform.channel rot.Y %s' % RotY)
        lx.eval('transform.channel rot.Z %s' % RotZ)
        lx.eval('transform.channel pos.X %s' % PosX)
        lx.eval('transform.channel pos.Y %s' % PosY)
        lx.eval('transform.channel pos.Z %s' % PosZ)

FileDATA.close()  # Closes the file

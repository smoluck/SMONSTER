# python
"""
# Name:         SMO_XYZ_Vertex_RoundedValuePath.py
# Version: 1.0
#
# Purpose:	Open a txt file (Target) and create 
# 			Vertex at current position defined by the target File 3 float value (separated by a coma)
#			Each line is a new vertex and round the value to the Centimeter (2 Decimals)
#
# Author:       Franck ELISABETH
# Website:      https://www.smoluck.com
#
# Created:      29/11/2019
# Copyright:    (c) Franck Elisabeth 2017-2022
"""

import modo, lx, lxu, os

modo_ver = int(lx.eval('query platformservice appversion ?'))
try:
	lx.eval ('dialog.setup fileOpenMulti')
	lx.eval ('dialog.title "Load an XYZ file"')
	lx.eval ('dialog.fileType xyz')
	if modo_ver == 801:
		lx.eval ('+dialog.open')
	else:
		lx.eval ('dialog.open')
	xyz_path = lx.eval1 ('dialog.result ?')
except:
	lx.out ('Failed to load the XYZ Input file.')
if xyz_path == None:
	lx.out ('Failed to load the XYZ Input file.')
else:
	xyz_path = os.path.splitext (xyz_path)[0] + '.xyz'
	xyz_file_name = os.path.splitext (os.path.basename (xyz_path))[0]
	lx.out('XYZ Input file name', xyz_file_name)


# The object that represents the current scene
scene = lxu.select.SceneSelection().current()

# Create new mesh item: an object to perform various functions upon a scene
scene_service = lx.service.Scene()

# Lookup global type value of the mesh type
mesh_type = scene_service.ItemTypeLookup(lx.symbol.sTYPE_MESH)
mesh_item = scene.ItemAdd(mesh_type)

# A global object that represents editing of channels
chanWrite = lx.object.ChannelWrite(scene.Channels(lx.symbol.s_ACTIONLAYER_SETUP, 0))

write_mesh_obj = chanWrite.ValueObj(mesh_item, mesh_item.ChannelLookup(lx.symbol.sICHAN_MESH_MESH))
mesh = lx.object.Mesh(write_mesh_obj)

# Get a writable object representing the meshes' mesh channel
valObj = channelWriter.ValueObj(mesh_item, meshChannelIndex)
# Get a mesh item from the channel obj
meshItem = lx.object.Mesh(valObj)

meshName = mesh_item.UniqueName()
print(meshName)


for index in lx.evalN('query layerservice layers ? fg'):
	activeItem = lx.eval('query layerservice layer.name ? %s' %index)

decimals = 2 # how many decimals to round to
# print type(decimals)

PositionfloatList = [] # Define an array of floats
FileDATA= open(xyz_path, 'r') #Opens and read file

with FileDATA as f:
	line = f.readline()
	pointAccessor = mesh.PointAccessor() # Add a point using the PointAccessor interface
	
	for line in f:
		PositionfloatList = map (float, line.split (','))
		
		FormatedPositionFloatList = [ '%.2f' % elem for elem in PositionfloatList ]
		
		PosX_Round = (FormatedPositionFloatList[0])
		PosY_Round = (FormatedPositionFloatList[1])
		PosZ_Round = (FormatedPositionFloatList[2])
		
		newPointID = pointAccessor.New([float(PosX_Round), float(PosY_Round), float(PosZ_Round)])
		
		# Update the mesh
		mesh.SetMeshEdits(lx.symbol.f_MESHEDIT_POINTS)
		
FileDATA.close() #Closes the file

lx.eval('item.name "%s" mesh' % xyz_file_name)
lx.eval('vert.merge fixed false 0.004 false false')

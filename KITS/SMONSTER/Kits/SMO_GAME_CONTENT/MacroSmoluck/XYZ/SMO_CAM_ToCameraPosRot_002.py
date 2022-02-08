#python
#---------------------------------------
# Name:         SMO_XYZ_Vertex.py
# Version: 1.0
#
# Purpose:	Open a txt file (Target) and create 
# 			Vertex at current position defined by the target File 3 float value (separated by a coma)
#			Each line is a new Vertex
#
# Author:       Franck ELISABETH
# Website:      http://www.smoluck.com
#
# Created:      29/11/2019
# Copyright:    (c) Franck Elisabeth 2017-2022
#---------------------------------------

import lx, lxu, os

# Get current scene
scene = lxu.select.SceneSelection().current()


Pi = 3.14159265358979323846
lx.out('Pi ',Pi)
Radian = (180/Pi)
lx.out('Radian ',Radian)


PositionfloatList = [] # Define an array of floats
file_path='D:\EXTRIPLE\POSCO\CLOUDCOMP\ROOM_B\Cam_ROOM_B_LIST.cam' #Defines path of output text file
FileDATA= open(file_path, 'r') #Opens and read file



with FileDATA as f:
	line = f.readline()
	
	for line in f:
		PositionfloatList = map (float, line.split (','))
		# print('\n'.join([str(x) for x in PositionfloatList]))
		
		# #Create a user value that define the CameraName Tag.
		# lx.eval("user.defNew name:CameraName type:string life:momentary")
		# CameraName = ('(Camera) + {%s}') % line )
		
		RadRotX = PositionfloatList[0]
		RadRotY = PositionfloatList[1]
		RadRotZ = PositionfloatList[2]
		lx.out('Rot X in Radian:' ,RadRotX)
		lx.out('Rot Y in Radian:' ,RadRotY)
		lx.out('Rot Z in Radian:' ,RadRotZ)
		
		RotX = RadRotX * Radian
		RotY = RadRotY * Radian
		RotZ = RadRotZ * Radian
		lx.out('Rot X in Degree:' ,RotX)
		lx.out('Rot Y in Degree:' ,RotY)
		lx.out('Rot Z in Degree:' ,RotZ)

		PosX = PositionfloatList[3]
		PosY = PositionfloatList[4]
		PosZ = PositionfloatList[5]
		lx.out('Camera Position X:' ,PosX)
		lx.out('Camera Position Y:' ,PosY)
		lx.out('Camera Position Z:' ,PosZ)
		
		lx.eval('item.create camera')
		# lx.eval('item.name %s xfrmcore' % CameraName)
		lx.eval('camera.hfov 90.0')
		lx.eval('transform.channel rot.X %f' % RotX)
		lx.eval('transform.channel rot.Y %f' % RotY)
		lx.eval('transform.channel rot.Z %f' % RotZ)
		lx.eval('transform.channel pos.X %f' % PosX)
		lx.eval('transform.channel pos.Y %f' % PosY)
		lx.eval('transform.channel pos.Z %f' % PosZ)
		lx.eval('select.drop item')
		
FileDATA.close() #Closes the file

# python
# Select the mesh to rotate (in item mode)
# and it will add the deisred value to the current transform value.
#
# If an item as RY 58.2 deg
# using SMO_ShiftRotateXYZ_Item.py 1 180
# will add 180 degree to the current value of the item
# ending in a RY of 238.2 deg
#
# 
# Arguments properties
# arg1 = Axis -> x y z  are 0 1 2
# arg2 = Rotation Value in degree
#
# lx.eval('@{kit_SMO_GAME_CONTENT:MacroSmoluck/Setup/SMO_SET_ShiftRotateXYZ_Item.py} 1 180')

import lx

args = lx.args()
lx.out(args)
UserAxe = int(args[0])
UserRot = float(args[1])
lx.out('Desired Axe change:',UserAxe)
lx.out('Desired Rotation Value:',UserRot)


# My Variables
itemName = lx.eval('item.name ?')
xRot = lx.eval("transform.channel rot.X ?")
yRot = lx.eval("transform.channel rot.Y ?")
zRot = lx.eval("transform.channel rot.Z ?")
# Output X Pos in Event Log
lx.out('X Rotation:',xRot)
lx.out('Y Rotation:',yRot)
lx.out('Z Rotation:',zRot)

if UserAxe == 0 :	
	xRot += UserRot
	#Output Name and New X Pos
	lx.out('New X Rotation:',xRot)
	lx.eval('transform.channel rot.X {%f} shift' % xRot)
	#lx.eval('transform.channel rot.X {%s}', % xRot)
if UserAxe == 1 :
	yRot += UserRot
	#Output Name and New X Pos
	lx.out('New X Rotation:',yRot)
	lx.eval('transform.channel rot.Y {%f} shift' % yRot)
	#lx.eval('transform.channel rot.Y {%s}', % yRot)
if UserAxe == 2 :
	zRot += UserRot
	#Output Name and New X Pos
	lx.out('New X Rotation:',zRot)
	lx.eval('transform.channel rot.Z {%f} shift' % zRot)
	#lx.eval('transform.channel rot.Z {%s}', % zRot)
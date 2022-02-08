#python
#---------------------------------------
# Name:         SMO_ExportMeshOpRig_to_OBJSequence
# Version: 1.01
#
# Purpose: This script is designed to test Export MeshOps rig as a freezed Mesh, over time, as an FBX sequence.
# Select the MeshOp item and run. 
#
# Author:       Franck ELISABETH
# Website:      http://www.smoluck.com
#
# Created:      03/12/2018
# Modified:		03/06/2019
# Copyright:    (c) Franck Elisabeth 2017-2022
#---------------------------------------

#import the necessary Python libraries
import lx, os, modo

scene = modo.Scene()

# # # Set the Undo to PAUSE Mode during the execution of that Script.
# # lx.eval('app.undoSuspend')


# init File Dialog
try:
	
	# # Get the directory to export to.
	# lx.eval('dialog.setup fileSave')
	# lx.eval('dialog.title \"Select path to export to ...\"')
	# lx.eval('dialog.fileTypeCustom fbx \'Fbx\' \'*.fbx\' fbx')
	# lx.eval('dialog.open')
	# fullPath = lx.eval('dialog.result ?')
	# (dirPath, filename) = os.path.split(fullPath)
	# (shortFileName, extension) = os.path.splitext(filename)
	
	# Get the directory to export to.
	lx.eval('dialog.setup fileSave')
	lx.eval('dialog.title \"Select path to export to ...\"')
	lx.eval('dialog.fileTypeCustom obj \"Obj\" \"*.obj\" obj')
	lx.eval('dialog.open')
	
	fullPath = lx.eval('dialog.result ?')
	(dirPath, filename) = os.path.split(fullPath)
	(shortFileName, extension) = os.path.splitext(filename)
	
except RuntimeError:
	lx.out('script Stopped')
	sys.exit

# # store current scene
oldscene = lx.eval('query sceneservice scene.index ? current')

# manage time frame
frate = lx.eval('time.fpsCustom ?')
timeStart = lx.eval('time.range current ?')
timeEnd = lx.eval('time.range current out:?')
frameStart = int(round(timeStart * frate, 0))
frameEnd = int(round(timeEnd * frate, 0))
lx.eval('select.time %s' % timeStart)
frame = frameStart

# get selected items
selectedMeshes = scene.selected


# Define a tag on the selected mesh item, in order to select it back during the process.
try:
	lx.eval('select.editSet SOURCE_MESH add')
	lx.eval('select.drop item')
	lx.eval('!scene.save')
	
except:
	sys.exit

	
###########-LOOP START-############
lx.out('<------------------ START ------------------->')
lx.out('<--- Smoluck: Export MeshOp Rig to OBJ Sequence Script --->')
lx.out('-')

while frame <= frameEnd:

	lx.eval('select.type item')
	lx.eval('select.useSet SOURCE_MESH select')

	# tempMesh = scene.addItem(modo.c.MESH_TYPE)
	# lx.eval('item.componentMode polygon true')

	# for meshItem in selectedMeshes:
		# scene.select(meshItem)
		# lx.eval('select.polygon add 0 face')
		# lx.eval('select.copy')
		# scene.select(tempMesh)
		# lx.eval('select.paste')

	# create new scene
	lx.eval('scene.new')
	newscene = lx.eval('query sceneservice scene.index ? current')

	# go back to old scene and throw item over to a new scene
	lx.eval('scene.set %s' %oldscene)

	# # select prev selected meshes
	lx.eval('select.useSet SOURCE_MESH select')

	# Freeze the Meshop Stack
	lx.eval('deformer.freeze false')

	# export selected to a new scene
	lx.eval('layer.import %s {} move:false position:0' %newscene)

	# save result mesh to a file
	objPath = dirPath + '\\' + shortFileName + '_' + str(frame) + '.obj'
	lx.eval('!scene.saveAs "%s" wf_OBJ false' % (objPath))

	lx.eval('!scene.close')
	# lx.eval('scene.set %s' %oldscene)

	lx.eval('select.type item')

	# Revert to Scene Orignal State
	lx.eval('!scene.revert')

	# go to a next frame 
	timePos = lx.eval('select.time ?')
	lx.eval('select.time %s' % timePos)
	lx.eval('time.step frame next')

	# Save scene at new frame state
	lx.eval('!scene.save')

	# scene.removeItems(tempMesh)

	lx.out('Mesh "%s" Exported to OBJ' % frame )
	lx.out('-')

	frame += 1
###########-LOOP END-############


lx.out('<--- Smoluck: Export MeshOp Rig to OBJ Sequence Script --->')
lx.out('<------------------ END ------------------->')
lx.eval('select.time 0')

# Delete the temporary Item selection Set
lx.eval('!select.deleteSet SOURCE_MESH')

# Save scene at frame Start
lx.eval('!scene.save')
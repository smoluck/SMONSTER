#python
#---------------------------------------
# Name:         SMO_ExportMeshOpRig_to_FBXSequence
# Version: 1.01
#
# Purpose: This script is designed to test Export MeshOps rig as a freezed Mesh, over time, as an FBX sequence.
# Select the MeshOp item and run. 
#
# Author:       Franck ELISABETH
# Website:      http://www.smoluck.com
#
# Created:      03/12/2018
# Modified:		19/03/2019
# Copyright:    (c) Franck Elisabeth 2017-2022
#---------------------------------------

#import the necessary Python libraries
import lx
import os
import modo

scene = modo.Scene()

# # # Set the Undo to PAUSE Mode during the execution of that Script.
# # lx.eval('app.undoSuspend')


# Save the current Scene (.lxo) to the same directory of FBX export
# # get modo's temp dir
# temp_dir = lx.eval('query platformservice path.path ? temp')
# # name our temp file
# temp_file = "SMO_ExportMeshOpRig_ToFBXSequence.lxo"
# # builds the complete path out of the temp dir and the temp file name
# temp_path = os.path.join(temp_dir, "SMO_ExportMeshOpRig_ToFBXSequence", temp_file)

# # make sure the SMO_REBEVEL directory exists, if not create it
# if not os.path.exists(os.path.dirname(temp_path)):
    # # try to create the directory. 
    # try:
        # os.makedirs(os.path.dirname(temp_path))
    # except:
        # # if that fails for any reason print out the error
        # print(traceback.format_exc())

# # replay name:"Save Scene As"
# # here we just call the save as command with our new custom
# # path Python style instead of macro style.
# lx.eval('!scene.saveAs filename:"{}" format:"$LXOB" export:false'.format(temp_path))





# init File Dialog
try:
	# Get the directory to export to.
	lx.eval('dialog.setup fileSave')
	lx.eval('dialog.title \"Select path to export to ...\"')
	lx.eval('dialog.fileTypeCustom fbx \'Fbx\' \'*.fbx\' fbx')
	lx.eval('dialog.open')
	fullPath = lx.eval('dialog.result ?')
	(dirPath, filename) = os.path.split(fullPath)
	(shortFileName, extension) = os.path.splitext(filename)
	
except RuntimeError:
	lx.out('script Stopped')
	sys.exit

# # store current scene
# oldscene = lx.eval('query sceneservice scene.index ? current')

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


##########################
# Vertex Map Analysis pass
##########################
lx.out('<Vertex Map Analysis pass ------------ START ------------->')

# get the Available Vertex Map Count
Vmap_Count = lx.evalN('query layerservice vmap.n ?')
lx.out('Vertex Map Count: {%s}' % Vmap_Count)
lx.out('--------------------------')

# get the First Vmap Name of all type
FirstVmap_Name = lx.evalN('query layerservice vmap.name ? first')
lx.out('First Vertex Map Name: {%s}' % FirstVmap_Name)
lx.out('--------------------------')

# get the First Selected VertexMap Index
Vmap_FirstSelected = lx.evalN('query layerservice vmap.selected ? first')
lx.out('First Selected VertexMap Index: {%s}' % Vmap_FirstSelected)
lx.out('--------------------------')

# get the first VertexMap Index
Vmap_Index = lx.evalN('query layerservice vmap.index ? first')
lx.out('First Vertex Map Index: {%s}' % Vmap_Index)
lx.out('--------------------------')

# get the Vmap type for the first Vmap
UVmap_Type = lx.evalN('query layerservice vmap.type ? first')
lx.out('Vertex Map type for the first Vmap: {%s}' % UVmap_Type)
lx.out('--------------------------')

# List of Index for the different Vmap available
AllVmapGroup = lx.evalN('query layerservice vmaps ? all')
lx.out('<- Index for the different Vertex Map available ->')
lx.out(AllVmapGroup)
lx.out('--------------------------')

# get the VertexMap Index of UVTexture Type
Vmap_UVIndex = lx.evalN('query layerservice vmaps ? texture')
# lx.out('Vertex Map Index that is from UV (Texture) Type: {%s}' % Vmap_UVIndex)

lx.out('Vertex Map Analysis pass END -------------->')

lx.out('-')
# ##########################
# lx.out('-')

# lx.out('--------------------------')
# lx.out('Vertex Map Selected and Index Test')

# if Vmap_FirstSelected == Vmap_UVIndex:
	# # Select the first UV Map
	# lx.out('Good')
# elif Vmap_FirstSelected != Vmap_UVIndex:
	# # Select the first UV Map
	# lx.out('Bad')
	
# lx.out('-')
# ##########################
lx.out('-')

##########################
lx.out('<------------- START -------------->')
lx.out('<--- UV Map Safety Check --->')
	
# Get info about the selected UVMap.
UVmap_Selected = lx.evalN('query layerservice vmaps ? selected')
UVmap_SelectedN = len(lx.evalN('query layerservice vmaps ? selected'))
lx.out('Selected UV Map Index:', UVmap_SelectedN)


if UVmap_SelectedN <= 0:
	lx.eval('dialog.setup info')
	lx.eval('dialog.title {Smoluck: Export MeshOp Rig to FBX Sequence:}')
	lx.eval('dialog.msg {You must have a UV map selected to run this script.}')
	lx.eval('dialog.open')
	sys.exit()

if UVmap_SelectedN > 1:
	lx.eval('dialog.setup info')
	lx.eval('dialog.title {Smoluck: Export MeshOp Rig to FBX Sequence:}')
	lx.eval('dialog.msg {Please select Only One Vertex Map and run that script again.}')
	lx.eval('dialog.open')
	sys.exit()
	

UserUVMapName = lx.eval1('query layerservice vmap.name ? %s' %UVmap_Selected)
lx.out('USER UV Map Name:', UserUVMapName)	
	
lx.out('<- UV Map Safety Check ->')
lx.out('<------------- END -------------->')
##########################


#########################
# lx.out('<------------- START -------------->')
# lx.out('<--- Modo Default UV Map Name --->')
# lx.out('-')

# DefaultUVMapName = lx.eval1('query application.defaultTexture ?')
# lx.out('Modo Default Vertex Map name for UVs:', DefaultUVMapName)

# lx.out('-')
# lx.out('<--- Modo Default UV Map Name --->')
# lx.out('<------------- END -------------->')
#########################


# Define a tag on the selected mesh item, in order to select it back during the process.
try:
	lx.eval('select.editSet SOURCE_MESH add')
	lx.eval('select.drop item')
	lx.eval('!scene.save')
	
except:
	lx.eval('sys.exit()')

	
###########-LOOP START-############
lx.out('<------------------ START ------------------->')
lx.out('<--- Smoluck: Export MeshOp Rig to FBX Sequence Script --->')
lx.out('-')

while frame <= frameEnd:
		lx.eval('select.useSet SOURCE_MESH select')
		# Freeze the Meshop Stack
		lx.eval('deformer.freeze false')
		
		# Set the active UV Map
		lx.eval('select.vertexMap {%s} txuv replace' % UserUVMapName)

		# Create Mikk Tangent Space Map
		# lx.eval('mesh.mikktspacegen')
		# lx.out('Mikk Tangent Space Map for Mesh "%s" created' % frame )
		
		# Select all the Meshes in the Scene
		lx.eval('select.itemType mesh')
		# Deselect the Mesh to export
		lx.eval('select.useSet SOURCE_MESH deselect')
		# Delete Unnecessary Meshes
		lx.eval('!delete')
		# Select again the Mesh to Export
		lx.eval('select.useSet SOURCE_MESH select')
		# save result mesh to a file
		fbxPath = dirPath + '\\' + shortFileName + '_' + str(frame) + '.fbx'
		output_dir = lx.eval1 ('dialog.result ?')
		
		# Set the FBX Export seetings using Defined Preset for Unity.
		lx.eval('preset.fbx SMO_MeshopsAnimToFBX_Triple')
		
		### DEFINE the FBX Export Type: Selection OR Selection with Hierarchy ###
		###
		# Get the current FBX Export setting.
		# fbx_export_setting = lx.eval1 ('user.value sceneio.fbx.save.exportType ?')
		# Set the FBX Export setting to export selection.	
		# lx.eval('user.value sceneio.fbx.save.exportType FBXExportSelection')
		# Set the FBX Export setting to export selection with hierarchy children.
		# lx.eval('user.value sceneio.fbx.save.exportType FBXExportSelectionWithHierarchy')
		
		# Export to FBX.
		lx.eval('!scene.saveAs "%s" fbx true' % fbxPath)
		#lx.eval('!scene.saveAs {%s} FBX 2018' % {fbxPath})


		# Revert to Scene Orignal State
		lx.eval('!scene.revert')
		
		# go to a next frame 
		timePos = lx.eval('select.time ?')
		lx.eval('select.time %s' % timePos)
		lx.eval('time.step frame next')
		
		# Save scene at frame 1
		lx.eval('!scene.save')
		
		lx.out('Mesh "%s" Exported to FBX' % frame )
		lx.out('-')
	
		frame += 1
		
###########-LOOP END-############
lx.out('<--- Smoluck: Export MeshOp Rig to FBX Sequence Script --->')
lx.out('<------------------ END ------------------->')
lx.eval('select.time 0')

# Delete the temporary Item selection Set
lx.eval('!select.deleteSet SOURCE_MESH')

# Save scene at frame Start
lx.eval('!scene.save')
# python
"""
Name:         	SMO_MES_ExportMeshOpRig_QuadRemeshed_to_FBXSequence.py

Purpose: 		This script is designed to:
				Test Export MeshOps rig as a freezed Mesh,
				over time, as an FBX sequence.
				Select the MeshOp item and run.

Author:       	Franck ELISABETH
Website:      	https://www.linkedin.com/in/smoluck/
Created:      	03/12/2018
Copyright:    	(c) Franck Elisabeth 2017-2022
"""

import lx
import os
import modo
import sys

scene = modo.scene.current()
mesh = scene.selectedByType('mesh')

# Set the Undo to PAUSE Mode during the execution of that Script.
# lx.eval('app.undoSuspend')


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
	
	
# -------------------------------------- #
# DEFINE USER Variable for QUAD REMESHER #
# -------------------------------------- #
#####--- Define User Value for PolyCount max to be used by QuadRemesh Processing --- START ---#####
#Create a user value that define the EdgeCount for the Rebevel.
lx.eval("user.defNew name:PolyCountQuadRemesh type:integer life:momentary")
#Set the title name for the dialog window
lx.eval('user.def PolyCountQuadRemesh dialogname "PolyCount max for QuadRemesh Processing"')
#Set the input field name for the value that the users will see
lx.eval("user.def PolyCountQuadRemesh username {Enter the desired Max Polycount here}")
#The '?' before the user.value calls a popup to have the user set the value
lx.eval("?user.value PolyCountQuadRemesh")
#Now that the user set the value, i can query it
user_inputPolyCountQuadRemesh = lx.eval("user.value PolyCountQuadRemesh ?")
lx.out('PolyCountQuadRemesh:',user_inputPolyCountQuadRemesh)


# -------------------------------------- #
# Get current Variable for QUAD REMESHER #
# -------------------------------------- #
lx.out('-------- QR User Values: --------')
lx.eval("user.defNew name:USER_QR_TargPCount type:integer life:momentary")
USER_QR_TargPCount = lx.eval1('user.value xr.TargetQuadCount ?')
lx.out('QR State - Target Polycount:',USER_QR_TargPCount)

lx.eval("user.defNew name:USER_QR_UseMatParts type:boolean life:momentary")
USER_QR_UseMatParts = lx.eval1('user.value xr.UseMaterialParts ?')
lx.out('QR State - Use Material Parts:',USER_QR_UseMatParts)

lx.eval("user.defNew name:USER_QR_UsePolyParts type:boolean life:momentary")
USER_QR_UsePolyParts = lx.eval1('user.value xr.UsePolygonParts ?')
lx.out('QR State - Use Polygon Parts:',USER_QR_UsePolyParts)

lx.eval("user.defNew name:USER_QR_UseSGrpHE type:boolean life:momentary")
USER_QR_UseSGrpHE = lx.eval1('user.value xr.UseSmoothingGroups ?')
lx.out('QR State - Use Smoothing Groups / Hard Edges:',USER_QR_UseSGrpHE)

lx.eval("user.defNew name:USER_QR_UseIndNorm type:boolean life:momentary")
USER_QR_UseIndNorm = lx.eval1('user.value xr.UseIndexedNormals ?')
lx.out('QR State - Use Normals Creasing:',USER_QR_UseIndNorm)

lx.eval("user.defNew name:USER_QR_AutoDetHE type:boolean life:momentary")
USER_QR_AutoDetHE = lx.eval1('user.value xr.AutoDetectHardEdges ?')
lx.out('QR State - Detect Hard-Edges by angle:',USER_QR_AutoDetHE)

lx.eval("user.defNew name:USER_QR_SymX type:boolean life:momentary")
USER_QR_SymX = lx.eval1('user.value xr.SymX ?')
lx.out('QR State - Use Symmetry on X:',USER_QR_SymX)

lx.eval("user.defNew name:USER_QR_SymY type:boolean life:momentary")
USER_QR_SymY = lx.eval1('user.value xr.SymY ?')
lx.out('QR State - Use Symmetry on Y:',USER_QR_SymY)

lx.eval("user.defNew name:USER_QR_SymZ type:boolean life:momentary")
USER_QR_SymZ = lx.eval1('user.value xr.SymZ ?')
lx.out('QR State - Use Symmetry on Z:',USER_QR_SymZ)

lx.eval("user.defNew name:USER_QR_AutoFreeze type:boolean life:momentary")
USER_QR_AutoFreeze = lx.eval1('user.value xr.FreezeInputMesh ?')
lx.out('QR State - Auto Freeze Input Mesh:',USER_QR_AutoFreeze)
lx.out('-------- QR User Values: --------')
# ------------------------------------------ #

lx.out('-')
lx.out('-')
lx.out('-')

# store current scene
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
lx.out('<--- Vertex Map Analysis pass START --->')

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

lx.out('<--- Vertex Map Analysis pass END --->')
lx.out('<--------------- END ---------------->')
#########################

lx.out('-')
lx.out('-')
lx.out('-')

#########################
# UV Map Selection Test #
#########################
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

lx.out('-')
lx.out('-')
lx.out('-')

###########################
# Get Default UV Map Name #
###########################
lx.out('<-------------- START --------------->')
lx.out('<--- Get Modo Default UV Map Name --->')
lx.out('-')

#Create a user value that define the EdgeCount for the Rebevel.
lx.eval("user.defNew name:MODOPrefUVMapName type:string life:momentary")
MODOPrefUVMapName = lx.eval1('pref.value application.defaultTexture ?')
lx.out('Modo Default Vertex Map name for UVs:', MODOPrefUVMapName)

lx.out('-')
lx.out('<--- Get Modo Default UV Map Name --->')
lx.out('<--------------- END ---------------->')
#########################



# Set the Quad Remesher Settings
lx.eval('user.value xr.TargetQuadCount "%i"' % user_inputPolyCountQuadRemesh)


lx.eval('user.value xr.UseMaterialParts false')			# Use Material Parts
lx.eval('user.value xr.UsePolygonParts true')			# Use Polygon Parts
lx.eval('user.value xr.UseSmoothingGroups false')		# Use Smoothing Groups / Hard Edges
lx.eval('user.value xr.UseIndexedNormals false')		# Use Normals Creasing
lx.eval('user.value xr.AutoDetectHardEdges true')		# Detect Hard-Edges by angle
lx.eval('user.value xr.SymX true')						# Use Symmetry on X
lx.eval('user.value xr.SymY false')						# Use Symmetry on Y
lx.eval('user.value xr.SymZ false')						# Use Symmetry on Z
lx.eval('user.value xr.FreezeInputMesh false')			# Auto Freeze Input Mesh


# Set the FBX Export seetings using Defined Preset for Unity.
lx.eval('preset.fbx SMO_MeshopsAnimToFBX_QuadRemesher')



# Define a tag on the selected mesh item, in order to select it back during the process.
try:
	lx.eval('select.editSet SOURCE_MESH_QR add')
	lx.eval('select.drop item')
	lx.eval('item.create camera')
	lx.eval('!delete')
	
	lx.eval('!scene.save')
	
except:
	lx.out('ERROR')
	sys.exit()

	
###########-LOOP START-############
lx.out('<------------------ START ------------------->')
lx.out('<--- Smoluck: Export MeshOp Rig to FBX Sequence Script --->')
lx.out('-')

while frame <= frameEnd:
		lx.eval('select.useSet SOURCE_MESH_QR select')
		# Freeze the Meshop Stack
		lx.eval('deformer.freeze false')
		
		# Set the active UV Map
		# lx.eval('select.vertexMap {%s} txuv replace' % UserUVMapName)
		# Create Mikk Tangent Space Map
		# lx.eval('mesh.mikktspacegen')
		# lx.out('Mikk Tangent Space Map for Mesh "%s" created' % frame )
		
		# Launch the Quad Remesher Script to process the Retopo
		lx.eval('@kit_QuadRemesher:Scripts/XR_DoRetopo.py')
		
		# Add the Resulting Mesh to a new Selection Set
		lx.eval('select.editSet QR_MESH add')
		lx.eval('select.drop item')
		
		
		# Select all the Meshes in the Scene
		lx.eval('select.itemType mesh')
		# Deselect the Mesh to export
		lx.eval('select.useSet QR_MESH deselect')
		# Delete Unnecessary Meshes
		lx.eval('!delete')
		# Select again the Mesh to Export
		lx.eval('select.useSet QR_MESH select')
		
		
		lx.eval('vertMap.new {%s} txuv' % MODOPrefUVMapName)
		
		# Set the active UV Map
		lx.eval('select.vertexMap {%s} txuv replace' % MODOPrefUVMapName)
		
		
		# save result mesh to a file
		fbxPath = dirPath + '\\' + shortFileName + '_' + str(frame) + '.fbx'
		output_dir = lx.eval1 ('dialog.result ?')
		
		
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
		lx.eval('select.drop item')
		
		lx.out('Mesh "%s" Exported to FBX' % frame )
		lx.out('-')
		
		frame += 1
		
###########-LOOP END-############
lx.out('<--- Smoluck: Export MeshOp Rig to FBX Sequence Script --->')
lx.out('<------------------ END ------------------->')
lx.eval('select.time 0')

# Delete the temporary Item selection Set
lx.eval('!select.deleteSet SOURCE_MESH_QR')

# Save scene at frame Start
lx.eval('!scene.save')

lx.eval('user.value xr.TargetQuadCount {%i}' % USER_QR_TargPCount)
lx.eval('user.value xr.UseMaterialParts {%i}' % USER_QR_UseMatParts)
lx.eval('user.value xr.UsePolygonParts {%i}' % USER_QR_UsePolyParts)
lx.eval('user.value xr.UseSmoothingGroups {%i}' % USER_QR_UseSGrpHE)
lx.eval('user.value xr.UseIndexedNormals {%i}' % USER_QR_UseIndNorm)
lx.eval('user.value xr.AutoDetectHardEdges {%i}' % USER_QR_AutoDetHE)
lx.eval('user.value xr.SymX {%i}' % USER_QR_SymX)
lx.eval('user.value xr.SymY {%i}' % USER_QR_SymY)
lx.eval('user.value xr.SymZ {%i}' % USER_QR_SymZ)
lx.eval('user.value xr.FreezeInputMesh {%i}' % USER_QR_AutoFreeze)	
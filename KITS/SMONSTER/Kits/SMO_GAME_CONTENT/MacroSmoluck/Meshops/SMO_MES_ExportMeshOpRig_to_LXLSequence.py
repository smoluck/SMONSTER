# python
"""
Name:         	SMO_ExportMeshOpRig_to_LXLSequence

Purpose:		This script is designed to:
                Test Export MeshOps rig as a freezed Mesh, over time, as a Mesh Preset LXL sequence.
                Select the MeshOp item and run.

Author:       	Franck ELISABETH
Website:      	https://www.linkedin.com/in/smoluck/
Created:      	28/02/2018
Copyright:    	(c) Franck Elisabeth 2017-2022
"""

import lx
import os
import modo
import sys

scene = modo.Scene()

# # Set the Undo to PAUSE Mode during the execution of that Script.
# lx.eval('app.undoSuspend')

# get modo's temp dir
# temp_dir = lx.eval('query platformservice path.path ? temp')
# name our temp file
# temp_file = "SMO_ExportMeshOpRig_ToFBXSequence.lxo"
# builds the complete path out of the temp dir and the temp file name
# temp_path = os.path.join(temp_dir, "SMO_ExportMeshOpRig_ToFBXSequence", temp_file)

# make sure the SMO_REBEVEL directory exists, if not create it
# if not os.path.exists(os.path.dirname(temp_path)):
# try to create the directory.
# try:
# os.makedirs(os.path.dirname(temp_path))
# except:
# if that fails for any reason print out the error
# print(traceback.format_exc())

# replay name:"Save Scene As"
# here we just call the save as command with our new custom
# path Python style instead of macro style.
# lx.eval('!scene.saveAs filename:"{}" format:"$LXOB" export:false'.format(temp_path))


# init File Dialog
try:
    # Get the directory to export to.
    lx.eval('dialog.setup fileSave')
    lx.eval('dialog.title \"Select path to MeshItem to ...\"')
    lx.eval('dialog.fileTypeCustom lxl \'LXl\' \'*.lxl\' lxl')
    lx.eval('dialog.open')
    fullPath = lx.eval('dialog.result ?')
    (dirPath, filename) = os.path.split(fullPath)
    (shortFileName, extension) = os.path.splitext(filename)

except RuntimeError:
    lx.eval('sys.exit()')

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

# Define a tag on the selected mesh item, in order to select it back during the process.
try:
    lx.eval('select.editSet SOURCE_MESH add')
    lx.eval('select.drop item')
    lx.eval('!scene.save')

except:
    lx.out('script Stopped')
    sys.exit

###########-LOOP START-############
lx.out('<------------------ START ------------------->')
lx.out('<--- Smoluck: Export MeshOp Rig to LXL Mesh Preset Script --->')
lx.out('-')

while frame <= frameEnd:
    # if frame == 0:
    lx.eval('select.useSet SOURCE_MESH select')
    # Freeze the Meshop Stack
    lx.eval('deformer.freeze false')
    # Select the UV Map
    lx.eval('select.vertexMap 00_Texture txuv replace')
    # Create Mikk Tangent Space Map
    lx.eval('mesh.mikktspacegen')
    # Select all the Meshes in the Scene
    lx.eval('select.itemType mesh')
    # Deselect the Mesh to export
    lx.eval('select.useSet SOURCE_MESH deselect')
    # Delete Unnecessary Meshes
    lx.eval('!delete')
    # Select again the Mesh to Export
    lx.eval('select.useSet SOURCE_MESH select')
    # save result mesh to a file
    lxlPath = dirPath + '\\' + shortFileName + '_' + str(frame) + '.lxl'
    output_dir = lx.eval1('dialog.result ?')

    # i should use this no ?
    lx.eval('dialog.setup fileSave')
    lx.eval('dialog.title \"Select path to MeshItem to ...\"')
    lx.eval('dialog.fileTypeCustom lxl \'LXl\' \'*.lxl\' lxl')
    # Export to LXL ItemPreset.
    lx.eval('mesh.presetSave "%s" {} {} reuseThumb:0' % lxlPath)

    # Revert to Scene Orignal State
    lx.eval('!scene.revert')

    # go to a next frame
    timePos = lx.eval('select.time ?')
    lx.eval('select.time %s' % timePos)
    lx.eval('time.step frame next')

    # Save scene at frame 1
    lx.eval('!scene.save')

    lx.out('Mesh "%s" Exported to LXL' % frame)
    lx.out('-')

    frame += 1

###########-LOOP END-############
lx.out('<--- Smoluck: Export MeshOp Rig to LXL Mesh Preset Script --->')
lx.out('<------------------ END ------------------->')
lx.eval('select.time 0')

# Delete the temporary Item selection Set
lx.eval('!select.deleteSet SOURCE_MESH')

# Save scene at frame Start
lx.eval('!scene.save')

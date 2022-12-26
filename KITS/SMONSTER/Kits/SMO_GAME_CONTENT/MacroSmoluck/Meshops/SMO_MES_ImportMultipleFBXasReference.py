# python
"""
# Name:         SMO_ImportMultipleFBXasReference
# Version: 1.0
#
# Purpose: 	This script is designed to:
#			Import a set of FBX
# 			Apply the same loading Preset
#			Parent those referenced Folder to a Locator
#			Tag those to a Group
#			Then select the ArrayTarget Assembly
#
# Author:       Franck ELISABETH
# Website:      https://www.smoluck.com
#
# Created:      04/01/2019
# Modified:		19/03/2019
# Copyright:    (c) Franck Elisabeth 2017-2022
"""

import	lx
import	lxifc
import	lxu.command
import	lxu.select
import	subprocess
import	os
import  modo

try:
	### Part 1 : Get the directory to export to.	
	lx.eval('dialog.setup fileOpenMulti')
	lx.eval('dialog.title "Select FBX File to Import"')
	#lx.eval('dialog.fileTypeCustom FBX \'*.fbx\' fbx')
	lx.eval('dialog.open')
	FilesToLoad = lx.eval('dialog.result ?')
	#(dirPath, filename) = os.path.split(FilesPath)
	#(shortFileName, extension) = os.path.splitext(FilesToLoad)
	lx.out ('Import Path', FilesToLoad)

	if FilesToLoad:
		lx.eval('loaderOptions.fbx false true true true false false true false false false false false false false false FBXAnimSampleRate_x1 1.0 defaultimport')
		for FilesPath in FilesToLoad:
			lx.eval('!!scene.importReference "%s" true true false false false' % FilesPath)
			
			
except:
	lx.eval('sys.exit()')	
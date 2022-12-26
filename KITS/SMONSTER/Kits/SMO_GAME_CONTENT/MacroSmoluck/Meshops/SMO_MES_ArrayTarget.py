# python
"""
# Name:         SMO_ArrayTarget
# Version: 1.01
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


import	lx, lxifc, lxu.command, lxu.select, subprocess, os, modo



scene = modo.Scene()

# # Set the Undo to PAUSE Mode during the execution of that Script.
lx.eval('app.undoSuspend')

### DEFINE a Command


class SMO_ArrayTarget_Cmd (lxu.command.BasicCommand):
	def __init__ (self):
		lxu.command.BasicCommand.__init__ (self)

		self.scrp_svc = lx.service.ScriptSys ()
		self.sel_svc = lx.service.Selection ()

	def cmd_Interact (self):
		pass

	def cmd_UserName (self):
		return 'SMOLUCK - Create ArrayTarget Setup'

	def cmd_Desc (self):
		return 'Load FBX as Reference and Array it.'

	def cmd_Tooltip (self):
		return 'Load FBX as Reference and Array it.'

	def cmd_Help (self):
		return 'https://twitter.com/sm0luck'

	def basic_ButtonName (self):
		return 'SMOLUCK - Create ArrayTarget Setup'

	def cmd_Flags (self):
		return lx.symbol.fCMD_UNDO

	def basic_Enable (self, msg):
		return True

		
		
		
	### Part 1 : import FBX files as reference	
	try:
		# Get the files list	
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
		
		
		
		
	# ### Store Import Settings for Import Reference
	# try:
		
	
		
		# # Store FBXImportSettings
		# def storeFBXSettings (self):
		# FBX_USERVALUE_PREFIX	= 'sceneio.fbx.save.'
		# FBX_USERVALUE_COMMAND	= 'user.value ' + FBX_USERVALUE_PREFIX
		
		# fbxSettings = {}
		
		# for x in range(self.scrp_svc.UserValueCount ()):
			# uval = self.scrp_svc.UserValueByIndex (x)
			# name = uval.Name ()
			# if name.startswith ('sceneio.fbx.save.'):
				# fbxSettings[name] = self.getUserValue (name)
		
		# return fbxSettings
	
		# def restoreFBXSettings (self, fbxSettings):
			# for name, value in fbxSettings.items():
				# lx.eval ('user.value %s %s' % (name, value))

		# def basic_Execute (self, msg, flags):	
		
		# # Store user's FBX preferences for restoring later.
		# fbxSettings = self.storeFBXSettings ()

		


	### Part 2 : Load the Predefined Assembly Preset: ArrayTarget	
	try:			
		#####--- Define the Preset directory of the Custom kit_SMO_GAME_CONTENT Presets to load the ArrayTarget Assembly --- START ---#####
		#####
		SMO_GAME_CONTENTPresetPath = lx.eval("query platformservice alias ? {kit_SMO_GAME_CONTENT:Presets}")
		lx.out('Smoluck GAME CONTENT PresetPath:', SMO_GAME_CONTENTPresetPath )
		#####
		#####--- Define the Preset directory of the Custom kit_SMO_GAME_CONTENT Presets to load the ArrayTarget Assembly --- END ---#####
		lx.eval('preset.do {%s/SMO_ArrayTarget_ASS.lxp}' % SMO_GAME_CONTENTPresetPath)
		lx.eval('select.type item')
		lx.eval('select.drop item')
		
	except:
		lx.eval('sys.exit()')

		
		
		
	### Part 4 : Define Variable and process the Main Macro	
	try:	
		#####--- Define User Value for Rebevel Count --- START ---#####
		#####
		#Create a user value that define the EdgeCount for the Rebevel.
		lx.eval("user.defNew name:MatchName type:string life:momentary")
		#Set the title name for the dialog window
		lx.eval('user.def MatchName dialogname "Reference Pattern Name"')
		#Set the input field name for the value that the users will see
		lx.eval("user.def MatchName username {Enter the Pattern name of your current Reference Target (FBX filename)}")
		#The '?' before the user.value calls a popup to have the user set the value
		lx.eval("?user.value MatchName")
		#Now that the user set the value, i can query it
		user_inputMatchName = lx.eval("user.value MatchName ?")
		
		
		# Select Imported Reference Group using Pattern selection
		PatternName = lx.eval('selectPattern.pattern label: {*%s*}' % user_inputMatchName )
		lx.out ('Matched pattern name:', user_inputMatchName)	
		
		lx.eval('selectPattern.none')
		lx.eval('selectPattern.toggleGroup enable:true')
		lx.eval('selectPattern.apply mode:set')
		lx.eval('selectPattern.all')
		
		# replay name:"Edit Selection Set"
		lx.eval('select.editSet name:FBXTarget_ITEMS mode:add')
		
		# Add to the selection the Loc_TARGET_Transform
		lx.eval('select.useSet name:TARGET_LOC mode:select')
		# replay name:"Parent"
		lx.eval('item.parent inPlace:0')
		# replay name:"Drop selection"
		lx.eval('select.drop item')
		
		# Add to the selection the Loc_TARGET_Transform
		lx.eval('select.useSet name:FBXTarget_ITEMS mode:select')
		
		
		# Add Imported Reference to the Group TARGET_FBX
		lx.eval('zen.groupAdd_Popup group:TARGET_FBX')
		
		# replay name:"Delete Selection Set"
		lx.eval('!select.deleteSet name:TARGET_LOC all:false')
		# replay name:"Delete Selection Set"
		lx.eval('!select.deleteSet name:FBXTarget_ITEMS all:false')
		
		
		lx.eval('select.item ArrayTarget_Ass set')
		
		# Command Block Begin: 
		lx.eval('select.channel channel:"ArrayTarget_Ass:FBXSourceCount_Count" mode:add')
		lx.eval('select.channel channel:"ArrayTarget_Ass:UsePrototypeTransform" mode:add')
		lx.eval('select.channel channel:"ArrayTarget_Ass:OffsetZ" mode:add')
		lx.eval('select.channel channel:"ArrayTarget_Ass:OffsetY" mode:add')
		lx.eval('select.channel channel:"ArrayTarget_Ass:OffsetX" mode:add')
		lx.eval('select.channel channel:"ArrayTarget_Ass:Mode3D" mode:add')
		lx.eval('select.channel channel:"ArrayTarget_Ass:Mode2D" mode:add')
		lx.eval('select.channel channel:"ArrayTarget_Ass:FBXSourceCount_Count" mode:add')
		# Command Block End: 
		lx.eval('tool.set channel.haul on')
		
		# # replay name:"Use Selection Set"
		# lx.eval('select.useSet name:FBXTarget_ITEMS mode:select')
		
	except:
		lx.eval('sys.exit()')

lx.bless (SMO_ArrayTarget_Cmd, 'SMO.ArrayTarget')
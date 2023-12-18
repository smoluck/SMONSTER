# python
"""
Name:         SMO_Detriangulate_Optimized.py

Purpose:      This script is designed to:
              Optimizely process a detriangulate only on Triangle in the selected Mesh Layer.

Author:       Franck ELISABETH
Website:      https://www.linkedin.com/in/smoluck/
Created:      22/01/2020
Copyright:    (c) Franck Elisabeth 2017-2022
"""

import lx
import modo
import sys

scene = modo.scene.current()
mesh = scene.selectedByType('mesh')[0]


# ---------------- COPY/PASTE Check Procedure ---------------- #
## create variables
lx.eval("user.defNew name:User_Pref_CopyDeselectChangedState type:boolean life:momentary")
lx.eval("user.defNew name:User_Pref_PasteSelectionChangedState type:boolean life:momentary")
lx.eval("user.defNew name:User_Pref_PasteDeselectChangedState type:boolean life:momentary")

lx.eval("user.defNew name:User_Pref_CopyDeselect type:boolean life:momentary")
lx.eval("user.defNew name:User_Pref_PasteSelection type:boolean life:momentary")
lx.eval("user.defNew name:User_Pref_PasteDeselect type:boolean life:momentary")
###################

# Look at current Copy / Paste user Preferences:
User_Pref_CopyDeselect = lx.eval('pref.value application.copyDeSelection ?')
lx.out('User Pref: Deselect Elements after Copying', User_Pref_CopyDeselect)
User_Pref_PasteSelection = lx.eval('pref.value application.pasteSelection ?')
lx.out('User Pref: Select Pasted Elements', User_Pref_PasteSelection)
User_Pref_PasteDeselect = lx.eval('pref.value application.pasteDeSelection ?')
lx.out('User Pref: Deselect Elements Before Pasting', User_Pref_PasteDeselect)
# Is Copy Deselect False ?
if User_Pref_CopyDeselect == 0:
	lx.eval('pref.value application.copyDeSelection true')
	User_Pref_CopyDeselectChangedState = 1

# Is Paste Selection False ?
if User_Pref_PasteSelection == 0:
	lx.eval('pref.value application.pasteSelection true')
	User_Pref_PasteSelectionChangedState = 1

# Is Paste Deselect False ?
if User_Pref_PasteDeselect == 0:
	lx.eval('pref.value application.pasteDeSelection true')
	User_Pref_PasteDeselectChangedState = 1

# Is Copy Deselect True ?
if User_Pref_CopyDeselect == 1:
	User_Pref_CopyDeselectChangedState = 0

# Is Paste Selection True ?
if User_Pref_PasteSelection == 1:
	User_Pref_PasteSelectionChangedState = 0

# Is Paste Deselect True ?
if User_Pref_PasteDeselect == 1:
	User_Pref_PasteDeselectChangedState = 0
# -------------------------------------------- #


# -------------------------- #
# <---( SAFETY CHECK 1 )---> #
# -------------------------- #

# --------------------  safety check 1 : Only One Item Selected --- START
ItemCount = lx.eval('query layerservice layer.N ? fg')
lx.out('Selected Item count:', ItemCount)

if ItemCount != 1:
	SMO_SafetyCheck_Only1MeshItemSelected = 0
	lx.eval('dialog.setup info')
	lx.eval('dialog.title {SMO Cut to NewMesh:}')
	lx.eval('dialog.msg {You must only select the Mesh Item layer you are working on, in Item List, to run that script}')
	lx.eval('+dialog.open')
	lx.out('Only One Item Selected result:', SMO_SafetyCheck_Only1MeshItemSelected)
	lx.out('script Stopped: Select only one Mesh Item')
	sys.exit
	
else:
	SMO_SafetyCheck_Only1MeshItemSelected = 1
	lx.out('Only One Item Selected:', SMO_SafetyCheck_Only1MeshItemSelected)
	lx.out('script running: right amount of Mesh Item selected')
# --------------------  safety check 1 : Only One Item Selected --- END



if SMO_SafetyCheck_Only1MeshItemSelected == 1 :
	# detect if Ngons are detected.
	lx.eval('select.polygon add vertex curve 4')
	lx.eval('select.polygon add vertex b-spline 4')
	#####--- Get current selected polygon count --- START ---#####
	#####
	CsPolys = len(mesh.geometry.polygons.selected)
	lx.out('Count Selected Poly',CsPolys)
	#####
	#####--- Get current selected polygon count --- END ---#####
	if CsPolys < 1 :
		lx.out('Ngons Detected')

	elif CsPolys >= 1 :
		lx.eval('hide.sel')


	lx.eval('tool.set preset:"detriangulate.meshop" mode:on')
	lx.eval('tool.setAttr tool:"detriangulate.meshop" attr:material value:false')
	lx.eval('tool.setAttr tool:"detriangulate.meshop" attr:material value:true')
	lx.eval('tool.setAttr tool:"detriangulate.meshop" attr:part value:false')
	lx.eval('tool.setAttr tool:"detriangulate.meshop" attr:part value:true')
	lx.eval('tool.setAttr tool:"detriangulate.meshop" attr:smoothingGroup value:false')
	lx.eval('tool.setAttr tool:"detriangulate.meshop" attr:smoothingGroup value:true')
	lx.eval('tool.setAttr tool:"detriangulate.meshop" attr:flatness value:"0.2"')
	lx.eval('tool.flag name:"detriangulate.meshop" flag:auto enable:true')
	lx.eval('tool.doApply')
	lx.eval('tool.flag name:"detriangulate.meshop" flag:auto enable:false')
	lx.eval('tool.drop')
	# replay name:"Select Next Mode"
	lx.eval('select.nextMode')
	# replay name:"Unhide"
	lx.eval('unhide')
	# replay name:"Item"
	lx.eval('select.type item')



# -------------- COPY/PASTE END Procedure  -------------- #
# Restore user Preferences:
if User_Pref_CopyDeselectChangedState == 1 :
	lx.eval('pref.value application.copyDeSelection false')
	lx.out('"Deselect Elements after Copying" have been Restored')
if User_Pref_PasteSelectionChangedState == 1 :
	lx.eval('pref.value application.pasteSelection false')
	lx.out('"Select Pasted Elements" have been Restored')
if User_Pref_PasteDeselectChangedState == 1 :
	lx.eval('pref.value application.pasteDeSelection false')
	lx.out('"Deselect Elements Before Pasting" have been Restored')
# -------------------------------------------- #

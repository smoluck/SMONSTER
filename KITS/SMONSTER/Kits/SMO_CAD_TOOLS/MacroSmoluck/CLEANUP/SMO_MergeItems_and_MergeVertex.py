# python
"""
# Name:         SMO_MergeItems_and_MergeVertex.py
# Version:      1.0
#
# Purpose:      This script is designed to:
#               Merge the selected Mesh Layers and reconnect their boundary
#
# Author:       Franck ELISABETH
# Website:      https://www.smoluck.com
#
# Created:      22/01/2020
# Copyright:    (c) Franck Elisabeth 2017-2022
"""

import lx
import modo
import sys

scene = modo.scene.current()
mesh = scene.selectedByType('mesh')

###############COPY/PASTE Check Procedure#################
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
################################################


# -------------------------- #
# <---( SAFETY CHECK 1 )---> #
# -------------------------- #
lx.eval("user.defNew name:SMO_SafetyCheck_AtLeast2MeshItemSelected type:integer life:momentary")
# --------------------  safety check 1 : Only One Item Selected --- START
ItemCount = lx.eval('query layerservice layer.N ? fg')
# TotalItemCount = lx.eval('query sceneservice mesh.N ?')
lx.out('Selected Item count:', ItemCount)

if ItemCount == 1 or ItemCount == 0:
    SMO_SafetyCheck_AtLeast2MeshItemSelected = 0
    lx.eval('dialog.setup info')
    lx.eval('dialog.title {SMO Merge Items and Merge Border:}')
    lx.eval('dialog.msg {You must select at least 2 Mesh Item layer, in Item List, to run that script}')
    lx.eval('+dialog.open')
    lx.out('Only One Item Selected result:', SMO_SafetyCheck_AtLeast2MeshItemSelected)
    lx.out('script Stopped: Select at least 2 Mesh Item')
    sys.exit

elif ItemCount >= 2:
    SMO_SafetyCheck_AtLeast2MeshItemSelected = 1
    lx.out('At least 2 Mesh Item Selected:', SMO_SafetyCheck_AtLeast2MeshItemSelected)
    lx.out('script running: right amount of Mesh Item selected')
# --------------------  safety check 1 : Only One Item Selected --- END


if SMO_SafetyCheck_AtLeast2MeshItemSelected == 1:
    lx.eval('layer.mergeMeshes comp:true')
    lx.eval('select.type edge')
    # replay name:"Add Boundary"
    lx.eval('script.run hash:"macro.scriptservice:92663570022:macro"')
    lx.eval('select.convert type:vertex')
    # replay name:"Merge Vertices"
    lx.eval('!vert.merge range:fixed dist:"9.999999999999999e-06" disco:false')
    # replay name:"Drop Selection"
    lx.eval('select.drop vertex')
    # replay name:"Add Boundary"
    lx.eval('script.run hash:"macro.scriptservice:92663570022:macro"')
    # replay name:"Item"
    lx.eval('select.type item')
    # replay name:"Random Vertex Colour"
    lx.eval('ffr.randomRGBA')
    lx.eval('select.type edge')
    # replay name:"Select by Items"
    lx.eval('select.type item')

###############COPY/PASTE END Procedure#################
# Restore user Preferences:
if User_Pref_CopyDeselectChangedState == 1:
    lx.eval('pref.value application.copyDeSelection false')
    lx.out('"Deselect Elements after Copying" have been Restored')
if User_Pref_PasteSelectionChangedState == 1:
    lx.eval('pref.value application.pasteSelection false')
    lx.out('"Select Pasted Elements" have been Restored')
if User_Pref_PasteDeselectChangedState == 1:
    lx.eval('pref.value application.pasteDeSelection false')
    lx.out('"Deselect Elements Before Pasting" have been Restored')
########################################################

# python
"""
Name:         SMO_UnmergeUsingHardEdge.py

Purpose:      This script is designed to:
              Unmerge separate one Mesh ItemCount
              using the HardEdge as guide.
              (All Vertex Borders will be merged in the process)

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
lx.eval("user.defNew name:SMO_SafetyCheck_Only1MeshItemSelected type:integer life:momentary")
# --------------------  safety check 1 : Only One Item Selected --- START
ItemCount = lx.eval('query layerservice layer.N ? fg')
lx.out('Selected Item count:', ItemCount)

if ItemCount != 1:
    SMO_SafetyCheck_Only1MeshItemSelected = 0
    lx.eval('dialog.setup info')
    lx.eval('dialog.title {SMO Unmerge by HardEdge:}')
    lx.eval(
        'dialog.msg {You must only select the Mesh Item layer you are working on, in Item List, to run that script}')
    lx.eval('+dialog.open')
    lx.out('Only One Item Selected result:', SMO_SafetyCheck_Only1MeshItemSelected)
    lx.out('script Stopped: Select only one Mesh Item')
    sys.exit

else:
    SMO_SafetyCheck_Only1MeshItemSelected = 1
    lx.out('Only One Item Selected:', SMO_SafetyCheck_Only1MeshItemSelected)
    lx.out('script running: right amount of Mesh Item selected')
# --------------------  safety check 1 : Only One Item Selected --- END


if SMO_SafetyCheck_Only1MeshItemSelected == 1:
    lx.eval('select.type item')
    # replay name:"Convert to Hard Edge"
    lx.eval('hardedge.convert removeSMGP:true removeNorm:true')
    # replay name:"Select by Edge Hardness"
    lx.eval('hardedge.select type:hard')
    # replay name:"Split Edges"
    lx.eval('edge.split caps:false gap:"0.0"')
    # replay name:"Item"
    lx.eval('select.type item')
    lx.eval('layer.unmergeMeshes')
    lx.eval('view3d.sameAsActive state:false')
    lx.eval('view3d.shadingStyle style:shd1 bgmesh:inactive')
    # replay name:"Select Item by Type"
    lx.eval('select.itemType type:mesh')
    # replay name:"StitchGeoBoundaries.LXM"
    lx.eval('script.implicit name:"kit_SMO_CAD_TOOLS:MacroSmoluck/StitchGeoBoundaries.LXM"')
    # replay name:"Item"
    lx.eval('select.type item')
    lx.eval('select.drop item')

# -------------- COPY/PASTE END Procedure  -------------- #
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
# -------------------------------------------- #

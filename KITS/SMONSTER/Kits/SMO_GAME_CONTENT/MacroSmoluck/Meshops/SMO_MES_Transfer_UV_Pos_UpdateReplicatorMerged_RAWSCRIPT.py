# python
"""
Name:         SMO_Transfer_UV_Pos_UpdateReplicatorMerged.py

Purpose:	  This script is designed to:
			  Copy and Transfer Original UV's from a Backup
			  MeshItems to a set of Replicators Merged via MergeMesh

Author:       Franck ELISABETH
Website:      https://www.smoluck.com
Created:      29/03/2019
Copyright:    (c) Franck Elisabeth 2017-2022
"""

#import the necessary Python libraries
import lx, lxu, os, modo

# get selected items using TD SDK
scene = modo.Scene()
selectedItems = scene.selected
SOURCE_Mesh = scene.selectedByType('mesh')[0]
TARGET_Mesh = scene.selectedByType('mesh')[1]

# ------------------------------ #
# <----( DEFINE VARIABLES )----> #
# ------------------------------ #
#####--- Define the PolygonSelSet Name Prefix --- START ---#####
#####
lx.eval("user.defNew name:PolySelSetPrefixName type:string life:momentary")
PolySelSetPrefixName = 'TRANSUVPOS'
#####
#####--- Define the PolygonSelSet Name Prefix --- END ---#####


lx.out('<--- Item Selection Set Tag --->')
lx.out('<----------- START ------------>')

# check if exactly two Mesh Items are selected and raise an error if not
if len(selectedItems) != 2:
	raise Exception('Please select at least 2 Meshes')
	
if len(selectedItems) == 2:
	lx.eval('select.editSet TRANSUVPOS_ALL add {}')
	# lx.eval('select.drop item')
	
	# for this command we get the id of the first selected item to select it again
	lx.eval('select.item %s' % selectedItems[0].id)
	# Tag it using Selection Set
	lx.eval('select.editSet TRANSUVPOS_SOURCE add {}')
	lx.eval('select.drop item')
	
	lx.eval('select.useSet TRANSUVPOS_ALL select')
	lx.eval('select.useSet TRANSUVPOS_SOURCE deselect')
	lx.eval('select.editSet TRANSUVPOS_TARGET add {}')
	lx.eval('select.drop item')
	
lx.out('<------------ END ------------->')




## UV Map Selection Check ##
lx.out('<--- UV Map Safety Check --->')
lx.out('<---------- START ---------->')
	
# Get info about the selected UVMap.
UVmap_Selected = lx.evalN('query layerservice vmaps ? selected')
UVmap_SelectedN = len(lx.evalN('query layerservice vmaps ? selected'))
lx.out('Selected UV Map Index:', UVmap_SelectedN)

if UVmap_SelectedN < 1:
	lx.eval('dialog.setup info')
	lx.eval('dialog.title {Smoluck: Export MeshOp Rig to FBX Sequence:}')
	lx.eval('dialog.msg {You must have a UV map selected to run this script.}')
	lx.eval('dialog.open')
	sys.exit()

elif UVmap_SelectedN >= 1:
	lx.out('UV Map Selected')
	
UserUVMapName = lx.eval1('query layerservice vmap.name ? %s' %UVmap_Selected)
lx.out('USER UV Map Name:', UserUVMapName)	
	
lx.out('<----------- END ----------->')


## Clear UV Map for Target Mesh ##
lx.out('<--- Clear UV Map for Target --->')
lx.out('<------------ START ------------>')
try:
	lx.eval('select.useSet TRANSUVPOS_TARGET select')
	lx.eval('vertMap.clear txuv')
	lx.eval('select.drop item')
except:
	sys.exit()
lx.out('<------------- END ------------->')


## Set Polygon Mode and Select UV Map ##
lx.out('<--- Prepass Select UV Map --->')
lx.out('<----------- START ----------->')
try:
	lx.eval('select.typeFrom item;pivot;center;edge;polygon;vertex;ptag true')
	lx.eval('select.useSet TRANSUVPOS_SOURCE select')
	lx.eval('select.typeFrom polygon;edge;vertex;item;pivot;center;ptag true')
	# Set the active UV Map
	lx.eval('select.vertexMap {%s} txuv replace' % UserUVMapName)
	lx.eval('select.typeFrom item;pivot;center;edge;polygon;vertex;ptag true')
	lx.eval('select.drop item')
	
except RuntimeError:
	sys.exit()
	
lx.out('<----------- END ----------->')

lx.eval('select.useSet TRANSUVPOS_ALL select')									# Select back the Target and SOURCE Mesh
lx.eval('select.typeFrom polygon;edge;vertex;item;pivot;center;ptag true')		
	
try:
	lx.eval('select.useSet TRANSUVPOS_01 select')
	lx.eval('uv.transfer')
	lx.eval('select.useSet TRANSUVPOS_01 deselect')
except RuntimeError:
	pass
	
try:
	lx.eval('select.useSet TRANSUVPOS_02 select')
	lx.eval('uv.transfer')
	lx.eval('select.useSet TRANSUVPOS_02 deselect')
except RuntimeError:
	pass
	
try:
	lx.eval('select.useSet TRANSUVPOS_03 select')
	lx.eval('uv.transfer')
	lx.eval('select.useSet TRANSUVPOS_03 deselect')
except RuntimeError:
	pass
	
try:
	lx.eval('select.useSet TRANSUVPOS_04 select')
	lx.eval('uv.transfer')
	lx.eval('select.useSet TRANSUVPOS_04 deselect')
except RuntimeError:
	pass
	
try:
	lx.eval('select.useSet TRANSUVPOS_05 select')
	lx.eval('uv.transfer')
	lx.eval('select.useSet TRANSUVPOS_05 deselect')
except RuntimeError:
	pass
	
try:
	lx.eval('select.useSet TRANSUVPOS_06 select')
	lx.eval('uv.transfer')
	lx.eval('select.useSet TRANSUVPOS_06 deselect')
except RuntimeError:
	pass
	
try:
	lx.eval('select.useSet TRANSUVPOS_07 select')
	lx.eval('uv.transfer')
	lx.eval('select.useSet TRANSUVPOS_07 deselect')
except RuntimeError:
	pass
	
try:
	lx.eval('select.useSet TRANSUVPOS_08 select')
	lx.eval('uv.transfer')
	lx.eval('select.useSet TRANSUVPOS_08 deselect')
except RuntimeError:
	pass
	
try:
	lx.eval('select.useSet TRANSUVPOS_09 select')
	lx.eval('uv.transfer')
	lx.eval('select.useSet TRANSUVPOS_09 deselect')
except RuntimeError:
	pass
	
try:
	lx.eval('select.useSet TRANSUVPOS_10 select')
	lx.eval('uv.transfer')
	lx.eval('select.useSet TRANSUVPOS_10 deselect')
except RuntimeError:
	pass
############ 01-10 END ###########
	
	
try:
	lx.eval('select.useSet TRANSUVPOS_11 select')
	lx.eval('uv.transfer')
	lx.eval('select.useSet TRANSUVPOS_11 deselect')
except RuntimeError:
	pass
	
try:
	lx.eval('select.useSet TRANSUVPOS_12 select')
	lx.eval('uv.transfer')
	lx.eval('select.useSet TRANSUVPOS_12 deselect')
except RuntimeError:
	pass
	
try:
	lx.eval('select.useSet TRANSUVPOS_13 select')
	lx.eval('uv.transfer')
	lx.eval('select.useSet TRANSUVPOS_13 deselect')
except RuntimeError:
	pass
	
try:
	lx.eval('select.useSet TRANSUVPOS_14 select')
	lx.eval('uv.transfer')
	lx.eval('select.useSet TRANSUVPOS_14 deselect')
except RuntimeError:
	pass
	
try:
	lx.eval('select.useSet TRANSUVPOS_15 select')
	lx.eval('uv.transfer')
	lx.eval('select.useSet TRANSUVPOS_15 deselect')
except RuntimeError:
	pass
	
try:
	lx.eval('select.useSet TRANSUVPOS_16 select')
	lx.eval('uv.transfer')
	lx.eval('select.useSet TRANSUVPOS_16 deselect')
except RuntimeError:
	pass
	
try:
	lx.eval('select.useSet TRANSUVPOS_17 select')
	lx.eval('uv.transfer')
	lx.eval('select.useSet TRANSUVPOS_17 deselect')
except RuntimeError:
	pass
	
try:
	lx.eval('select.useSet TRANSUVPOS_18 select')
	lx.eval('uv.transfer')
	lx.eval('select.useSet TRANSUVPOS_18 deselect')
except RuntimeError:
	pass
	
try:
	lx.eval('select.useSet TRANSUVPOS_19 select')
	lx.eval('uv.transfer')
	lx.eval('select.useSet TRANSUVPOS_19 deselect')
except RuntimeError:
	pass
	
try:
	lx.eval('select.useSet TRANSUVPOS_20 select')
	lx.eval('uv.transfer')
	lx.eval('select.useSet TRANSUVPOS_20 deselect')
except RuntimeError:
	pass
############ 11-20 END ###########
	
try:
	lx.eval('select.useSet TRANSUVPOS_21 select')
	lx.eval('uv.transfer')
	lx.eval('select.useSet TRANSUVPOS_21 deselect')
except RuntimeError:
	pass
	
try:
	lx.eval('select.useSet TRANSUVPOS_22 select')
	lx.eval('uv.transfer')
	lx.eval('select.useSet TRANSUVPOS_22 deselect')
except RuntimeError:
	pass
	
try:
	lx.eval('select.useSet TRANSUVPOS_23 select')
	lx.eval('uv.transfer')
	lx.eval('select.useSet TRANSUVPOS_23 deselect')
except RuntimeError:
	pass
	
try:
	lx.eval('select.useSet TRANSUVPOS_24 select')
	lx.eval('uv.transfer')
	lx.eval('select.useSet TRANSUVPOS_24 deselect')
except RuntimeError:
	pass
	
try:
	lx.eval('select.useSet TRANSUVPOS_25 select')
	lx.eval('uv.transfer')
	lx.eval('select.useSet TRANSUVPOS_25 deselect')
except RuntimeError:
	pass
	
try:
	lx.eval('select.useSet TRANSUVPOS_26 select')
	lx.eval('uv.transfer')
	lx.eval('select.useSet TRANSUVPOS_26 deselect')
except RuntimeError:
	pass
	
try:
	lx.eval('select.useSet TRANSUVPOS_27 select')
	lx.eval('uv.transfer')
	lx.eval('select.useSet TRANSUVPOS_27 deselect')
except RuntimeError:
	pass
	
try:
	lx.eval('select.useSet TRANSUVPOS_28 select')
	lx.eval('uv.transfer')
	lx.eval('select.useSet TRANSUVPOS_28 deselect')
except RuntimeError:
	pass
	
try:
	lx.eval('select.useSet TRANSUVPOS_29 select')
	lx.eval('uv.transfer')
	lx.eval('select.useSet TRANSUVPOS_29 deselect')
except RuntimeError:
	pass
	
try:
	lx.eval('select.useSet TRANSUVPOS_30 select')
	lx.eval('uv.transfer')
	lx.eval('select.useSet TRANSUVPOS_30 deselect')
except RuntimeError:
	pass
############ 21-30 END ###########

	
try:
	lx.eval('select.useSet TRANSUVPOS_31 select')
	lx.eval('uv.transfer')
	lx.eval('select.useSet TRANSUVPOS_31 deselect')
except RuntimeError:
	pass
	
try:
	lx.eval('select.useSet TRANSUVPOS_32 select')
	lx.eval('uv.transfer')
	lx.eval('select.useSet TRANSUVPOS_32 deselect')
except RuntimeError:
	pass
	
try:
	lx.eval('select.useSet TRANSUVPOS_33 select')
	lx.eval('uv.transfer')
	lx.eval('select.useSet TRANSUVPOS_33 deselect')
except RuntimeError:
	pass
	
try:
	lx.eval('select.useSet TRANSUVPOS_34 select')
	lx.eval('uv.transfer')
	lx.eval('select.useSet TRANSUVPOS_34 deselect')
except RuntimeError:
	pass
	
try:
	lx.eval('select.useSet TRANSUVPOS_35 select')
	lx.eval('uv.transfer')
	lx.eval('select.useSet TRANSUVPOS_35 deselect')
except RuntimeError:
	pass
	
try:
	lx.eval('select.useSet TRANSUVPOS_36 select')
	lx.eval('uv.transfer')
	lx.eval('select.useSet TRANSUVPOS_36 deselect')
except RuntimeError:
	pass
	
try:
	lx.eval('select.useSet TRANSUVPOS_37 select')
	lx.eval('uv.transfer')
	lx.eval('select.useSet TRANSUVPOS_37 deselect')
except RuntimeError:
	pass
	
try:
	lx.eval('select.useSet TRANSUVPOS_38 select')
	lx.eval('uv.transfer')
	lx.eval('select.useSet TRANSUVPOS_38 deselect')
except RuntimeError:
	pass
	
try:
	lx.eval('select.useSet TRANSUVPOS_39 select')
	lx.eval('uv.transfer')
	lx.eval('select.useSet TRANSUVPOS_39 deselect')
except RuntimeError:
	pass
	
try:
	lx.eval('select.useSet TRANSUVPOS_40 select')
	lx.eval('uv.transfer')
	lx.eval('select.useSet TRANSUVPOS_40 deselect')
except RuntimeError:
	pass
############ 31-40 END ###########

	
try:
	lx.eval('select.useSet TRANSUVPOS_41 select')
	lx.eval('uv.transfer')
	lx.eval('select.useSet TRANSUVPOS_41 deselect')
except RuntimeError:
	pass
	
try:
	lx.eval('select.useSet TRANSUVPOS_42 select')
	lx.eval('uv.transfer')
	lx.eval('select.useSet TRANSUVPOS_42 deselect')
except RuntimeError:
	pass
	
try:
	lx.eval('select.useSet TRANSUVPOS_43 select')
	lx.eval('uv.transfer')
	lx.eval('select.useSet TRANSUVPOS_43 deselect')
except RuntimeError:
	pass
	
try:
	lx.eval('select.useSet TRANSUVPOS_44 select')
	lx.eval('uv.transfer')
	lx.eval('select.useSet TRANSUVPOS_44 deselect')
except RuntimeError:
	pass
	
try:
	lx.eval('select.useSet TRANSUVPOS_45 select')
	lx.eval('uv.transfer')
	lx.eval('select.useSet TRANSUVPOS_45 deselect')
except RuntimeError:
	pass
	
try:
	lx.eval('select.useSet TRANSUVPOS_46 select')
	lx.eval('uv.transfer')
	lx.eval('select.useSet TRANSUVPOS_46 deselect')
except RuntimeError:
	pass
	
try:
	lx.eval('select.useSet TRANSUVPOS_47 select')
	lx.eval('uv.transfer')
	lx.eval('select.useSet TRANSUVPOS_47 deselect')
except RuntimeError:
	pass
	
try:
	lx.eval('select.useSet TRANSUVPOS_48 select')
	lx.eval('uv.transfer')
	lx.eval('select.useSet TRANSUVPOS_48 deselect')
except RuntimeError:
	pass
	
try:
	lx.eval('select.useSet TRANSUVPOS_49 select')
	lx.eval('uv.transfer')
	lx.eval('select.useSet TRANSUVPOS_49 deselect')
except RuntimeError:
	pass
	
try:
	lx.eval('select.useSet TRANSUVPOS_50 select')
	lx.eval('uv.transfer')
	lx.eval('select.useSet TRANSUVPOS_50 deselect')
except RuntimeError:
	pass	
############ 41-50 END ###########	


try:
	lx.eval('select.useSet TRANSUVPOS_51 select')
	lx.eval('uv.transfer')
	lx.eval('select.useSet TRANSUVPOS_51 deselect')
except RuntimeError:
	pass
	
try:
	lx.eval('select.useSet TRANSUVPOS_52 select')
	lx.eval('uv.transfer')
	lx.eval('select.useSet TRANSUVPOS_52 deselect')
except RuntimeError:
	pass
	
try:
	lx.eval('select.useSet TRANSUVPOS_53 select')
	lx.eval('uv.transfer')
	lx.eval('select.useSet TRANSUVPOS_53 deselect')
except RuntimeError:
	pass
	
try:
	lx.eval('select.useSet TRANSUVPOS_54 select')
	lx.eval('uv.transfer')
	lx.eval('select.useSet TRANSUVPOS_54 deselect')
except RuntimeError:
	pass
	
try:
	lx.eval('select.useSet TRANSUVPOS_55 select')
	lx.eval('uv.transfer')
	lx.eval('select.useSet TRANSUVPOS_55 deselect')
except RuntimeError:
	pass
	
try:
	lx.eval('select.useSet TRANSUVPOS_56 select')
	lx.eval('uv.transfer')
	lx.eval('select.useSet TRANSUVPOS_56 deselect')
except RuntimeError:
	pass
	
try:
	lx.eval('select.useSet TRANSUVPOS_57 select')
	lx.eval('uv.transfer')
	lx.eval('select.useSet TRANSUVPOS_57 deselect')
except RuntimeError:
	pass
	
try:
	lx.eval('select.useSet TRANSUVPOS_58 select')
	lx.eval('uv.transfer')
	lx.eval('select.useSet TRANSUVPOS_58 deselect')
except RuntimeError:
	pass
	
try:
	lx.eval('select.useSet TRANSUVPOS_59 select')
	lx.eval('uv.transfer')
	lx.eval('select.useSet TRANSUVPOS_59 deselect')
except RuntimeError:
	pass
	
try:
	lx.eval('select.useSet TRANSUVPOS_60 select')
	lx.eval('uv.transfer')
	lx.eval('select.useSet TRANSUVPOS_60 deselect')
except RuntimeError:
	pass
############ 51-60 END ###########


try:
	lx.eval('select.useSet TRANSUVPOS_61 select')
	lx.eval('uv.transfer')
	lx.eval('select.useSet TRANSUVPOS_61 deselect')
except RuntimeError:
	pass
	
try:
	lx.eval('select.useSet TRANSUVPOS_62 select')
	lx.eval('uv.transfer')
	lx.eval('select.useSet TRANSUVPOS_62 deselect')
except RuntimeError:
	pass
	
try:
	lx.eval('select.useSet TRANSUVPOS_63 select')
	lx.eval('uv.transfer')
	lx.eval('select.useSet TRANSUVPOS_63 deselect')
except RuntimeError:
	pass
	
try:
	lx.eval('select.useSet TRANSUVPOS_64 select')
	lx.eval('uv.transfer')
	lx.eval('select.useSet TRANSUVPOS_64 deselect')
except RuntimeError:
	pass
	
try:
	lx.eval('select.useSet TRANSUVPOS_65 select')
	lx.eval('uv.transfer')
	lx.eval('select.useSet TRANSUVPOS_65 deselect')
except RuntimeError:
	pass
	
try:
	lx.eval('select.useSet TRANSUVPOS_66 select')
	lx.eval('uv.transfer')
	lx.eval('select.useSet TRANSUVPOS_66 deselect')
except RuntimeError:
	pass
	
try:
	lx.eval('select.useSet TRANSUVPOS_67 select')
	lx.eval('uv.transfer')
	lx.eval('select.useSet TRANSUVPOS_67 deselect')
except RuntimeError:
	pass
	
try:
	lx.eval('select.useSet TRANSUVPOS_68 select')
	lx.eval('uv.transfer')
	lx.eval('select.useSet TRANSUVPOS_68 deselect')
except RuntimeError:
	pass
	
try:
	lx.eval('select.useSet TRANSUVPOS_69 select')
	lx.eval('uv.transfer')
	lx.eval('select.useSet TRANSUVPOS_69 deselect')
except RuntimeError:
	pass
	
try:
	lx.eval('select.useSet TRANSUVPOS_70 select')
	lx.eval('uv.transfer')
	lx.eval('select.useSet TRANSUVPOS_70 deselect')
except RuntimeError:
	pass
############ 61-70 END ###########


try:
	lx.eval('select.useSet TRANSUVPOS_71 select')
	lx.eval('uv.transfer')
	lx.eval('select.useSet TRANSUVPOS_71 deselect')
except RuntimeError:
	pass
	
try:
	lx.eval('select.useSet TRANSUVPOS_72 select')
	lx.eval('uv.transfer')
	lx.eval('select.useSet TRANSUVPOS_72 deselect')
except RuntimeError:
	pass
	
try:
	lx.eval('select.useSet TRANSUVPOS_73 select')
	lx.eval('uv.transfer')
	lx.eval('select.useSet TRANSUVPOS_73 deselect')
except RuntimeError:
	pass
	
try:
	lx.eval('select.useSet TRANSUVPOS_74 select')
	lx.eval('uv.transfer')
	lx.eval('select.useSet TRANSUVPOS_74 deselect')
except RuntimeError:
	pass
	
try:
	lx.eval('select.useSet TRANSUVPOS_75 select')
	lx.eval('uv.transfer')
	lx.eval('select.useSet TRANSUVPOS_75 deselect')
except RuntimeError:
	pass
	
try:
	lx.eval('select.useSet TRANSUVPOS_76 select')
	lx.eval('uv.transfer')
	lx.eval('select.useSet TRANSUVPOS_76 deselect')
except RuntimeError:
	pass
	
try:
	lx.eval('select.useSet TRANSUVPOS_77 select')
	lx.eval('uv.transfer')
	lx.eval('select.useSet TRANSUVPOS_77 deselect')
except RuntimeError:
	pass
	
try:
	lx.eval('select.useSet TRANSUVPOS_78 select')
	lx.eval('uv.transfer')
	lx.eval('select.useSet TRANSUVPOS_78 deselect')
except RuntimeError:
	pass
	
try:
	lx.eval('select.useSet TRANSUVPOS_79 select')
	lx.eval('uv.transfer')
	lx.eval('select.useSet TRANSUVPOS_79 deselect')
except RuntimeError:
	pass
	
try:
	lx.eval('select.useSet TRANSUVPOS_80 select')
	lx.eval('uv.transfer')
	lx.eval('select.useSet TRANSUVPOS_80 deselect')
except RuntimeError:
	pass
############ 71-80 END ###########


try:
	lx.eval('select.useSet TRANSUVPOS_81 select')
	lx.eval('uv.transfer')
	lx.eval('select.useSet TRANSUVPOS_81 deselect')
except RuntimeError:
	pass
	
try:
	lx.eval('select.useSet TRANSUVPOS_82 select')
	lx.eval('uv.transfer')
	lx.eval('select.useSet TRANSUVPOS_82 deselect')
except RuntimeError:
	pass
	
try:
	lx.eval('select.useSet TRANSUVPOS_83 select')
	lx.eval('uv.transfer')
	lx.eval('select.useSet TRANSUVPOS_83 deselect')
except RuntimeError:
	pass
	
try:
	lx.eval('select.useSet TRANSUVPOS_84 select')
	lx.eval('uv.transfer')
	lx.eval('select.useSet TRANSUVPOS_84 deselect')
except RuntimeError:
	pass
	
try:
	lx.eval('select.useSet TRANSUVPOS_85 select')
	lx.eval('uv.transfer')
	lx.eval('select.useSet TRANSUVPOS_85 deselect')
except RuntimeError:
	pass
	
try:
	lx.eval('select.useSet TRANSUVPOS_86 select')
	lx.eval('uv.transfer')
	lx.eval('select.useSet TRANSUVPOS_86 deselect')
except RuntimeError:
	pass
	
try:
	lx.eval('select.useSet TRANSUVPOS_87 select')
	lx.eval('uv.transfer')
	lx.eval('select.useSet TRANSUVPOS_87 deselect')
except RuntimeError:
	pass
	
try:
	lx.eval('select.useSet TRANSUVPOS_88 select')
	lx.eval('uv.transfer')
	lx.eval('select.useSet TRANSUVPOS_88 deselect')
except RuntimeError:
	pass
	
try:
	lx.eval('select.useSet TRANSUVPOS_89 select')
	lx.eval('uv.transfer')
	lx.eval('select.useSet TRANSUVPOS_89 deselect')
except RuntimeError:
	pass
	
try:
	lx.eval('select.useSet TRANSUVPOS_90 select')
	lx.eval('uv.transfer')
	lx.eval('select.useSet TRANSUVPOS_90 deselect')
except RuntimeError:
	pass
############ 81-90 END ###########


lx.eval('select.itemType mesh')
lx.eval('!select.deleteSet SOURCE_MESH true')
lx.eval('!scene.save')
lx.eval('scene.close')
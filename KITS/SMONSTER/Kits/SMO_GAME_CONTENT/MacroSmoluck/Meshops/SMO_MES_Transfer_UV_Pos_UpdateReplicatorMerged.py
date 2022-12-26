# python
"""
# Name:         SMO_Transfer_UV_Pos_UpdateReplicatorMerged.py
# Version: 1.00
#
# Purpose: This script is designed to Copy and 
# Transfer Original UV's from a Backup MeshItems to a set of Replicators Merged via MergeMesh 
#
# Author:       Franck ELISABETH
# Website:      https://www.smoluck.com
#
# Created:      29/03/2019
# Modified:		01/04/2019
# Copyright:    (c) Franck Elisabeth 2017-2022
"""

#import the necessary Python libraries
import lx, lxu, os, modo

# get selected items using TD SDK
scene = modo.Scene()
selectedItems = scene.selectedByType('mesh')
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

	


lx.out('<--- Polygon Sel Set Counter --->')
lx.out('<------------ START ------------>')
## Polygon Sel Set Counter / Enumerator ##
## this step will test the PolySelSet count over the Target Mesh Only
try:
	lx.eval('select.useSet TRANSUVPOS_TARGET select')
	lx.eval('select.typeFrom polygon;edge;vertex;item;pivot;center;ptag true')
	# Select the main layer
	lx.eval('query layerservice layer.id ? main')
	# Number of Poly Sel Set
	PolySelSet_COUNT = lx.eval('query layerservice polset.N ? all')
	lx.out('<---Polygon Selection Set Total Count:--->')
	lx.out(PolySelSet_COUNT)
	# for i in range(PolySelSet_COUNT):
		# PolySelSet_NAME = lx.eval('query layerservice polset.name ? %s' %i)
		# lx.out('<---Polygon Selection Set Name:--->')
		# lx.out(PolySelSet_NAME)
		
except RuntimeError:
	sys.exit()
lx.out('<----------- END ----------->')



lx.out('<--- Transfer UV Position --->')
lx.out('<----------- START ---------->')
# Here we clear the current selection then select back the Target
lx.eval('select.typeFrom item;pivot;center;edge;polygon;vertex;ptag true')
lx.eval('select.useSet TRANSUVPOS_TARGET select')
lx.eval('select.typeFrom polygon;edge;vertex;item;pivot;center;ptag true')

for i in range(PolySelSet_COUNT):

	PolySelSet_NAME = lx.eval('query layerservice polset.name ? %s' %i)
	lx.out('<---Polygon Selection Set Name:--->')
	lx.out(PolySelSet_NAME)

	if PolySelSetPrefixName in PolySelSet_NAME:
		lx.eval('select.typeFrom item;pivot;center;edge;polygon;vertex;ptag true')		# Switch to Item Selection Mode
		lx.eval('select.drop item')														# Drop the current item Selection
		lx.eval('select.useSet TRANSUVPOS_ALL select')									# Select back the Target and SOURCE Mesh
		lx.eval('select.typeFrom polygon;edge;vertex;item;pivot;center;ptag true')		# Switch to Polygon Selection Mode
		lx.eval('select.useSet {%s} select' % PolySelSet_NAME)							# Select the current Poly Selection Set from the list 
		
		# #####------  safety check: at Least 4 Polygons are selected --- START #####
		# #CsPolys = len(mesh.geometry.polygons.selected)
		# CsPolys = lx.eval('query layerservice poly.N ? selected')
		# lx.out('Count Selected Poly',CsPolys)
		
		# if CsPolys < 4:
			# lx.out('Not enough Polygon selected to perform a Transfer UV Position:')
		# if CsPolys >= 4:
			# # Transfer UV Position using the current Selected Polygons
			# lx.eval('uv.transfer')														# Transfer UV Position using the current Selected Polygons
		
		lx.eval('uv.transfer')	
		lx.eval('select.useSet {%s} deselect' % PolySelSet_NAME)						# Deselect the current Poly Selection Set
lx.out('<----------- END ----------->')
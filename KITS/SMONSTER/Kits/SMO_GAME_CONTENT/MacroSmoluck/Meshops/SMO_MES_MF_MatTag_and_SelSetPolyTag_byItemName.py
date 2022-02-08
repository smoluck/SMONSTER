#python
#---------------------------------------
# Name:         SMO_MES_MF_MatTag_and_SelSetPolyTag_byItemName.py
# Version:      1.01
#
# Purpose:      This script is designed to create random
#               Materials and Selection Set (polygons) to the Sources of a selected MeshFusionItem
#               Select MeshFusion item and run. 
#
# Author:       Franck ELISABETH
# Website:      http://www.smoluck.com
#
# Created:      03/12/2018
# Modified:     19/03/2019
# Copyright:    (c) Franck Elisabeth 2017-2022
#---------------------------------------

#import the necessary Python libraries
import lx
import os
import modo
scene = modo.scene.current()
selSvc = lx.service.Selection ()

# Tag the current MeshFusion Item
lx.eval('select.editSet TEMP_ProcessedMFI add')

# Select the Sources Mesh of this MF Item
lx.eval('@SDF_StripHaul.pl 126')
lx.eval('unhide')
lx.eval('layer.setVisibility')
lx.eval('layer.setVisibility')
lx.eval('hide.unsel')

# Tag the Sources Mesh of this MF Item
lx.eval('select.editSet TEMP_ProcessedItem add')

# list the Sources Mesh
SelItems = (lx.evalN('query sceneservice selection ? mesh'))
# lx.out('In Selected items, List of their Unique Name is:',SelItems)

# For each selected item in the selected list of items
for item in SelItems:
    lx.eval('select.item %s set mesh' % item)
    currentLayerName = lx.eval('query layerservice layer.name ? selected')
    # lx.out('ITEM:',currentLayerName)
    lx.eval('select.editSet EditeddMeshLayer add {}')
    lx.eval('select.type polygon')
    lx.eval('deformer.selectBaseMesh select:true')
    lx.eval('select.type polygon')
    try:
        lx.eval('!!select.all')
        SelPolyCount = selSvc.Count (selSvc.LookupType (lx.symbol.sSELTYP_POLYGON))
        # lx.out('In Selected items, Polygon count selected:',SelPolyCount)
        if SelPolyCount >= 1:
            SMO_NoPolyBaseMesh = 0
        # lx.out('Polygon in BaseMesh: True')
    except:
        SMO_NoPolyBaseMesh = 1
        # lx.out('Polygon in BaseMesh: False')
    ##############################
    ####### SAFETY CHECK 1 #######
    ##############################
    #####--------------------  safety check 1: at Least 1 Polygons is selected --- START --------------------#####
    # SelPolyCount = selSvc.Count (selSvc.LookupType (lx.symbol.sSELTYP_POLYGON))
    # lx.out('In Selected items, Polygon count selected:',SelPolyCount)
    # lx.out('Count Selected Poly',CsPolys)
    #####--------------------  safety check 1: at Least 1 Polygons is selected --- END --------------------#####
    if SMO_NoPolyBaseMesh == 0:
        lx.eval('select.editSet {SelSet_%s} add' % currentLayerName)
        lx.eval('tagger.setMaterial_pTag {%s_mat} random selected material use' % currentLayerName) 
        lx.eval('select.type item')
    if SMO_NoPolyBaseMesh == 1:
        lx.eval('select.type item')
        lx.eval('deformer.selectBaseMesh select:false')
        lx.eval('meshop.create pmodel.materialTag.item')
        currentNodeID = (lx.evalN('query sceneservice selection ? all'))
        lx.out('Selected Node ID is:',currentNodeID)
        lx.eval('deformer.setGroup %s seq:0' % currentNodeID)
        lx.eval('item.channel pmodel.materialTag.item$materialName {%s_mat}' % currentLayerName )
        lx.eval('select.drop item')
        lx.eval('shader.create mask')
        lx.eval('mask.setPTag {%s_mat}' % currentLayerName)
        lx.eval('shader.create advancedMaterial')
        from random import randrange
        
        for mat_id in lx.evalN('query sceneservice selection ? advancedMaterial'):
            r, g, b = [randrange(0, 255, 10) / 255.0 for i in range(3)]
            try:
                lx.eval('!item.channel diffCol {%s %s %s} item:{%s}' %(r, g, b, mat_id))
            except RuntimeError: # diffuse amount is zero.
                pass
        lx.eval('select.drop item')
    lx.eval('select.useSet EditeddMeshLayer select')
    lx.eval('!select.deleteSet EditeddMeshLayer')

# Select back the Sources Mesh
lx.eval('select.useSet TEMP_ProcessedItem select')
lx.eval('deformer.selectBaseMesh select:false')
# delete the Tag for Sources Mesh
lx.eval('!select.deleteSet TEMP_ProcessedItem')
lx.eval('unhide')
lx.eval('select.drop item')
# Select back the MF Item and Delete is SelSet Tag
lx.eval('select.useSet TEMP_ProcessedMFI select')
lx.eval('!select.deleteSet TEMP_ProcessedMFI')
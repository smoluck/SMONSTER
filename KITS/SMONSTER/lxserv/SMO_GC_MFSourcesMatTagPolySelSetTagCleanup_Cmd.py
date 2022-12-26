# python
"""
# Name:         SMO_GC_MF_Sources_MatTag_PolySelSetTags_Cleanup_Cmd.py
# Version:      1.3
#
# Purpose:      This script is designed to:
#               Create random Materials and Selection Set (polygons)
#               to the SOURCES of the selected Mesh Fusion Item
#                   Each Mesh Layer will have is own:
#                       Material Tag                ==> "MeshName"_mat
#                       Polygon Selection Set       ==> SelSet_"MeshName"
# Select one Mesh Fusion Item and run. 
#
# Author:       Franck ELISABETH
# Website:      https://www.smoluck.com
#
# Created:      21/09/2019
# Copyright:    (c) Franck Elisabeth 2017-2022
"""

import lx
import lxu
import modo
import random

Cmd_Name = "smo.GC.MFSourcesMatTagPolySelSetTagCleanup"
# smo.GC.MFSourcesMatTagPolySelSetTagCleanup


class SMO_GC_MF_Sources_MatTag_PolySelSetTags_Cleanup_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)

    def cmd_Flags(self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO

    def cmd_Interact (self):
        pass

    def cmd_UserName (self):
        return 'SMO GC - MeshFusion - Sources Mat & PolySelSet Tags Cleanup'

    def cmd_Desc (self):
        return 'Rebuild the Sources Material Tag and Polygon Selection Set Tags of current MF Item.'

    def cmd_Tooltip (self):
        return 'Select the MF Item and run. Rebuild the Sources Material Tag and Polygon Selection Set Tags of current MF Item.'

    def cmd_Help (self):
        return 'https://twitter.com/sm0luck'

    def basic_ButtonName (self):
        return 'SMO GC - MeshFusion - Sources Mat & PolySelSet Tags Cleanup'

    def basic_Enable (self, msg):
        return True

    def basic_Execute(self, msg, flags):
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
        
        
        
        scene = modo.Scene()
        selSvc = lx.service.Selection ()
        
        # Tag the Sources Mesh of this MF Item
        lx.eval('select.editSet TEMP_ProcessedItem add')
        
        # list the Sources Mesh
        SelItems = (lx.evalN('query sceneservice selection ? mesh'))
        lx.out('In Selected items, List of their Unique Name is:',SelItems)
        
        # For each selected item in the selected list of items
        for item in SelItems:
            lx.eval('select.item %s set mesh' % item)
            currentLayerName = lx.eval('query layerservice layer.name ? selected')
            lx.out('ITEM mesh name:',currentLayerName)
            
            
            mesh = modo.Mesh()
            #Check for polys in layers
            if mesh.geometry.numPolygons == 0:
                lx.out('Item Mesh named %s is empty' % currentLayerName)
                ItemMeshIsEmpty = 1
            else:
                lx.out('Item Mesh named %s contains polygons.' % currentLayerName)
                ItemMeshIsEmpty = 0
            
            # Check for procedural  
            for mesh in scene.selectedByType('mesh'):
                print(mesh.name)
                print(mesh.index)
                lyr_svc = lx.service.Layer()
                #print('isProc: %s' % lyr_svc.IsProcedural(mesh.index))
            
            #check for command failure
            ItemIsDirectMod = 0
            try:
                lx.eval('select.type polygon')
                lx.eval('!!select.all')
                ItemIsDirectMod = 1
            except:
                ItemIsDirectMod = 0
            
            
            
            if ItemMeshIsEmpty == 0 and ItemIsDirectMod == 1:
                PMOD = 0
                lx.out('%s is a Direct Modeling Mesh.' % currentLayerName)
                lx.eval('select.type polygon')
                lx.eval('!!select.all')
                lx.eval('select.editSet {SelSet_%s} add' % currentLayerName)
                lx.eval('poly.setMaterial {%s_mat} {0,6 0,6 0,6} 0,8 0,04 true false' % currentLayerName)
                for items in scene.selectedByType('advancedMaterial')[:1]:
                    random_numR = random.random()
                    items.channel('diffCol.R').set(random_numR)
                    random_numG = random.random()
                    items.channel('diffCol.G').set(random_numG)
                    random_numB = random.random()
                    items.channel('diffCol.B').set(random_numB)
                lx.eval('select.type item')
            if ItemMeshIsEmpty == 1 and ItemIsDirectMod == 0:
                PMOD = 1
                lx.out('%s is a Procedural Modeling Mesh.' % currentLayerName)
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
        
        # Select back the Sources Mesh
        lx.eval('select.useSet TEMP_ProcessedItem select')
        # delete the Tag for Sources Mesh
        lx.eval('!select.deleteSet TEMP_ProcessedItem')
        lx.eval('unhide')
        lx.eval('select.drop item')
        # Select back the MF Item and Delete is SelSet Tag
        lx.eval('select.useSet TEMP_ProcessedMFI select')
        lx.eval('!select.deleteSet TEMP_ProcessedMFI')


    def cmd_Query(self, index, vaQuery):
        lx.notimpl()


lx.bless(SMO_GC_MF_Sources_MatTag_PolySelSetTags_Cleanup_Cmd, Cmd_Name)

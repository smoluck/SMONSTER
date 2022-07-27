#python
#---------------------------------------
# Name:         SMO_GC_MatTag_and_PolySelSetTags_Cleanup_Cmd.py
# Version:      1.01
#
# Purpose:      This script is designed to:
#               Create random Materials and Selection Set (polygons) to the selected Mesh Layers
#               Each Mesh Layer will have is own:
#                       Material Tag                ==> "MeshName"_mat
#                       Polygon Selection Set       ==> SelSet_"MeshName"
#
#               Select Mesh Layers and run. 
#
# Author:       Franck ELISABETH
# Website:      http://www.smoluck.com
#
# Created:      20/09/2019
# Copyright:    (c) Franck Elisabeth 2017-2022
#---------------------------------------

import lx, lxu, lxifc, os, modo, random

Cmd_Name = "smo.GC.MatTag.PolySelSetTag.Cleanup"
# smo.GC.MatTag.PolySelSetTag.Cleanup

class SMO_GC_MatTag_and_PolySelSetTags_Cleanup_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)

    def cmd_Flags(self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO

    def cmd_Interact (self):
        pass

    def cmd_UserName (self):
        return 'SMO GC - Mat and PolySelSet Tags Cleanup'

    def cmd_Desc (self):
        return 'Rebuild Material Tag and Polygon Selection Set Tags of current Mesh Layer selected.'

    def cmd_Tooltip (self):
        return 'Select one or multiple Mesh Layer and run. Rebuild Material Tag and Polygon Selection Set Tags of current Mesh Layer selected.'

    def cmd_Help (self):
        return 'https://twitter.com/sm0luck'

    def basic_ButtonName (self):
        return 'SMO GC - Mat and PolySelSet Tags Cleanup'

    def basic_Enable (self, msg):
        return True

    def basic_Execute(self, msg, flags):
        scene = modo.scene.current()
        selSvc = lx.service.Selection ()
        
        # list the Sources Mesh
        SelItems = (lx.evalN('query sceneservice selection ? mesh'))
        lx.out('In Selected items, List of their Unique Name is:',SelItems)
        
        # For each selected item in the selected list of items
        for item in SelItems:
            lx.eval('select.item %s set mesh' % item)
            currentLayerName = lx.eval('query layerservice layer.name ? selected')
            lx.out('ITEM:',currentLayerName)
            lx.eval('select.editSet EditeddMeshLayer add {}')
            lx.eval('select.type polygon')
            lx.eval('deformer.selectBaseMesh select:true')
            lx.eval('select.type polygon')
            try:
                lx.eval('!!select.all')
                SelPolyCount = selSvc.Count (selSvc.LookupType (lx.symbol.sSELTYP_POLYGON))
                lx.out('In Selected items, Polygon count selected:',SelPolyCount)
                if SelPolyCount >= 1:
                    SMO_NoPolyBaseMesh = 0
                lx.out('Polygon in BaseMesh: True')
            except:
                SMO_NoPolyBaseMesh = 1
                lx.out('Polygon in BaseMesh: False')
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
                lx.eval('poly.setMaterial {%s_mat} {0,6 0,6 0,6} 0,8 0,04 true false' % currentLayerName)
                for item in scene.selectedByType('advancedMaterial')[:1]:
                    random_numR = random.random()
                    item.channel('diffCol.R').set(random_numR)
                    random_numG = random.random()
                    item.channel('diffCol.G').set(random_numG)
                    random_numB = random.random()
                    item.channel('diffCol.B').set(random_numB)
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
        
    
    def cmd_Query(self, index, vaQuery):
        lx.notimpl()


lx.bless(SMO_GC_MatTag_and_PolySelSetTags_Cleanup_Cmd, Cmd_Name)

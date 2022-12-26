# python
"""
# Name:         SMO_GC_RebuildSelectedItemsViaPolyline_Cmd
# Version:      1.0
#
# Purpose:      This script is designed to
#               Merge Selected Items and recreate a Polyline from the resulting edges.
#               Delete the original Data.
#
# Author:       Franck ELISABETH (with the help of Tom Dymond for debug)
# Website:      https://www.smoluck.com
#
# Created:      18/09/2020
# Copyright:    (c) Franck Elisabeth 2017-2022
"""

import lx
import lxu
import modo

Cmd_Name = "smo.GC.RebuildSelectedItemsViaPolyline"
# smo.GC.RebuildSelectedItemsViaPolyline


class SMO_GC_RebuildSelectedItemsViaPolyline_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
        self.dyna_Add("Incremental Save Mode", lx.symbol.sTYPE_INTEGER)
        self.basic_SetFlags (0, lx.symbol.fCMDARG_OPTIONAL)
    
    def cmd_Flags(self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO
    
    def cmd_Interact (self):
        pass
    
    def cmd_UserName (self):
        return 'SMO GC - Rebuild selected Items Via Polyline'
    
    def cmd_Desc (self):
        return 'Merge Selected Items and recreate a Polyline from the resulting edges. Delete the original Data.'
    
    def cmd_Tooltip (self):
        return 'Merge Selected Items and recreate a Polyline from the resulting edges. Delete the original Data.'
    
    def cmd_Help (self):
        return 'https://twitter.com/sm0luck'
    
    def basic_ButtonName (self):
        return 'SMO GC - Rebuild selected Items Via Polyline'
    
    def basic_Enable (self, msg):
        return True
    
    def basic_Execute(self, msg, flags):
        scene = modo.Scene()
        lx.eval('layer.mergeMeshes false')
        
        ItemUniqueName = lx.eval('query layerservice layer.id ? main')# store the Unique name of the current mesh layer
        #lx.out('Item Unique Name:', ItemUniqueName)
        
        lx.eval('select.type edge')
        lx.eval('select.all')
        
        lx.eval('pmodel.edgeToCurveCMD polyline true')
        lx.eval('select.drop item')
        
        lx.eval('select.subItem %s set mesh;replicator;meshInst;camera;light;txtrLocator;backdrop;groupLocator;replicator;surfGen;locator;falloff;deform;locdeform;weightContainer;morphContainer;deformGroup;deformMDD2;ABCStreamingDeformer;morphDeform;itemInfluence;genInfluence;deform.push;deform.wrap;softLag;ABCCurvesDeform.sample;ABCdeform.sample;force.root;baseVolume;chanModify;itemModify;meshoperation;chanEffect;defaultShader;defaultShader 0 0' % ItemUniqueName)
        lx.eval('!delete')
        
    
    def cmd_Query(self, index, vaQuery):
        lx.notimpl()


lx.bless(SMO_GC_RebuildSelectedItemsViaPolyline_Cmd, Cmd_Name)

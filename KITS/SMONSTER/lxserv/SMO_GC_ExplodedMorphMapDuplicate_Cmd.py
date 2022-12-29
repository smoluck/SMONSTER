# python
"""
Name:         SMO_GC_ExplodedMorphMapDuplicate_Cmd.py

Purpose:      This script is designed to
              Duplicate the Current Selected Mesh, Rename the mesh with a Suffix "_EXPLODE"
              then Create the Morph Influence out of the current selected Morph Map
              and Freeze the deformation / delete the morph map in order to export it.

Author:       Franck ELISABETH (with the help of Tom Dymond for debug)
Website:      https://www.smoluck.com
Created:      09/07/2020
Copyright:    (c) Franck Elisabeth 2017-2022
"""

import lx
import lxu
import modo
import sys

Cmd_Name = "smo.GC.ExplodedMorphMapDuplicate"
# smo.GC.ExplodedMorphMapDuplicate


class SMO_GC_ExplodedMorphMapDuplicate_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)

    def cmd_Flags(self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO

    def cmd_Interact (self):
        pass

    def cmd_UserName (self):
        return 'SMO GC - Exploded MorphMap of current Mesh as Duplicated'

    def cmd_Desc (self):
        return 'Duplicate the Current Selected Mesh, Rename the mesh with a Suffix "_EXPLODE" then Create the Morph Influence out of the current selected Morph Map and Freeze the deformation / delete the morph map in order to export it.'

    def cmd_Tooltip (self):
        return 'Duplicate the Current Selected Mesh, Rename the mesh with a Suffix "_EXPLODE" then Create the Morph Influence out of the current selected Morph Map and Freeze the deformation / delete the morph map in order to export it.'

    def cmd_Help (self):
        return 'https://twitter.com/sm0luck'

    def basic_ButtonName (self):
        return 'SMO GC - Exploded MorphMap of current Mesh as Duplicated'

    def basic_Enable (self, msg):
        return True

    def basic_Execute(self, msg, flags):
        scene = modo.scene.current()
        mesh = scene.selectedByType('mesh')[0]
        selitems = len(lx.evalN('query sceneservice selection ? locator'))
        lx.out('selitems',selitems)
        
        
        
        ##################################################################
        # <----( Main Macro )----> Create the Duplicated Exploded Mesh ##
        ##################################################################
        
        lx.eval('select.type item')
        
        if selitems < 1:
            lx.eval('dialog.setup info')
            lx.eval('dialog.title {SMO ExplodedMorphMapDuplicate:}')
            lx.eval('dialog.msg {"You must have a mesh item selected to run this script.}')
            lx.eval('+dialog.open')
            sys.exit()
        
        
        if selitems >= 1:
            Item_Name = lx.eval('item.name ? xfrmcore')
            lx.out('Item name', Item_Name)
            ExplodeItemName = Item_Name + '_' + 'EXPLODED'
            lx.eval('item.duplicate false locator false true')
            lx.eval('item.name {%s} xfrmcore' % ExplodeItemName)
            lx.eval('select.editSet EXPLODED_MESH add')
            
            lx.eval('item.addDeformer morphDeform')
            lx.eval('layer.setVisibility')
            lx.eval('select.drop item')
            lx.eval('select.useSet EXPLODED_MESH select')
            lx.eval('deformer.freeze false')
            
            lx.eval('smo.GC.ClearSelectionVmap 1 1')
            lx.eval('smo.GC.ClearSelectionVmap 2 1')
            lx.eval('smo.GC.ClearSelectionVmap 8 1')
            lx.eval('!!vertMap.delete EXPLODED')
            lx.eval('!select.deleteSet EXPLODED_MESH')
        

lx.bless(SMO_GC_ExplodedMorphMapDuplicate_Cmd, Cmd_Name)

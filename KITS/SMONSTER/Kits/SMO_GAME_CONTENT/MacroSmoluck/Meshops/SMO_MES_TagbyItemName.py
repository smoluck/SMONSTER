# python
"""
Name:         SMO_MES_TagbyItemName.py

Purpose:      This script is designed to:
              create random Materials and Selection Set (polygons) to each selected Mesh
              Select a list of mesh layer and run.

Author:       Franck ELISABETH
Website:      https://www.linkedin.com/in/smoluck/
Created:      03/12/2018
Copyright:    (c) Franck Elisabeth 2017-2022
"""

import lx
import modo

scene = modo.scene.current()

# For each selected item in the selected list of items
for item_ident in selected_meshes:
    # Select only that item.
    lx.eval('select.item %s set mesh' % item_ident)
    currentLayerName = lx.eval('query layerservice layer.name ? selected')
    lx.eval('select.type polygon')
    lx.eval('select.all')
    lx.eval('select.editSet {SelSet_%s} add' % currentLayerName)
    lx.eval('tagger.setMaterial_pTag {%s_mat} random selected material use' % currentLayerName) 
    lx.eval('select.type item')
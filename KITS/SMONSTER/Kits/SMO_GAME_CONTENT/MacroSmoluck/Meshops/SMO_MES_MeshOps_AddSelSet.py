# python
"""
# Name:         SMO_MeshOps_AddSelSet.py
# Version: 1.0
#
# Purpose: 
#
#
# Author:       Franck ELISABETH
# Website:      https://www.smoluck.com
#
# Created:      03/02/2019
# Copyright:    (c) Franck Elisabeth 2017-2022
"""
import modo
import lx

scene = modo.scene.current()
mesh = scene.selectedByType('mesh')[0]

try:
    #Name = lx.eval('query layerservice layer.name ?')
    #lx.out('Item name is',Name)
    #LayerIndex = lx.eval('query layerservice layer.index ?')
    #lx.out('Layer index is',LayerIndex)
    #LayerID = lx.eval('query layerservice layer.id ?')
    #lx.out('Layer ID is',LayerID)
    CurrentMesh = lx.eval('query sceneservice selection ? mesh')
    lx.out('Current Mesh is',CurrentMesh)
	
    
except:
    lx.eval('sys.exit()')
    lx.out('error in the script')



lx.eval('meshop.create type:"assignselectionset.meshop.item"')

try:
    CurrentSchem = lx.eval('query sceneservice schmNode ?')
    lx.out('Current Schematic is',CurrentSchem)
    # Command Block Begin: 
    lx.eval('select.drop type:schmNode')
    lx.eval('select.drop type:link')  
    lx.eval('schematic.addItem "%s" "%s" true 6.0 5.0' % CurrentMesh)
    # Command Block End:
    
except:
    lx.eval('sys.exit()')
    lx.out('error in the script')
# python
"""
Name:           SMO_UV_CheckUVbyArg.py

Purpose:        This script is designed to:
                Search if a specific UV Map exist, select it and rename it
                via String Argument.

Author:         Franck ELISABETH
Website:        https://www.linkedin.com/in/smoluck/
Created:        18/01/2019
Copyright:      (c) Franck Elisabeth 2017-2022
"""

import lx
import modo

scene = modo.scene.current()
meshitems = [item for item in scene.items() if item.type == "mesh"]

# ------------- ARGUMENTS ------------- #
# RenameByDefault = 1
# SearchString = "UVChannel_1"
# TargetString = "TargetUVMap"
# ------------- ARGUMENTS ------------- #
# args = lx.args()
# lx.out(args)

# RenameByDefault = bool(args[0])
# lx.out('Rename by user default UVMap name:', RenameByDefault)

# SearchString = string(args[1])
# lx.out('Searched UVMap name:', SearchString)

# TargetString = string(args[2])
# lx.out('Target UVMap name:', TargetString)
# ------------- ARGUMENTS ------------- #


# Get the default UV Map name of the user
DefaultUVMapName =  lx.eval('pref.value application.defaultTexture ?')
lx.out('Current Default UV Map name:', DefaultUVMapName)


for item in meshitems:
    item.select(True)
    if item.geometry.vmaps.uvMaps:
        # print('number of UV maps: ', len(item.geometry.vmaps.uvMaps))
        UVMapCount = lx.evalN('query layerservice vmaps.N ? texture')
        lx.out('UV map Count:', UVMapCount)
        # Get the name of UV Seam map available on mesh
        DetectedVMapName = lx.eval('vertMap.list uvMaps ?')
        lx.out('UVmap Name:', DetectedVMapName)
        # Returns true if the vertex map is selected. 
        uvmaps = lx.evalN('query layerservice vmaps ? texture')
        lx.out('UVmap Name:', uvmaps)
        for uvmap in uvmaps:
            uvmap_name = lx.eval('query layerservice vmap.name ? %s' % uvmap)
            lx.out('UVmap Name :', uvmap_name)
            if UVMapCount == 1 :
                lx.eval('select.vertexMap {%s} txuv replace' % uvmap_name)
                lx.eval('vertMap.rename {%s} {%s} txuv active' % (uvmap_name, DefaultUVMapName))
    elif not item.geometry.vmaps.uvMaps:
        lx.eval('?vertMap.new {%s} txuv' % DefaultUVMapName)
        lx.eval('select.vertexMap {%s} txuv remove' % DefaultUVMapName)


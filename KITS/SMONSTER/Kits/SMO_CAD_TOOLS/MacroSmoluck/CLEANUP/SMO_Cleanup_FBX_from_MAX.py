# python
"""
Name:         SMO_Cleanup_FBX_from_MAX

Purpose:      This script is designed to:
              Cleanup Files that comes from 3DS MAX:
              Removing custom user channels
              Cleanup Mesh Topology
              Consolidate materials using Tagger command

Author:       Franck ELISABETH
Website:      https://www.linkedin.com/in/smoluck/
Created:      30/05/2019
Copyright:    (c) Franck Elisabeth 2017-2022
"""

import lx
import modo

lx.eval('!tagger.shaderTree_consolidateByColor')

lx.eval('!tagger.pTagRemoveAll part scene')

lx.eval('select.itemType mesh')

lx.eval('!mesh.cleanup true mergeVertex:false')

# -------------- 1 --------------
lx.eval('select.drop item')
lx.eval('select.itemType mesh')
# Select current scene for query.
lx.eval('query sceneservice scene.index ? current')
# Get ID list of locator type items selected in the scene.
myitemsID = lx.evalN('query sceneservice selection ? locator')


def uNameItem():
    item = modo.item.Item()
    return item.UniqueName()

# Seek in the list.
for eachItem in myitemsID:
    selItem = uNameItem()
    lx.out(selItem)
    # Select the FBX_mrdisplacementmethod channel, if it exists.
    lx.eval('select.channel {%s:FBX_mrdisplacementmethod} add' % selItem)
lx.eval('channel.delete')
lx.eval('select.drop item')


# -------------- 2 --------------
lx.eval('select.drop item')
lx.eval('select.itemType mesh')
# Select current scene for query.
lx.eval('query sceneservice scene.index ? current')
# Get ID list of locator type items selected in the scene.
myitemsID = lx.evalN('query sceneservice selection ? locator')

# Seek in the list.
for eachItem in myitemsID:
    selItem = uNameItem()
    lx.out(selItem)
    # Select the FBX_mrdisplacementedgelength channel, if it exists.
    lx.eval('select.channel {%s:FBX_mrdisplacementedgelength} add' % selItem)
lx.eval('channel.delete')
lx.eval('select.drop item')


# -------------- 3 --------------
lx.eval('select.drop item')
lx.eval('select.itemType mesh')
# Select current scene for query.
lx.eval('query sceneservice scene.index ? current')
# Get ID list of locator type items selected in the scene.
myitemsID = lx.evalN('query sceneservice selection ? locator')

# Seek in the list.
for eachItem in myitemsID:
    selItem = uNameItem()
    lx.out(selItem)
    # Select the FBX_mrdisplacementmaxdisplace channel, if it exists.
    lx.eval('select.channel {%s:FBX_mrdisplacementmaxdisplace} add' % selItem)
lx.eval('channel.delete')
lx.eval('select.drop item')


# -------------- 4 --------------
lx.eval('select.itemType mesh')
# Select current scene for query.
lx.eval('query sceneservice scene.index ? current')
# Get ID list of locator type items selected in the scene.
myitemsID = lx.evalN('query sceneservice selection ? locator')

# Seek in the list.
for eachItem in myitemsID:
    selItem = uNameItem()
    lx.out(selItem)
    # Select the FBX_mrdisplacementparametricsubdivisionlevel channel, if it exists.
    lx.eval('select.channel {%s:FBX_mrdisplacementparametricsubdivisionlevel} add' % selItem)
lx.eval('channel.delete')
lx.eval('select.drop item')


# -------------- 5 --------------
lx.eval('select.itemType mesh')
# Select current scene for query.
lx.eval('query sceneservice scene.index ? current')
# Get ID list of locator type items selected in the scene.
myitemsID = lx.evalN('query sceneservice selection ? locator')

# Seek in the list.
for eachItem in myitemsID:
    selItem = uNameItem()
    lx.out(selItem)
    # Select the FBX_MaxHandle channel, if it exists.
    lx.eval('select.channel {%s:FBX_MaxHandle} add' % selItem)
lx.eval('channel.delete')
lx.eval('select.drop item')
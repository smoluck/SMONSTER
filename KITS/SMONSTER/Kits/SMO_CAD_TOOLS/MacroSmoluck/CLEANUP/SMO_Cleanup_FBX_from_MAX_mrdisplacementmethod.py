#python
#---------------------------------------
# Name:         SMO_Cleanup_FBX_from_MAX
# Version: 1.0
#
# Purpose:      This script is designed to:
#               Cleanup Files that comes from 3DS MAX:
#               Removing custom user channels
#               Cleanup Mesh Topology
#               Consolidate materials using Tagger command
#
#
# Author:       Franck ELISABETH
# Website:      http://www.smoluck.com
#
# Created:      30/05/2019
# Copyright:    (c) Franck Elisabeth 2017-2022
#---------------------------------------
import lx, modo


########################### 1 ############################
lx.eval('select.drop item')
lx.eval('select.itemType mesh')
# Select current scene for query.
lx.eval('query sceneservice scene.index ? current')
# Get ID list of locator type items selected in the scene.
myitemsID = lx.evalN('query sceneservice selection ? locator')

# Seek in the list.
for eachItem in myitemsID:
	def uNameItem():
		item = modo.item.Item()
		return item.UniqueName()
	selItem = uNameItem()
	lx.out(selItem)
	# Select the FBX_mrdisplacementmethod channel, if it exists.
	lx.eval('select.channel {%s:FBX_mrdisplacementmethod} add' % selItem)
# lx.eval('channel.delete')
# lx.eval('select.drop item')

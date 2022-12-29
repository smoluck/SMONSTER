# python
"""
Name:           SMO_Cleanup_DeleteChannels.py

Purpose:        This script is designed to:
                Test the channel created in the current selected mesh
                and delete a defined channel if it exists (via string Argument)

Author:         Franck ELISABETH
Website:        https://www.smoluck.com
Created:        14/02/2020
Copyright:      (c) Franck Elisabeth 2017-2022
"""

import lx
import modo

scene = modo.scene.current()

# ------------- ARGUMENTS Test
Search_name = "FBX_MaxHandle"
# ------------- ARGUMENTS ------------- #

# ------------- ARGUMENTS ------------- #
# args = lx.args()
# lx.out(args)

# Search_name = string(args[0])
# lx.out('Channel Name to delete:', Search_name)
# ------------- ARGUMENTS ------------- #


selected_Meshes = lx.evalN('query sceneservice selection ? mesh')
copied_channels = []
lx.eval('query sceneservice scene.index ? current')  # ensures current scene is 'selected'
for item_index in range(lx.eval('query sceneservice item.N ?')):  # item.N is number of items
    item = lx.eval('query sceneservice item.id ? %s' % item_index)  # sets 'item' to the item ID
    for channel_index in lx.evalN('query sceneservice channel.selection ?'):
        name = lx.eval('query sceneservice channel.name ? %s' % channel_index)
        # evalType = lx.eval('query sceneservice channel.type ? %s' % channel_index)
        try:
            username = lx.eval('channel.username username:?')
        except:
            username = name

        lx.out('item:', item)
        # lx.out('channel type:', evalType)
        # lx.out('channel name:', name)
        lx.out('channel ID:', channel_index)
        # print  (item)
        # print  (evalType)
        # print  (name)
        # print  (channel_index)
        lx.eval('select.channel {%s:%s} add' % (item, Search_name))
        lx.eval('channel.delete')

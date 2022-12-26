# python
"""
# Name:         SMO_DeleteChan.py
# Version:      1.0
#
# Purpose:      This script is designed to:
#               Search if a specific channel exist
#               via String Argument and delete it
#
# Author:       Franck ELISABETH
# Website:      https://www.smoluck.com
#
# Created:      17/02/2020
# Copyright:    (c) Franck Elisabeth 2017-2022
"""

import modo
import lx

scn = modo.Scene()


# # ------------- ARGUMENTS ------------- #
args = lx.args()
lx.out(args)

SearchString=  args[0]
lx.out('Searched String chain:', SearchString)
# # ------------- ARGUMENTS ------------- #

# SearchString = 'FBX_UDP3DSMAX'
for mesh in scn.items('mesh'):
    for channelName in mesh.channelNames:
        if channelName.startswith('%s' % SearchString ):
            try:
                lx.eval('select.channel {%s:%s} set' % (mesh.id, channelName))
                lx.eval('channel.delete')
            except:
                pass
# python
"""
Name:           SMO_MES_Add_EdgeExtrudeMeshOp.py

Purpose:		This script is designed to:
                Add an Edge Extrude Meshop and add it to the Schematic.

Author:         Franck ELISABETH
Website:        https://www.linkedin.com/in/smoluck/
Created:        07/03/2019
Copyright:      (c) Franck Elisabeth 2017-2022
"""

import lx
import modo
import sys

# -------------------------------------------- #
# <----( Specific Action )----> #
# -------------------------------------------- #
try:
    lx.eval('meshop.create edge.extrude.item')

except:
    sys.exit
# -------------------------------------------- #
# <----( Specific Action )----> #
# -------------------------------------------- #

sel_svc = lx.service.Selection()
selItem = modo.Scene().selected
chan_transpacket = lx.object.ChannelPacketTranslation(sel_svc.Allocate(lx.symbol.sSELTYP_CHANNEL))

bDoChannels = True

for item in selItem:
    lx.eval("schematic.addItem {%s}" % item.name)

if bDoChannels:
    chanType = lx.symbol.sSELTYP_CHANNEL
    pktID = sel_svc.LookupType(chanType)
    numChanns = sel_svc.Count(pktID)
    for chanId in range(0, numChanns):
        c = sel_svc.ByIndex(pktID, chanId)
        i = lx.object.Item(chan_transpacket.Item(c))
        chan_idx = chan_transpacket.Index(c)
        cName = item.ChannelName(chan_idx)
        lx.eval("schematic.addChannel chanIdx:{%s}" % cName)

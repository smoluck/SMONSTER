# python
"""
# Name:         SMO_MES_Add_DefFolder.py
# Version:      1.0
#
# Purpose:      This script is designed to:
#               Add a Deform Folder and add it to the Schematic.
#
# Author:       Franck ELISABETH
# Website:      https://www.smoluck.com
#
# Created:      07/03/2019
# Copyright:    (c) Franck Elisabeth 2017-2022
"""

import modo

sel_svc = lx.service.Selection()
selItem = modo.Scene().selected
chan_transpacket = lx.object.ChannelPacketTranslation(sel_svc.Allocate(lx.symbol.sSELTYP_CHANNEL))



for item in selItem:
  lx.eval("schematic.addItem {%s}" % item.name)
    
bDoChannels = True
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

###################################
# <----( Specific Action )----> #
###################################
try:
    lx.eval('schematic.deformerCreate deformFolder')
    
except:
    sys.exit
###################################
# <----( Specific Action )----> #
###################################

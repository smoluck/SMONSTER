# python
"""
# Name:         SMO_MATH_MeasureSpeed.py
# Version: 1.0
#
# Purpose: Add a Square Root node.
#
# Author:       Franck ELISABETH
# Website:      https://www.smoluck.com
#
# Created:      28/10/2019
# Copyright:    (c) Franck Elisabeth 2017-2022
"""

import modo

###################################
# <----( Specific Action )----> #
###################################
try:
    lx.eval('modifier.create cmSpeed insert:true')
    lx.eval('select.editSet Temp_MathNode add')
except:
    sys.exit
###################################
# <----( Specific Action )----> #
###################################

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

lx.eval('select.useSet Temp_MathNode select')
lx.eval('!select.deleteSet Temp_MathNode')
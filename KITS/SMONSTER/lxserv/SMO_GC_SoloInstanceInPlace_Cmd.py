# python
# ---------------------------------------
# Name:         SMO_GC_SoloInstanceInPlace_Cmd.py
# Version:      1.0
#
# Purpose:      This script is designed to
#               Duplicate the current item and Unlink the transform from the Source mesh/item.
#
#
# Author:       Franck ELISABETH (with the help of Pavel Efimov)
# Website:      http://www.smoluck.com
#
# Created:      16/04/2021
# Copyright:    (c) Franck Elisabeth 2017-2022
# ---------------------------------------

import lx, lxu, modo

Cmd_Name = "smo.GC.SoloInstanceInPlace"
# smo.GC.SoloInstanceInPlace

class SMO_GC_SoloInstanceInPlace_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
    
    def cmd_Flags(self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO
    
    def cmd_Interact(self):
        pass
    
    def cmd_UserName(self):
        return 'SMO GC - Solo Instance In Place'
    
    def cmd_Desc(self):
        return 'Instance the current item and Unlink the transform from the Source mesh/item then select back the Source Mesh.'
    
    def cmd_Tooltip(self):
        return 'Instance the current item and Unlink the transform from the Source mesh/item then select back the Source Mesh.'
    
    def cmd_Help(self):
        return 'https://twitter.com/sm0luck'
    
    def basic_ButtonName(self):
        return 'SMO GC - Solo Instance In Place'
    
    def basic_Enable(self, msg):
        return True
    
    def basic_Execute(self, msg, flags):
        scene = modo.scene.current()
        selected_Items = lxu.select.ItemSelection().current()
        lx.eval('item.duplicate true locator false false')
        NewInstances = lxu.select.ItemSelection().current()
        for i in range(len(NewInstances)) :
            scene.select(NewInstances[i])
            lx.eval('smo.GC.ClearTransformLink')
        lx.eval('smo.GC.DeselectAll')
        scene.select(selected_Items)

            
lx.bless(SMO_GC_SoloInstanceInPlace_Cmd, Cmd_Name)

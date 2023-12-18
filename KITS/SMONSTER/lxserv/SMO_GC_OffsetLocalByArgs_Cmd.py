# python
"""
Name:         SMO_GC_OffsetLocalByArgs_Cmd.py

Purpose:      This script is designed to:
              Move the current Selection by a specific distance in Float on X Y Z.

Author:       Franck ELISABETH (with the help of James O'Hare)
Website:      https://www.linkedin.com/in/smoluck/
Created:      28/03/2021
Copyright:    (c) Franck Elisabeth 2017-2022
"""

import lx
import lxu

Cmd_Name = "smo.GC.OffsetLocalByArgs"
# smo.GC.OffsetLocalByArgs 0.101382531226 0.0613391231745 0.00526303052902


class SMO_GC_OffsetLocalByArgs_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
        self.dyna_Add("Position X", lx.symbol.sTYPE_FLOAT)
        self.basic_SetFlags (0, lx.symbol.fCMDARG_OPTIONAL)
        self.dyna_Add("Position Y", lx.symbol.sTYPE_FLOAT)
        self.basic_SetFlags (1, lx.symbol.fCMDARG_OPTIONAL)
        self.dyna_Add("Position Z", lx.symbol.sTYPE_FLOAT)
        self.basic_SetFlags (2, lx.symbol.fCMDARG_OPTIONAL)
        
    def cmd_Flags(self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO
    
    def cmd_Interact (self):
        pass
    
    def cmd_UserName (self):
        return 'SMO GC - Offset Locally by Arguments'
    
    def cmd_Desc (self):
        return 'Move the current Selection by a specific distance in Float on X Y Z.'
    
    def cmd_Tooltip (self):
        return 'Move the current Selection by a specific distance in Float on X Y Z.'
    
    def cmd_Help (self):
        return 'https://twitter.com/sm0luck'
    
    def basic_ButtonName (self):
        return 'SMO GC - Offset Locally by Arguments'
    
    def basic_Enable (self, msg):
        return True
    
    def basic_Execute(self, msg, flags):
        
        F_X = self.dyna_Float (0)
        F_Y = self.dyna_Float (1)
        F_Z = self.dyna_Float (2)
        print('Move Float Values')
        print(F_X)
        print(F_Y)
        print(F_Z)
        
        Instance = (lx.eval('query sceneservice selection ? locator'))
        print(Instance)
        lx.eval('select.item %s add' % Instance)
        # lx.eval('item.refSystem %s' % InstancesNameList[i])
        lx.eval('item.create locator')
        Locator = (lx.eval('query sceneservice selection ? locator'))
        print(Locator)
        lx.eval('select.item %s add' % Instance)
        lx.eval('item.parent')
        lx.eval('item.parent parent:{} inPlace:1')
        lx.eval('select.drop item')
        lx.eval('select.item %s add' % Instance)
        lx.eval('select.item %s add' % Locator)
        lx.eval('item.parent %s %s inPlace:1' %(Instance, Locator))
        lx.eval('select.drop item')
        lx.eval('select.item %s add' % Instance)
        lx.eval('transform.channel pos.X {%f}' % F_X)
        lx.eval('transform.channel pos.Y {%f}' % F_Y)
        lx.eval('transform.channel pos.Z {%f}' % F_Z)
        lx.eval('item.parent parent:{} inPlace:1')
        lx.eval('select.drop item')
        lx.eval('select.item %s add' % Locator)
        lx.eval('!delete')


lx.bless(SMO_GC_OffsetLocalByArgs_Cmd, Cmd_Name)

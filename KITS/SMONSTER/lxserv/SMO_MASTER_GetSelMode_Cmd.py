# python
"""
# Name:         SMO_MASTER_GetSelMode_Cmd.py
# Version:      1.0
#
# Purpose:      Give current Selection Mode Type and set it to String User Value.
#
# Author:       Franck ELISABETH
# Website:      https://www.smoluck.com
#
# Created:      19/10/2021
# Copyright:    (c) Franck Elisabeth 2017-2022
"""

import lx
import lxu

Cmd_Name = "smo.Master.GetSelMode"
# smo.Master.GetSelMode


class SMO_MASTER_GetSelMode_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
        self.dyna_Add("Query Result", lx.symbol.sTYPE_STRING)
        self.basic_SetFlags (0, lx.symbol.fCMDARG_QUERY)

    def cmd_Flags(self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO

    def cmd_Interact(self):
        pass

    def cmd_UserName(self):
        return 'SMO MASTER - Get Selection Mode'

    def cmd_Desc(self):
        return 'Give current Selection Mode Type and set it to String User Value.'

    def cmd_Tooltip(self):
        return 'Give current Selection Mode Type and set it to String User Value.'

    def cmd_Help(self):
        return 'https://twitter.com/sm0luck'

    def basic_ButtonName(self):
        return 'SMO MASTER - Get Selection Mode'

    def basic_Enable(self, msg):
        return True

    def basic_Execute(self, msg, flags):
        lx.notimpl()
        # Value = lx.eval('user.value SMO_UseVal_MASTER_GetSelMode ?')
        # print(Value)
        # if (lx.eval('select.typeFrom typelist:vertex;polygon;edge;item;ptag ?')) == True:
        #     Value = "Vertex"
        # if (lx.eval('select.typeFrom typelist:edge;vertex;polygon;item ?')) == True:
        #     Value = "Edge"
        # if (lx.eval('select.typeFrom typelist:polygon;vertex;edge;item ?')) == True:
        #     Value = "Polygon"
        # if (lx.eval('select.typeFrom typelist:item;pivot;center;edge;polygon;vertex;ptag ?')) == True:
        #     Value = "Item"

    def cmd_Query(self, index, vaQuery):

        Value = lx.eval('user.value SMO_UseVal_MASTER_GetSelMode ?')
        print(Value)
        if lx.eval('select.typeFrom typelist:vertex;polygon;edge;item;ptag ?'):
            Value = "Vertex"
        if lx.eval('select.typeFrom typelist:edge;vertex;polygon;item ?'):
            Value = "Edge"
        if lx.eval('select.typeFrom typelist:polygon;vertex;edge;item ?'):
            Value = "Polygon"
        if lx.eval('select.typeFrom typelist:item;pivot;center;edge;polygon;vertex;ptag ?'):
            Value = "Item"

        va = lx.object.ValueArray()
        # Initialise the ValueArray
        va.set(vaQuery)

        result = Value
        print(result)
        va.AddString(result)
        return lx.result.OK


lx.bless(SMO_MASTER_GetSelMode_Cmd, Cmd_Name)

# ############# USE CASE
# StringResult = lx.eval('smo.Master.GetSelMode ?')
# print('Current Selection Mode is:',StringResult)
# ######################
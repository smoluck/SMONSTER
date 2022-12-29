# python
"""
Name:         SMO_GC_ReadTags_Cmd.py

Purpose:      This script is designed to:
              Read value of defined Tags (by Args)

Author:       (Code by Ivo Grigull -- CmdSetTag.py command)
              Adapted to kit needs:     Franck ELISABETH
Website:      https://www.smoluck.com
Created:      30/11/2020
"""

import lx
import lxu.command
import lxu.select
import modo

Cmd_Name = "smo.GC.ReadTag"
# smo.GC.ReadTag MTyp ?


class SMO_GC_ReadTags_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
                
        self.dyna_Add('item', '&item')
        
        self.dyna_Add('tagName', lx.symbol.sTYPE_STRING)
        
        self.dyna_Add('tagValue', lx.symbol.sTYPE_STRING)
        
        # Make this argument queryable
        self.basic_SetFlags(2, lx.symbol.fCMDARG_QUERY)
        
    def cmd_Flags(self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO
    
    def cmd_Interact (self):
        pass
    
    def cmd_UserName (self):
        return 'SMO GC - Read Tags by Arguments'
    
    def cmd_Desc (self):
        return 'Read value of defined Tags (by Args)'
    
    def cmd_Tooltip (self):
        return 'Read value of defined Tags (by Args)'
    
    def cmd_Help (self):
        return 'https://twitter.com/sm0luck'
    
    def basic_ButtonName (self):
        return 'SMO GC - Read Tags by Arguments'
    
    def basic_Enable (self, msg):
        return True

    def basic_Execute(self, msg, flags):
        
        # Those lines prevent the script to run, if the 2 Arguments are not defined.
        if not self.dyna_IsSet(0) or not self.dyna_IsSet(1):
            return False
        
        itemIdent = self.dyna_String(0, None)
        tagName = self.dyna_String(1, None)
        
        if not all( (itemIdent, tagName)):
            return False
        
        if self.dyna_IsSet(2):
            tagValue = self.dyna_String(2, None)        
            if not tagValue:
                return False
            
            # Set tag value
            modo.Item(itemIdent).setTag(tagName, tagValue)
        
    
    def cmd_Query(self,index,vaQuery):
        
        if not self.dyna_IsSet(0) or not self.dyna_IsSet(1):
            return False
        
        itemIdent = self.dyna_String(0, None)
        tagName = self.dyna_String(1, None)
        
        if not all( (itemIdent, tagName)):
            return False
        
        item = modo.Item(itemIdent)
        tags = item.getTags()
        if tagName in tags.keys():
            
            # Read tag value
            result = tags[tagName]
        
            va = lx.object.ValueArray(vaQuery)            
            iptr = va.AddEmptyValue()
            iptr.SetString(result)
            return True
        
        return False


lx.bless(SMO_GC_ReadTags_Cmd, Cmd_Name)

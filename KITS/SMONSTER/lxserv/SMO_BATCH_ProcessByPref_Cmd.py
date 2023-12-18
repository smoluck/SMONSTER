# python
"""
Name:         SMO_BATCH_ProcessByPref_Cmd.py

Purpose:      This script is designed to:
              Batch Process a set of files stored in a Folder, using User Defined Preferences.

Author:       Franck ELISABETH (with the help of James O'Hare)
Website:      https://www.linkedin.com/in/smoluck/
Created:      01/10/2020
Copyright:    (c) Franck Elisabeth 2017-2022
"""

import lx
import lxu
import os

Cmd_Name = "smo.BATCH.ProcessByPref"
# smo.BATCH.ProcessByPref


class SMO_BATCH_ProcessByPref_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)

    def cmd_Flags(self):
        return lx.symbol.fCMD_MODEL

    def cmd_Interact (self):
        pass
    
    def cmd_UserName (self):
        return 'SMO BATCH - Process By Pref'
    
    def cmd_Desc (self):
        return 'Batch Process a set of files stored in a Folder, using User Defined Preferences.'
    
    def cmd_Tooltip (self):
        return 'Batch Process a set of files stored in a Folder, using User Defined Preferences..'
    
    def cmd_Help (self):
        return 'https://twitter.com/sm0luck'
    
    def basic_ButtonName (self):
        return 'SMO BATCH - Process By Pref'
    
    def basic_Enable (self, msg):
        return True

    def basic_Execute(self, msg, flags):
        
        # ------------------------------ #
        # <----( DEFINE VARIABLES )----> #
        # ------------------------------ #
        lx.eval("user.defNew name:BPLine001 type:string life:momentary")
        lx.eval("user.defNew name:BPLine002 type:string life:momentary")
        lx.eval("user.defNew name:BPLine003 type:string life:momentary")
        lx.eval("user.defNew name:BPLine004 type:string life:momentary")
        lx.eval("user.defNew name:BPLine005 type:string life:momentary")
        lx.eval("user.defNew name:BPLine006 type:string life:momentary")
        lx.eval("user.defNew name:BPLine007 type:string life:momentary")
        lx.eval("user.defNew name:BPLine008 type:string life:momentary")
        lx.eval("user.defNew name:BPLine009 type:string life:momentary")
        lx.eval("user.defNew name:BPLine010 type:string life:momentary")
        lx.eval("user.defNew name:BPLine011 type:string life:momentary")
        lx.eval("user.defNew name:BPLine012 type:string life:momentary")
        lx.eval("user.defNew name:BPLine013 type:string life:momentary")
        lx.eval("user.defNew name:BPLine014 type:string life:momentary")
        lx.eval("user.defNew name:BPLine015 type:string life:momentary")
        lx.eval("user.defNew name:BPLine016 type:string life:momentary")
        lx.eval("user.defNew name:BPLine017 type:string life:momentary")
        lx.eval("user.defNew name:BPLine018 type:string life:momentary")
        lx.eval("user.defNew name:BPLine019 type:string life:momentary")
        lx.eval("user.defNew name:BPLine020 type:string life:momentary")
        # ------------------------------ #
        
        
        BPLine001 = lx.eval('user.value SMO_UseVal_BATCH_String_Line001 ?')
        lx.out('Batch Process Line 1:', BPLine001)
        BPLine002 = lx.eval('user.value SMO_UseVal_BATCH_String_Line002 ?')
        lx.out('Batch Process Line 2:', BPLine002)
        BPLine003 = lx.eval('user.value SMO_UseVal_BATCH_String_Line003 ?')
        lx.out('Batch Process Line 3:', BPLine003)
        BPLine004 = lx.eval('user.value SMO_UseVal_BATCH_String_Line004 ?')
        lx.out('Batch Process Line 4:', BPLine004)
        BPLine005 = lx.eval('user.value SMO_UseVal_BATCH_String_Line005 ?')
        lx.out('Batch Process Line 5:', BPLine005)
        BPLine006 = lx.eval('user.value SMO_UseVal_BATCH_String_Line006 ?')
        lx.out('Batch Process Line 6:', BPLine006)
        BPLine007 = lx.eval('user.value SMO_UseVal_BATCH_String_Line007 ?')
        lx.out('Batch Process Line 7:', BPLine007)
        BPLine008 = lx.eval('user.value SMO_UseVal_BATCH_String_Line008 ?')
        lx.out('Batch Process Line 8:', BPLine008)
        BPLine009 = lx.eval('user.value SMO_UseVal_BATCH_String_Line009 ?')
        lx.out('Batch Process Line 9:', BPLine009)
        BPLine010 = lx.eval('user.value SMO_UseVal_BATCH_String_Line010 ?')
        lx.out('Batch Process Line 10:', BPLine010)
        
        BPLine011 = lx.eval('user.value SMO_UseVal_BATCH_String_Line011 ?')
        lx.out('Batch Process Line 11:', BPLine011)
        BPLine012 = lx.eval('user.value SMO_UseVal_BATCH_String_Line012 ?')
        lx.out('Batch Process Line 12:', BPLine012)
        BPLine013 = lx.eval('user.value SMO_UseVal_BATCH_String_Line013 ?')
        lx.out('Batch Process Line 13:', BPLine013)
        BPLine014 = lx.eval('user.value SMO_UseVal_BATCH_String_Line014 ?')
        lx.out('Batch Process Line 14:', BPLine014)
        BPLine015 = lx.eval('user.value SMO_UseVal_BATCH_String_Line015 ?')
        lx.out('Batch Process Line 15:', BPLine015)
        BPLine016 = lx.eval('user.value SMO_UseVal_BATCH_String_Line016 ?')
        lx.out('Batch Process Line 16:', BPLine016)
        BPLine017 = lx.eval('user.value SMO_UseVal_BATCH_String_Line017 ?')
        lx.out('Batch Process Line 17:', BPLine017)
        BPLine018 = lx.eval('user.value SMO_UseVal_BATCH_String_Line018 ?')
        lx.out('Batch Process Line 18:', BPLine018)
        BPLine019 = lx.eval('user.value SMO_UseVal_BATCH_String_Line019 ?')
        lx.out('Batch Process Line 19:', BPLine019)
        BPLine020 = lx.eval('user.value SMO_UseVal_BATCH_String_Line020 ?')
        lx.out('Batch Process Line 20:', BPLine020)
        
        
        
        
        if len(BPLine001) == 0 :
            lx.out('NOTIFICATION: line 001 Empty')
        if len(BPLine002) == 0 :
            lx.out('NOTIFICATION: line 002 Empty')
        if len(BPLine003) == 0 :
            lx.out('NOTIFICATION: line 003 Empty')
        if len(BPLine004) == 0 :
            lx.out('NOTIFICATION: line 004 Empty')
        if len(BPLine005) == 0 :
            lx.out('NOTIFICATION: line 005 Empty')
        if len(BPLine006) == 0 :
            lx.out('NOTIFICATION: line 006 Empty')
        if len(BPLine007) == 0 :
            lx.out('NOTIFICATION: line 007 Empty')
        if len(BPLine008) == 0 :
            lx.out('NOTIFICATION: line 008 Empty')
        if len(BPLine009) == 0 :
            lx.out('NOTIFICATION: line 009 Empty')
        if len(BPLine010) == 0 :
            lx.out('NOTIFICATION: line 010 Empty')
            
        if len(BPLine011) == 0 :
            lx.out('NOTIFICATION: line 011 Empty')
        if len(BPLine012) == 0 :
            lx.out('NOTIFICATION: line 012 Empty')
        if len(BPLine013) == 0 :
            lx.out('NOTIFICATION: line 013 Empty')
        if len(BPLine014) == 0 :
            lx.out('NOTIFICATION: line 014 Empty')
        if len(BPLine015) == 0 :
            lx.out('NOTIFICATION: line 015 Empty')
        if len(BPLine016) == 0 :
            lx.out('NOTIFICATION: line 016 Empty')
        if len(BPLine017) == 0 :
            lx.out('NOTIFICATION: line 017 Empty')
        if len(BPLine018) == 0 :
            lx.out('NOTIFICATION: line 018 Empty')
        if len(BPLine019) == 0 :
            lx.out('NOTIFICATION: line 019 Empty')
        if len(BPLine020) == 0 :
            lx.out('NOTIFICATION: line 020 Empty')
        
        
        if len(BPLine001) != 0 :
            lx.out('NOTIFICATION: line 001 Used')
        if len(BPLine002) != 0 :
            lx.out('NOTIFICATION: line 002 Used')
        if len(BPLine003) != 0 :
            lx.out('NOTIFICATION: line 003 Used')
        if len(BPLine004) != 0 :
            lx.out('NOTIFICATION: line 004 Used')
        if len(BPLine005) != 0 :
            lx.out('NOTIFICATION: line 005 Used')
        if len(BPLine006) != 0 :
            lx.out('NOTIFICATION: line 006 Used')
        if len(BPLine007) != 0 :
            lx.out('NOTIFICATION: line 007 Used')
        if len(BPLine008) != 0 :
            lx.out('NOTIFICATION: line 008 Used')
        if len(BPLine009) != 0 :
            lx.out('NOTIFICATION: line 009 Used')
        if len(BPLine010) != 0 :
            lx.out('NOTIFICATION: line 010 Used')
        
        if len(BPLine011) != 0 :
            lx.out('NOTIFICATION: line 011 Used')
        if len(BPLine012) != 0 :
            lx.out('NOTIFICATION: line 012 Used')
        if len(BPLine013) != 0 :
            lx.out('NOTIFICATION: line 013 Used')
        if len(BPLine014) != 0 :
            lx.out('NOTIFICATION: line 014 Used')
        if len(BPLine015) != 0 :
            lx.out('NOTIFICATION: line 015 Used')
        if len(BPLine016) != 0 :
            lx.out('NOTIFICATION: line 016 Used')
        if len(BPLine017) != 0 :
            lx.out('NOTIFICATION: line 017 Used')
        if len(BPLine018) != 0 :
            lx.out('NOTIFICATION: line 018 Used')
        if len(BPLine019) != 0 :
            lx.out('NOTIFICATION: line 019 Used')
        if len(BPLine020) != 0 :
            lx.out('NOTIFICATION: line 020 Used')
        
        
        
        lx.eval ('dialog.setup dir')
        lx.eval ('dialog.title "Select a the target Folder to Analyse and Process"')
        # MODO version checks.
        modo_ver = int(lx.eval ('query platformservice appversion ?'))
        if modo_ver == 801:
            lx.eval ('+dialog.open')
        else:
            lx.eval ('dialog.open')
        Target_Path = lx.eval ('dialog.result ?')
        lx.out('Path', Target_Path)
        
        # Target_Path = "D:\hkdhgfkjhgkfdhgkdfg"
        for dxf in os.listdir(Target_Path):
            if ".dxf" in dxf:
                finalPath = Target_Path + "/" + dxf
                lx.eval("!!scene.open {%s} normal" % finalPath)
                # lx.eval("!!scene.open {%s} import" % finalPath)
                
                if len(BPLine001) != 0 :
                    try:
                        lx.eval('%s' % BPLine001)
                    except:
                        lx.out('ERROR: Impossible to run line 001')
                if len(BPLine001) == 0 :
                    lx.out('NOTIFICATION: line 001 Empty')
                    
                    
                if len(BPLine002) != 0 :
                    try:
                        lx.eval('%s' % BPLine002)
                    except:
                        lx.out('ERROR: Impossible to run line 002')
                if len(BPLine002) == 0 :
                    lx.out('NOTIFICATION: line 002 Empty')
                        
                        
                if len(BPLine003) != 0 :
                    try:
                        lx.eval('%s' % BPLine003)
                    except:
                        lx.out('ERROR: Impossible to run line 003')
                if len(BPLine003) == 0 :
                    lx.out('NOTIFICATION: line 003 Empty')
                        
                        
                if len(BPLine004) != 0 :
                    try:
                        lx.eval('%s' % BPLine004)
                    except:
                        lx.out('ERROR: Impossible to run line 004')
                if len(BPLine004) == 0 :
                    lx.out('NOTIFICATION: line 004 Empty')
                        
                        
                if len(BPLine005) != 0 :
                    try:
                        lx.eval('%s' % BPLine005)
                    except:
                        lx.out('ERROR: Impossible to run line 005')
                if len(BPLine005) == 0 :
                    lx.out('NOTIFICATION: line 005 Empty')
                        
                        
                if len(BPLine006) != 0 :
                    try:
                        lx.eval('%s' % BPLine006)
                    except:
                        lx.out('ERROR: Impossible to run line 006')
                if len(BPLine006) == 0 :
                    lx.out('NOTIFICATION: line 006 Empty')
                        
                        
                if len(BPLine007) != 0 :
                    try:
                        lx.eval('%s' % BPLine007)
                    except:
                        lx.out('ERROR: Impossible to run line 007')
                if len(BPLine007) == 0 :
                    lx.out('NOTIFICATION: line 007 Empty')
                        
                        
                if len(BPLine008) != 0 :
                    try:
                        lx.eval('%s' % BPLine008)
                    except:
                        lx.out('ERROR: Impossible to run line 008')
                if len(BPLine008) == 0 :
                    lx.out('NOTIFICATION: line 008 Empty')
                        
                        
                if len(BPLine009) != 0 :
                    try:
                        lx.eval('%s' % BPLine009)
                    except:
                        lx.out('ERROR: Impossible to run line 009')
                if len(BPLine009) == 0 :
                    lx.out('NOTIFICATION: line 009 Empty')
            
        

    def cmd_Query(self, index, vaQuery):
        lx.notimpl()

lx.bless(SMO_BATCH_ProcessByPref_Cmd, Cmd_Name)

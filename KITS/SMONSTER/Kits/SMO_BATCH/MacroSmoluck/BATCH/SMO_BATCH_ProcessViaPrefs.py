import lx, os

BPLine001 = lx.eval('user.value SMO_UseVal_BP_String_Line001 ?')
lx.out('Batch Process Line 1:', BPLine001)
BPLine002 = lx.eval('user.value SMO_UseVal_BP_String_Line002 ?')
lx.out('Batch Process Line 1:', BPLine002)
BPLine003 = lx.eval('user.value SMO_UseVal_BP_String_Line003 ?')
lx.out('Batch Process Line 1:', BPLine003)
BPLine004 = lx.eval('user.value SMO_UseVal_BP_String_Line004 ?')
lx.out('Batch Process Line 1:', BPLine004)
BPLine005 = lx.eval('user.value SMO_UseVal_BP_String_Line005 ?')
lx.out('Batch Process Line 1:', BPLine005)
BPLine006 = lx.eval('user.value SMO_UseVal_BP_String_Line006 ?')
lx.out('Batch Process Line 1:', BPLine006)
BPLine007 = lx.eval('user.value SMO_UseVal_BP_String_Line007 ?')
lx.out('Batch Process Line 1:', BPLine007)
BPLine008 = lx.eval('user.value SMO_UseVal_BP_String_Line008 ?')
lx.out('Batch Process Line 1:', BPLine008)
BPLine009 = lx.eval('user.value SMO_UseVal_BP_String_Line009 ?')
lx.out('Batch Process Line 1:', BPLine009)





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





path = "D:\hkdhgfkjhgkfdhgkdfg"
for dxf in os.listdir(path):
    if ".dxf" in dxf:
        finalPath = path + "/" + dxf
        lx.eval("!!scene.open {%s} normal" % finalPath)
        # lx.eval("!!scene.open {%s} import" % finalPath)
        
        if len(BPLine001) != 0 :
            try:
                lx.eval('%s' % BPLine001)
            except:
                lx.out('EROOR: Impossible to run line 001')
        if len(BPLine001) == 0 :
            lx.out('NOTIFICATION: line 001 Empty')
            
            
        if len(BPLine002) != 0 :
            try:
                lx.eval('%s' % BPLine002)
            except:
                lx.out('EROOR: Impossible to run line 002')
        if len(BPLine002) == 0 :
            lx.out('NOTIFICATION: line 002 Empty')
                
                
        if len(BPLine003) != 0 :
            try:
                lx.eval('%s' % BPLine003)
            except:
                lx.out('EROOR: Impossible to run line 003')
        if len(BPLine003) == 0 :
            lx.out('NOTIFICATION: line 003 Empty')
                
                
        if len(BPLine004) != 0 :
            try:
                lx.eval('%s' % BPLine004)
            except:
                lx.out('EROOR: Impossible to run line 004')
        if len(BPLine004) == 0 :
            lx.out('NOTIFICATION: line 004 Empty')
                
                
        if len(BPLine005) != 0 :
            try:
                lx.eval('%s' % BPLine005)
            except:
                lx.out('EROOR: Impossible to run line 005')
        if len(BPLine005) == 0 :
            lx.out('NOTIFICATION: line 005 Empty')
                
                
        if len(BPLine006) != 0 :
            try:
                lx.eval('%s' % BPLine006)
            except:
                lx.out('EROOR: Impossible to run line 006')
        if len(BPLine006) == 0 :
            lx.out('NOTIFICATION: line 006 Empty')
                
                
        if len(BPLine007) != 0 :
            try:
                lx.eval('%s' % BPLine007)
            except:
                lx.out('EROOR: Impossible to run line 007')
        if len(BPLine007) == 0 :
            lx.out('NOTIFICATION: line 007 Empty')
                
                
        if len(BPLine008) != 0 :
            try:
                lx.eval('%s' % BPLine008)
            except:
                lx.out('EROOR: Impossible to run line 008')
        if len(BPLine008) == 0 :
            lx.out('NOTIFICATION: line 008 Empty')
                
                
        if len(BPLine009) != 0 :
            try:
                lx.eval('%s' % BPLine009)
            except:
                lx.out('EROOR: Impossible to run line 009')
        if len(BPLine009) == 0 :
            lx.out('NOTIFICATION: line 009 Empty')
        

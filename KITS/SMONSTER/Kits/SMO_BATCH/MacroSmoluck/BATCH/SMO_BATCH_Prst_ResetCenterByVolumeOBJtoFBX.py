# python

import lx

lx.eval('smo.BATCH.SetInputFileTypeViaPref {OBJ}')
lx.eval('smo.BATCH.SetOutputFileTypeViaPref {FBX}')

lx.eval('user.value SMO_UseVal_BATCH_String_Line001 {smo.CLEANUP.DelCam}')
lx.eval('user.value SMO_UseVal_BATCH_String_Line002 {smo.CLEANUP.DelLight}')
lx.eval('user.value SMO_UseVal_BATCH_String_Line003 {smo.CLEANUP.DelEmptyMeshItem}')
lx.eval('user.value SMO_UseVal_BATCH_String_Line004 {select.itemType mesh}')
lx.eval('user.value SMO_UseVal_BATCH_String_Line005 {select.type polygon}')

lx.eval('user.value SMO_UseVal_BATCH_String_Line006 {select.all}')
lx.eval('user.value SMO_UseVal_BATCH_String_Line007 {smo.GC.Setup.MoveRotateCenterToSelection 1 0}')
lx.eval('user.value SMO_UseVal_BATCH_String_Line008 {select.type item}')
lx.eval('user.value SMO_UseVal_BATCH_String_Line009 {smo.GC.RenameMeshesBySceneName}')
lx.eval('user.value SMO_UseVal_BATCH_String_Line010 {}')

lx.eval('user.value SMO_UseVal_BATCH_String_Line011 {}')
lx.eval('user.value SMO_UseVal_BATCH_String_Line012 {}')
lx.eval('user.value SMO_UseVal_BATCH_String_Line013 {}')
lx.eval('user.value SMO_UseVal_BATCH_String_Line014 {}')
lx.eval('user.value SMO_UseVal_BATCH_String_Line015 {}')
lx.eval('user.value SMO_UseVal_BATCH_String_Line016 {}')
lx.eval('user.value SMO_UseVal_BATCH_String_Line017 {}')
lx.eval('user.value SMO_UseVal_BATCH_String_Line018 {}')
lx.eval('user.value SMO_UseVal_BATCH_String_Line019 {}')
lx.eval('user.value SMO_UseVal_BATCH_String_Line020 {}')
# python

import lx

lx.eval('smo.BATCH.SetInputFileTypeViaPref {FBX}')
lx.eval('smo.BATCH.SetOutputFileTypeViaPref {LXO}')

lx.eval('user.value SMO_UseVal_BATCH_String_Line001 {smo.CLEANUP.DelCam}')
lx.eval('user.value SMO_UseVal_BATCH_String_Line002 {smo.CLEANUP.DelLight}')
lx.eval('user.value SMO_UseVal_BATCH_String_Line003 {select.itemType mesh}')
lx.eval('user.value SMO_UseVal_BATCH_String_Line004 {smo.CLEANUP.UnparentInPlace}')
lx.eval('user.value SMO_UseVal_BATCH_String_Line005 {select.itemType mesh}')

lx.eval('user.value SMO_UseVal_BATCH_String_Line006 {layer.mergeMeshes true}')
lx.eval('user.value SMO_UseVal_BATCH_String_Line007 {transform.freeze translation}')
lx.eval('user.value SMO_UseVal_BATCH_String_Line008 {transform.freeze rotation}')
lx.eval('user.value SMO_UseVal_BATCH_String_Line009 {select.type polygon}')
lx.eval('user.value SMO_UseVal_BATCH_String_Line010 {select.all}')

lx.eval('user.value SMO_UseVal_BATCH_String_Line011 {smo.MIFABOMA.SliceLocal 0 0 false}')
lx.eval('user.value SMO_UseVal_BATCH_String_Line012 {select.type vertex}')
lx.eval('user.value SMO_UseVal_BATCH_String_Line013 {smo.GC.SelectVertexByLocalAxis x false}')
lx.eval('user.value SMO_UseVal_BATCH_String_Line014 {delete}')
lx.eval('user.value SMO_UseVal_BATCH_String_Line015 {}')
lx.eval('user.value SMO_UseVal_BATCH_String_Line016 {}')
lx.eval('user.value SMO_UseVal_BATCH_String_Line017 {}')
lx.eval('user.value SMO_UseVal_BATCH_String_Line018 {}')
lx.eval('user.value SMO_UseVal_BATCH_String_Line019 {}')
lx.eval('user.value SMO_UseVal_BATCH_String_Line020 {}')
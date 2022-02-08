# python

__version__ = "0.20"
__author__ = "Franck Elisabeth"

import sys
python_majorver = sys.version_info.major
# print('the Highest version number 2 for 2.7 release / 3 for 3.7 release')
# print(python_majorver)

if python_majorver == 2 :
    # print("do something for 2.X code")
    from SMO_AI_RemappingFCL import *
    from SMO_BAKE_RemappingFCL import *
    from SMO_BATCH_RemappingFCL import *
    from SMO_CAD_RemappingFCL import *
    from SMO_CLEANUP_Remapping_FCL  import *
    from SMO_CB_RemappingFCL import *
    from SMO_GC_MAIN_RemappingFCL import *
    from SMO_GC_EXTRA_RemappingFCL import *
    from SMO_GC_151_RemappingFCL import *
    from SMO_MATH_RemappingFCL import *
    from SMO_MIFABOMA_RemappingFCL import *
    from SMO_QT_RemappingFCL import *
    from SMO_SMONSTER_RemappingFCL import *
    from SMO_UV_RemappingFCL import *
    from SMO_VENOM_RemappingFCL import *

    from SMO_LL_MARMOSET_RemappingFCL import *
    from SMO_LL_PIXAFLUX_RemappingFCL import *
    from SMO_LL_RIZOMUV_RemappingFCL import *

elif python_majorver >= 3 :
    # print("do something for 3.X code")
    from . import SMO_AI_RemappingFCL
    from . import SMO_BAKE_RemappingFCL
    from . import SMO_BATCH_RemappingFCL
    from . import SMO_CAD_RemappingFCL
    from . import SMO_CLEANUP_Remapping_FCL
    from . import SMO_CB_RemappingFCL
    from . import SMO_GC_MAIN_RemappingFCL
    from . import SMO_GC_EXTRA_RemappingFCL
    from . import SMO_GC_151_RemappingFCL
    from . import SMO_MATH_RemappingFCL
    from . import SMO_MIFABOMA_RemappingFCL
    from . import SMO_QT_RemappingFCL
    from . import SMO_SMONSTER_RemappingFCL
    from . import SMO_UV_RemappingFCL
    from . import SMO_VENOM_RemappingFCL

    from . import SMO_LL_MARMOSET_RemappingFCL
    from . import SMO_LL_PIXAFLUX_RemappingFCL
    from . import SMO_LL_RIZOMUV_RemappingFCL
# python
"""
Name:           SMO_MOD_PolyLazySelect.py

Purpose:		This script is designed to:
                Select every polygon in the layer that
                is sharing the same normal in a range of 40 Degree

Author:         Franck ELISABETH
Website:        https://www.smoluck.com
Created:        01/07/2019
Copyright:      (c) Franck Elisabeth 2017-2022
"""

import lx

# ------------- ARGUMENTS ------------- #
args = lx.args()
lx.out(args)
# Similar Touching Fast = 0
# Similar Touching Accurate = 1
# Similar on Object = 2
# Similar in Layer = 3
LSMode = int(args[0])
lx.out('Desired Axe change:', LSMode)
# LS_Angle 2 Deg = 2
# LS_Angle 40 Deg = 40
LS_Angle = int(args[1])
lx.out('Desired Axe change:', LS_Angle)
##\\# ------------- ARGUMENTS ------------- #


# ------------- ARGUMENTS Test ------ #
# LSMode = 1
# lx.out('Lazy Select Mode:', LSMode)
# LS_Angle = 2
# lx.out('Lazy Defined Value:', LS_Angle)
# ------------- ARGUMENTS ------------- #

# LazySelectUserValue = lx.eval('user.value sene_LS_facingRatio ?')
# lx.out('Lazy Select User Value:', LazySelectUserValue)
# lx.eval('user.value sene_LS_facingRatio {%i}' % LS_Angle)

if LSMode == 0:
    lx.eval('smo.GC.SelectCoPlanarPoly 0 {%i} 0' % LS_Angle)

if LSMode == 1:
    # lx.eval('@lazySelect.pl selectTouching 2')
    lx.eval('smo.GC.SelectCoPlanarPoly 0 {%i} 0' % LS_Angle)

if LSMode == 2:
    # lx.eval('@lazySelect.pl selectOnObject')
    lx.eval('smo.GC.SelectCoPlanarPoly 1 {%i} 1000' % LS_Angle)

if LSMode == 3:
    # lx.eval('@lazySelect.pl selectAll')
    lx.eval('smo.GC.SelectCoPlanarPoly 2 {%i} 1000' % LS_Angle)

# lx.eval('user.value sene_LS_facingRatio {%i}' % LazySelectUserValue)

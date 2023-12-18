# python
"""
Name:           SMO_MOD_FallOff.py

Purpose:        This script is designed to:
                Set automatically a defined Falloff

Author:         Franck ELISABETH
Website:        https://www.linkedin.com/in/smoluck/
Created:        16/09/2019
Copyright:      (c) Franck Elisabeth 2017-2022
"""

import lx

# scene = modo.scene.current()
# mesh = scene.selectedByType('mesh')[0]
# CsPolys = len(mesh.geometry.polygons.selected)
# SelItems = (lx.evalN('query sceneservice selection ? locator'))
# lx.out('In Selected items, List of their Unique Name is:',SelItems)


# FallOff_Mode = 0
# Auto_AXES = 2
# Decay_Shape = 1
# Sym_Mode = 1
# ------------------------------ #
# <----( DEFINE ARGUMENTS )----> #
# ------------------------------ #
args = lx.args()
lx.out(args)
FallOff_Mode = args[0]          # Falloff mode:         Linear = 0 / Cylinder = 1 / Radial = 2
# Expose the Result of the Arguments 
lx.out(FallOff_Mode)
Auto_AXES = args[1]             # Axes selection:       X = 0 / Y = 1 / Z = 2
# Expose the Result of the Arguments 
lx.out(Auto_AXES)
Decay_Shape = args[2]           # Decay Shape:          Linear = 0 / EaseIn = 1 / EaseOut = 2 / Smooth = 3
# Expose the Result of the Arguments 
lx.out(Decay_Shape)
Sym_Mode = args[3]              # Symmetry mode:        None = 0 ### Start = 1 ### End = 2
# Expose the Result of the Arguments 
lx.out(Sym_Mode)
# ------------------------------ #
# <----( DEFINE ARGUMENTS )----> #
# ------------------------------ #


FallOff_Status = lx.eval('falloff.state ?')
if FallOff_Status == 0:
    lx.eval('tool.set falloff.linear ?+')
else:
    lx.out('FallOff Enabled')

if FallOff_Status == 1:
    lx.eval('tool.clearTask falloff')
    lx.eval('tool.set falloff.linear ?+')
    lx.out("FallOff already active")
else:
    lx.out('FallOff Enabled')

if Auto_AXES == 0:
    lx.out('FallOff on X')
if Auto_AXES == 1:
    lx.out('FallOff on Y')
if Auto_AXES == 2:
    lx.out('FallOff on Z')

# <----( FallOff MODE)

if FallOff_Mode == 0:
    lx.eval('tool.set falloff.linear on')
    lx.out('FallOff Mode: Linear')
if FallOff_Mode == 1:
    lx.eval('tool.set falloff.cylinder on')
    lx.out('FallOff Mode: Cylinder')

# <----( FallOff AXIS)

# <----( Linear FallOff )----> #
if FallOff_Mode == 0 and Auto_AXES == 0:
    lx.eval('@kit_SMO_MIFABOMA:MacroSmoluck/Modeling/FallOff/SMO_MOD_FallOffLinearAxis.LXM 0')
    # lx.eval('falloff.axisAutoSize axis:0')
    lx.out('FallOff AutoSize on X')
if FallOff_Mode == 0 and Auto_AXES == 1:
    lx.eval('@kit_SMO_MIFABOMA:MacroSmoluck/Modeling/FallOff/SMO_MOD_FallOffLinearAxis.LXM 1')
    # lx.eval('falloff.axisAutoSize axis:1')
    lx.out('FallOff AutoSize on Y')
if FallOff_Mode == 0 and Auto_AXES == 2:
    lx.eval('@kit_SMO_MIFABOMA:MacroSmoluck/Modeling/FallOff/SMO_MOD_FallOffLinearAxis.LXM 2')
    # lx.eval('falloff.axisAutoSize axis:2')
    lx.out('FallOff AutoSize on Z')

# <----( Cylinder FallOff )----> #
if FallOff_Mode == 1 and Auto_AXES == 0:
    lx.eval('tool.setAttr falloff.cylinder axis 0')
    lx.eval('falloff.autoSize')
    lx.out('FallOff AutoSize on X')
if FallOff_Mode == 1 and Auto_AXES == 1:
    lx.eval('tool.setAttr falloff.cylinder axis 1')
    lx.eval('falloff.autoSize')
    lx.out('FallOff AutoSize on Y')
if FallOff_Mode == 1 and Auto_AXES == 2:
    lx.eval('tool.setAttr falloff.cylinder axis 2')
    lx.eval('falloff.autoSize')
    lx.out('FallOff AutoSize on Z')

# <----( SYMMETRY)

# Linear <----( Symmetry Mode )----> #
if FallOff_Mode == 0:
    if Sym_Mode == 0:
        lx.eval('@kit_SMO_MIFABOMA:MacroSmoluck/Modeling/FallOff/SMO_MOD_FallOff_SymNO.py')
        # lx.eval('tool.setAttr falloff.linear symmetric none')
        lx.out('FallOff Symmetry: None')
    if Sym_Mode == 1:
        lx.eval('@kit_SMO_MIFABOMA:MacroSmoluck/Modeling/FallOff/SMO_MOD_FallOff_SymStart.py')
        # lx.eval('tool.setAttr falloff.linear symmetric start')
        lx.out('FallOff Symmetry: Start')
    if Sym_Mode == 2:
        lx.eval('@kit_SMO_MIFABOMA:MacroSmoluck/Modeling/FallOff/SMO_MOD_FallOff_SymEnd.py')
        # lx.eval('tool.setAttr falloff.linear symmetric end')
        lx.out('FallOff Symmetry: End')

# Cylinder <----( Symmetry Mode )----> #
if FallOff_Mode == 1:
    if Sym_Mode == 0:
        lx.eval('@kit_SMO_MIFABOMA:MacroSmoluck/Modeling/FallOff/SMO_MOD_FallOff_SymNO.py')
        # lx.eval('tool.setAttr falloff.cylinder symmetric none')
        lx.out('FallOff Symmetry: None')
    if Sym_Mode == 1:
        lx.eval('@kit_SMO_MIFABOMA:MacroSmoluck/Modeling/FallOff/SMO_MOD_FallOff_Start.py')
        # lx.eval('tool.setAttr falloff.cylinder symmetric start')
        lx.out('FallOff Symmetry: Start')
    if Sym_Mode == 2:
        lx.eval('@kit_SMO_MIFABOMA:MacroSmoluck/Modeling/FallOff/SMO_MOD_FallOff_End.py')
        # lx.eval('tool.setAttr falloff.cylinder symmetric end')
        lx.out('FallOff Symmetry: End')

# <----( DECAY SHAPE)

# Linear <----(Decay shape)----> #
if FallOff_Mode == 0 and Decay_Shape == 0:
    lx.eval('@kit_SMO_MIFABOMA:MacroSmoluck/Modeling/FallOff/SMO_MOD_FallOff_DecayShapeLinear.py')
    # lx.eval('tool.setAttr falloff.linear shape linear')
    lx.out('FallOff Decay Shape: Linear')
if FallOff_Mode == 0 and Decay_Shape == 1:
    lx.eval('@kit_SMO_MIFABOMA:MacroSmoluck/Modeling/FallOff/SMO_MOD_FallOff_DecayShapeEaseIn.py')
    # lx.eval('tool.setAttr falloff.linear shape easeIn')
    lx.out('FallOff Decay Shape: EaseIn')
if FallOff_Mode == 0 and Decay_Shape == 2:
    lx.eval('@kit_SMO_MIFABOMA:MacroSmoluck/Modeling/FallOff/SMO_MOD_FallOff_DecayShapeEaseOut.py')
    # lx.eval('tool.setAttr falloff.linear shape easeOut')
    lx.out('FallOff Decay Shape: EaseOut')
if FallOff_Mode == 0 and Decay_Shape == 3:
    lx.eval('@kit_SMO_MIFABOMA:MacroSmoluck/Modeling/FallOff/SMO_MOD_FallOff_DecayShapeSmooth.py')
    # lx.eval('tool.setAttr falloff.linear shape smooth')
    lx.out('FallOff Decay Shape: Smooth')

lx.eval('tool.set actr.auto on')

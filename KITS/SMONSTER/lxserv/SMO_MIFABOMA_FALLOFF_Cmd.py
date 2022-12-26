# python
"""
# Name:         SMO_MIFABOMA_FALLOFF_Cmd.py
# Version:      1.0
#
# Purpose:      This Command is designed to Mirror
#               a Polygon Selection from the current Layer
#               on a defined Axis (controlled by Argument).
#
# Author:       Franck ELISABETH (with the help of Tom Dymond for debug)
# Website:      https://www.smoluck.com
#
# Created:      16/09/2019
# Copyright:    (c) Franck Elisabeth 2017-2022
"""

import lx
import lxu

Cmd_Name = "smo.MIFABOMA.FallOff"


class SMO_MIFABOMA_FallOff_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
        self.dyna_Add("Falloffmode", lx.symbol.sTYPE_INTEGER)
        self.dyna_Add("Axe", lx.symbol.sTYPE_INTEGER)
        self.dyna_Add("Decayshape", lx.symbol.sTYPE_INTEGER)
        self.dyna_Add("Sym", lx.symbol.sTYPE_INTEGER)
        # self.basic_SetFlags (1, lx.symbol.fCMDARG_OPTIONAL)				# here the (1) define the argument index.

    def cmd_Flags(self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO

    def cmd_Interact (self):
        pass

    def cmd_UserName (self):
        return 'SMO MIFABOMA - FallOff'

    def cmd_Desc (self):
        return 'Setup the corresponding FallOff to the current Selection.'

    def cmd_Tooltip (self):
        return 'Setup the corresponding FallOff to the current Selection.'

    def cmd_Help (self):
        return 'https://twitter.com/sm0luck'

    def basic_ButtonName (self):
        return 'SMO MIFABOMA - FallOff'

    def basic_Enable (self, msg):
        return True

    def basic_Execute(self, msg, flags):
        Falloffmode = self.dyna_Int (0)
        Axe = self.dyna_Int (1)
        Decayshape = self.dyna_Int (2)
        Sym = self.dyna_Int (3)



        #FallOff_Mode = 0
        #Auto_AXES = 2
        #Decay_Shape = 1
        #Sym_Mode = 1
        # ------------------------------ #
        # <----( DEFINE ARGUMENTS )----> #
        # ------------------------------ #
        args = lx.args()
        lx.out(args)
        FallOff_Mode = Falloffmode                      # Falloff mode:                         Linear = 0 / Cylinder = 1 / Radial = 2
        # Expose the Result of the Arguments
        lx.out(FallOff_Mode)
        Auto_AXES = Axe                         # Axes selection:                       X = 0 / Y = 1 / Z = 2
        # Expose the Result of the Arguments
        lx.out(Auto_AXES)
        Decay_Shape = Decayshape                       # Decay Shape:                          Linear = 0 / EaseIn = 1 / EaseOut = 2 / Smooth = 3
        # Expose the Result of the Arguments
        lx.out(Decay_Shape)
        Sym_Mode = Sym                          # Symmetry mode:                        None = 0 ### Start = 1 ### End = 2
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

        # <----( FallOff MODE)###########################  to test:       lx.eval('falloff.axisAutoSize "falloff.linear" 0')

        if FallOff_Mode == 0:
            lx.eval('tool.set falloff.linear on')
            lx.out('FallOff Mode: Linear')
        if FallOff_Mode == 1:
            lx.eval('tool.set falloff.cylinder on')
            lx.out('FallOff Mode: Cylinder')

        # <----( SYMMETRY)###########################

        ## Linear <----( Symmetry Mode )----> #
        if FallOff_Mode == 0:
            if Sym_Mode == 0:
                lx.eval('tool.setAttr falloff.linear symmetric none')
                lx.out('FallOff Symmetry: None')
            if Sym_Mode == 1:
                lx.eval('tool.setAttr falloff.linear symmetric start')
                lx.out('FallOff Symmetry: Start')
            if Sym_Mode == 2:
                lx.eval('tool.setAttr falloff.linear symmetric end')
                lx.out('FallOff Symmetry: End')

        ## Cylinder <----( Symmetry Mode )----> #
        if FallOff_Mode == 1:
            if Sym_Mode == 0:
                lx.eval('tool.setAttr falloff.cylinder symmetric none')
                lx.out('FallOff Symmetry: None')
            if Sym_Mode == 1:
                lx.eval('tool.setAttr falloff.cylinder symmetric start')
                lx.out('FallOff Symmetry: Start')
            if Sym_Mode == 2:
                lx.eval('tool.setAttr falloff.cylinder symmetric end')
                lx.out('FallOff Symmetry: End')

        # <----( DECAY SHAPE)###########################

        ## Linear <----(Decay shape)----> #
        if FallOff_Mode == 0 and Decay_Shape == 0:
            lx.eval('tool.setAttr falloff.linear shape linear')
            lx.out('FallOff Decay Shape: Linear')
        if FallOff_Mode == 0 and Decay_Shape == 1:
            lx.eval('tool.setAttr falloff.linear shape easeIn')
            lx.out('FallOff Decay Shape: EaseIn')
        if FallOff_Mode == 0 and Decay_Shape == 2:
            lx.eval('tool.setAttr falloff.linear shape easeOut')
            lx.out('FallOff Decay Shape: EaseOut')
        if FallOff_Mode == 0 and Decay_Shape == 3:
            lx.eval('tool.setAttr falloff.linear shape smooth')
            lx.out('FallOff Decay Shape: Smooth')

        # <----( FallOff AXIS)###########################

        # <----( Linear FallOff )----> #
        if FallOff_Mode == 0 and Auto_AXES == 0:
            # lx.eval('@kit_SMO_MIFABOMA:MacroSmoluck/Modeling/FallOff/SMO_MOD_FallOffLinearAxis.LXM 0')
            lx.eval('falloff.axisAutoSize axis:0')
            lx.out('FallOff AutoSize on X')
        if FallOff_Mode == 0 and Auto_AXES == 1:
            # lx.eval('@kit_SMO_MIFABOMA:MacroSmoluck/Modeling/FallOff/SMO_MOD_FallOffLinearAxis.LXM 1')
            lx.eval('falloff.axisAutoSize axis:1')
            lx.out('FallOff AutoSize on Y')
        if FallOff_Mode == 0 and Auto_AXES == 2:
            # lx.eval('@kit_SMO_MIFABOMA:MacroSmoluck/Modeling/FallOff/SMO_MOD_FallOffLinearAxis.LXM 2')
            lx.eval('falloff.axisAutoSize axis:2')
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

        lx.eval('tool.set actr.auto on')

    def cmd_Query(self, index, vaQuery):
        lx.notimpl()


lx.bless(SMO_MIFABOMA_FallOff_Cmd, Cmd_Name)

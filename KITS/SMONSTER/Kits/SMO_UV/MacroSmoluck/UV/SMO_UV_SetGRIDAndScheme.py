# python
"""
Name:           SMO_UV_SetGridAndColorScheme_Cmd.py

Purpose:        This script is designed to:
                Activate the Dark Color Scheme in current UV View
                and set the Grid Settings for the Smart Unwrap Tools.

Author:         Franck ELISABETH
Website:        https://www.linkedin.com/in/smoluck/
Created:        27/10/2019
Copyright:      (c) Franck Elisabeth 2017-2022
"""

import lx
import lxu


class SMO_UV_SetGridAndColorScheme_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
        self.dyna_Add("Mode UDIM", lx.symbol.sTYPE_INTEGER)
        self.basic_SetFlags(0, lx.symbol.fCMDARG_OPTIONAL)  # here the (0) define the argument index.

    def cmd_Flags(self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO

    def cmd_Interact(self):
        pass

    def cmd_UserName(self):
        return 'SMO UV Relax'

    def cmd_Desc(self):
        return 'Relax the UVs of the current Polygon Selection.'

    def cmd_Tooltip(self):
        return 'Relax the UVs of the current Polygon Selection.'

    def cmd_Help(self):
        return 'https://twitter.com/sm0luck'

    def basic_ButtonName(self):
        return 'SMO UV Relax'

    def basic_Enable(self, msg):
        return True

    def basic_Execute(self, msg, flags):
        Int_UDIMMode = self.dyna_Int(0)

        # ------------- ARGUMENTS ------------- #
        args = lx.args()
        lx.out(args)

        # Default Mode= 0
        # UDIM Mode = 1
        UDIMMode = Int_UDIMMode
        lx.out('Udim Mode State: {%s}' % UDIMMode)
        # ------------- ARGUMENTS ------------- #

        # ------------------------ #
        # <----( Main Macro )----> #
        # ------------------------ #
        lx.out('Start of SMO_UV_SetGRIDAndScheme Script')

        lx.eval('!!viewport.scheme SMOLUCK_Dark_ColorScheme.3d')
        lx.eval('viewport.scheme "Modo UV.3d"')
        lx.eval('viewuv.showInactive false')
        lx.eval('viewuv.showGrid true')
        lx.eval('viewuv.showSubgrid false')
        lx.eval('viewuv.showInsideLabel true')
        lx.eval('viewuv.uLabelSpace 0.5')
        lx.eval('viewuv.vLabelSpace 0.5')
        lx.eval('viewuv.uGridSpace 1.0')
        lx.eval('viewuv.vGridSpace 1.0')
        if UDIMMode == 0:
            lx.eval('viewuv.uLowSpan -2')
            lx.eval('viewuv.uHighSpan 2')
            lx.eval('viewuv.vLowSpan -2')
            lx.eval('viewuv.vHighSpan 2')
        if UDIMMode == 1:
            lx.eval('viewuv.uLowSpan 0')
            lx.eval('viewuv.uHighSpan 10')
            lx.eval('viewuv.vLowSpan 0')
            lx.eval('viewuv.vHighSpan 10')
        lx.eval('viewuv.showBackdropImage false')

        lx.out('End of SMO_UV_SetGRIDAndScheme Script')


lx.bless(SMO_UV_SetGridAndColorScheme_Cmd, "smo.UV.SetGridAndColorScheme")

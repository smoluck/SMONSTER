# python
"""
Name:         SMO_GC_LoadViewportPreset_Cmd.py

Purpose:      This Command is designed to :
              Load Corresponding Viewport Preset based on Modo Version to limit struggle with Preset form changes.

Author:       Franck ELISABETH
Website:      https://www.smoluck.com
Created:     13/10/2021
Copyright:    (c) Franck Elisabeth 2017-2022
"""

import lx
import lxu

Cmd_Name = "smo.GC.LoadViewportPreset"
# smo.GC.LoadViewportPreset 1


class SMO_GC_LoadViewportPreset_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
        self.dyna_Add("Preset ID", lx.symbol.sTYPE_INTEGER)

    def cmd_Interact(self):
        pass

    def cmd_UserName(self):
        return 'SMO GC - Load Viewport Preset'

    def cmd_Desc(self):
        return 'Check if CAGE Map exist on current Mesh. If not, create a new MorphMap, then Select that CAGE Morph.'

    def cmd_Tooltip(self):
        return 'Check if CAGE Map exist on current Mesh. If not, create a new MorphMap, then Select that CAGE Morph.'

    def cmd_Help(self):
        return 'https://twitter.com/sm0luck'

    def basic_ButtonName(self):
        return 'SMO GC - Load Viewport Preset'

    def cmd_Flags(self):
        return lx.symbol.fCMD_UNDO

    def basic_Enable(self, msg):
        return True

    def basic_Execute(self, msg, flags):
        # ------------------------------ #
        # <----( DEFINE ARGUMENTS )----> #
        # ------------------------------ #
        Preset_ID = self.dyna_Int(0)
        # ------------------------------ #
        # <----( DEFINE ARGUMENTS )----> #
        # ------------------------------ #

        # MODO version checks.
        # Modo 14.0 aand 15.0 have different ViewportPresets.
        Modo_ver = int(lx.eval('query platformservice appversion ?'))
        # print('Modo Version:',Modo_ver)

        # check the MatCap state on current viewport
        MatCapState = bool(lx.eval('vpover.enable ?'))

        # MatCapPrefs = bool(lx.eval('user value SMO_UseVal_VENOM_MatCapState ?'))

        # if MatCapState:
        #     currentMatCapPath = lx.eval('vpover.setOverride path:{?} type:matcap')

        if Modo_ver >= 1500:
            if Preset_ID == 0:
                # lx.eval('attr.formPresetLoad "SMONSTERAVPGame:formPreset" {27036209057:sheet} contextForm:{27036209057:sheet}')
                lx.eval('attr.formPresetLoad "SMONSTERAVPGame:formPreset"')
            if Preset_ID == 1:
                lx.eval('attr.formPresetLoad "SMONSTERAVPGameAA:formPreset"')
            if Preset_ID == 2:
                lx.eval('attr.formPresetLoad "SMONSTERAVPGameRef:formPreset"')
        if Modo_ver < 1500:
            if Preset_ID == 0:
                lx.eval('view3d.presetload AVP_Game')
            if Preset_ID == 1:
                lx.eval('view3d.presetload AVP_Game_AA')
            if Preset_ID == 2:
                lx.eval('view3d.presetload AVP_Game')

        lx.eval('view3d.shadingStyle gnzgl active')
        if MatCapState:
            lx.eval('vpover.enable true')
        if not MatCapState:
            lx.eval('vpover.enable false')


lx.bless(SMO_GC_LoadViewportPreset_Cmd, Cmd_Name)

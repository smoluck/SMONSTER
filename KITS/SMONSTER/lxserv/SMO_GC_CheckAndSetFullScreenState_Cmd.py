# python
"""
# Name:         SMO_GC_CheckAndSetFullScreenState_Cmd.py
# Version:      1.0
#
# Purpose:      This script is designed to:
#               Check Top/Down/Left/Right Side Bars State.
#
#
# Author:       Franck ELISABETH
# Website:      https://www.smoluck.com
#
# Created:      06/12/2020
# Copyright:    (c) Franck Elisabeth 2017-2022
"""

import lx
import lxu

Cmd_Name = "smo.GC.CheckAndSetFullScreenState"
# smo.GC.CheckAndSetFullScreenState


class SMO_GC_CheckAndSetFullScreenState_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)

    def cmd_Flags(self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO

    def cmd_Interact(self):
        pass

    def cmd_UserName(self):
        return 'SMO GC - Check FullScreen Mode State'

    def cmd_Desc(self):
        return 'Check Top/Down/Left/Right Side Bars State.'

    def cmd_Tooltip(self):
        return 'Check Top/Down/Left/Right Side Bars State.'

    def cmd_Help(self):
        return 'https://twitter.com/sm0luck'

    def basic_ButtonName(self):
        return 'SMO GC - Check FullScreen Mode State'

    def basic_Enable(self, msg):
        return True

    def basic_Execute(self, msg, flags):
        FullscreenState = bool(lx.eval('user.value SMO_UseVal_GC_FullscreenState ?'))
        #lx.out('Modo Layout FullscreenMode state: %s' % FullscreenState)

        # Test and Query current Layout State ### START
        LaySwitchState = bool()
        LayTopState = bool()
        LayDownState = bool()
        LayLeftState = bool()
        LayRightState = bool()

        try:
            LaySwitchState = bool(lx.eval('layout.switcherBar ?'))
        except:
            LaySwitchState = False
        #print('SwitcherBar :', LaySwitchState)

        try:
            LayTopState = bool(lx.eval('viewport.collapse ? hash LayoutModoXXSwitcherTop up "89528021001:xkey"'))
        except:
            LayTopState = False
        #print('Small TopBar :', LayTopState)

        try:
            LayDownState = bool(lx.eval('viewport.collapse ? hash LayoutModoXXSwitcherBottom down "56685021006:xkey"'))
        except:
            LayDownState = False
        #print('Small DownBar :', LayDownState)

        try:
            LayLeftState = bool(lx.eval('viewport.collapse ? hash LayoutMODOXXLeftPanelGroup left "01869021009:xkey"'))
        except:
            LayLeftState = False
        #print('Small LeftBar :', LayLeftState)

        try:
            LayRightState = bool(lx.eval('viewport.collapse ? hash LayoutMODOXXRightPanelGroup right "50054021014:xkey"'))
        except:
            LayRightState = False
        #print('Small RightBar :', LayRightState)

        lx.eval('user.value SMO_UseVal_GC_FSLaySwitchState %s' % LaySwitchState)
        lx.eval('user.value SMO_UseVal_GC_FSLayTopState %s' % LayTopState)
        lx.eval('user.value SMO_UseVal_GC_FSLayDownState %s' % LayDownState)
        lx.eval('user.value SMO_UseVal_GC_FSLayLeftState %s' % LayLeftState)
        lx.eval('user.value SMO_UseVal_GC_FSLayRightState %s' % LayRightState)

        #print('----------')
        if LaySwitchState == False and LayTopState == False and LayDownState == False and LayLeftState == False and LayRightState == False:
            lx.eval('user.value SMO_UseVal_GC_FullscreenState true')
            #print('Good')
        if LaySwitchState == True or LayTopState == True or LayDownState == True or LayLeftState == True or LayRightState == True:
            lx.eval('user.value SMO_UseVal_GC_FullscreenState false')
            #print('Bad')

        #print('----------')
        FullscreenState = bool(lx.eval('user.value SMO_UseVal_GC_FullscreenState ?'))
        #print('FullScreen Mode State', bool(FullscreenState))
        lx.out('FullScreen Mode State', bool(FullscreenState))

        #print('----------')
        del FullscreenState
        del LaySwitchState
        del LayTopState
        del LayDownState
        del LayLeftState
        del LayRightState


lx.bless(SMO_GC_CheckAndSetFullScreenState_Cmd, Cmd_Name)

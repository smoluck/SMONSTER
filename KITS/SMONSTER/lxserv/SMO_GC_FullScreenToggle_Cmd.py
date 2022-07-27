#python
#---------------------------------------
# Name:         SMO_GC_FullScreenToggle_Cmd.py
# Version:      1.0
#
# Purpose:      This script is designed to:
#               Toggle the Side Bars On or Off
#
#
# Author:       Franck ELISABETH
# Website:      http://www.smoluck.com
#
# Created:      06/12/2020
# Copyright:    (c) Franck Elisabeth 2017-2022
#---------------------------------------

import lx, lxu, modo

Cmd_Name = "smo.GC.FullScreenToggle"
# smo.GC.FullScreenToggle

class SMO_GC_FullScreenToggle_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
        
    def cmd_Flags(self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO
    
    def cmd_Interact (self):
        pass
    
    def cmd_UserName (self):
        return 'SMO GC - FullScreen Toggle'
    
    def cmd_Desc (self):
        return 'Toggle the Side Bars On or Off.'
    
    def cmd_Tooltip (self):
        return 'Toggle the Side Bars On or Off.'
    
    def cmd_Help (self):
        return 'https://twitter.com/sm0luck'
    
    def basic_ButtonName (self):
        return 'SMO GC - FullScreen Toggle'
    
    def basic_Enable (self, msg):
        return True
    
    def basic_Execute(self, msg, flags):
        lx.eval('smo.GC.CheckAndSetFullScreenState')
        FullscreenState = bool(lx.eval('user.value SMO_UseVal_GC_FullscreenState ?'))
        LaySwitchState = bool(lx.eval('user.value SMO_UseVal_GC_FSLaySwitchState ?'))
        LayTopState = bool(lx.eval('user.value SMO_UseVal_GC_FSLayTopState ?'))
        LayDownState = bool(lx.eval('user.value SMO_UseVal_GC_FSLayDownState ?'))
        LayLeftState = bool(lx.eval('user.value SMO_UseVal_GC_FSLayLeftState ?'))
        LayRightState = bool(lx.eval('user.value SMO_UseVal_GC_FSLayRightState ?'))

        print(FullscreenState)
        print('---')
        print(LaySwitchState)
        print(LayTopState)
        print(LayDownState)
        print(LayLeftState)
        print(LayRightState)
        print('---')

        lx.out('LaySwitchState %s' % LaySwitchState)
        lx.out('LayTopState %s' % LayTopState)
        lx.out('LayDownState %s' % LayDownState)
        lx.out('LayLeftState %s' % LayLeftState)
        lx.out('LayRightState %s' % LayRightState)
        lx.out('---')

        if FullscreenState == False:
            if LaySwitchState == True:
                lx.eval('layout.switcherBar false')
            if LayTopState == True:
                lx.eval('viewport.collapse false hash LayoutModoXXSwitcherTop up "89528021001:xkey"')
            if LayDownState == True:
                lx.eval('viewport.collapse false hash LayoutModoXXSwitcherBottom down "56685021006:xkey"')
            if LayLeftState == True:
                lx.eval('viewport.collapse false hash LayoutMODOXXLeftPanelGroup left "01869021009:xkey"')
            if LayRightState == True:
                lx.eval('viewport.collapse false hash LayoutMODOXXRightPanelGroup right "50054021014:xkey"')
            lx.eval('user.value SMO_UseVal_GC_FullscreenState true')

        if FullscreenState == True:
            if LaySwitchState == False:
                lx.eval('layout.switcherBar true')
            if LayTopState == False:
                lx.eval('viewport.collapse true hash LayoutModoXXSwitcherTop up "89528021001:xkey"')
            if LayDownState == False:
                lx.eval('viewport.collapse true hash LayoutModoXXSwitcherBottom down "56685021006:xkey"')
            if LayLeftState == False:
                lx.eval('viewport.collapse true hash LayoutMODOXXLeftPanelGroup left "01869021009:xkey"')
            if LayRightState == False:
                lx.eval('viewport.collapse true hash LayoutMODOXXRightPanelGroup right "50054021014:xkey"')
            lx.eval('user.value SMO_UseVal_GC_FullscreenState false')


lx.bless(SMO_GC_FullScreenToggle_Cmd, Cmd_Name)



# New script, that doesn't trigger well
#
#
# import lx, lxu, modo
# FullscreenState = bool(lx.eval('user.value SMO_UseVal_GC_FullscreenState ?'))
# print('Modo Layout FullscreenMode state:', FullscreenState)
#
# CurrentStartingState = FullscreenState
#
# if FullscreenState == False:
#     try:
#         ExpandedSwitchSaved = bool(lx.eval('layout.switcherBar ?'))
#     except:
#         ExpandedSwitchSaved = False
#     try:
#         ExpandedTopSaved = bool(
#             lx.eval('viewport.collapse ? hash LayoutModoXXSwitcherTop up "89528021001:xkey"'))
#     except:
#         ExpandedTopSaved = False
#     try:
#         ExpandedDownSaved = bool(
#             lx.eval('viewport.collapse ? hash LayoutModoXXSwitcherBottom down "56685021006:xkey"'))
#     except:
#         ExpandedDownSaved = False
#     try:
#         ExpandedLeftSaved = bool(
#             lx.eval('viewport.collapse ? hash LayoutMODOXXLeftPanelGroup left "01869021009:xkey"'))
#     except:
#         ExpandedLeftSaved = False
#     try:
#         ExpandedRightState = bool(
#             lx.eval('viewport.collapse ? hash LayoutMODOXXRightPanelGroup right "50054021014:xkey"'))
#     except:
#         ExpandedRightState = False
#     print('Current Expanded Configuration Saved:',
#           (ExpandedSwitchSaved, ExpandedTopSaved, ExpandedDownSaved, ExpandedLeftSaved, ExpandedRightState))
#     lx.eval('user.value SMO_UseVal_GC_ExpandedSwitchSaved %s' % ExpandedSwitchSaved)
#     lx.eval('user.value SMO_UseVal_GC_ExpandedTopSaved %s' % ExpandedTopSaved)
#     lx.eval('user.value SMO_UseVal_GC_ExpandedDownSaved %s' % ExpandedDownSaved)
#     lx.eval('user.value SMO_UseVal_GC_ExpandedLeftSaved %s' % ExpandedLeftSaved)
#     lx.eval('user.value SMO_UseVal_GC_ExpandedRightState %s' % ExpandedRightState)
#
# ###############################################
# # Test and Query current Layout State ### START
# LaySwitchState = bool(lx.eval('layout.switcherBar ?'))
# # print(LaySwitchState)
#
# try:
#     LayTopState = bool(lx.eval('viewport.collapse ? hash LayoutModoXXSwitcherTop up "89528021001:xkey"'))
# except:
#     LayTopState = False
#
# try:
#     LayDownState = bool(lx.eval('viewport.collapse ? hash LayoutModoXXSwitcherBottom down "56685021006:xkey"'))
# except:
#     LayDownState = False
#
# try:
#     LayLeftState = bool(lx.eval('viewport.collapse ? hash LayoutMODOXXLeftPanelGroup left "01869021009:xkey"'))
# except:
#     LayLeftState = False
#
# try:
#     LayRightState = bool(
#         lx.eval('viewport.collapse ? hash LayoutMODOXXRightPanelGroup right "50054021014:xkey"'))
# except:
#     LayRightState = False
#
# print('Current Expanded Configuration Saved:',
#       (LaySwitchState, LayTopState, LayDownState, LayLeftState, LayRightState))
# # Test and Query current Layout State ### END
# #############################################
#
#
#
#
# #############################################################
# # Reset current state to Fulscreen as a Temporary base state.
# if LaySwitchState == True:
#     lx.eval('layout.switcherBar false')
# if LayTopState == True:
#     lx.eval('viewport.collapse false hash LayoutModoXXSwitcherTop up "89528021001:xkey"')
# if LayDownState == True:
#     lx.eval('viewport.collapse false hash LayoutModoXXSwitcherBottom down "56685021006:xkey"')
# if LayLeftState == True:
#     lx.eval('viewport.collapse false hash LayoutMODOXXLeftPanelGroup left "01869021009:xkey"')
# if LaySwitchState == True:
#     lx.eval('viewport.collapse false hash LayoutMODOXXRightPanelGroup right "50054021014:xkey"')
# #############################################################
#
#
#
#
# if CurrentStartingState == False:
#     lx.eval('user.value SMO_UseVal_GC_FullscreenState true')
#
# if CurrentStartingState == True:
#     if ExpandedSwitchSaved == False:
#         lx.eval('layout.switcherBar false')
#         print('Switcher Collapsed')
#     if ExpandedSwitchSaved == True:
#         lx.eval('layout.switcherBar true')
#         print('Switcher Expanded')
#
#     if ExpandedTopSaved == False:
#         lx.eval('viewport.collapse true hash LayoutModoXXSwitcherTop up "89528021001:xkey"')
#         print('Top Panel Collapsed')
#     if ExpandedTopSaved == True:
#         lx.eval('viewport.collapse false hash LayoutModoXXSwitcherTop up "89528021001:xkey"')
#         print('Top Panel Expanded')
#
#     if ExpandedDownSaved == False:
#         lx.eval('viewport.collapse true hash LayoutModoXXSwitcherBottom down "56685021006:xkey"')
#         print('Bottom Panel Collapsed')
#     if ExpandedDownSaved == True:
#         lx.eval('viewport.collapse false hash LayoutModoXXSwitcherBottom down "56685021006:xkey"')
#         print('Bottom Panel Expanded')
#
#     if ExpandedLeftSaved == False:
#         lx.eval('viewport.collapse true hash LayoutMODOXXLeftPanelGroup left "01869021009:xkey"')
#         print('Right Panel Collapsed')
#     if ExpandedLeftSaved == True:
#         lx.eval('viewport.collapse false hash LayoutMODOXXLeftPanelGroup left "01869021009:xkey"')
#         print('Right Panel Expanded')
#
#     if ExpandedRightState == False:
#         lx.eval('viewport.collapse true hash LayoutMODOXXRightPanelGroup right "50054021014:xkey"')
#         print('Left Panel Expanded')
#     if ExpandedRightState == True:
#         lx.eval('viewport.collapse false hash LayoutMODOXXRightPanelGroup right "50054021014:xkey"')
#         print('Left Panel Expanded')
#
#     lx.eval('user.value SMO_UseVal_GC_FullscreenState false')
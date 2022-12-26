# python
"""
# Name:         SMO_MIFABOMA_SetRADIALSWEEPAnglePreset_Cmd.py
# Version:      1.0
#
# Purpose:      This Command is designed to :
#               Set the current Angle Preset for Radial Sweep.
#                   
#
# Author:       Franck ELISABETH (with the help of Tom Dymond for debug)
# Website:      https://www.smoluck.com
#
# Created:      16/09/2019
# Copyright:    (c) Franck Elisabeth 2017-2022
"""

import lx
import lxu

Cmd_Name = "smo.MIFABOMA.SetRadialSweepAnglePreset"
# smo.MIFABOMA.SetRadialSweepAnglePreset 0 90 1


class SMO_MIFABOMA_SetRadialSweepAnglePreset_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
        self.dyna_Add("Start Angle", lx.symbol.sTYPE_INTEGER)
        self.dyna_Add("End Angle", lx.symbol.sTYPE_INTEGER)
        self.basic_SetFlags (1, lx.symbol.fCMDARG_OPTIONAL)             # here the (1) define the argument index.
        self.dyna_Add("InBetween", lx.symbol.sTYPE_INTEGER)
        self.basic_SetFlags (2, lx.symbol.fCMDARG_OPTIONAL)

    def cmd_Flags(self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO
    
    def cmd_Interact (self):
        pass
    
    def cmd_UserName (self):
        return 'SMO MIFABOMA - Set Radial Sweep Angle Preset'
    
    def cmd_Desc (self):
        return 'Set the current Angle Preset for Radial Sweep.'
    
    def cmd_Tooltip (self):
        return 'Set the current Angle Preset for Radial Sweep.'
    
    def cmd_Help (self):
        return 'https://twitter.com/sm0luck'
    
    def basic_ButtonName (self):
        return 'SMO MIFABOMA - Set Radial Sweep Angle Preset'
    
    def basic_Enable (self, msg):
        return True

    def basic_Execute(self, msg, flags):
        
        # ------------------------------ #
        # <----( DEFINE ARGUMENTS )----> #                # smo.MIFABOMA.SetRadialSweepAnglePreset 0 90 1
        # ------------------------------ #
        args = lx.args()
        lx.out(args)
        StartANGLE= self.dyna_Int (0)                   # Start Angle
        EndANGLE = self.dyna_Int (1)                    # End Angle
        InBetween= self.dyna_Bool (2)                   # Define the InBetween Mirror Mode    Off = 0 ### On = 1
        # Expose the Result of the Arguments 
        lx.out(StartANGLE,EndANGLE,InBetween)
        # ------------------------------ #
        # <----( DEFINE ARGUMENTS )----> #
        # ------------------------------ #
        
        
        lx.eval('user.value  SMO_UseVal_MIFABOMA_RadialSweep_StartAngle_Preset %s' % StartANGLE)
        lx.eval('user.value  SMO_UseVal_MIFABOMA_RadialSweep_EndAngle_Preset %s' % EndANGLE)
        
        lx.out('user.value SMO_UseVal_MIFABOMA_RadialSweep_StartAngle_Preset ?')
        lx.out('user.value SMO_UseVal_MIFABOMA_RadialSweep_EndAngle_Preset ?')
        
        if InBetween:
            Inbetween_S_Angle = -(EndANGLE / 2)
            Inbetween_E_Angle = (EndANGLE / 2)
            lx.eval('user.value SMO_UseVal_MIFABOMA_RadialSweep_StartAngle_Preset %s' % Inbetween_S_Angle)
            lx.eval('user.value SMO_UseVal_MIFABOMA_RadialSweep_EndAngle_Preset %s' % Inbetween_E_Angle)
            
            lx.out('user.value SMO_UseVal_MIFABOMA_RadialSweep_StartAngle_Preset ?')
            lx.out('user.value SMO_UseVal_MIFABOMA_RadialSweep_EndAngle_Preset ?')

    
    def cmd_Query(self, index, vaQuery):
        lx.notimpl()


lx.bless(SMO_MIFABOMA_SetRadialSweepAnglePreset_Cmd, Cmd_Name)

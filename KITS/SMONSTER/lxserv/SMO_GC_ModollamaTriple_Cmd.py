#python
#---------------------------------------
# Name:         SMO_GC_ModollamaTriple_Cmd.py
# Version:      1.0
#
# Purpose:      This script is designed to:
#               SMO Triple current Polygon selection using Modollama Kit using arguments as Iteration count.
#
#
# Author:       Franck ELISABETH
# Website:      http://www.smoluck.com
#
# Created:      27/05/2021
# Copyright:    (c) Franck Elisabeth 2017-2022
#---------------------------------------
import lx, lxu, modo

Command_Name = "smo.GC.ModollamaTriple"
# smo.GC.ModollamaTriple 8

class SMO_GC_ModollamaTriple_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
        self.dyna_Add("Iteration Count", lx.symbol.sTYPE_INTEGER)

        self.SelModePoly = bool(lx.eval1("select.typeFrom typelist:polygon;vertex;edge;item ?"))

    def cmd_Flags(self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO

    def cmd_Interact(self):
        pass

    def cmd_UserName(self):
        return 'SMO Modollama Triple'

    def cmd_Desc(self):
        return 'SMO Triple current Polygon selection using Modollama Kit using arguments as Iteration count.'

    def cmd_Tooltip(self):
        return 'SMO Triple current Polygon selection using Modollama Kit using arguments as Iteration count.'

    def cmd_Help(self):
        return 'https://twitter.com/sm0luck'

    def basic_ButtonName(self):
        return 'SMO Modollama Triple'

    def cmd_Flags(self):
        return lx.symbol.fCMD_UNDO

    def basic_Enable(self, msg):
        return True

    def basic_Execute(self, msg, flags):
        Iteration = self.dyna_Int(0)
        if self.SelModePoly == True:
            lx.eval('smo.MASTER.ForceSelectMeshItemOnly')

            KeepUVBoundsState = lx.eval('user.value llama_keepuvbounds ?')
            lx.eval('user.value llama_keepuvbounds false')
            KeepMatBoundsState = lx.eval('user.value llama_keepmatbounds ?')
            lx.eval('user.value llama_keepmatbounds false')
            lx.eval('user.value llama_iterations %i' % Iteration)
            lx.eval('user.value llama_anglethreshold 0.005')
            lx.eval('@SmartTriangulation.pl')
            lx.eval('user.value llama_keepuvbounds %s' % KeepUVBoundsState)
            lx.eval('user.value llama_keepmatbounds %s' % KeepMatBoundsState)

lx.bless(SMO_GC_ModollamaTriple_Cmd, Command_Name)